"""Bumpkin theme: Kin the raccoon mascot (mrkin2.svg) + clean purple/orange spooky CSS."""
import base64
from pathlib import Path

_MASCOT = Path(__file__).parent / "mrkin2.svg"
# Encode once at import; the image is injected a single time via CSS so each bubble doesn't repeat ~1 MB.
_MASCOT_B64 = base64.b64encode(_MASCOT.read_bytes()).decode()
_FONT_B64 = base64.b64encode((Path(__file__).parent / "Minecraft.ttf").read_bytes()).decode()


def kin_img(scale: int = 6) -> str:
    size = scale * 16
    return f'<div class="kin-sprite" role="img" aria-label="Kin the raccoon" style="width:{size}px;height:{size}px"></div>'


def kin_says(text: str, scale: int = 5) -> str:
    return (
        f'<div class="kin-row">{kin_img(scale)}'
        f'<div class="kin-bubble"><span class="kin-name">KIN</span>{text}</div></div>'
    )


CSS = """
<style>
@font-face { font-family: 'Minecraft'; src: url("data:font/ttf;base64,__FONT__") format('truetype'); }

:root {
  --bg: #faf7ff; --card: #ffffff; --lilac: #f1eafc; --line: #e6dcf7;
  --purple: #9b7fd4; --purple-dark: #7a5fb8; --ink: #2e2340; --muted: #6b5d85;
  --orange: #ff8c42; --orange-dark: #e8732a; --orange-soft: #ffe3cc;
  --shadow: 0 6px 24px rgba(122, 95, 184, .12);
}

html, body, .stMarkdown, p, label, input, textarea, li {
  font-family: 'Minecraft', monospace !important; color: var(--ink);
}
h1, h2, h3 { font-family: 'Minecraft', monospace !important; letter-spacing: 1.5px; font-weight: 400 !important; color: var(--purple-dark); }
h1 { font-size: 52px !important; } h2, h3 { font-size: 28px !important; }

.stApp {
  background: radial-gradient(ellipse at top, #efe6ff 0%, var(--bg) 55%) fixed;
}
[data-testid="stHeader"] { background: transparent; }
.block-container { padding-top: 2.5rem !important; max-width: 1200px; }

/* Sidebar */
[data-testid="stSidebar"] { background: var(--lilac); border-right: 1px solid var(--line); }

/* Inputs */
input, textarea, [data-baseweb="select"] > div {
  border-radius: 12px !important; border-color: var(--line) !important; background: var(--card) !important;
}

/* Buttons */
.stButton button {
  border-radius: 999px !important; font-weight: 700; border: 1.5px solid var(--purple) !important;
  color: var(--purple-dark) !important; background: var(--card) !important;
  padding: 8px 20px !important; transition: transform .15s ease, box-shadow .15s ease;
}
.stButton button:hover { transform: translateY(-2px); box-shadow: var(--shadow); }
.stButton button[kind="primary"] {
  background: var(--orange) !important; border-color: var(--orange) !important; color: #fff !important;
  box-shadow: 0 6px 18px rgba(255, 140, 66, .35);
}
.stButton button[kind="primary"]:hover { background: var(--orange-dark) !important; }

/* Metrics + bordered containers = soft cards */
[data-testid="stMetric"], [data-testid="stVerticalBlockBorderWrapper"] > div, div[data-testid="stExpander"] {
  background: var(--card); border: 1px solid var(--line) !important; border-radius: 14px !important;
  box-shadow: var(--shadow);
}
[data-testid="stMetric"] { padding: 14px 18px; }
[data-testid="stMetricValue"] { color: var(--orange) !important; font-weight: 800; }
[data-testid="stMetricLabel"] { color: var(--muted) !important; }

/* Tabs = pills */
[data-baseweb="tab-list"] { gap: 8px; }
[data-baseweb="tab"] {
  border-radius: 999px !important; padding: 6px 18px !important; background: var(--lilac) !important;
  color: var(--muted) !important; font-weight: 700;
}
[data-baseweb="tab"][aria-selected="true"] { background: var(--orange-soft) !important; color: var(--orange-dark) !important; }
[data-baseweb="tab-highlight"], [data-baseweb="tab-border"] { display: none; }

[data-testid="stDataFrame"], [data-testid="stDeckGlJsonChart"] { border-radius: 14px; overflow: hidden; border: 1px solid var(--line); }
[data-testid="stAlert"] { border-radius: 14px !important; }

/* Kin */
.kin-row { display: flex; align-items: flex-end; gap: 14px; margin: 8px 0 18px; }
.kin-sprite {
  flex-shrink: 0; border-radius: 22%;
  background: center / contain no-repeat url("data:image/svg+xml;base64,__MASCOT__");
  filter: drop-shadow(0 6px 12px rgba(122, 95, 184, .25));
  animation: kin-float 3.5s ease-in-out infinite;
}
@keyframes kin-float { 0%,100% { transform: translateY(0); } 50% { transform: translateY(-6px); } }
.kin-bubble {
  position: relative; background: var(--card); border: 1.5px solid var(--purple);
  border-radius: 16px 16px 16px 4px; box-shadow: var(--shadow); padding: 12px 16px; max-width: 640px; line-height: 1.45;
}
.kin-name { display: block; font-size: 11px; font-weight: 800; letter-spacing: 2px; color: var(--orange); margin-bottom: 2px; }

.hero { display: flex; align-items: center; gap: 24px; }
.hero h1 { margin: 0; }
.hero .sub { color: var(--muted); font-size: 18px; }
.quest-time { font-weight: 800; color: var(--purple-dark); font-size: 18px; }
.trend-badge {
  display: inline-block; background: var(--orange-soft); color: var(--orange-dark) !important; font-size: 12px; font-weight: 700;
  padding: 2px 10px; border-radius: 999px; margin-left: 8px;
}
.day-banner {
  display: inline-block; background: var(--orange); color: #fff !important; border-radius: 999px;
  font-weight: 800; font-size: 13px; letter-spacing: 2px; padding: 6px 16px; margin: 18px 0 8px;
  box-shadow: 0 6px 18px rgba(255, 140, 66, .3);
}
</style>
""".replace("__MASCOT__", _MASCOT_B64).replace("__FONT__", _FONT_B64)
