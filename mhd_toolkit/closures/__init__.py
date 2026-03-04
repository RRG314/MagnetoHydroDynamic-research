from __future__ import annotations

from .base import Closure, ClosureContext
from .ideal import IdealClosure
from .resistive import ResistiveClosure
from .viscous import ViscousClosure


def make_closure(name: str, *, eta: float = 1e-3, nu: float = 0.0) -> Closure:
    n = name.lower()
    if n == "ideal":
        return IdealClosure()
    if n == "resistive":
        return ResistiveClosure(eta=eta)
    if n == "viscous":
        return ViscousClosure(nu=nu)
    if n == "resistive+viscous":
        # Lightweight combined closure.
        class Combined(Closure):
            name = "resistive+viscous"

            def __init__(self) -> None:
                self._r = ResistiveClosure(eta=eta)
                self._v = ViscousClosure(nu=nu)

            def apply_1d(self, U, context):  # type: ignore[override]
                return self._r.apply_1d(U, context) + self._v.apply_1d(U, context)

            def apply_2d(self, U, context):  # type: ignore[override]
                return self._r.apply_2d(U, context) + self._v.apply_2d(U, context)

        return Combined()
    raise ValueError(f"Unknown closure: {name}")


__all__ = [
    "Closure",
    "ClosureContext",
    "IdealClosure",
    "ResistiveClosure",
    "ViscousClosure",
    "make_closure",
]
