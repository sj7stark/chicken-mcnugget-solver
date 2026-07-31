"""Sources page — citations for the math, formulas, and tools used.

The numbered entries here are referenced as [1], [2], ... from the
*The Math* page and the README.
"""

from __future__ import annotations

import streamlit as st

from core.ui import NUGGET_EMOJI, author_byline

st.set_page_config(
    page_title="Sources — Chicken Nugget Problem",
    page_icon=NUGGET_EMOJI,
    layout="wide",
)

st.title("📚 Sources & Citations")
author_byline()
st.markdown(
    """
The mathematical statements, formulas, and algorithmic ideas used in this app
are drawn from the sources below (numbers match the citations on **The Math**
page).

1. **Art of Problem Solving — "Chicken McNugget Theorem."**
   Statement of the two-pack-size theorem $g(m,n) = mn - m - n$, its history,
   and worked examples.
   [artofproblemsolving.com/wiki/index.php/Chicken_McNugget_Theorem](https://artofproblemsolving.com/wiki/index.php/Chicken_McNugget_Theorem)

2. **Wikipedia — "Coin problem" (Frobenius problem).**
   The general Frobenius problem, the existence condition
   $\\gcd(p_1,\\dots,p_k)=1$, Schur's theorem on representability of all
   sufficiently large integers, and upper bounds on the Frobenius number.
   [en.wikipedia.org/wiki/Coin_problem](https://en.wikipedia.org/wiki/Coin_problem)

3. **Sylvester, J. J. (1882).** "On Subinvariants, i.e. Semi-Invariants to
   Binary Quantics of an Unlimited Order." *American Journal of
   Mathematics*, 5(1), 79–136. Origin of the two-denomination result
   underlying the Chicken McNugget Theorem (with the related counting
   problem posed by Sylvester in the *Educational Times*, 1884).

4. **Ramírez Alfonsín, J. L. (2005).** *The Diophantine Frobenius Problem.*
   Oxford University Press. Comprehensive treatment of the Frobenius
   problem, including existence, bounds, and the NP-hardness of computing
   the Frobenius number for arbitrarily many denominations (see also
   Ramírez Alfonsín, "Complexity of the Frobenius problem,"
   *Combinatorica* 16, 1996).

5. **Brilliant.org — "Postage Stamp Problem / Chicken McNugget Theorem."**
   Accessible treatment of the problem, examples, and the
   consecutive-values stopping idea used by round-based searches.
   [brilliant.org/wiki/postage-stamp-problem-chicken-mcnugget-theorem](https://brilliant.org/wiki/postage-stamp-problem-chicken-mcnugget-theorem/)

6. **Google OR-Tools — Constraint Optimization (CP-SAT).**
   Official documentation for the CP-SAT solver used for every feasibility
   check in this app.
   [developers.google.com/optimization/cp](https://developers.google.com/optimization/cp)

7. **Google OR-Tools — `ortools.sat.python.cp_model` API reference.**
   API documentation for `CpModel`, `NewIntVar`, `Add`, and `CpSolver`
   as used in `core/solver.py`.
   [or-tools.github.io/docs/pdoc/ortools/sat/python/cp_model.html](https://or-tools.github.io/docs/pdoc/ortools/sat/python/cp_model.html)

---

**Artwork note:** the nugget images on the landing page are original
illustrations generated programmatically for this project
(`scripts/generate_images.py`) and are not copied from, or derived from, any
photograph or third-party artwork. The Chicken McNugget Theorem figure on the
Math page was provided by the project owner.
    """
)
