@echo off
echo ========================================
echo   Amazon Sentiment Analysis Pipeline
echo ========================================

echo.
echo [1/4] Verification des containers Docker...

:check_containers
set all_running=true

docker inspect -f "{{.State.Running}}" amazon-kafka 2>nul | findstr "true" >nul
if errorlevel 1 (
    set all_running=false
    echo ⏳ amazon-kafka pas encore pret...
)

docker inspect -f "{{.State.Running}}" amazon-spark-master 2>nul | findstr "true" >nul
if errorlevel 1 (
    set all_running=false
    echo ⏳ amazon-spark-master pas encore pret...
)

docker inspect -f "{{.State.Running}}" amazon-mongodb 2>nul | findstr "true" >nul
if errorlevel 1 (
    set all_running=false
    echo ⏳ amazon-mongodb pas encore pret...
)

docker inspect -f "{{.State.Running}}" amazon-flask 2>nul | findstr "true" >nul
if errorlevel 1 (
    set all_running=false
    echo ⏳ amazon-flask pas encore pret...
)

if "%all_running%"=="false" (
    echo ⏳ Attente 10 secondes...
    timeout /t 10 /nobreak
    goto check_containers
)

echo ✅ Tous les containers sont prets !

echo.
echo [2/4] Lancement du Consumer Spark...
start "Consumer" cmd /k "docker exec amazon-spark-master /opt/spark/bin/spark-submit /opt/spark-apps/consumer.py"

echo.
echo [3/4] Attente que le Consumer charge le modele et se connecte a Kafka (3 minutes)...
timeout /t 180 /nobreak

echo.
echo [4/4] Lancement du Producer...
start "Producer" cmd /k "c:\Users\hp\AppData\Local\Programs\Python\Python310\python.exe producer/producer.py"

echo.
echo ========================================
echo   Projet lance ! Ouvre le navigateur :
echo   Live      : http://localhost:5000
echo   Dashboard : http://localhost:5000/dashboard
echo   MongoDB   : http://localhost:8081
echo   Spark     : http://localhost:8090
echo ========================================
pause