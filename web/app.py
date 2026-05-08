from flask import Flask, render_template, jsonify
from pymongo import MongoClient
import os

app = Flask(__name__)

# Connexion MongoDB
MONGO_URI = os.environ.get("MONGO_URI", "mongodb://localhost:27017/")
client = MongoClient(MONGO_URI)
db = client["amazon_db"]
collection = db["predictions"]

# ─────────────────────────────
# PAGE 1 — Flux temps réel
# ─────────────────────────────
@app.route('/')
def live():
    return render_template('live.html')

# ─────────────────────────────
# PAGE 2 — Dashboard offline
# ─────────────────────────────
@app.route('/dashboard')
def dashboard():
    return render_template('dashboard.html')

# ─────────────────────────────
# API — 10 dernières prédictions
# ─────────────────────────────
@app.route('/api/latest')
def latest():
    results = list(collection.find(
        {}, {"_id": 0}
    ).sort("timestamp", -1).limit(10))
    return jsonify(results)

# ─────────────────────────────
# API — Prédictions par date
# ─────────────────────────────
@app.route('/api/by_date')
def by_date():
    pipeline = [
        {"$group": {
            "_id": {
                "date": {"$substr": ["$timestamp", 0, 10]},
                "label": "$predicted_label"
            },
            "count": {"$sum": 1}
        }},
        {"$sort": {"_id.date": 1}}
    ]
    results = list(collection.aggregate(pipeline))
    for r in results:
        r['date'] = r['_id']['date']
        r['label'] = r['_id']['label']
        del r['_id']
    return jsonify(results)

# ─────────────────────────────
# API — Scoring par produit
# ─────────────────────────────
@app.route('/api/product/<product_id>')
def product_score(product_id):
    pipeline = [
        {"$match": {"ProductId": product_id}},
        {"$group": {
            "_id": "$predicted_label",
            "count": {"$sum": 1}
        }}
    ]
    results = list(collection.aggregate(pipeline))
    for r in results:
        r['label'] = r['_id']
        del r['_id']
    return jsonify(results)

# ─────────────────────────────
# API — Statistiques globales
# ─────────────────────────────
@app.route('/api/stats')
def stats():
    total = collection.count_documents({})
    positive = collection.count_documents({"predicted_label": "positive"})
    neutral = collection.count_documents({"predicted_label": "neutral"})
    negative = collection.count_documents({"predicted_label": "negative"})
    return jsonify({
        "total": total,
        "positive": positive,
        "neutral": neutral,
        "negative": negative
    })

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)