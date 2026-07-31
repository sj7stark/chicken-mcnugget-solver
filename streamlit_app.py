"""Landing page for the Chicken Nugget Problem Solver Streamlit app.

Run locally from the repository root with:

    streamlit run streamlit_app.py

The other pages (Problem Solver, The Math, About the Author, Sources) live in
the ``pages/`` directory and are picked up automatically by Streamlit's
multipage mechanism.
"""

from __future__ import annotations

import streamlit as st

from core.ui import ASSETS_DIR, LINKEDIN_URL, NUGGET_EMOJI, author_byline

st.set_page_config(
    page_title="Chicken Nugget Problem Solver",
    page_icon=NUGGET_EMOJI,
    layout="wide",
)


def render_landing_page() -> None:
    """Render the landing page: title, author link, description, artwork.

    Returns:
        None. Writes the page content directly to the running Streamlit app.
    """
    st.title(f"{NUGGET_EMOJI} The Chicken Nugget Problem Solver")
    author_byline()

    st.image(str(ASSETS_DIR / "nugget_banner.png"), use_container_width=True)
    st.caption(
        "Original illustrations created programmatically for this project "
        "(see `scripts/generate_images.py`) — no copyrighted images used."
    )

    st.header("What is the Chicken Nugget Problem?")
    st.markdown(
        """
Imagine a restaurant sells chicken nuggets **only in packs of 6, 9, and 20**.
You can buy as many packs of each size as you like, but you cannot buy a
partial pack.

Some quantities are easy to buy exactly: 15 nuggets is a 6-pack plus a 9-pack,
and 21 is 6 + 6 + 9. But other quantities are *impossible* — try to buy
exactly **43** nuggets and you will find that no combination of 6s, 9s, and
20s ever adds up to it. In fact, 43 turns out to be the **largest** impossible
order: every quantity from 44 onward can be purchased exactly.

The **Chicken Nugget Problem** asks precisely that question:

> **Given a set of pack sizes, what is the largest number of nuggets that
> CANNOT be purchased exactly?**

In mathematics this is known as the **Frobenius coin problem** (named after
Ferdinand Frobenius, who posed it with coin denominations instead of nugget
packs), and the answer is called the **Frobenius number**. A solution does
not always exist — if every pack size shares a common factor, infinitely
many quantities are unreachable — and the *Math* page explains exactly when
it does.
        """
    )

    col1, col2 = st.columns(2)
    with col1:
        st.subheader("Try it yourself")
        st.markdown(
            """
Head to the **Problem Solver** page (sidebar), enter 2–5 pack sizes, and hit
**Solve**. Behind the scenes the app uses **Google OR-Tools' CP-SAT
constraint programming solver** to search for the answer.
            """
        )
        st.page_link(
            "pages/1_Problem_Solver.py",
            label="Open the Problem Solver",
            icon="🧮",
        )
        st.page_link("pages/2_The_Math.py", label="Read the Math", icon="📐")
    with col2:
        st.image(str(ASSETS_DIR / "nugget_1.png"), width=280)


render_landing_page()
