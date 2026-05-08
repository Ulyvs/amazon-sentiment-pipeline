# ============================================
# producer.py — Envoie test.csv dans Kafka
# ============================================
from kafka import KafkaProducer
import pandas as pd
import json
import time

print("⏳ Connexion à Kafka...")
producer = KafkaProducer(
    bootstrap_servers='localhost:9092',
    value_serializer=lambda v: json.dumps(v).encode('utf-8')
)
print("✅ Connecté à Kafka !")

# Charger les données de test
df = pd.read_csv("data/test.csv")
print(f"✅ {len(df)} avis à envoyer")
print("⏳ Envoi en cours... (1 avis/seconde)")

for i, row in df.iterrows():
    message = {
        "Id":         str(row["Id"]),
        "ProductId":  str(row["ProductId"]),
        "UserId":     str(row["UserId"]),
        "Score":      float(row["Score"]),
        "label":      float(row["label"]),
        "clean_text": str(row["clean_text"])
    }
    producer.send("amazon-reviews", value=message)
    print(f"📤 Envoyé [{i+1}/{len(df)}] → {row['ProductId']}")
    time.sleep(1)

producer.flush()
print("✅ Tous les avis ont été envoyés !")