# Amazon Real-Time Sentiment Analysis Pipeline

## Architecture
Amazon Reviews CSV → Kafka → Spark MLlib → MongoDB → Flask Dashboard

## Technologies
- Apache Kafka + Zookeeper
- Apache Spark MLlib (Logistic Regression - 86% accuracy)
- MongoDB
- Flask
- Docker

## Lancer le projet

### Méthode simple (Windows)
Double-cliquer sur `start.bat`

### Méthode manuelle
1. `docker-compose up -d`
2. Attendre 2 minutes que Spark installe les librairies
3. `docker exec amazon-spark-master /opt/spark/bin/spark-submit /opt/spark-apps/consumer.py`
4. `python producer/producer.py`

### Accès
- Live      : http://localhost:5000
- Dashboard : http://localhost:5000/dashboard
- MongoDB   : http://localhost:8081
- Spark     : http://localhost:8090


## Accès
- Live : http://localhost:5000
- Dashboard : http://localhost:5000/dashboard  
- MongoDB : http://localhost:8081
- Spark : http://localhost:8090

## Dataset
Amazon Fine Food Reviews - Kaggle (568,000 reviews)