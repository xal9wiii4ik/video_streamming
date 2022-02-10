#!/bin/sh

flask db upgrade
python main.py

exec "$@"