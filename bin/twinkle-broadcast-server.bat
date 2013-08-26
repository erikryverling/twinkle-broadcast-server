@echo off
SET SCRIPT_DIR=%~dp0..\twinkle-broadcast-server
cd %SCRIPT_DIR%
python broadcastserver.py %*
