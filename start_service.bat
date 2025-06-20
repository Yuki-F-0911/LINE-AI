@echo off
echo LINE練習相談アプリケーション 24時間サービス起動中...

cd /d "%~dp0"

REM 仮想環境をアクティベート
call .venv\Scripts\activate.bat

REM サービス起動
python scripts\windows_service.py

pause 