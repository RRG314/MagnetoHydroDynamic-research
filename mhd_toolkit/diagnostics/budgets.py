from __future__ import annotations

from dataclasses import dataclass, field
import json
from pathlib import Path
from typing import Any

from .invariants import totals_1d, totals_2d
from .divergence import divergence_report_2d
from ..equations.mhd_ideal import BX, BY


@dataclass
class Diagnostics:
    dim: int
    records: list[dict[str, Any]] = field(default_factory=list)
    initial: dict[str, float] | None = None

    def observe(self, U, time: float, dx: float, dy: float | None = None) -> dict[str, Any]:
        if self.dim == 1:
            totals = totals_1d(U, dx)
            div = {"l2_divB": 0.0, "max_abs_divB": 0.0, "normalized_l2_divB": 0.0}
        else:
            if dy is None:
                raise ValueError("dy is required for 2D diagnostics")
            totals = totals_2d(U, dx, dy)
            div = divergence_report_2d(U[BX], U[BY], dx, dy)

        if self.initial is None:
            self.initial = totals.copy()

        drift = {f"drift_{k}": totals[k] - self.initial[k] for k in totals.keys()}
        record: dict[str, Any] = {"time": float(time), **totals, **div, **drift}
        self.records.append(record)
        return record

    def latest(self) -> dict[str, Any]:
        return self.records[-1] if self.records else {}

    def to_json(self, path: str | Path) -> None:
        p = Path(path)
        p.parent.mkdir(parents=True, exist_ok=True)
        payload = {
            "initial": self.initial,
            "num_records": len(self.records),
            "records": self.records,
        }
        p.write_text(json.dumps(payload, indent=2), encoding="utf-8")
