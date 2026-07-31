"""Shared UI helpers for the Streamlit pages.

Everything visual that is reused across pages — the author byline, the
falling-emoji "No Solution" animation, and the emoji answer box — lives here
so the page scripts stay short and focused.
"""

from __future__ import annotations

import random
from pathlib import Path

import streamlit as st
import streamlit.components.v1 as components

# The closest standard emoji to a chicken nugget.
NUGGET_EMOJI: str = "\U0001F357"  # 🍗

# Repository root (this file lives in repo_root/core/).
REPO_ROOT: Path = Path(__file__).resolve().parent.parent
ASSETS_DIR: Path = REPO_ROOT / "assets"

AUTHOR_NAME: str = "Steven Stark"
LINKEDIN_URL: str = "https://www.linkedin.com/in/steven-stark"


def author_byline() -> None:
    """Render the "Built by Steven Stark" byline with a LinkedIn hyperlink.

    Returns:
        None. Writes markdown directly to the running Streamlit app.
    """
    st.markdown(
        f"Built by **[{AUTHOR_NAME}]({LINKEDIN_URL})** — "
        "Operations Research | Data Science"
    )


def no_solution_banner(height: int = 420, n_emojis: int = 36) -> None:
    """Show the animated "No Solution" banner with falling nugget emojis.

    Renders an HTML component containing big, bold, flashing "No Solution"
    text while nugget emojis fall continuously from the top of the frame.
    Pure CSS animations, so it keeps running without reruns.

    Args:
        height: Pixel height of the embedded animation frame.
        n_emojis: How many falling emojis to animate (each loops forever).

    Returns:
        None. Writes an HTML component directly to the running Streamlit app.
    """
    rng = random.Random(20260731)  # fixed seed: identical animation each run
    spans = []
    for _ in range(n_emojis):
        left = rng.uniform(0, 97)          # horizontal position (%)
        delay = rng.uniform(0, 6)          # stagger the starts (s)
        duration = rng.uniform(3.5, 8)     # fall speed (s)
        size = rng.uniform(1.2, 2.6)       # emoji size (rem)
        spans.append(
                f'<span class="nug" style="left:{left:.1f}%;'
                f"animation-delay:{delay:.2f}s;"
                f"animation-duration:{duration:.2f}s;"
                f'font-size:{size:.2f}rem;">{NUGGET_EMOJI}</span>'
        )
    html = f"""
    <div class="scene">
      <div class="nosol">No Solution</div>
      {''.join(spans)}
    </div>
    <style>
      html, body {{ margin: 0; padding: 0; }}
      .scene {{
        position: relative; overflow: hidden;
        width: 100%; height: {height - 20}px;
        background: transparent;
      }}
      .nosol {{
        position: absolute; top: 40%; left: 50%;
        transform: translate(-50%, -50%);
        font-family: "Source Sans Pro", "Segoe UI", sans-serif;
        font-size: 4.5rem; font-weight: 900; color: #d62718;
        text-shadow: 0 2px 10px rgba(0,0,0,.15);
        animation: flash 0.9s step-start infinite;
        z-index: 2; white-space: nowrap;
      }}
      @keyframes flash {{ 50% {{ opacity: 0; }} }}
      .nug {{
        position: absolute; top: -3rem;
        animation-name: fall;
        animation-timing-function: linear;
        animation-iteration-count: infinite;
        z-index: 1;
      }}
      @keyframes fall {{
        from {{ transform: translateY(0) rotate(0deg); }}
        to   {{ transform: translateY({height + 80}px) rotate(360deg); }}
      }}
    </style>
    """
    components.html(html, height=height)


def answer_box(answer: int) -> None:
    """Show the solved answer with one nugget emoji per unreachable nugget.

    Displays "<answer> Chicken Nuggets" in large text, followed by a bordered,
    scrollable box containing exactly ``answer`` nugget emojis.

    Args:
        answer: The Frobenius number (largest unpurchasable nugget count).

    Returns:
        None. Writes markdown directly to the running Streamlit app.
    """
    st.markdown(
        f"<h2 style='text-align:center;color:#8a5a00;'>"
        f"{answer} Chicken Nuggets</h2>",
        unsafe_allow_html=True,
    )
    emojis = NUGGET_EMOJI * answer
    st.markdown(
        "<div style='border:3px solid #d98e04;border-radius:12px;"
        "background:#fff6e3;padding:14px;max-height:320px;overflow-y:auto;"
        "font-size:1.6rem;line-height:2rem;text-align:center;"
        "word-break:break-all;'>"
        f"{emojis}</div>",
        unsafe_allow_html=True,
    )
