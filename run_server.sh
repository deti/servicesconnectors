#! /usr/bin/env bash

source .venv/bin/activate

 python -m uvicorn src.main:app --reload