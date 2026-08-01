"""Landing page and navigation for the Chicken McNugget Problem Solver app.

Run locally from the repository root with:

    streamlit run streamlit_app.py

Navigation uses Streamlit's explicit ``st.navigation`` API (instead of the
automatic ``pages/`` discovery) so the landing page appears in the sidebar
as **Home** — both locally and on Streamlit Community Cloud, regardless of
the main file's name. The page scripts still live in ``pages/``.

The Streamlit Community Cloud deployment uses a small shim as its main module
(see the repository root); that shim imports this module and calls
:func:`main` on every rerun. Keeping the rendering inside a function — rather
than at module level — matters: Python caches imported modules, so
module-level ``st.*`` calls in an imported module would only execute on the
very first script run and the landing page would render blank on every rerun
after that.
"""

from __future__ import annotations

import streamlit as st

from core.ui import ASSETS_DIR, LINKEDIN_URL, NUGGET_EMOJI, author_byline


def render_landing_page() -> None:
    """Render the landing page: title, author link, description, artwork.

    Returns:
        None. Writes the page content directly to the running Streamlit app.
    """
    st.title(f"{NUGGET_EMOJI} Chicken McNugget Problem Solver")
    author_byline()

    st.image(str(ASSETS_DIR / "nugget_banner.jpg"), use_container_width=True)
    st.caption("Delicious chicken nuggets")

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
Head to the **Problem Solver** page (sidebar), enter 2–20 pack sizes, and hit
**Solve**. Behind the scenes the app computes the answer instantly with the
**residue-class (Apéry set) table** — a classic piece of number theory
explained on **The Math** page.
            """
        )
        st.page_link(
            "pages/1_Problem_Solver.py",
            label="Open the Problem Solver",
            icon="🧮",
        )
        st.page_link("pages/2_The_Math.py", label="Read the Math", icon="📐")
    with col2:
        st.image(str(ASSETS_DIR / "nugget_photo.jpg"), width=280)


def main() -> None:
    """Configure the page, build the navigation, and run the current page.

    This is the single entry point used by BOTH ways of running the app:
    directly (``streamlit run streamlit_app.py``) and via the deployment
    shim, which imports this module and calls ``main()`` explicitly.

    Returns:
        None.
    """
    st.set_page_config(
        page_title="Chicken McNugget Problem Solver",
        page_icon=NUGGET_EMOJI,
        layout="wide",
    )
    pages = st.navigation(
        [
            st.Page(
                render_landing_page,
                title="Home",
                icon=NUGGET_EMOJI,
                url_path="home",
                default=True,
            ),
            st.Page(
                "pages/1_Problem_Solver.py", title="Problem Solver", icon="🧠"
            ),
            st.Page("pages/2_The_Math.py", title="The Math", icon="🔢"),
            st.Page(
                "pages/3_About_the_Author.py",
                title="About the Creator",
                icon="👋",
            ),
            st.Page("pages/4_Sources.py", title="Sources", icon="📚"),
        ]
    )
    pages.run()


if __name__ == "__main__":
    main()
