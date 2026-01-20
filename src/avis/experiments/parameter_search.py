"""Parameter search / sweep wrapper.

Original notebook:
- `original/Parameter_search_til_rapport.ipynb`

Goal of this module:
- make the sweep reproducible (fixed seeds)
- save results as CSV/JSONL
- decouple data loading from the search logic

This file currently contains scaffolding only.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Dict, Iterable, List, Optional


@dataclass
class SweepResult:
    params: Dict[str, Any]
    metric: float
    extra: Dict[str, Any]


def run_sweep(*args: Any, **kwargs: Any) -> List[SweepResult]:
    raise NotImplementedError(
        "Port the sweep logic from the original notebook into this module."
    )
