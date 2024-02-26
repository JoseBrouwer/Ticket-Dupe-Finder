@echo off

python -m ensurepip --upgrade --quiet
python -m pip install -r requirements.txt

python tickets.py

pause
