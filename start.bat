@echo off
echo ========================================
echo   Amazon Sentiment Analysis Pipeline
echo ========================================

echo.
echo [1/5] Lancement de tous les services Docker...
docker-compose up -d

echo.
echo [2/5] Attente que Kafka et Spark demarrent (5 minutes)...
timeout /t 300 /nobreak

echo.
echo [3/5] Lancement du Consumer Spark...
start "Consumer" cmd /k "docker exec amazon-spark-master /opt/spark/bin/spark-submit /opt/spark-apps/consumer.py"

echo.
echo [4/5] Attente que le Consumer charge le modele (3 minutes)...
timeout /t 180 /nobreak

echo.
echo [5/5] Lancement du Producer...
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