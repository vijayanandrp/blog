```bash
# Create virtual environment LINUX
python3 -m venv venv

# Activate virtual environment (MAC and LINUX)
. venv/bin/activate

pip install -r requirements.txt

pip install flake8 pytest pytest-cov

flake8 --exclude=venv* --statistics
pytest -v --cov=code
```

```powershell 
Set-ExecutionPolicy Unrestricted -Scope Process

# Run virtual environment WINDOWS
cd venv
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
    rev: v4.0.1
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
    rev: v0.910
    hooks:
    -   id: mypy
        args: [--ignore-missing-imports]
-   repo: https://github.com/asottile/seed-isort-config
    rev: v2.2.0
    hooks:
    -   id: seed-isort-config
-   repo: https://github.com/pre-commit/mirrors-isort
    rev: v5.9.3
    hooks:
    -   id: isort
-   repo: https://github.com/psf/black
    rev: 21.9b0
    hooks:
    -   id: black
-   repo: https://github.com/asottile/pyupgrade
    rev: v2.26.0
    hooks:
    -   id: pyupgrade
        args: [--py36-plus]
-   repo: https://github.com/asottile/blacken-docs
    rev: v1.11.0
    hooks:
    -   id: blacken-docs
        additional_dependencies: [black==20.8b1]
-   repo: https://gitlab.com/pycqa/flake8
    rev: '3.9.2'
    hooks:
    -   id: flake8
        args: [--ignore=E501]
-   repo: https://github.com/asottile/reorder_python_imports
    rev: v2.6.0
    hooks:
    -   id: reorder-python-imports
        args: [--py3-plus]
-   repo: local
    hooks:
    -   id: tests
        name: run tests
        entry: venv/Scripts/pytest.exe -v -m fast
        language: python
        additional_dependencies: [pre-commit, pytest]
        always_run: true
        pass_filenames: false
        types: [python]
        stages: [commit]

```

https://towardsdatascience.com/pre-commit-hooks-you-must-know-ff247f5feb7e

# Local 
```yaml
## Apply to all files without commiting:
##   pre-commit run --all-files --verbose
## Update this file:
##   pre-commit autoupdate


repos:
  - repo: https://github.com/aws-cloudformation/cfn-python-lint
    rev: v0.54.2  # The version of cfn-lint to use
    hooks:
      - id: cfn-python-lint
        name: AWS CloudFormation Linter
        entry: cfn-lint
        language: python
        args: [ '--template', 'template.yml', '--ignore-checks', 'W3011,W2001,W7001' ]
  - repo: https://github.com/PyCQA/flake8
    rev: 3.9.2
    hooks:
      - id: flake8
        additional_dependencies: [ flake8-typing-imports ]
        args: [ '--ignore=W605,E501' ]
  - repo: https://github.com/pre-commit/mirrors-autopep8
    rev: v1.5.7
    hooks:
      - id: autopep8
  - repo: local
    hooks:
      - id: pytest-cov
        name: coverage
        stages: [ push, commit ]
        language: system
        entry: pytest --cov=functions/src tests/  # --cov-fail-under=10
        types: [ python ]
        pass_filenames: false
      - id: pytest
        name: pytest
        stages: [ commit ]
        language: system
        entry: pytest tests
        pass_filenames: false
        always_run: true
        types: [ python ]
        
 ```
 
 
