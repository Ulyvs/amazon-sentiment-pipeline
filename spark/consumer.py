# ============================================
# consumer.py — Consumer Python direct
# ============================================
from kafka import KafkaConsumer
from pymongo import MongoClient
from pyspark.sql import SparkSession
from pyspark.ml import PipelineModel
import json
from datetime import datetime

print("⏳ Démarrage du consumer...")

# ── Lancer Spark local ──
spark = SparkSession.builder \
    .appName("AmazonConsumer") \
    .master("local[*]") \
    .getOrCreate()
spark.sparkContext.setLogLevel("ERROR")
print("✅ Spark local démarré")

# ── Charger le modèle ──
model = PipelineModel.load("/opt/spark-models/best_model")
print("✅ Modèle chargé")

# ── Connexion MongoDB ──
client     = MongoClient("mongodb://amazon-mongodb:27017/")
collection = client["amazon_db"]["predictions"]
print("✅ MongoDB connecté")

# ── Connexion Kafka ──
consumer = KafkaConsumer(
    "amazon-reviews",
    bootstrap_servers="amazon-kafka:29092",
    value_deserializer=lambda v: json.loads(v.decode("utf-8")),
    auto_offset_reset="earliest",
    group_id="amazon-consumer-group"
)
print("✅ Kafka connecté")
print("⏳ En attente des messages...")

label_map = {0.0: "negative", 1.0: "neutral", 2.0: "positive"}

# ── Traiter les messages ──
for message in consumer:
    data = message.value

    try:
        # Créer un DataFrame Spark avec 1 ligne
        df = spark.createDataFrame([{
            "clean_text": str(data.get("clean_text", "")),
            "label":      float(data.get("label", 0.0))
        }])

        # Prédire
        prediction = model.transform(df).collect()[0]
        predicted  = label_map.get(float(prediction["prediction"]), "unknown")
        real       = label_map.get(float(data.get("label", 0.0)), "unknown")

        # Stocker dans MongoDB
        doc = {
            "Id":              str(data.get("Id", "")),
            "ProductId":       str(data.get("ProductId", "")),
            "UserId":          str(data.get("UserId", "")),
            "Score":           float(data.get("Score", 0)),
            "Text":            str(data.get("clean_text", "")),
            "real_label":      real,
            "predicted_label": predicted,
            "timestamp":       datetime.now().isoformat()
        }
        collection.insert_one(doc)
        print(f"📥 Prédit: {predicted} | Réel: {real} | {data.get('ProductId', '')}")

    except Exception as e:
        print(f"❌ Erreur: {e}")
        continue