# Contributing

Thanks for contributing to `MagnetoHydroDynamic-research`.

## Development Setup

```bash
pip install -e .[dev]
```

## Before Opening a PR

1. Run tests:

```bash
pytest
```

2. Run at least one CLI smoke command and attach output JSON path in the PR description.

3. Keep changes modular. Avoid mixing unrelated numerical, API, and docs rewrites in a single PR.

## Style Expectations

- Keep APIs explicit and typed where practical.
- Prefer deterministic behavior for tests and demos.
- Document every new CLI command in `docs/cli_reference.md`.
- Document every new module in `docs/tool_reference.md`.

## Scientific Changes

If you change equations, fluxes, closures, or divergence cleaning methods:
- include a short derivation or rationale in docs
- include at least one verification metric in tests or benchmark report
- avoid novelty claims without evidence
