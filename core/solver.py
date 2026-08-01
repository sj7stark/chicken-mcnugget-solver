"""Core math and solver logic for the Chicken Nugget (Frobenius) problem.

Given a set of nugget pack sizes (e.g. 6, 9, 20), the Chicken Nugget Problem —
also known as the Frobenius coin problem — asks for the largest number of
nuggets that CANNOT be purchased exactly using any combination of those packs.

This module contains:

* :func:`solution_exists` — the gcd test that decides whether a largest
  unreachable number exists at all.
* :func:`is_representable_cpsat` — a feasibility check for a single target
  amount, solved with Google OR-Tools' CP-SAT constraint programming solver.
* :func:`find_largest_unreachable` — the sliding-window search that finds the
  Frobenius number by repeatedly calling the CP-SAT feasibility check.

The search algorithm follows the approach specified by the project owner
(scan N = 1, 2, 3, ... and stop once ``max(pack_sizes)`` consecutive values
are representable), with two small corrections noted in the function
docstring so that the search always terminates and is correct for small
edge cases.
"""

from __future__ import annotations

import heapq
from functools import reduce
from math import gcd
from typing import Callable, Iterable, Optional

# ---------------------------------------------------------------------------
# Input bounds enforced by the UI and re-validated here (defense in depth).
# ---------------------------------------------------------------------------
MIN_PACK_SIZE: int = 2
MAX_PACK_SIZE: int = 250
MIN_NUM_PACKS: int = 2
MAX_NUM_PACKS: int = 20


class NoSolutionError(ValueError):
    """Raised when the Frobenius number does not exist for the given packs.

    This happens exactly when ``gcd(pack_sizes) > 1``: every purchasable
    amount is then a multiple of that gcd, so infinitely many amounts are
    unreachable and there is no *largest* unreachable amount.
    """


def validate_pack_sizes(pack_sizes: Iterable[int]) -> list[int]:
    """Validate and normalize user-provided pack sizes.

    Duplicates are removed (a duplicated pack size adds no new purchasable
    amounts) and the result is sorted ascending.

    Args:
        pack_sizes: Iterable of pack sizes as integers.

    Returns:
        Sorted list of unique pack sizes.

    Raises:
        ValueError: If any size is not an integer in
            [``MIN_PACK_SIZE``, ``MAX_PACK_SIZE``], or if the number of
            *distinct* sizes falls outside
            [1, ``MAX_NUM_PACKS``] (a single distinct size is allowed here so
            duplicates entered in the UI degrade gracefully; the UI itself
            asks for ``MIN_NUM_PACKS``..``MAX_NUM_PACKS`` sizes).
    """
    sizes = list(pack_sizes)
    for s in sizes:
        # bool is a subclass of int, so exclude it explicitly.
        if isinstance(s, bool) or not isinstance(s, int):
            raise ValueError(f"Pack size {s!r} is not an integer.")
        if not (MIN_PACK_SIZE <= s <= MAX_PACK_SIZE):
            raise ValueError(
                f"Pack size {s} is outside the allowed range "
                f"[{MIN_PACK_SIZE}, {MAX_PACK_SIZE}]."
            )
    unique_sizes = sorted(set(sizes))
    if not (1 <= len(unique_sizes) <= MAX_NUM_PACKS):
        raise ValueError(
            f"Expected between 1 and {MAX_NUM_PACKS} distinct pack sizes, "
            f"got {len(unique_sizes)}."
        )
    return unique_sizes


def solution_exists(pack_sizes: Iterable[int]) -> bool:
    """Decide whether the Chicken Nugget Problem has a solution.

    A largest unreachable amount (Frobenius number) exists if and only if the
    greatest common divisor of ALL pack sizes equals 1. The pack sizes do not
    need to be pairwise coprime — e.g. {6, 10, 15} has gcd 1 (and Frobenius
    number 29) even though every pair shares a factor.

    Args:
        pack_sizes: Iterable of validated pack sizes (each >= 2).

    Returns:
        True if gcd(pack_sizes) == 1 (a solution exists), False otherwise.
    """
    sizes = validate_pack_sizes(pack_sizes)
    return reduce(gcd, sizes) == 1


def is_representable_cpsat(target: int, pack_sizes: Iterable[int]) -> bool:
    """Check whether ``target`` nuggets can be bought exactly, via CP-SAT.

    Builds the constraint programming feasibility model

        p1*x1 + p2*x2 + ... + pk*xk == target,  xi >= 0 integer

    where ``pi`` are the pack sizes and ``xi`` are integer decision variables
    (how many packs of each size to buy). There is no objective function; we
    only need to know whether ANY solution exists. The model is solved with
    Google OR-Tools' CP-SAT solver.

    Args:
        target: The exact number of nuggets to reach (>= 0).
        pack_sizes: Iterable of validated pack sizes (each >= 2).

    Returns:
        True if some combination of packs sums exactly to ``target``,
        False otherwise.

    Raises:
        ValueError: If ``target`` is negative.
        ImportError: If Google OR-Tools is not installed.
    """
    # Imported lazily so that the pure-math parts of this module (gcd test,
    # window search with an injected checker) work even where OR-Tools is
    # not installed. On Streamlit Cloud / local runs it is installed via
    # requirements.txt.
    from ortools.sat.python import cp_model

    if target < 0:
        raise ValueError(f"target must be non-negative, got {target}.")

    sizes = validate_pack_sizes(pack_sizes)

    model = cp_model.CpModel()
    # Each xi can be at most target // pi packs (any more would overshoot).
    variables = [
        model.NewIntVar(0, target // size, f"x_{i}")
        for i, size in enumerate(sizes)
    ]
    # The single equality constraint: packs bought must total `target`.
    model.Add(
        sum(size * var for size, var in zip(sizes, variables)) == target
    )

    solver = cp_model.CpSolver()
    status = solver.Solve(model)
    # FEASIBLE/OPTIMAL both mean "a combination exists".
    return status in (cp_model.OPTIMAL, cp_model.FEASIBLE)


def apery_set(pack_sizes: Iterable[int]) -> dict[int, int]:
    """Compute the Apéry set of the pack sizes w.r.t. the smallest size.

    Let ``a = min(pack_sizes)``. For each residue ``r`` in ``0..a-1``, the
    Apéry set records ``w_r`` — the SMALLEST purchasable amount congruent to
    ``r`` modulo ``a`` [8]. Because adding an ``a``-pack moves any purchasable
    amount to the next member of its residue class, an amount ``n`` is
    purchasable **iff** ``n >= w_{n mod a}``, and the Frobenius number is
    ``max_r(w_r) - a`` (Brauer–Shockley formula [9]).

    The set is built with Nijenhuis's shortest-path method [10]: one graph
    node per residue class, and for every other pack size ``p`` an edge
    ``r -> (r + p) mod a`` of weight ``p``. Dijkstra's algorithm from node 0
    then yields exactly ``w_r`` as the shortest-path distance to node ``r``.
    Runtime is O(a * k * log a) for k pack sizes — effectively instant for
    pack sizes up to 250.

    Args:
        pack_sizes: Iterable of validated pack sizes (each >= 2) whose gcd
            must be 1 (otherwise some residue classes are unreachable and the
            Apéry set is not fully defined).

    Returns:
        Dict mapping each residue ``r`` (0..a-1) to ``w_r``, the smallest
        purchasable amount congruent to ``r`` mod ``a``.

    Raises:
        NoSolutionError: If gcd(pack_sizes) > 1.
    """
    sizes = validate_pack_sizes(pack_sizes)
    if not solution_exists(sizes):
        raise NoSolutionError(
            f"gcd({', '.join(map(str, sizes))}) > 1 — some residue classes "
            "are entirely unreachable, so the Apéry set is not defined and "
            "no largest unreachable number exists."
        )

    a = sizes[0]           # smallest pack size; residues are taken mod a
    others = sizes[1:]     # non-empty here: a single size >= 2 has gcd >= 2

    # Dijkstra over the residue graph. distances[r] = smallest purchasable
    # amount congruent to r (mod a) reachable using only the *other* pack
    # sizes; a-packs are implicit (they move within a residue class).
    distances: dict[int, Optional[int]] = {r: None for r in range(a)}
    distances[0] = 0
    frontier: list[tuple[int, int]] = [(0, 0)]  # (distance, residue)
    while frontier:
        dist, residue = heapq.heappop(frontier)
        if dist > distances[residue]:  # stale heap entry
            continue
        for p in others:
            new_dist = dist + p
            new_residue = (residue + p) % a
            if distances[new_residue] is None or new_dist < distances[new_residue]:
                distances[new_residue] = new_dist
                heapq.heappush(frontier, (new_dist, new_residue))

    # gcd == 1 guarantees every residue class was reached.
    return {r: d for r, d in distances.items()}


def find_largest_unreachable_apery(pack_sizes: Iterable[int]) -> int:
    """Find the Frobenius number directly from the Apéry set.

    Uses the Brauer–Shockley formula [9]: with ``a = min(pack_sizes)`` and
    Apéry set values ``w_r``, the largest unpurchasable amount is

        g = max_r(w_r) - a

    (the largest non-representable member of the residue class whose first
    representable member arrives latest). This needs no scanning loop and no
    constraint solver — see :func:`apery_set` for how the table is built.

    Args:
        pack_sizes: Iterable of validated pack sizes (each >= 2) whose gcd
            must be 1.

    Returns:
        The largest number of nuggets that cannot be purchased exactly.

    Raises:
        NoSolutionError: If gcd(pack_sizes) > 1.
    """
    sizes = validate_pack_sizes(pack_sizes)
    table = apery_set(sizes)
    return max(table.values()) - sizes[0]


def find_largest_unreachable(
    pack_sizes: Iterable[int],
    is_representable: Optional[Callable[[int], bool]] = None,
    progress_callback: Optional[Callable[[int, int], None]] = None,
) -> int:
    """Find the Frobenius number via the sliding-window CP-SAT search.

    The search scans target amounts N = 1, 2, 3, ... and, for each N, asks the
    CP-SAT solver whether N is exactly purchasable:

    * ``solve_threshold`` starts at ``max(pack_sizes)``.
    * If N IS representable, decrement ``solve_threshold`` by 1.
    * If N is NOT representable, record ``answer = N`` and reset
      ``solve_threshold`` back to ``max(pack_sizes)``.
    * Stop when ``solve_threshold`` reaches 0; ``answer`` is then the largest
      unreachable amount.

    Why stopping is valid: once ``max(pack_sizes)`` consecutive amounts are
    all representable, every larger amount is too — for any larger N,
    subtracting a suitable multiple of the smallest pack size lands inside
    that fully-representable window (the window is at least ``smallest``
    wide, since ``smallest <= max(pack_sizes)``). Hence no unreachable
    amount can occur later, and the last recorded ``answer`` is the largest.

    Note: this implements the algorithm specified by the project owner with
    two small corrections: (1) the increment/decrement roles of the two
    branches are arranged so the counter counts *consecutive successes*
    (otherwise the loop would never terminate once every amount becomes
    representable), and (2) the scan starts at N = 1 rather than
    ``max(pack_sizes) + 1`` so small answers (e.g. packs {2, 3}, whose answer
    is 1) are found correctly.

    Args:
        pack_sizes: Iterable of validated pack sizes (each >= 2) whose gcd
            must be 1.
        is_representable: Optional replacement feasibility checker taking a
            target amount and returning bool. Defaults to the CP-SAT checker
            (:func:`is_representable_cpsat`). Injecting a checker is used by
            the unit tests, which verify the window logic against an
            independent dynamic-programming oracle.
        progress_callback: Optional callable invoked after every check with
            ``(current_target, safety_cap)`` — handy for UI progress bars.

    Returns:
        The largest number of nuggets that cannot be purchased exactly.

    Raises:
        NoSolutionError: If gcd(pack_sizes) > 1, i.e. no solution exists.
        RuntimeError: If the search exceeds its theoretical safety cap
            (indicates a bug or a faulty ``is_representable`` implementation).
    """
    sizes = validate_pack_sizes(pack_sizes)
    if not solution_exists(sizes):
        raise NoSolutionError(
            f"gcd({', '.join(map(str, sizes))}) > 1 — every purchasable "
            "amount is a multiple of that gcd, so no largest unreachable "
            "number exists."
        )

    if is_representable is None:
        # Default: ask CP-SAT about each target amount.
        def is_representable(n: int, _sizes: tuple[int, ...] = tuple(sizes)) -> bool:
            return is_representable_cpsat(n, _sizes)

    smallest, largest = sizes[0], sizes[-1]
    # Schur-type upper bound: for gcd = 1, the Frobenius number is at most
    # (smallest - 1) * (largest - 1) - 1. Scanning must finish within the
    # bound plus one full window; anything beyond that indicates a bug.
    safety_cap = (smallest - 1) * (largest - 1) + largest + 1

    solve_threshold = largest  # consecutive representable amounts still needed
    answer = 0                 # largest unreachable amount seen so far
    n = 1                      # current target amount being tested

    while solve_threshold > 0:
        if n > safety_cap:
            raise RuntimeError(
                "Search exceeded its theoretical upper bound — "
                "the feasibility checker appears to be inconsistent."
            )
        if is_representable(n):
            solve_threshold -= 1
        else:
            answer = n
            solve_threshold = largest
        if progress_callback is not None:
            progress_callback(n, safety_cap)
        n += 1

    return answer
