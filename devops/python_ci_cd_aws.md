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
