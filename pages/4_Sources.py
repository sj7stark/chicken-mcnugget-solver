"""Sources page — citations for the math, formulas, and tools used.

The numbered entries here are referenced as [1], [2], ... from the
*The Math* page and the README.
"""

from __future__ import annotations

import streamlit as st

# Page config (title, icon, wide layout) is set once for the whole app in
# streamlit_app.main(), which routes here via st.navigation.

st.title("📚 Sources & Citations")
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
   Accessible treatment of the problem, with examples.
   [brilliant.org/wiki/postage-stamp-problem-chicken-mcnugget-theorem](https://brilliant.org/wiki/postage-stamp-problem-chicken-mcnugget-theorem/)

6. **Apéry, R. (1946).** "Sur les branches superlinéaires des courbes
   algébriques." *Comptes Rendus de l'Académie des Sciences de Paris*, 222,
   1198–1200. Introduces the set now known as the **Apéry set** of a
   numerical semigroup, used by the app's solver. (See also
   Wikipedia, ["Numerical semigroup"](https://en.wikipedia.org/wiki/Numerical_semigroup),
   for a modern statement.)

7. **Brauer, A., & Shockley, J. E. (1962).** "On a problem of Frobenius."
   *Journal für die reine und angewandte Mathematik*, 211, 215–220. Source
   of the **Brauer–Shockley formula**
   $g(p_1,\\dots,p_k) = \\max_r(w_r) - a$ relating the Frobenius number to
   the Apéry set, and of the $O(1)$ membership criterion
   $n \\in S \\iff n \\ge w_{n \\bmod a}$.

8. **Nijenhuis, A. (1979).** "A minimal-path algorithm for the 'money
   changing problem'." *The American Mathematical Monthly*, 86(10),
   832–835. The shortest-path (Dijkstra) construction of the Apéry set
   used in `core/solver.py` (`apery_set`).

---

**Artwork note:** the chicken nugget photographs on the landing page were
provided by the project owner. The Chicken McNugget Theorem figure on the
Math page was also provided by the project owner.
    """
)
