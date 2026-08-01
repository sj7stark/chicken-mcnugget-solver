"""Unit tests for ``core.solver``.

Run from the repository root with either:

    python -m pytest tests/ -q
    python tests/test_solver.py        # no pytest needed

The sliding-window search is verified against an independent
dynamic-programming oracle (`dp_frobenius`), so the window logic is tested
even in environments where OR-Tools is unavailable. When OR-Tools IS
installed, the CP-SAT feasibility checker and the full end-to-end solve are
tested too.
"""

from __future__ import annotations

import sys
from functools import reduce
from math import gcd
from pathlib import Path

# Allow "python tests/test_solver.py" from the repo root without installing.
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from core import (  # noqa: E402
    NoSolutionError,
    apery_set,
    find_largest_unreachable,
    find_largest_unreachable_apery,
    solution_exists,
    validate_pack_sizes,
)

try:  # OR-Tools is optional for the pure-logic tests.
    from core import is_representable_cpsat

    from ortools.sat.python import cp_model  # noqa: F401

    HAVE_ORTOOLS = True
except ImportError:  # pragma: no cover - depends on environment
    HAVE_ORTOOLS = False


def dp_representable(limit: int, packs: list[int]) -> list[bool]:
    """Compute representability of 0..limit by dynamic programming.

    Args:
        limit: Largest amount to evaluate.
        packs: Pack sizes (positive integers).

    Returns:
        List ``r`` where ``r[n]`` is True iff ``n`` is a non-negative integer
        combination of ``packs``.
    """
    reachable = [False] * (limit + 1)
    reachable[0] = True
    for n in range(1, limit + 1):
        reachable[n] = any(n >= p and reachable[n - p] for p in packs)
    return reachable


def dp_frobenius(packs: list[int]) -> int:
    """Reference Frobenius number via brute-force dynamic programming.

    Args:
        packs: Pack sizes with gcd 1 (each >= 2).

    Returns:
        The largest non-representable positive integer.
    """
    assert reduce(gcd, packs) == 1
    limit = (min(packs) - 1) * (max(packs) - 1) + max(packs)
    reachable = dp_representable(limit, packs)
    return max(n for n in range(1, limit + 1) if not reachable[n])


def make_dp_checker(packs: list[int]):
    """Build a DP-backed ``is_representable`` callable for injection.

    Args:
        packs: Pack sizes with gcd 1.

    Returns:
        Callable mapping a target amount to a bool, backed by the DP table.
    """
    limit = (min(packs) - 1) * (max(packs) - 1) + max(packs) + 2
    table = dp_representable(limit, packs)
    return lambda n: table[n]


# ---------------------------------------------------------------------------
# Test cases: (packs, expected Frobenius number or None if no solution)
# ---------------------------------------------------------------------------
KNOWN_CASES: list[tuple[list[int], int | None]] = [
    ([6, 9, 20], 43),        # the classic McNugget numbers
    ([2, 3], 1),             # smallest possible answer
    ([2, 5], 3),             # McNugget theorem: 2*5-2-5 = 3
    ([3, 5], 7),             # 3*5-3-5 = 7
    ([6, 10, 15], 29),       # pairwise NON-coprime, overall gcd 1
    ([11, 13, 15, 17, 19], 42),  # five pack sizes
    ([4, 6, 10], None),      # gcd 2 -> no solution
    ([10, 20, 30, 40, 50], None),  # gcd 10 -> no solution
]


def test_validate_pack_sizes() -> None:
    """Validation accepts good input, dedupes, and rejects bad input."""
    assert validate_pack_sizes([9, 6, 20, 9]) == [6, 9, 20]
    for bad in ([1, 5], [0, 3], [-2, 7], [101, 3], [2.5, 3], [True, 3]):
        try:
            validate_pack_sizes(bad)  # type: ignore[arg-type]
            raise AssertionError(f"expected ValueError for {bad!r}")
        except ValueError:
            pass


def test_solution_exists() -> None:
    """The gcd existence test agrees with the expected outcomes."""
    for packs, expected in KNOWN_CASES:
        assert solution_exists(packs) is (expected is not None), packs


def test_window_search_against_dp_oracle() -> None:
    """The sliding-window logic returns the true Frobenius number.

    Uses the DP oracle as the feasibility checker (no OR-Tools needed) and
    cross-checks against the independent brute-force reference, plus the
    known expected values.
    """
    for packs, expected in KNOWN_CASES:
        if expected is None:
            continue
        result = find_largest_unreachable(
            packs, is_representable=make_dp_checker(packs)
        )
        assert result == expected == dp_frobenius(packs), packs


def test_window_search_random_cases() -> None:
    """Randomized cross-check of the window logic vs. the DP reference."""
    import random

    rng = random.Random(1234)
    tested = 0
    while tested < 40:
        k = rng.randint(2, 8)
        packs = sorted(rng.sample(range(2, 40), k))
        if reduce(gcd, packs) != 1:
            continue
        tested += 1
        result = find_largest_unreachable(
            packs, is_representable=make_dp_checker(packs)
        )
        assert result == dp_frobenius(packs), packs


def test_no_solution_raises() -> None:
    """Sets with gcd > 1 raise NoSolutionError."""
    for packs, expected in KNOWN_CASES:
        if expected is not None:
            continue
        try:
            find_largest_unreachable(
                packs, is_representable=lambda n: True
            )
            raise AssertionError(f"expected NoSolutionError for {packs!r}")
        except NoSolutionError:
            pass


def test_apery_set_mcnugget() -> None:
    """The Apéry set of {6, 9, 20} matches the hand-computed table."""
    assert apery_set([6, 9, 20]) == {0: 0, 1: 49, 2: 20, 3: 9, 4: 40, 5: 29}


def test_apery_set_membership_criterion() -> None:
    """n is representable iff n >= w_{n mod a}, cross-checked against DP."""
    for packs in ([6, 9, 20], [2, 3], [6, 10, 15], [11, 13, 15, 17, 19]):
        a = min(packs)
        table = apery_set(packs)
        limit = max(table.values()) + a + 5
        reachable = dp_representable(limit, packs)
        for n in range(limit + 1):
            assert (n >= table[n % a]) == reachable[n], (packs, n)


def test_apery_method_known_cases() -> None:
    """The Apéry/Brauer–Shockley solver reproduces all known answers."""
    for packs, expected in KNOWN_CASES:
        if expected is None:
            continue
        assert find_largest_unreachable_apery(packs) == expected, packs


def test_apery_method_random_cases() -> None:
    """Randomized cross-check: Apéry solver vs. the DP reference."""
    import random

    rng = random.Random(98765)
    tested = 0
    while tested < 60:
        k = rng.randint(2, 8)
        packs = sorted(rng.sample(range(2, 101), k))
        if reduce(gcd, packs) != 1:
            continue
        tested += 1
        assert find_largest_unreachable_apery(packs) == dp_frobenius(packs), packs


def test_apery_agrees_with_window_search() -> None:
    """Both solver approaches return identical answers on random inputs."""
    import random

    rng = random.Random(555)
    tested = 0
    while tested < 25:
        k = rng.randint(2, 8)
        packs = sorted(rng.sample(range(2, 35), k))
        if reduce(gcd, packs) != 1:
            continue
        tested += 1
        window = find_largest_unreachable(
            packs, is_representable=make_dp_checker(packs)
        )
        assert find_largest_unreachable_apery(packs) == window, packs


def test_apery_no_solution_raises() -> None:
    """Apéry functions raise NoSolutionError when gcd > 1."""
    for packs, expected in KNOWN_CASES:
        if expected is not None:
            continue
        for fn in (apery_set, find_largest_unreachable_apery):
            try:
                fn(packs)
                raise AssertionError(
                    f"expected NoSolutionError from {fn.__name__} for {packs!r}"
                )
            except NoSolutionError:
                pass


def test_cpsat_checker() -> None:
    """CP-SAT feasibility answers match the DP oracle (needs OR-Tools)."""
    if not HAVE_ORTOOLS:
        print("  (OR-Tools not installed - skipping CP-SAT checker test)")
        return
    packs = [6, 9, 20]
    table = dp_representable(60, packs)
    for n in range(61):
        assert is_representable_cpsat(n, packs) == table[n], n


def test_cpsat_end_to_end() -> None:
    """Full CP-SAT-backed solve returns 43 for the classic McNugget packs."""
    if not HAVE_ORTOOLS:
        print("  (OR-Tools not installed - skipping CP-SAT end-to-end test)")
        return
    assert find_largest_unreachable([6, 9, 20]) == 43
    assert find_largest_unreachable([6, 10, 15]) == 29


if __name__ == "__main__":
    # Minimal runner so the tests work without pytest.
    failures = 0
    for name, fn in sorted(globals().items()):
        if name.startswith("test_") and callable(fn):
            try:
                fn()
                print(f"PASS  {name}")
            except AssertionError as exc:  # pragma: no cover
                failures += 1
                print(f"FAIL  {name}: {exc}")
    sys.exit(1 if failures else 0)
