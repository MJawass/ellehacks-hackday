import html
import json
import os

import pandas as pd
import streamlit as st

from kin import CSS, kin_img, kin_says
from queries import (
    CANDIDATES_SQL,
    INTERESTS,
    ITINERARY_SQL,
    PRESET_CITIES,
    SOCIAL_CITIES_SQL,
)

st.set_page_config(page_title="Bumpkin", page_icon=":raccoon:", layout="wide")
st.markdown(CSS, unsafe_allow_html=True)

st.markdown(
    f"""<div class="hero">{kin_img(9)}
    <div><h1>Bumpkin</h1>
    <div class="sub">Little adventures for short stays, scouted by Kin from Instagram &amp; TikTok chatter.</div></div>
    </div>""",
    unsafe_allow_html=True,
)

conn = st.connection("snowflake", ttl=os.getenv("SNOWFLAKE_CONNECTION_TTL"))

MODELS = ["claude-sonnet-4-5", "llama3.3-70b", "mistral-large2"]
SEASONS = ["Spring", "Summer", "Fall"]


def esc(v) -> str:
    return html.escape(str(v)) if v is not None and not (isinstance(v, float) and pd.isna(v)) else ""


@st.cache_data(ttl=3600, show_spinner=False)
def load_social_cities() -> pd.DataFrame:
    return conn.query(SOCIAL_CITIES_SQL)


@st.cache_data(ttl=1800, show_spinner=False)
def load_candidates(lon: float, lat: float, radius_m: float, cats_json: str) -> pd.DataFrame:
    df = conn.query(CANDIDATES_SQL, params=[lon, lat, radius_m, cats_json])
    df.columns = [c.lower() for c in df.columns]
    return df


def clear_caches():
    load_social_cities.clear()
    load_candidates.clear()
    st.session_state.pop("itinerary", None)


def build_prompt(city, days, hours_per_day, start_time, interests, pace, notes, cands, feedback=None):
    lines = []
    for r in cands.itertuples():
        social = "-"
        if pd.notna(r.num_posts) and r.num_posts:
            social = (
                f"TRENDING on {r.platforms}: {int(r.num_posts)} posts, {int(r.total_likes or 0)} likes, "
                f"sentiment {r.sentiment_score}, vibe '{r.vibe or ''}'"
            )
        lines.append(f"- {r.name} | {r.category} | {r.km} km from center | social: {social}")
    stops_per_day = {"Relaxed": "3-4", "Balanced": "4-6", "Packed": "6-8"}[pace]
    prompt = f"""You are a local travel expert building a short-stay itinerary in {city}.
Traveler: in town for {days} day(s), about {hours_per_day} hours per day, starting at {start_time} each day.
Interests: {', '.join(interests) or 'anything'}. Pace: {pace} ({stops_per_day} stops per day).
Extra notes from traveler: {notes or 'none'}.

Rules:
- Use ONLY places from the candidate list below; copy names exactly.
- Strongly prefer places marked TRENDING (social media buzz) and mention why people love them.
- Skip candidates that look like non-visitable entries (car parks, offices, apartments, obviously mislocated places).
- Group stops that are close together, schedule meals at sensible times, never repeat a place.
- 'why' is 1-2 sentences in a warm, cozy, slightly playful tone; 'tip' is one practical tip.

Candidates (name | category | distance | social signal):
{chr(10).join(lines)}
"""
    if feedback:
        prompt += f"\nThe traveler reviewed a previous draft and asked for this change: {feedback}\n"
    return prompt


def generate_itinerary(model, prompt):
    df = conn.query(ITINERARY_SQL, params=[model, prompt], ttl=0)
    raw = df.iloc[0, 0]
    return json.loads(raw) if isinstance(raw, str) else raw


# ---------------- Sidebar: the tool shed ----------------
with st.sidebar:
    st.markdown(f'<div style="text-align:center">{kin_img(6)}</div>', unsafe_allow_html=True)
    st.header("Trip Shed")
    social_cities = load_social_cities()
    social_names = [c for c in social_cities["CITY"].tolist() if c and c not in PRESET_CITIES]
    city_options = list(PRESET_CITIES.keys()) + social_names + ["Custom location"]
    city = st.selectbox(":world_map: Where are you?", city_options, index=0)

    if city == "Custom location":
        city_label = st.text_input("Place name", "My location")
        lat = st.number_input("Latitude", value=40.7580, format="%.4f")
        lon = st.number_input("Longitude", value=-73.9855, format="%.4f")
    elif city in PRESET_CITIES:
        city_label = city
        lat, lon = PRESET_CITIES[city]
    else:
        city_label = city
        row = social_cities[social_cities["CITY"] == city].iloc[0]
        lat, lon = float(row["LAT"]), float(row["LON"])

    days = st.slider(":sunrise: Days in town", 1, 3, 1)
    hours_per_day = st.slider(":hourglass_flowing_sand: Hours free per day", 2, 12, 6)
    start_time = st.time_input(":alarm_clock: Start time", value=pd.Timestamp("10:00").time()).strftime("%H:%M")
    interests = st.multiselect(":seedling: Interests", list(INTERESTS.keys()), default=["Food", "Coffee & cafes", "Culture & history"])
    pace = st.segmented_control("Pace", ["Relaxed", "Balanced", "Packed"], default="Balanced") or "Balanced"
    radius_km = st.slider(":athletic_shoe: How far will you wander? (km)", 1, 10, 3)
    notes = st.text_area(":scroll: Notes for Kin", placeholder="e.g. vegetarian, travelling with kids, love views")
    model = st.selectbox("AI model", MODELS)
    st.button("Restock data", on_click=clear_caches, help="Clear cached place data")

cats = sorted({c for i in (interests or INTERESTS.keys()) for c in INTERESTS[i]})

# ---------------- Candidates ----------------
with st.spinner("Kin is sniffing around for good spots..."):
    cands = load_candidates(float(lon), float(lat), float(radius_km * 1000), json.dumps(cats))

trending = cands[cands["num_posts"].fillna(0) > 0]

m1, m2, m3 = st.columns(3)
m1.metric(":house_with_garden: Spots nearby", len(cands))
m2.metric(":fire: Trending", len(trending))
m3.metric(":basket: Kinds of fun", cands["category"].nunique() if len(cands) else 0)

if cands.empty:
    st.markdown(kin_says("Hmm... my basket's empty here! Try wandering farther or picking other interests."), unsafe_allow_html=True)
    st.stop()

tab_plan, tab_places, tab_social = st.tabs(["Quest Log", "Town Map", "Gossip Board"])

with tab_plan:
    itin = st.session_state.get("itinerary")
    if not itin:
        greeting = f"Howdy, traveler! Welcome to <b>{esc(city_label)}</b>. I found <b>{len(cands)}</b> spots"
        greeting += f", and <b>{len(trending)}</b> of them have folks buzzing online!" if len(trending) else "."
        greeting += " Press the big orange button and I'll plan your adventure."
        st.markdown(kin_says(greeting), unsafe_allow_html=True)

    if st.button("Plan my adventure!", type="primary"):
        prompt = build_prompt(city_label, days, hours_per_day, start_time, interests, pace, notes, cands)
        with st.spinner("Kin is scribbling on a map..."):
            try:
                st.session_state["itinerary"] = generate_itinerary(model, prompt)
                st.session_state["itinerary_ctx"] = (city_label, days, hours_per_day, start_time, tuple(interests), pace, notes)
                st.rerun()
            except Exception as e:  # surface model / SQL errors to the user
                st.error(f"Kin tripped over a log: {e}")

    if itin:
        st.markdown(
            kin_says(f"<b>{esc(itin.get('title', 'Your adventure'))}</b><br>{esc(itin.get('summary', ''))}"),
            unsafe_allow_html=True,
        )
        stops = itin.get("stops", [])
        by_name = cands.drop_duplicates("name").set_index("name")
        for d in sorted({s.get("day") or 1 for s in stops}):
            st.markdown(f'<div class="day-banner">DAY {d} &middot; {SEASONS[(d - 1) % 3].upper()}</div>', unsafe_allow_html=True)
            for s in [s for s in stops if (s.get("day") or 1) == d]:
                info = by_name.loc[s["name"]] if s["name"] in by_name.index else None
                with st.container(border=True):
                    h1, h2 = st.columns([1, 6])
                    h1.markdown(
                        f'<div class="quest-time">{esc(s.get("start_time", ""))}</div>{esc(s.get("duration_min", ""))} min',
                        unsafe_allow_html=True,
                    )
                    badge = ""
                    if info is not None and pd.notna(info["num_posts"]):
                        badge = f'<span class="trend-badge">&#9733; hot on {esc(info["platforms"])}</span>'
                    h2.markdown(f"<b>{esc(s['name'])}</b>{badge}", unsafe_allow_html=True)
                    h2.write(s.get("why", ""))
                    if s.get("tip"):
                        h2.caption(f":bulb: Kin's tip: {s['tip']}")
                    if info is not None:
                        links = []
                        if pd.notna(info["address"]):
                            links.append(str(info["address"]))
                        if pd.notna(info["website"]):
                            links.append(f"[website]({info['website']})")
                        if pd.notna(info["sample_post_url"]):
                            links.append(f"[see the post]({info['sample_post_url']})")
                        if links:
                            h2.caption(" · ".join(links))

        stop_pts = cands[cands["name"].isin([s["name"] for s in stops])][["lat", "lon"]]
        if not stop_pts.empty:
            st.map(stop_pts, latitude="lat", longitude="lon", size=40, color="#ff8c42")

        feedback = st.chat_input("Tell Kin what to change, e.g. 'swap dinner for something cheaper'")
        if feedback:
            ctx = st.session_state["itinerary_ctx"]
            prompt = build_prompt(*ctx, cands, feedback=feedback + f"\nPrevious draft: {json.dumps(itin)[:4000]}")
            with st.spinner("Kin is rearranging the map..."):
                st.session_state["itinerary"] = generate_itinerary(model, prompt)
            st.rerun()

with tab_places:
    st.markdown(kin_says("Here's every spot I sniffed out. Higher score = Kin-approved!"), unsafe_allow_html=True)
    st.map(cands, latitude="lat", longitude="lon", size=25, color="#9b7fd4")
    st.dataframe(
        cands[["name", "category", "km", "score", "num_posts", "total_likes", "address", "website"]],
        hide_index=True,
        use_container_width=True,
        column_config={
            "website": st.column_config.LinkColumn("website"),
            "score": st.column_config.ProgressColumn("score", min_value=0, max_value=float(cands["score"].max())),
        },
    )

with tab_social:
    if trending.empty:
        st.markdown(
            kin_says(
                "Quiet around here... nobody's gossiping online about these spots yet, so I picked by local reputation. "
                "Try Sydney, London, Sheffield or Varanasi to hear the town gossip!"
            ),
            unsafe_allow_html=True,
        )
    else:
        st.markdown(kin_says("Psst! Here's what folks are posting about on Instagram &amp; TikTok."), unsafe_allow_html=True)
        st.dataframe(
            trending[["name", "category", "platforms", "num_posts", "total_likes", "total_comments", "sentiment_score", "vibe", "sample_post_url"]],
            hide_index=True,
            use_container_width=True,
            column_config={"sample_post_url": st.column_config.LinkColumn("post")},
        )
