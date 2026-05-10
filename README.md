# Amazon Real-Time Sentiment Analysis Pipeline

## Architecture
Amazon Reviews CSV → Kafka → Spark MLlib → MongoDB → Flask Dashboard

## Technologies
- Apache Kafka + Zookeeper
- Apache Spark MLlib (Logistic Regression - 86% accuracy)
- MongoDB + Mongo Express
- Flask
- Docker
- Python 3.10

## Prérequis
- Docker Desktop installé
- Python 3.10 installé

## Lancer le projet

### Méthode 1 — Automatique (recommandée)

**Étape 1 — Lancer les containers Docker**

Option A : Depuis Docker Desktop
Ouvrir Docker Desktop → trouver "bdproject" → cliquer Play
Attendre que tous les containers soient verts

Option B : Depuis le terminal
docker-compose up -d

**Étape 2 — Double-cliquer sur start.bat**
Le script vérifie automatiquement que les containers sont prets
Lance le Consumer Spark
Attend 3 minutes que le modele soit charge
Lance le Producer

### Méthode 2 — Manuelle

**Étape 1 — Lancer les containers**
docker-compose up -d

**Étape 2 — Lancer le Consumer (Terminal 1)**
docker exec amazon-spark-master /opt/spark/bin/spark-submit /opt/spark-apps/consumer.py

**Étape 3 — Attendre 3 minutes que le Consumer soit pret**

**Étape 4 — Lancer le Producer (Terminal 2)**
python producer/producer.py

## Accès
- Live      : http://localhost:5000
- Dashboard : http://localhost:5000/dashboard
- MongoDB   : http://localhost:8081
- Spark     : http://localhost:8090

## Dataset
Amazon Fine Food Reviews - Kaggle (568 000 reviews)
https://www.kaggle.com/datasets/snap/amazon-fine-food-reviews