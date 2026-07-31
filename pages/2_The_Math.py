"""The Math page — existence test, Chicken McNugget Theorem, and algorithm.

All numbered citations like [1] refer to the entries on the *Sources* page.
"""

from __future__ import annotations

import streamlit as st

from core.ui import ASSETS_DIR, NUGGET_EMOJI, author_byline

st.set_page_config(
    page_title="The Math — Chicken Nugget Problem",
    page_icon=NUGGET_EMOJI,
    layout="wide",
)

st.title("📐 The Math Behind the Solver")
author_byline()
st.markdown(
    "Numbered citations like **[1]** point to the entries on the "
    "**Sources** page."
)

# ---------------------------------------------------------------------------
# 1. When does a solution exist?
# ---------------------------------------------------------------------------
st.header("1. Does a solution even exist?")
st.markdown(
    r"""
Suppose there are $k \ge 2$ pack sizes $p_1, p_2, \dots, p_k$ (each an
integer $\ge 2$). A purchasable quantity is any value of
$p_1 x_1 + p_2 x_2 + \dots + p_k x_k$ with non-negative integers $x_i$.
The Chicken Nugget Problem has a solution — i.e. a **largest** unreachable
quantity (the *Frobenius number* $g(p_1,\dots,p_k)$) exists — **exactly
when the pack sizes have no common factor** [2][4]:
"""
)
st.latex(
    r"g(p_1, p_2, \ldots, p_k) \text{ exists} \iff"
    r"\gcd(p_1, p_2, \ldots, p_k) = 1"
)
st.markdown(
    r"""
**Why the condition is necessary.** If $\gcd(p_1,\dots,p_k) = d > 1$, then
every purchasable amount $p_1 x_1 + \dots + p_k x_k$ is a multiple of $d$.
Every quantity that is *not* a multiple of $d$ (and there are infinitely many)
can never be purchased, so no largest unreachable quantity exists.

**Why the condition is sufficient.** If $\gcd(p_1,\dots,p_k) = 1$, a
classical result of Schur (see [2][4]; the two-pack case goes back to
Sylvester [3]) guarantees that **every sufficiently large integer is
purchasable**. The unreachable quantities therefore form a *finite* set, and
a finite non-empty set has a largest element — the Frobenius number. (With
every pack size $\ge 2$, the set is never empty: 1 nugget is always
unreachable.)

**Checking the condition** is fast: fold the Euclidean algorithm across the
list, using $\gcd(a, b, c) = \gcd(\gcd(a, b), c)$.

| Pack sizes | Overall gcd | Solution? |
|---|---|---|
| 6, 9, 20 | 1 | ✅ exists (it's 43) |
| 4, 6, 10 | 2 | ❌ none — every purchase is even |
| 6, 10, 15 | 1 | ✅ exists (it's 29) |

Note the last row: **the pack sizes do not need to be pairwise coprime** —
6, 10, and 15 share factors in every pair, yet the gcd of all three is 1.
"""
)

# ---------------------------------------------------------------------------
# 2. The Chicken McNugget Theorem
# ---------------------------------------------------------------------------
st.header("2. The Chicken McNugget Theorem (two pack sizes)")
st.markdown(
    r"""
For **two** pack sizes there is a beautiful closed-form answer, popularly
known as the **Chicken McNugget Theorem** (a special case of results by
Sylvester, 1882 [1][3]):

> For relatively prime positive integers $m$ and $n$ (i.e.
> $\gcd(m, n) = 1$), the greatest integer that **cannot** be written as
> $am + bn$ with non-negative integers $a, b$ is
"""
)
st.latex(r"g(m, n) = mn - m - n")
st.markdown(
    r"""
**Simple example.** Packs of $m = 2$ and $n = 5$:
$g(2,5) = 2 \cdot 5 - 2 - 5 = 3$. Indeed, 3 nuggets cannot be bought with
2-packs and 5-packs, while $4 = 2+2$, $5 = 5$, $6 = 2+2+2$, $7 = 2+5$, and
every larger quantity works.

The theorem is named after the classic 6, 9, 20 McDonald's nugget-pack
puzzle [1][5] — although with *three* pack sizes the formula above no longer
applies. In fact, **no general closed-form formula is known for three or
more pack sizes**, and computing the Frobenius number in general is
NP-hard [4]. That is exactly why this app switches to a solver-based search.
"""
)
st.image(
    str(ASSETS_DIR / "chicken_mcnugget_theorem.png"),
    caption="The Chicken McNugget Theorem for two coprime pack sizes.",
    width=560,
)

# ---------------------------------------------------------------------------
# 3. The CP-SAT sliding-window algorithm
# ---------------------------------------------------------------------------
st.header("3. Approach A — the CP-SAT sliding-window search")
st.markdown(
    r"""
Once the gcd test says a solution exists, the app runs a **sliding-window
search** powered by **Google OR-Tools' CP-SAT constraint programming
solver** [6][7].

**The feasibility question.** For a target quantity $N$, CP-SAT is asked
whether the equation
"""
)
st.latex(
    r"p_1 x_1 + p_2 x_2 + p_3 x_3 + p_4 x_4 + p_5 x_5 = N,"
    r"\qquad x_i \in \{0, 1, 2, \ldots\}"
)
st.markdown(
    r"""
has **any** solution (unused pack slots simply don't appear). The $x_i$ are
integer decision variables — how many packs of size $p_i$ to buy. There is
**no objective function**: this is a pure feasibility check, which is exactly
what CP-SAT excels at [6].

**The search loop.** Let $P = \max(p_1,\dots,p_k)$.

```text
solve_threshold ← P          # consecutive feasible N's still needed
answer ← 0                   # largest infeasible N found so far
N ← 1
while solve_threshold > 0:
    if CP-SAT finds x with  p·x = N:      # N is purchasable
        solve_threshold ← solve_threshold − 1
    else:                                  # N is NOT purchasable
        answer ← N
        solve_threshold ← P                # reset the window
    N ← N + 1
return answer
```

**Why it can stop.** Suppose $P$ consecutive quantities
$N-P+1, \dots, N$ are all purchasable. Any larger quantity $M$ can be
reduced by repeatedly subtracting the smallest pack size $p_1$
($p_1 \le P$, so the window is wide enough) until it lands inside that
window — and "something purchasable plus whole packs" is still purchasable.
So once the window of $P$ consecutive successes closes, **no unreachable
quantity can ever appear again**, and the last recorded failure is the
answer. (Stopping after a run of consecutive representable values is the
standard round-based way to detect the Frobenius number [2][5].)

**Termination is guaranteed** by a Schur-type bound: when
$\gcd = 1$, the Frobenius number is at most
$(p_{\min}-1)(p_{\max}-1) - 1$ [2][4], so the loop provably finishes within
that many iterations plus one window.
"""
)
st.info(
    "Fine print: the search issues one CP-SAT solve per candidate N. For "
    "small everyday inputs (like 6, 9, 20) the answer appears in about a "
    "second; for adversarial inputs such as packs of 99 and 100 (answer "
    "9,701) it can take a few minutes, since thousands of tiny models are "
    "solved sequentially. That cost is exactly what Approach B below "
    "eliminates — which is why it is the app's default."
)

# ---------------------------------------------------------------------------
# 4. The residue-class (Apéry set) method
# ---------------------------------------------------------------------------
st.header("4. Approach B (default) — the residue-class table (Apéry set)")
st.markdown(
    r"""
The default solver skips the scanning loop entirely using a classical piece
of number theory: the **Apéry set** of a numerical semigroup, introduced by
Roger Apéry in 1946 [8].

#### Setup and notation

Write the set of *all* purchasable amounts as the **numerical semigroup**
generated by the pack sizes:
"""
)
st.latex(
    r"S = \langle p_1, \ldots, p_k \rangle = "
    r"\{\, p_1 x_1 + \cdots + p_k x_k \;:\; x_i \in \mathbb{Z}_{\ge 0} \,\}"
)
st.markdown(
    r"""
Let $a = \min(p_1, \dots, p_k)$ be the smallest pack size. The key
observation: **if $n$ is purchasable, so is $n + a$** (buy one more
$a$-pack). So inside each residue class modulo $a$ — the amounts leaving
remainder $r$ when divided by $a$ — the purchasable amounts are simply
*"everything from the first one upward, in steps of $a$."*

The **Apéry set of $S$ with respect to $a$** collects those "first ones"
[8][9]:
"""
)
st.latex(
    r"\operatorname{Ap}(S; a) = \{\, w_0, w_1, \ldots, w_{a-1} \,\},"
    r"\qquad w_r = \min\{\, s \in S : s \equiv r \ (\mathrm{mod}\ a) \,\}"
)
st.markdown(
    r"""
When $\gcd(p_1,\dots,p_k) = 1$, every residue class contains purchasable
amounts, so all $a$ values $w_r$ exist and are finite.

#### The two payoffs

**Membership in $O(1)$.** An amount $n$ is purchasable **iff** it is at
least as large as the first purchasable member of its residue class:
"""
)
st.latex(r"n \in S \iff n \ge w_{\,n \bmod a}")
st.markdown(
    r"""
**The Frobenius number by formula.** The largest *un*purchasable member of
residue class $r$ is exactly $w_r - a$ (one $a$-step below the class's
first purchasable member). Taking the worst class gives the
**Brauer–Shockley formula** [9]:
"""
)
st.latex(
    r"g(p_1, \ldots, p_k) \;=\; \max_{r} \bigl( w_r \bigr) \; - \; a"
)
st.markdown(
    r"""
#### Building the table: Nijenhuis's shortest-path algorithm

The table is computed with a lovely reduction to a shortest-path problem,
due to Nijenhuis [10]. Build a directed graph with one node per residue
$0, 1, \dots, a-1$. For every *other* pack size $p_j \ne a$, add an edge
"""
)
st.latex(r"r \;\xrightarrow{\;\text{weight } p_j\;}\; (r + p_j) \bmod a")
st.markdown(
    r"""
Buying an $a$-pack never changes a residue, so the cheapest way to *reach*
residue $r$ from 0 using the other packs is precisely $w_r$ — and that is a
single run of **Dijkstra's algorithm** from node 0, in
$O(a \cdot k \log a)$ time. For pack sizes capped at 100 this is
microseconds.

**Worked example — packs $\{6, 9, 20\}$**, residues mod $a = 6$:

| $r$ | $w_r$ | how |
|---|---|---|
| 0 | 0 | buy nothing |
| 1 | 49 | 9 + 20 + 20 |
| 2 | 20 | 20 |
| 3 | 9 | 9 |
| 4 | 40 | 20 + 20 |
| 5 | 29 | 9 + 20 |

Then $g = \max(0, 49, 20, 9, 40, 29) - 6 = 49 - 6 = \boxed{43}$ — the
famous McNugget number, with no search loop at all.

**A bonus:** the existence test of section 1 falls out automatically. If
$\gcd > 1$, the residues that are not multiples of the gcd are simply
unreachable in Nijenhuis's graph — Dijkstra reports no path — which *is*
the "No Solution" verdict.

Both approaches are available in the Problem Solver's dropdown; they always
agree (the app's unit tests verify this), differing only in speed and in
what they demonstrate — number theory versus constraint programming.
"""
)
