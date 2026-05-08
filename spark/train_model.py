# ============================================
# train_model.py — Entraînement MLlib
# ============================================
from pyspark.sql import SparkSession
from pyspark.sql.functions import col
from pyspark.sql.types import FloatType
from pyspark.ml import Pipeline
from pyspark.ml.feature import Tokenizer, StopWordsRemover, HashingTF, IDF
from pyspark.ml.classification import LogisticRegression, NaiveBayes
from pyspark.ml.evaluation import MulticlassClassificationEvaluator

# ── ÉTAPE 1 : Lancer Spark EN PREMIER ──
spark = SparkSession.builder \
    .appName("AmazonSentimentTraining") \
    .master("spark://amazon-spark-master:7077") \
    .getOrCreate()

spark.sparkContext.setLogLevel("ERROR")
print("✅ Spark connecté au master")

# ── ÉTAPE 2 : Charger les données APRÈS Spark ──
train = spark.read.csv("/opt/spark-data/train.csv", header=True, inferSchema=True)
val   = spark.read.csv("/opt/spark-data/val.csv",   header=True, inferSchema=True)

# ── ÉTAPE 3 : Corriger les types ──
train = train.withColumn("label", col("label").cast(FloatType()))
val   = val.withColumn("label",   col("label").cast(FloatType()))

# ── ÉTAPE 4 : Supprimer les nulls et invalides ──
train = train.dropna(subset=["clean_text", "label"])
train = train.filter(col("clean_text") != "")
train = train.filter(col("label").isin([0.0, 1.0, 2.0]))

val = val.dropna(subset=["clean_text", "label"])
val = val.filter(col("clean_text") != "")
val = val.filter(col("label").isin([0.0, 1.0, 2.0]))

print(f"✅ Train : {train.count()} lignes")
print(f"✅ Val   : {val.count()} lignes")

# ── ÉTAPE 5 : Evaluateur ──
evaluator = MulticlassClassificationEvaluator(
    labelCol="label",
    predictionCol="prediction",
    metricName="accuracy"
)

# ── ÉTAPE 6 : Pipeline Logistic Regression ──
pipeline_lr = Pipeline(stages=[
    Tokenizer(inputCol="clean_text", outputCol="words"),
    StopWordsRemover(inputCol="words", outputCol="filtered"),
    HashingTF(inputCol="filtered", outputCol="raw_features", numFeatures=10000),
    IDF(inputCol="raw_features", outputCol="features"),
    LogisticRegression(labelCol="label", maxIter=20, regParam=0.01, family="multinomial")
])

print("⏳ Entraînement Logistic Regression...")
model_lr = pipeline_lr.fit(train)
acc_lr   = evaluator.evaluate(model_lr.transform(val))
print(f"✅ LR Accuracy : {acc_lr:.4f}")

# ── ÉTAPE 7 : Pipeline Naive Bayes ──
pipeline_nb = Pipeline(stages=[
    Tokenizer(inputCol="clean_text", outputCol="words"),
    StopWordsRemover(inputCol="words", outputCol="filtered"),
    HashingTF(inputCol="filtered", outputCol="raw_features", numFeatures=10000),
    IDF(inputCol="raw_features", outputCol="features"),
    NaiveBayes(labelCol="label", smoothing=1.0, modelType="multinomial")
])

print("⏳ Entraînement Naive Bayes...")
model_nb = pipeline_nb.fit(train)
acc_nb   = evaluator.evaluate(model_nb.transform(val))
print(f"✅ NB Accuracy : {acc_nb:.4f}")

# ── ÉTAPE 8 : Choisir le meilleur ──
if acc_lr >= acc_nb:
    best_model = model_lr
    best_name  = "Logistic Regression"
    best_acc   = acc_lr
else:
    best_model = model_nb
    best_name  = "Naive Bayes"
    best_acc   = acc_nb

print(f"🏆 Meilleur modèle : {best_name} ({best_acc:.4f})")

# ── ÉTAPE 9 : Sauvegarder ──
best_model.write().overwrite().save("/opt/spark-models/best_model")
print("✅ Modèle sauvegardé dans /opt/spark-models/best_model")

spark.stop()
print("✅ Terminé !")