"""mhd-toolkit: practical MHD utilities and closure-research helpers."""

from .config import SolverConfig
from .solvers.fv1d import FV1DSolver
from .solvers.fv2d import FV2DSolver

__all__ = ["SolverConfig", "FV1DSolver", "FV2DSolver"]
__version__ = "0.1.0"
