# PLAN: Guide developers on installing pre-commit hooks and coding style
# Contributing

This project uses [pre-commit](https://pre-commit.com) to maintain code quality.

## Setup

```bash
pip install pre-commit
pre-commit install
```

Run all checks before pushing changes:

```bash
pre-commit run --all-files
```

### Secret Scanning

Generate a baseline to capture existing secrets and reduce false positives:

```bash
detect-secrets scan > .secrets.baseline
```

### Troubleshooting

If hooks fail unexpectedly, ensure your packages match `dev-requirements.txt` and
reinstall hooks with `pre-commit install`.
