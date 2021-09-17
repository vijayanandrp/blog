You can create a workflow by creating a YAML file inside the .github/workflows/ci.yml folder.

Next, open the file and add the following content:

```yaml
name: Run Python Tests
on:
  push:
    branches:
      - master
  pull_request:
    branches:
      - master

jobs:
  build:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2
      - name: Install Python 3
        uses: actions/setup-python@v1
        with:
          python-version: 3.6
      - name: Install dependencies
        run: |
          python -m pip install --upgrade pip
          pip install -r requirements.txt
      - name: Run tests with pytest
        run: pytest 
 ```
 
 ```yaml
 name: Run Python Tests

# Triggers the workflow on push or pull request events
on: [push, pull_request]

jobs:
  test:
    name: Test (python-${{ matrix.python-version }}, ${{ matrix.os }})
    runs-on: ${{ matrix.os }}
    strategy:
      fail-fast: false
      max-parallel: 10
      matrix:
        os:
          - macos-latest
          - ubuntu-18.04
          - ubuntu-20.04
          - ubuntu-latest
          - windows-2019
          - windows-2022
          - windows-latest
        python-version: [3.8]

        include:
          - os: macos-latest
            python-version: 3.7
          - os: ubuntu-latest
            python-version: 3.7
          - os: windows-latest
            python-version: 3.7

          - os: macos-latest
            python-version: 3.6
          - os: ubuntu-latest
            python-version: 3.6
          - os: windows-latest
            python-version: 3.6
    steps:
      - uses: actions/checkout@v2
      - name: Install Python 3
        uses: actions/setup-python@v1
        with:
          python-version: 3.8
      - name: Install dependencies
        run: |
          python -m pip install --upgrade pip
          pip install -r requirements.txt
      - name: Run tests with pytest
        run: pytest
        
 ```
