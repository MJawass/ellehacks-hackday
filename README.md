# Bumpkin

Little adventures for short stays, scouted by Kin.

Bumpkin is a cozy, pixel-art trip planner built with Streamlit on Snowflake. Tell Kin, the app's guide, where you are, how much free time you have and what you like, and Kin builds a short itinerary from real nearby places. Places that people are talking about on Instagram and TikTok are boosted to the top.

## Who it helps

- Travellers on a layover, a work trip or a weekend away who only have a few free hours and do not want to spend them researching.
- People who want to see what locals are actually excited about right now, not just the same top-ten list.
- Anyone who finds trip planning overwhelming and wants a friendly, low-effort starting point they can tweak.

## Features

- **Trip Shed (sidebar):** pick a city or enter custom coordinates, choose days in town (1-3), hours free per day, start time, interests, pace (Relaxed, Balanced, Packed), how far you will wander and any notes (for example "vegetarian" or "travelling with kids").
- **Quest Log:** press "Plan my adventure!" and Kin returns a day-by-day plan with start times, durations, why each stop is worth it and a practical tip, plus a map of the stops. Type into the chat box to ask for changes, such as "swap dinner for something cheaper".
- **Town Map:** every candidate place Kin found, on a map and in a table with its score, distance, address and website.
- **Gossip Board:** the trending places, with post counts, likes, sentiment, vibe and a link to a sample post.

## How it works

1. **Find candidates.** A SQL query looks up places within your chosen radius in the Overture Maps Places dataset, filtered to categories that match your interests, high-confidence and open places.
2. **Score them.** Each place is scored on data confidence, number of sources, having a website or social accounts, distance from the centre and, where available, social media buzz and sentiment. The top places per category are kept.
3. **Plan the trip.** The candidate list and your preferences are sent to an open-weight large language model through Snowflake Cortex `AI_COMPLETE` with a structured output schema, so the model returns a clean JSON itinerary that uses only real places from the list.
4. **Revise.** Your feedback and the previous draft are sent back to the model to produce an updated plan.

## Models used

The model is selectable in the sidebar. Both options are open-weight models served through Snowflake Cortex AI:

| Model | Provider | License / terms |
|---|---|---|
| `llama3.3-70b` (Llama 3.3 70B Instruct) | Meta | [Llama 3.3 Community License](https://www.llama.com/llama3_3/license/) |
| `mistral-large2` (Mistral Large 2) | Mistral AI | [Mistral Research License](https://mistral.ai/licenses/MRL-0.1.md) |

Use of these models through Snowflake is also subject to the [Snowflake Cortex AI terms](https://www.snowflake.com/en/legal/).

## Datasets

- **Overture Maps Places** (`OVERTURE_MAPS_PLACES.CARTO.PLACE`), from the Snowflake Marketplace listing by CARTO. Open place data from the [Overture Maps Foundation](https://overturemaps.org/), licensed under [CDLA-Permissive-2.0](https://cdla.dev/permissive-2-0/).
- **Social signals** (`TOURISM_APP.CORE.PLACE_SOCIAL_SCORES` and `TOURISM_APP.CORE.SOCIAL_PLACES_GEOCODED`): our own tables of Instagram and TikTok post activity (post counts, likes, comments, sentiment, vibe) matched to Overture place IDs. Cities with social data include Sydney, London, Sheffield and Varanasi.

## How to run it

### Requirements

- Python 3.11 or 3.12
- A Snowflake account with access to the Overture Maps Places listing, the `TOURISM_APP` database and Cortex `AI_COMPLETE`

### Run locally

```bash
git clone https://github.com/MJawass/ellehacks-hackday.git
cd ellehacks-hackday/tourism-itinerary-app
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```


Then start the app:

```bash
streamlit run streamlit_app.py
```


## How to use it

1. Open the sidebar (the Trip Shed) and pick your city.
2. Set your days, free hours, start time, interests, pace and walking radius. Add any notes for Kin.
3. Choose an AI model.
4. On the Quest Log tab, press **Plan my adventure!**
5. Read your plan, check the map, and type into the chat box to ask Kin for changes.
6. Browse the Town Map and Gossip Board tabs to see every place Kin considered.
7. Use **Restock data** in the sidebar to clear cached results.

## How Cortex Code (CoCo) helped

We built this project with Snowflake Cortex Code. CoCo helped us:

- Explore the Overture Maps Places schema and write the geospatial candidate and scoring SQL.
- Wire up Cortex `AI_COMPLETE` with a structured response schema so itineraries come back as reliable JSON.
- Build the Streamlit app, including the pixel-art fall forest theme, the Kin character, custom CSS and generated pixel assets.
- Debug deployment issues, such as missing dependencies and Snowflake connection secrets.

## Project structure

```
tourism-itinerary-app/
  streamlit_app.py   Main Streamlit app
  queries.py         SQL queries, interest categories and preset cities
  kin.py             Theme CSS, Kin sprites and speech bubbles
  assets/            Pixel-art images used by the theme
  snowflake.yml      Streamlit in Snowflake deployment config
  requirements.txt   Python dependencies
```

## License

This project is licensed under the MIT License. See [LICENSE](LICENSE).
