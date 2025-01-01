#!/bin/bash

python src/wait_postgres.py

alembic upgrade head

python src/main.py