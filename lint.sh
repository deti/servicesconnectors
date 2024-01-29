#!/usr/bin/env bash

source .venv/bin/activate

echo
echo "------- Running black: -------"
black src tests

echo
echo "------- Running mypy: -------"
mypy src tests

echo
echo "------- Running isort: -------"
isort src tests

echo
echo "------- Running flake8: -------"
flake8 src tests

echo
echo "------- Running pylint: -------"
pylint src
