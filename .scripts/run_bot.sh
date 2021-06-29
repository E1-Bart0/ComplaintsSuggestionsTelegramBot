#!/bin/sh

cd db/ && alembic upgrade head
cd ../ && python main.py
