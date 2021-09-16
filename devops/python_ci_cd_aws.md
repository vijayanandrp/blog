```bash
# Create virtual environment
python3 -m venv venv

# Activate virtual environment (Mac and Linux)
. venv/bin/activate

pip install -r requirements.

pip install flake8 pytest pytest-cov

flake8 --exclude=venv* --statistics
pytest -v --cov=calculator
```

```bash

```


## Pre-commit hooks
I love pre-commit as it fits so well in my workflow. I just commit as usual and pre-commit does all the checks which I sometimes forget. It speeds up development because the CI/CD pipeline is just way slower than executing the same steps locally. Especially for linting, it’s an enormous time-saver to quickly run black over the code instead of committing, waiting for the CI/CD pipeline, finding an error, fixing that error locally, pushing, and waiting again for the CI/CD pipeline.


https://towardsdatascience.com/pre-commit-hooks-you-must-know-ff247f5feb7e
