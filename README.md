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
```bash
docker-compose up -d
docker exec amazon-spark-master /opt/spark/bin/spark-submit /opt/spark-apps/consumer.py
python producer/producer.py
```

## Accès
- Live : http://localhost:5000
- Dashboard : http://localhost:5000/dashboard  
- MongoDB : http://localhost:8081
- Spark : http://localhost:8090

## Dataset
Amazon Fine Food Reviews - Kaggle (568,000 reviews)