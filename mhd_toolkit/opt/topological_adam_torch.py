from __future__ import annotations

from typing import Any


def make_torch_topological_adam(params, **kwargs: Any):
    """Create torch-based TopologicalAdam if optional dependency is installed.

    This function keeps the main toolkit free from a hard torch dependency.
    """
    try:
        from topological_adam import TopologicalAdam as TorchTopologicalAdam  # type: ignore
    except Exception as exc:  # pragma: no cover
        raise ImportError(
            "Torch TopologicalAdam is not available. Install `topological-adam` and `torch` "
            "to use this optional backend."
        ) from exc

    return TorchTopologicalAdam(params, **kwargs)
