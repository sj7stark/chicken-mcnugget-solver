"""Problem Solver page — enter pack sizes, solve, and see the answer.

Page flow (driven by ``st.session_state``):

1. The user picks how many pack sizes exist (2–5) from a dropdown.
2. One numeric input appears per pack size (integers 2–100; type a value or
   use the +/- steppers).
3. A big **Solve** button appears; clicking it runs the CP-SAT search.
4. The result is shown — either the animated "No Solution" banner or the
   answer with one nugget emoji per nugget — plus a **Clear** button that
   resets the page back to step 1.
"""

from __future__ import annotations

import streamlit as st

from core import (
    MAX_PACK_SIZE,
    MIN_PACK_SIZE,
    find_largest_unreachable,
    find_largest_unreachable_apery,
    solution_exists,
    validate_pack_sizes,
)
from core.ui import NUGGET_EMOJI, answer_box, author_byline, no_solution_banner

st.set_page_config(
    page_title="Problem Solver — Chicken Nugget Problem",
    page_icon=NUGGET_EMOJI,
    layout="wide",
)

# Session-state keys used by this page (grouped here for easy reference).
KEY_NUM_PACKS = "num_pack_sizes"    # dropdown: how many pack sizes
KEY_METHOD = "solver_method"        # dropdown: which solver approach to use
KEY_RESULT = "solve_result"         # dict with the outcome of a solve run
PACK_KEY_PREFIX = "pack_size_"      # pack_size_0 .. pack_size_4

# Solver approach labels shown in the method dropdown.
METHOD_APERY = "Residue-class table (Apéry set) — instant"
METHOD_CPSAT = "CP-SAT sliding window (Google OR-Tools)"


def clear_all() -> None:
    """Reset the page: forget the pack count, pack sizes, and any result.

    Used as the callback of the Clear button; deleting the widget keys sends
    the user back to the initial "select the number of packs" state.

    Returns:
        None. Mutates ``st.session_state`` in place.
    """
    st.session_state.pop(KEY_NUM_PACKS, None)
    st.session_state.pop(KEY_METHOD, None)
    st.session_state.pop(KEY_RESULT, None)
    for i in range(5):
        st.session_state.pop(f"{PACK_KEY_PREFIX}{i}", None)


def run_solver(pack_sizes: list[int], method: str) -> None:
    """Solve the problem for ``pack_sizes`` and stash the outcome in state.

    Dispatches to the chosen solver approach:

    * ``METHOD_APERY`` — builds the residue-class (Apéry set) table via
      Nijenhuis's shortest-path algorithm and reads the answer directly
      from the Brauer–Shockley formula. Effectively instant.
    * ``METHOD_CPSAT`` — the sliding-window search that asks Google
      OR-Tools' CP-SAT solver one feasibility question per candidate N
      (shows a progress bar; can take a while for large pack sizes).

    The outcome is stored in ``st.session_state[KEY_RESULT]`` as a dict
    with keys ``packs`` (list[int]), ``exists`` (bool), ``answer``
    (int | None), and ``method`` (str) so it survives Streamlit reruns.

    Args:
        pack_sizes: The pack sizes entered by the user (2–5 integers).
        method: One of ``METHOD_APERY`` or ``METHOD_CPSAT``.

    Returns:
        None. Mutates ``st.session_state`` in place.
    """
    packs = validate_pack_sizes(pack_sizes)

    if not solution_exists(packs):
        st.session_state[KEY_RESULT] = {
            "packs": packs, "exists": False, "answer": None, "method": method,
        }
        return

    if method == METHOD_APERY:
        # Table build + formula: no scanning loop, no progress bar needed.
        answer = find_largest_unreachable_apery(packs)
    else:
        progress = st.progress(0.0, text="Solving with CP-SAT…")

        def update_progress(current: int, cap: int) -> None:
            """Advance the progress bar (fraction of the theoretical cap).

            Args:
                current: Target amount just checked by the solver.
                cap: Safety cap (theoretical upper bound) for the search.

            Returns:
                None.
            """
            progress.progress(
                min(current / cap, 1.0),
                text=f"Solving with CP-SAT… checked up to {current} nuggets",
            )

        with st.spinner("Asking Google OR-Tools CP-SAT…"):
            answer = find_largest_unreachable(
                packs, progress_callback=update_progress
            )
        progress.empty()

    st.session_state[KEY_RESULT] = {
        "packs": packs, "exists": True, "answer": answer, "method": method,
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
        "or use the **− / +** steppers to change it by 1."
    )
    defaults = [6, 9, 20, 4, 25]  # friendly starting values
    columns = st.columns(num_packs)
    pack_sizes: list[int] = []
    for i, column in enumerate(columns):
        with column:
            st.markdown(f"**Pack #{i + 1}**")
            value = st.number_input(
                f"Size of pack #{i + 1}",
                min_value=MIN_PACK_SIZE,
                max_value=MAX_PACK_SIZE,
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
    st.caption(
        f"Pack sizes used: {packs_text} · Approach: "
        f"{result.get('method', METHOD_APERY)}"
    )

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


st.title(f"{NUGGET_EMOJI} Problem Solver")
author_byline()
st.markdown(
    "Pick your pack sizes below, choose a solver approach, then smash that "
    "**Solve** button. The default **residue-class (Apéry set) table** "
    "answers instantly; the **CP-SAT** option shows Google OR-Tools solving "
    "the same problem with constraint programming."
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
    # Solver-approach dropdown, shown together with the Solve button.
    st.selectbox(
        "Solver approach",
        options=[METHOD_APERY, METHOD_CPSAT],
        index=0,  # default: the residue-class (Apéry set) table
        key=KEY_METHOD,
        help=(
            "The residue-class table answers instantly using number theory "
            "(see The Math page, section 4). The CP-SAT option demonstrates "
            "solving one constraint-programming feasibility model per "
            "candidate amount — same answer, slower on large pack sizes."
        ),
    )
    if st.button(
        f"{NUGGET_EMOJI}  SOLVE  {NUGGET_EMOJI}",
        type="primary",
        use_container_width=True,
    ):
        run_solver(entered_packs, st.session_state[KEY_METHOD])
        st.rerun()

render_result()
