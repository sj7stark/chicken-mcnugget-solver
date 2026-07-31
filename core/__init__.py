"""Core package for the Chicken Nugget Problem solver.

Exposes the math/solver API (``core.solver``) and the shared Streamlit UI
helpers (``core.ui``). Import the solver pieces directly from the package:

    from core import find_largest_unreachable, solution_exists
"""

from core.solver import (
    MAX_NUM_PACKS,
    MAX_PACK_SIZE,
    MIN_NUM_PACKS,
    MIN_PACK_SIZE,
    NoSolutionError,
    find_largest_unreachable,
    is_representable_cpsat,
    solution_exists,
    validate_pack_sizes,
)

__all__ = [
    "MAX_NUM_PACKS",
    "MAX_PACK_SIZE",
    "MIN_NUM_PACKS",
    "MIN_PACK_SIZE",
    "NoSolutionError",
    "find_largest_unreachable",
    "is_representable_cpsat",
    "solution_exists",
    "validate_pack_sizes",
]
