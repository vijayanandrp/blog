```bash
# Create virtual environment LINUX
python3 -m venv venv

# Activate virtual environment (MAC and LINUX)
. venv/bin/activate

pip install -r requirements.

pip install flake8 pytest pytest-cov

flake8 --exclude=venv* --statistics
pytest -v --cov=calculator
```

```powershell 
# Run virtual environment WINDOWS
Scripts\activate.ps1

# instead of activate.bat which doesn't work in PowerShell any more.
# Also deactivate it by just typing
deactivate

```



## Pre-commit hooks
I love pre-commit as it fits so well in my workflow. I just commit as usual and pre-commit does all the checks which I sometimes forget. It speeds up development because the CI/CD pipeline is just way slower than executing the same steps locally. Especially for linting, it’s an enormous time-saver to quickly run black over the code instead of committing, waiting for the CI/CD pipeline, finding an error, fixing that error locally, pushing, and waiting again for the CI/CD pipeline.

https://towardsdatascience.com/pre-commit-hooks-you-must-know-ff247f5feb7e

```yaml
# Apply to all files without commiting:
#   pre-commit run --all-files
# Update this file:
#   pre-commit autoupdate
repos:
-   repo: https://github.com/pre-commit/pre-commit-hooks
    rev: v3.2.0
    hooks:
    -   id: check-ast
    -   id: check-byte-order-marker
    -   id: check-case-conflict
    -   id: check-docstring-first
    -   id: check-executables-have-shebangs
    -   id: check-json
    -   id: check-added-large-files
    -   id: check-yaml
    -   id: debug-statements
    -   id: detect-aws-credentials
    -   id: detect-private-key
    -   id: end-of-file-fixer
    -   id: trailing-whitespace
    -   id: mixed-line-ending
-   repo: https://github.com/pre-commit/mirrors-mypy
    rev: v0.782
    hooks:
    -   id: mypy
        args: [--ignore-missing-imports]
-   repo: https://github.com/asottile/seed-isort-config
    rev: v2.2.0
    hooks:
    -   id: seed-isort-config
-   repo: https://github.com/pre-commit/mirrors-isort
    rev: v5.4.2
    hooks:
    -   id: isort
-   repo: https://github.com/psf/black
    rev: 20.8b1
    hooks:
    -   id: black
-   repo: https://github.com/asottile/pyupgrade
    rev: v2.7.2
    hooks:
    -   id: pyupgrade
        args: [--py36-plus]
-   repo: https://github.com/asottile/blacken-docs
    rev: v1.8.0
    hooks:
    -   id: blacken-docs
        additional_dependencies: [black==20.8b1]
-   repo: https://gitlab.com/pycqa/flake8
    rev: '3.8.3'
    hooks:
    -   id: flake8
        args: [--ignore=E501]

```

https://towardsdatascience.com/pre-commit-hooks-you-must-know-ff247f5feb7e
