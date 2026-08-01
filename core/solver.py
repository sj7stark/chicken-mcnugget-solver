"""Core math and solver logic for the Chicken Nugget (Frobenius) problem.

Given a set of nugget pack sizes (e.g. 6, 9, 20), the Chicken Nugget Problem —
also known as the Frobenius coin problem — asks for the largest number of
nuggets that CANNOT be purchased exactly using any combination of those packs.

This module contains:

* :func:`solution_exists` — the gcd test that decides whether a largest
  unreachable number exists at all.
* :func:`apery_set` — the residue-class table (Apéry set), built with
  Nijenhuis's shortest-path algorithm.
* :func:`find_largest_unreachable_apery` — the Frobenius number read
  directly off the Apéry set via the Brauer–Shockley formula.
"""

from __future__ import annotations

import heapq
from functools import reduce
from math import gcd
from typing import Iterable, Optional

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


def apery_set(pack_sizes: Iterable[int]) -> dict[int, int]:
    """Compute the Apéry set of the pack sizes w.r.t. the smallest size.

    Let ``a = min(pack_sizes)``. For each residue ``r`` in ``0..a-1``, the
    Apéry set records ``w_r`` — the SMALLEST purchasable amount congruent to
    ``r`` modulo ``a`` [6]. Because adding an ``a``-pack moves any purchasable
    amount to the next member of its residue class, an amount ``n`` is
    purchasable **iff** ``n >= w_{n mod a}``, and the Frobenius number is
    ``max_r(w_r) - a`` (Brauer–Shockley formula [7]).

    The set is built with Nijenhuis's shortest-path method [8]: one graph
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

    Uses the Brauer–Shockley formula [7]: with ``a = min(pack_sizes)`` and
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
