@echo off
powershell -WindowStyle Hidden -Command "Start-Process pythonw -ArgumentList "location\telegramAutomation.py" -Verb RunAs -WindowStyle Hidden"
exit