#! /usr/bin/env bash
source .venv/bin/activate

echo "------- Update live dependencies: -------"
rm -f requirements.txt
pip-compile -q

echo
echo "------- Update dev dependencies: -------"
rm -f requirements_dev.txt
pip-compile -q requirements_dev.in
pip install --upgrade -r requirements_dev.txt
