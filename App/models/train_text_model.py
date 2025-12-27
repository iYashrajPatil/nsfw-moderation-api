import pandas as pd
import joblib
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report

# ======================
# CONFIG
# ======================
DATASET_PATH = "../train.csv"   # adjust if needed
TEXT_COL = "comment_text"

TOXIC_COLS = [
    "toxic",
    "severe_toxic",
    "obscene",
    "threat",
    "insult",
    "identity_hate"
]

MODEL_PATH = "text_model.pkl"
VECTORIZER_PATH = "tfidf.pkl"

# ======================
# LOAD DATA
# ======================
print("[INFO] Loading dataset...")
df = pd.read_csv(DATASET_PATH)

# Drop rows without text
df = df.dropna(subset=[TEXT_COL])

# Create single NSFW label
df["label"] = df[TOXIC_COLS].max(axis=1)

X = df[TEXT_COL]
y = df["label"]

# ======================
# TRAIN / TEST SPLIT
# ======================
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)

# ======================
# TF-IDF VECTORIZATION
# ======================
print("[INFO] Vectorizing text...")
vectorizer = TfidfVectorizer(
    max_features=30000,
    ngram_range=(1, 2),
    stop_words="english"
)

X_train_vec = vectorizer.fit_transform(X_train)
X_test_vec = vectorizer.transform(X_test)

# ======================
# MODEL TRAINING
# ======================
print("[INFO] Training model...")
model = LogisticRegression(
    max_iter=1000,
    n_jobs=-1
)
model.fit(X_train_vec, y_train)

# ======================
# EVALUATION
# ======================
y_pred = model.predict(X_test_vec)
print("\n[REPORT]")
print(classification_report(y_test, y_pred))

# ======================
# SAVE MODEL
# ======================
joblib.dump(model, MODEL_PATH)
joblib.dump(vectorizer, VECTORIZER_PATH)

print("[SUCCESS] Model & vectorizer saved!")
