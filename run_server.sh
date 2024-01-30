#! /usr/bin/env bash

source .venv/bin/activate

# Upgrade the database
python -m alembic upgrade head

# Run the server
python -m uvicorn src.main:app --reload
