"""About the Author page — bio, education, and career summary.

The profile photo is loaded from ``assets/profile.jpg`` (or ``profile.png``)
if present; otherwise a neutral placeholder avatar is shown.

Organization logos live in ``assets/logos/`` (one image per organization,
matched by filename stem — e.g. ``ford.jpg`` for the ``"ford"`` entry).
"""

from __future__ import annotations

from pathlib import Path

import streamlit as st

from core.ui import ASSETS_DIR, AUTHOR_NAME, LINKEDIN_URL, author_byline

# Page config (title, icon, wide layout) is set once for the whole app in
# streamlit_app.main(), which routes here via st.navigation.

LOGOS_DIR = ASSETS_DIR / "logos"


def find_profile_photo() -> Path:
    """Locate the author photo, falling back to the placeholder avatar.

    Returns:
        Path to ``assets/profile.*`` when available, otherwise the generated
        placeholder image.
    """
    for name in ("profile.jpg", "profile.png", "profile.jpeg"):
        candidate = ASSETS_DIR / name
        if candidate.exists():
            return candidate
    return ASSETS_DIR / "author_placeholder.png"


def icon_entry(icon_name: str, heading: str, body: str) -> None:
    """Render one education/career entry with its organization logo.

    Args:
        icon_name: Filename stem of the logo in ``assets/logos`` (e.g.
            ``"ford"`` for ``assets/logos/ford.jpg``). Entries with no
            matching logo file simply render without one.
        heading: Markdown heading line for the entry (bolded by caller as
            desired).
        body: Markdown body text shown under the heading.

    Returns:
        None. Writes a two-column row directly to the running app.
    """
    icon_col, text_col = st.columns([1, 12], gap="small")
    with icon_col:
        for ext in ("jpg", "jpeg", "png"):
            logo_path = LOGOS_DIR / f"{icon_name}.{ext}"
            if logo_path.exists():
                st.image(str(logo_path), width=48)
                break
    with text_col:
        st.markdown(heading)
        if body:
            st.markdown(body)


st.title("👋 About the Author")
author_byline()

photo_col, bio_col = st.columns([1, 2], gap="large")

with photo_col:
    st.image(str(find_profile_photo()), width=280)
    st.markdown(
        f"### [{AUTHOR_NAME}]({LINKEDIN_URL})\n"
        "Lead Data Scientist · Operations Research · "
        "Mathematical Optimization · AI · Simulation · Python\n\n"
        f"🔗 [Connect on LinkedIn]({LINKEDIN_URL}) — 26,000+ followers"
    )

with bio_col:
    st.header("Background")
    st.markdown(
        """
Steven Stark is an **operations research data scientist with 10 years of
experience** delivering high-impact optimization solutions across the
sports, retail, pharmaceutical, aerospace, and automotive industries. His
expertise in mathematical optimization and simulation modeling drives
strategic business decision-making, and he is recognized for his passion
for bridging operations research with corporate objectives — thriving on
complex logistical and financial challenges in large-scale environments.

**Areas of expertise:** Mixed Integer Programming (MIP), Linear
Programming (LP), heuristics, simulation modeling, operations research,
data science, machine learning, and mentorship — working in Python, SQL,
R, VBA, and MATLAB with tools like Gurobi, CPLEX, Hexaly, GCP/BigQuery,
Snowflake, and Tableau.
        """
    )

    st.header("Education")
    icon_entry(
        "umich",
        "**University of Michigan** — Master of Science in Engineering (MSE)",
        "Industrial and Operations Engineering (IOE)",
    )
    icon_entry(
        "umich",
        "**University of Michigan** — Bachelor of Science in Engineering (BSE)",
        "Industrial and Operations Engineering (IOE)",
    )

    st.header("Career Highlights")
    icon_entry(
        "honeywell",
        "**Lead Data Scientist — Honeywell Aerospace Technologies** "
        "*(2026–present)*",
        "Leads data science work applying operations research in the "
        "aerospace industry.",
    )
    icon_entry(
        "cvs",
        "**Senior Data Scientist — CVS Health** *(2025–2026)*",
        "Led an advanced optimization system for Specialty Pharmacy "
        "Operations, combining discrete-event simulation with genetic "
        "algorithms to **save $9M in 2025**; won a corporate hackathon with "
        "AI agents that generate automated insights for business users.",
    )
    icon_entry(
        "atd",
        "**Senior Data Scientist — American Tire Distributors (via "
        "Torqata)** *(2023–2025)*",
        "Built a large-scale Pyomo MIP (Gurobi / Hexaly) to rebalance "
        "inventory, identifying **~$1M in savings per quarter**, and "
        "engineered SKU-distribution analytics on Snowflake, BigQuery, and "
        "GCP.",
    )
    icon_entry(
        "nbcu",
        "**Senior Data Scientist — NBCUniversal, NBC Sports Next** "
        "*(2022–2023)*",
        "Developed **ATHENA**, a pricing-optimization engine (Azure, Pyomo, "
        "SQL) making thousands of daily pricing decisions for US golf "
        "courses; built a PuLP-based fantasy-sports lineup optimizer that "
        "beat the previous product.",
    )
    icon_entry(
        "ford",
        "**Operations Research Scientist / Data Scientist — Ford Motor "
        "Company** *(2018–2022)*",
        "Created a graph-based heuristic (Python/NetworkX) that cut a "
        "~3-hour computation to seconds for an autonomous delivery-vehicle "
        "project — earning **a patent** and a top-5 finish in a company-wide "
        "competition; ran vehicle-routing simulations and geospatial "
        "analyses that helped a large retailer become the second-largest "
        "purchaser of Ford E-Transits; received **3 Ford Recognition "
        "Awards**.",
    )
    icon_entry(
        "walmart",
        "**Statistical Analyst — Walmart** *(2016–2018)*",
        "Automated new-item placement for a distribution center with "
        "Alteryx and R, with projected savings of **$5M+ per year**.",
    )

    st.markdown(
        """
Along the way he has mentored junior data scientists and interns (several
of whom earned return offers), and he shares career advice with a LinkedIn
audience of more than 26,000 followers.
        """
    )
