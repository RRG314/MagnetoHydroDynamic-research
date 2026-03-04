# mhd-toolkit

A practical, Python-first MHD toolkit for divergence control, closure experimentation, diagnostics, and reproducible verification workflows.

This repository is designed for researchers who need reliable building blocks, not a monolithic production simulator.

## Why This Exists

Many MHD projects need the same core utilities repeatedly:

1. Divergence control (`projection` and `GLM`)
2. Closure sandboxing (`ideal`, `resistive`, `viscous`)
3. Diagnostics and verification outputs suitable for papers and benchmarks
4. A clean path to optimization-based residual solves

`mhd-toolkit` provides these as modular tools with CLI workflows, tests, examples, and report-friendly JSON outputs.

## Implemented Today

- 1D finite-volume baseline solver (conservative state, Rusanov flux)
- 2D finite-volume baseline solver with split sweeps
- Divergence cleaning utilities:
  - Projection cleaning (Poisson solve, FFT periodic + Jacobi fallback)
  - GLM cleaning (Dedner-style `psi` field)
- Closure sandbox:
  - `ideal`
  - `resistive`
  - `viscous` (simple Laplacian momentum smoothing)
- Diagnostics object with:
  - mass, momentum, kinetic, magnetic, total energy
  - drift tracking
  - divergence metrics (`L2`, `max`, normalized)
- Standard initial-condition modules:
  - Brio-Wu
  - Orszag-Tang
  - reconnection toy
- Optimization module:
  - Adam residual minimization
  - Topological Adam (NumPy implementation)
  - Optional torch Topological Adam backend loader
- CLI + examples + pytest suite

## Not Implemented Yet

- High-order Riemann solvers (HLL/HLLD)
- Full constrained transport implementation
- AMR and large-scale production features

## Install

```bash
pip install -e .
```

Optional plotting extras:

```bash
pip install -e .[viz]
```

## CLI Quick Start

Run Brio-Wu:

```bash
python -m mhd_toolkit run brio-wu --nx 800 --closure resistive --divfree none
```

Run Orszag-Tang with projection cleaning:

```bash
python -m mhd_toolkit run orszag-tang --nx 256 --ny 256 --divfree projection
```

Compare closures:

```bash
python -m mhd_toolkit compare closures --problem brio-wu --closures ideal,resistive
```

Divergence cleaning demo:

```bash
python -m mhd_toolkit divfree demo --problem orszag-tang --method projection,glm
```

Residual optimization demo:

```bash
python -m mhd_toolkit opt residual-demo
```

## Documentation Map

- [Project Overview](docs/README.md)
- [User Guide](docs/user_guide.md)
- [Tool Reference](docs/tool_reference.md)
- [CLI Reference](docs/cli_reference.md)
- [Divergence Control](docs/divergence_control.md)
- [Closure Sandbox](docs/closure_sandbox.md)
- [Diagnostics and Verification](docs/diagnostics_and_verification.md)
- [Benchmark Report](docs/benchmark_report.md)
- [Topological Adam Branch Audit](docs/topological_adam_branch_audit.md)
- [Paper References](docs/paper_references.md)
- [Roadmap](docs/roadmap.md)

## Scientific Positioning

This is a research toolkit. It is useful for controlled experiments, comparisons, and rapid method prototyping. It is not presented as a replacement for mature MHD production codes such as Athena, PLUTO, or FLASH.

## Topological Adam Integration

Topological Adam is included in the optimization module and informed by branch-level audit of `RRG314/topological-adam`.

- NumPy implementation: `mhd_toolkit/opt/topological_adam.py`
- Optional torch backend loader: `mhd_toolkit/opt/topological_adam_torch.py`

See [docs/topological_adam_branch_audit.md](docs/topological_adam_branch_audit.md) for branch-by-branch integration notes.

## Paper References

- MHD preprint draft: `docs/papers/MHD_draft_2025.pdf`
- Topological Adam preprint: `docs/papers/Topological_Adam_Preprint_2025.pdf`

Details and citation notes are in [docs/paper_references.md](docs/paper_references.md).

## Development and Quality

- Run tests:

```bash
pytest
```

- CI workflow is included under `.github/workflows/ci.yml`.

## License

MIT. See [LICENSE](LICENSE).
