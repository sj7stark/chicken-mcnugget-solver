"""Problem Solver page — enter pack sizes, solve, and see the answer.

Page flow (driven by ``st.session_state``):

1. The user picks how many pack sizes exist (2–5) from a dropdown.
2. One numeric input appears per pack size (integers 2–100; type a value or
   use the +/- steppers).
3. A big **Solve** button appears; clicking it computes the answer with the
   residue-class (Apéry set) table. The button is disabled while any
   entered pack size is outside the valid range.
4. The result is shown — either the animated "No Solution" banner or the
   answer with one nugget emoji per nugget — plus a **Clear** button that
   resets the page back to step 1.
"""

from __future__ import annotations

import streamlit as st

from core import (
    MAX_PACK_SIZE,
    MIN_PACK_SIZE,
    find_largest_unreachable_apery,
    solution_exists,
    validate_pack_sizes,
)
from core.ui import NUGGET_EMOJI, answer_box, author_byline, no_solution_banner

# Page config (title, icon, wide layout) is set once for the whole app in
# streamlit_app.main(), which routes here via st.navigation.

# Session-state keys used by this page (grouped here for easy reference).
KEY_NUM_PACKS = "num_pack_sizes"    # dropdown: how many pack sizes
KEY_RESULT = "solve_result"         # dict with the outcome of a solve run
PACK_KEY_PREFIX = "pack_size_"      # pack_size_0 .. pack_size_4


def clear_all() -> None:
    """Reset the page: forget the pack count, pack sizes, and any result.

    Used as the callback of the Clear button. The pack-count dropdown is
    explicitly set back to ``None`` (no selection), so after clearing, the
    page shows the "Select the number of pack sizes…" placeholder again.

    Returns:
        None. Mutates ``st.session_state`` in place.
    """
    st.session_state[KEY_NUM_PACKS] = None
    st.session_state.pop(KEY_RESULT, None)
    for i in range(5):
        st.session_state.pop(f"{PACK_KEY_PREFIX}{i}", None)


def run_solver(pack_sizes: list[int]) -> None:
    """Solve the problem for ``pack_sizes`` and stash the outcome in state.

    Builds the residue-class (Apéry set) table via Nijenhuis's shortest-path
    algorithm and reads the answer directly from the Brauer–Shockley
    formula. Effectively instant — no scanning loop needed.

    The outcome is stored in ``st.session_state[KEY_RESULT]`` as a dict
    with keys ``packs`` (list[int]), ``exists`` (bool), and ``answer``
    (int | None) so it survives Streamlit reruns.

    Args:
        pack_sizes: The pack sizes entered by the user (2–5 integers).

    Returns:
        None. Mutates ``st.session_state`` in place.
    """
    packs = validate_pack_sizes(pack_sizes)

    if not solution_exists(packs):
        st.session_state[KEY_RESULT] = {
            "packs": packs, "exists": False, "answer": None,
        }
        return

    st.session_state[KEY_RESULT] = {
        "packs": packs,
        "exists": True,
        "answer": find_largest_unreachable_apery(packs),
    }


def render_inputs() -> list[int] | None:
    """Render the pack-count dropdown and the per-pack numeric inputs.

    Returns:
        The list of currently entered pack sizes, or None if the user has
        not yet picked how many pack sizes there are.
    """
    st.selectbox(
        "How many different pack sizes are available?",
        options=[2, 3, 4, 5],
        index=None,
        placeholder="Select the number of pack sizes…",
        key=KEY_NUM_PACKS,
    )
    num_packs = st.session_state.get(KEY_NUM_PACKS)
    if num_packs is None:
        st.info("Start by selecting how many pack sizes there are.")
        return None

    st.markdown("#### Enter each pack size")
    st.caption(
        f"Whole numbers from {MIN_PACK_SIZE} to {MAX_PACK_SIZE}. Type a value "
        "or use the **− / +** steppers to change it by 1. The Solve button "
        "stays disabled while any pack size is out of range."
    )
    defaults = [6, 9, 20, 4, 25]  # friendly starting values
    # Keep the − / + steppers visible: Streamlit removes them entirely when
    # a number input is rendered too narrow, so (a) never show more than 5
    # inputs side by side, and (b) force the stepper buttons to stay
    # displayed via CSS as a safety net.
    st.markdown(
        """
        <style>
        [data-testid="stNumberInput"] button {
            display: flex !important;
            visibility: visible !important;
        }
        </style>
        """,
        unsafe_allow_html=True,
    )
    pack_sizes: list[int] = []
    columns = st.columns(num_packs)
    for i, column in enumerate(columns):
        with column:
            st.markdown(f"**Pack #{i + 1}**")
            value = st.number_input(
                f"Size of pack #{i + 1}",
                value=defaults[i],
                step=1,
                key=f"{PACK_KEY_PREFIX}{i}",
                label_visibility="collapsed",
            )
            pack_sizes.append(int(value))
    return pack_sizes


def render_result() -> None:
    """Render the stored solve outcome (answer or No Solution) if present.

    Returns:
        None. Writes the result section directly to the running app.
    """
    result = st.session_state.get(KEY_RESULT)
    if result is None:
        return

    packs_text = ", ".join(map(str, result["packs"]))
    st.caption(f"Pack sizes used: {packs_text}")

    if not result["exists"]:
        no_solution_banner()
        st.markdown(
            "Every one of these pack sizes shares a common factor greater "
            "than 1, so **infinitely many** quantities can never be "
            "purchased — there is no *largest* one. See **The Math** page "
            "for why."
        )
    else:
        answer_box(result["answer"])

    st.button(
        "🧹 Clear",
        on_click=clear_all,
        type="secondary",
        use_container_width=True,
    )


st.title("🧠 Problem Solver")
author_byline()
st.markdown(
    "Pick your pack sizes below, then smash that **Solve** button. The "
    "**residue-class (Apéry set) table** computes the answer instantly — "
    "see **The Math** page for how it works."
)

entered_packs = render_inputs()

if entered_packs is not None and st.session_state.get(KEY_RESULT) is None:
    # Make the Solve button big and unmissable.
    st.markdown(
        """
        <style>
        div[data-testid="stButton"] > button[kind="primary"] {
            font-size: 1.6rem; font-weight: 800; padding: 0.9rem 0;
        }
        </style>
        """,
        unsafe_allow_html=True,
    )
    if len(set(entered_packs)) < len(entered_packs):
        st.warning(
            "Some pack sizes are duplicated — duplicates are treated as a "
            "single pack size."
        )
    # Out-of-range sizes keep the Solve button disabled until corrected.
    out_of_range = sorted(
        {p for p in entered_packs if not MIN_PACK_SIZE <= p <= MAX_PACK_SIZE}
    )
    if out_of_range:
        st.error(
            f"Pack size(s) {', '.join(map(str, out_of_range))} are outside "
            f"the valid range — every pack size must be a whole number from "
            f"{MIN_PACK_SIZE} to {MAX_PACK_SIZE}. Fix them to enable Solve."
        )
    if st.button(
        f"{NUGGET_EMOJI}  SOLVE  {NUGGET_EMOJI}",
        type="primary",
        use_container_width=True,
        disabled=bool(out_of_range),
    ):
        run_solver(entered_packs)
        st.rerun()

render_result()
