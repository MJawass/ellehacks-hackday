"""Bumpkin theme: Kin the raccoon mascot (assets/kin_*.png emotes) + dark-green forest CSS with a vine-wrapped wooden sidebar."""
import base64
from pathlib import Path

_ASSETS = Path(__file__).parent / "assets"


def _b64(name: str) -> str:
    return base64.b64encode((_ASSETS / name).read_bytes()).decode()


# Encode once at import; each image is injected a single time via CSS classes so bubbles don't repeat the bytes.
MOODS = ("wave", "cheer", "point", "walk", "shy")
_MOOD_B64 = {m: _b64(f"kin_{m}.png") for m in MOODS}
_LOGO_B64 = _b64("bumpkin_logo.png")
_WOOD_B64 = _b64("woodpanel.png")
_FOREST_B64 = _b64("forest.png")
_VINE_B64 = _b64("vine.png")
_TEXTBOX_B64 = _b64("textbox.png")
_LEAF_TL_B64 = _b64("leaves_tl.png")
_LEAF_BR_B64 = _b64("leaves_br.png")
_FONT_B64 = base64.b64encode((Path(__file__).parent / "Minecraft.ttf").read_bytes()).decode()

PAGE_ICON = str(_ASSETS / "kin_wave.png")


def kin_img(scale: int = 6, mood: str = "wave") -> str:
    size = scale * 16
    return (
        f'<div class="kin-sprite kin-{mood}" role="img" aria-label="Kin the raccoon"'
        f' style="width:{size}px;height:{size}px"></div>'
    )


def kin_says(text: str, mood: str = "wave", scale: int = 5) -> str:
    return (
        f'<div class="kin-row">{kin_img(scale, mood)}'
        f'<div class="kin-bubble"><span class="kin-name">KIN</span>{text}</div></div>'
    )


def logo_img() -> str:
    return '<div class="bumpkin-logo" role="img" aria-label="Bumpkin"></div>'


_MOOD_CSS = "\n".join(
    f'.kin-{m} {{ background-image: url("data:image/png;base64,{b}"); }}' for m, b in _MOOD_B64.items()
)

CSS = ("""
<style>
@font-face { font-family: 'Minecraft'; src: url("data:font/ttf;base64,__FONT__") format('truetype'); }

:root {
  --bg: #2e1a12; --card: #3b2414; --lilac: #4a2e1a; --line: #7a4a24;
  --purple: #6fae5a; --purple-dark: #fff1d6; --ink: #fff1d6; --muted: #fff1d6;
  --orange: #2f6b34; --orange-dark: #1f4a24; --orange-soft: #dcefd5;
  --wood-dark: #3b1d0e; --parchment: #fff4e0; --cream: #fff1d6;
  --shadow: 0 6px 24px rgba(20, 50, 24, .25);
}

/* Minecraft font everywhere (Material icon glyphs excluded so they don't turn into words) */
html, body, .stApp, .stApp *:not([data-testid="stIconMaterial"]):not(.material-symbols-rounded) {
  font-family: 'Minecraft', monospace !important;
}
html, body, .stMarkdown, p, label, input, textarea, li, span, small, td, th,
[data-testid="stMetricValue"], [data-testid="stMetricLabel"], [data-testid="stCaptionContainer"],
[data-testid="stSliderThumbValue"], [data-testid="stSliderTickBarMin"], [data-testid="stSliderTickBarMax"] { color: var(--ink) !important; }
h1, h2, h3 { letter-spacing: 1.5px; font-weight: 400 !important; color: var(--purple-dark); }
h2, h3 { font-size: 28px !important; }

.stApp {
  background: url("data:image/png;base64,__FOREST__") repeat var(--bg);
  background-size: 384px 384px; image-rendering: pixelated;
}
/* Main content sits on a parchment panel so text stays readable over the forest */
.block-container {
  background: rgba(40, 22, 12, .9); border: 4px solid var(--wood-dark); border-radius: 10px;
  margin-top: 2rem; padding-bottom: 2rem !important; box-shadow: 0 10px 0 rgba(10, 30, 14, .5);
}
/* Hide the "Running ..." status widget */
[data-testid="stStatusWidget"] { display: none !important; }
[data-testid="stHeader"] { background: transparent; }
.block-container { padding-top: 2.5rem !important; max-width: 1200px; }
.block-container h1, .block-container h2, .block-container h3 { color: var(--purple-dark); }

/* Sidebar: wooden planks with a dark tint so cream labels stay readable; inputs sit on parchment */
[data-testid="stSidebar"] {
  background: linear-gradient(rgba(40, 18, 6, .35), rgba(40, 18, 6, .35)),
              url("data:image/png;base64,__WOOD__") repeat;
  background-size: auto, 300px 300px;
  image-rendering: pixelated;
  border-right: 6px solid var(--wood-dark);
  position: relative; overflow: visible;
}
[data-testid="stSidebarUserContent"] { padding-left: 2.6rem !important; padding-right: 2.6rem !important; }
/* Pixel vines creeping down both edges of the wood panel */
[data-testid="stSidebar"]::before, [data-testid="stSidebar"]::after {
  content: ""; position: absolute; top: 0; bottom: 0; width: 32px; z-index: 5; pointer-events: none;
  background: url("data:image/png;base64,__VINE__") repeat-y; background-size: 32px 128px; image-rendering: pixelated;
}
[data-testid="stSidebar"]::before { left: -4px; }
[data-testid="stSidebar"]::after { right: -2px; transform: scaleX(-1); background-position: 0 40px; }
[data-testid="stSidebar"] h1, [data-testid="stSidebar"] h2, [data-testid="stSidebar"] h3 {
  color: var(--cream) !important; text-align: center; background: var(--wood-dark);
  border: 3px solid #6b3a1c; border-radius: 6px; padding: 6px 0 !important;
}
[data-testid="stSidebar"] label, [data-testid="stSidebar"] label p,
[data-testid="stSidebar"] [data-testid="stWidgetLabel"] p,
[data-testid="stSidebar"] [data-testid="stSliderTickBarMin"],
[data-testid="stSidebar"] [data-testid="stSliderTickBarMax"] {
  color: var(--cream) !important; font-size: 15px !important;
  text-shadow: 2px 2px 0 var(--wood-dark), -1px -1px 0 var(--wood-dark), 1px -1px 0 var(--wood-dark), -1px 1px 0 var(--wood-dark);
}
[data-testid="stSidebar"] [data-testid="stSlider"] div,
[data-testid="stSidebar"] [data-testid="stSliderThumbValue"],
[data-testid="stSidebar"] [data-testid="stSliderTickBarMin"] *,
[data-testid="stSidebar"] [data-testid="stSliderTickBarMax"] * {
  color: var(--cream) !important; font-size: 15px !important;
  text-shadow: 2px 2px 0 var(--wood-dark), -1px -1px 0 var(--wood-dark), 1px -1px 0 var(--wood-dark), -1px 1px 0 var(--wood-dark);
}
[data-testid="stSidebar"] input, [data-testid="stSidebar"] textarea,
[data-testid="stSidebar"] [data-baseweb="select"] > div, [data-testid="stSidebar"] [data-baseweb="input"] {
  background: var(--parchment) !important; color: var(--wood-dark) !important;
  border: 2px solid var(--wood-dark) !important; border-radius: 6px !important;
}
[data-testid="stSidebar"] [data-baseweb="select"] span, [data-testid="stSidebar"] [data-baseweb="select"] div,
[data-testid="stSidebar"] [data-baseweb="input"] *, [data-testid="stSidebar"] .stButton button * { color: var(--wood-dark) !important; text-shadow: none !important; }
[data-testid="stSidebar"] [data-baseweb="tag"] { background: var(--orange) !important; }
[data-testid="stSidebar"] [data-baseweb="tag"] span { color: #fff !important; }
[data-testid="stSidebar"] [data-testid="stButtonGroup"] button {
  background: var(--parchment) !important; color: var(--wood-dark) !important; border: 2px solid var(--wood-dark) !important;
}
[data-testid="stSidebar"] [data-testid="stButtonGroup"] button[kind*="Active"] {
  background: var(--orange) !important; color: #fff !important;
}
[data-testid="stSidebar"] [data-testid="stButtonGroup"] button * {
  color: var(--wood-dark) !important; text-shadow: none !important; font-size: 15px !important;
}
[data-testid="stSidebar"] [data-testid="stButtonGroup"] button {
  transition: transform .12s ease, background .12s ease, box-shadow .12s ease;
}
[data-testid="stSidebar"] [data-testid="stButtonGroup"] button:hover {
  background: #e8a24a !important; transform: translateY(-3px); box-shadow: 0 4px 0 var(--wood-dark);
}
[data-testid="stSidebar"] [data-testid="stButtonGroup"] button[kind*="Active"],
[data-testid="stSidebar"] [data-testid="stButtonGroup"] button[aria-checked="true"],
[data-testid="stSidebar"] [data-testid="stButtonGroup"] button[aria-pressed="true"] {
  background: var(--orange) !important; box-shadow: inset 0 3px 0 rgba(0,0,0,.35); transform: none;
}
[data-testid="stSidebar"] [data-testid="stButtonGroup"] button[kind*="Active"] *,
[data-testid="stSidebar"] [data-testid="stButtonGroup"] button[aria-checked="true"] *,
[data-testid="stSidebar"] [data-testid="stButtonGroup"] button[aria-pressed="true"] * {
  color: var(--cream) !important; text-shadow: 2px 2px 0 var(--wood-dark) !important;
}
[data-testid="stSidebar"] .stButton button {
  background: var(--parchment) !important; color: var(--wood-dark) !important; border: 2px solid var(--wood-dark) !important;
}

/* Inputs */
input, textarea, [data-baseweb="select"] > div {
  border-radius: 12px !important; border-color: var(--line) !important; background: var(--card) !important;
}

/* Buttons */
.stButton button {
  border-radius: 999px !important; border: 1.5px solid var(--purple) !important;
  color: var(--ink) !important; background: var(--card) !important;
  padding: 8px 20px !important; transition: transform .15s ease, box-shadow .15s ease;
}
.stButton button:hover { transform: translateY(-2px); box-shadow: var(--shadow); }
.stButton button[kind="primary"] {
  background: var(--orange) !important; border-color: var(--orange) !important; color: #fff !important;
  box-shadow: 0 6px 18px rgba(31, 74, 36, .35);
}
.stButton button[kind="primary"]:hover { background: var(--orange-dark) !important; }

/* Metrics + bordered containers = soft cards */
[data-testid="stMetric"], [data-testid="stVerticalBlockBorderWrapper"] > div, div[data-testid="stExpander"] {
  background: var(--card); border: 1px solid var(--line) !important; border-radius: 14px !important;
  box-shadow: var(--shadow);
}
[data-testid="stMetric"] { padding: 14px 18px; }
[data-testid="stMetricValue"] { color: var(--ink) !important; }
[data-testid="stMetricLabel"] { color: var(--muted) !important; }

/* Tabs = pills */
[data-baseweb="tab-list"] { gap: 8px; }
[data-baseweb="tab"] {
  border-radius: 999px !important; padding: 6px 18px !important; background: var(--lilac) !important;
  color: var(--muted) !important;
}
[data-baseweb="tab"][aria-selected="true"] { background: var(--orange) !important; color: var(--ink) !important; }
[data-baseweb="tab-highlight"], [data-baseweb="tab-border"] { display: none; }

[data-testid="stDataFrame"], [data-testid="stDeckGlJsonChart"] { border-radius: 14px; overflow: hidden; border: 1px solid var(--line); }
[data-testid="stAlert"] { border-radius: 14px !important; }

/* Kin */
.kin-row { display: flex; align-items: flex-end; gap: 14px; margin: 8px 0 18px; }
.kin-sprite {
  flex-shrink: 0; background-position: center; background-size: contain; background-repeat: no-repeat;
  filter: drop-shadow(0 6px 12px rgba(20, 50, 24, .3));
  animation: kin-float 3.5s ease-in-out infinite;
}
__MOODS__
@keyframes kin-float { 0%,100% { transform: translateY(0); } 50% { transform: translateY(-6px); } }
.kin-bubble {
  position: relative; max-width: 640px; line-height: 1.45; color: #3b1d0e;
  border: 20px solid transparent; border-image: url("data:image/png;base64,__TEXTBOX__") 20 fill stretch;
  image-rendering: pixelated; padding: 22px 30px 28px; filter: drop-shadow(0 4px 0 rgba(10, 30, 14, .35));
}
.kin-bubble, .kin-bubble * { color: #3b1d0e !important; }
/* Autumn leaves spilling off the bubble corners */
.kin-bubble::before, .kin-bubble::after, .block-container::before, .block-container::after {
  content: ""; position: absolute; width: 80px; height: 72px; pointer-events: none; image-rendering: pixelated;
  background-size: contain; background-repeat: no-repeat;
}
.kin-bubble::before { top: -44px; left: -46px; background-image: url("data:image/png;base64,__LEAFTL__"); }
.kin-bubble::after { bottom: -46px; right: -48px; background-image: url("data:image/png;base64,__LEAFBR__"); }
.block-container { position: relative; }
.block-container::before { top: -34px; left: -34px; width: 120px; height: 108px; background-image: url("data:image/png;base64,__LEAFTL__"); }
.block-container::after { bottom: -34px; right: -34px; width: 120px; height: 108px; background-image: url("data:image/png;base64,__LEAFBR__"); }
.kin-name { display: block; font-size: 11px; letter-spacing: 2px; color: #8a4a12 !important; margin-bottom: 2px; }

.hero { display: flex; align-items: center; gap: 24px; }
.bumpkin-logo {
  width: 420px; max-width: 100%; aspect-ratio: 2170 / 720;
  background: left center / contain no-repeat url("data:image/png;base64,__LOGO__");
}
.hero .sub { color: var(--muted); font-size: 18px; margin-top: 4px; }
.quest-time { color: var(--purple-dark); font-size: 18px; }
.trend-badge {
  display: inline-block; background: var(--orange); color: var(--ink) !important; font-size: 12px;
  padding: 2px 10px; border-radius: 999px; margin-left: 8px;
}
.day-banner {
  display: inline-block; background: var(--orange); color: #fff !important; border-radius: 999px;
  font-size: 13px; letter-spacing: 2px; padding: 6px 16px; margin: 18px 0 8px;
  box-shadow: 0 6px 18px rgba(31, 74, 36, .3);
}
</style>
""".replace("__MOODS__", _MOOD_CSS).replace("__LOGO__", _LOGO_B64).replace("__WOOD__", _WOOD_B64).replace("__FONT__", _FONT_B64)
       .replace("__FOREST__", _FOREST_B64).replace("__VINE__", _VINE_B64).replace("__TEXTBOX__", _TEXTBOX_B64)
       .replace("__LEAFTL__", _LEAF_TL_B64).replace("__LEAFBR__", _LEAF_BR_B64))
