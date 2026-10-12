@echo off
python -m nexarack.cli info
python -m nexarack.cli run --seconds 10 --workload matrix --output outputs\run.json
pause
