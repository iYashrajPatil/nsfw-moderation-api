# 🛡️ NSFW Image Moderation API (NudeNet + Rule-Based Scoring)

An **NSFW image moderation system** that classifies images as **SAFE**, **NSFW**, or **REVIEW** using **NudeNet** for detection and a **custom rule-based scoring layer** to reduce false positives.

This project focuses on **practical content moderation**, not just raw machine-learning output.

---

## 📌 Problem Statement

Platforms that accept user-generated images (social media, forums, marketplaces) must automatically detect **explicit or inappropriate visual content** to ensure safety and compliance.

Pure ML-based detection systems often suffer from:
- ❌ High false positives (beach, gym, medical images)
- ❌ Lack of explainability
- ❌ Poor control over moderation strictness

---

## 🧠 Solution Overview

This project solves the problem using a **hybrid approach**:

### 1️⃣ Detection Layer (Machine Learning)
- Uses **NudeNet** to detect exposed or covered body parts
- Returns labels with confidence scores

### 2️⃣ Decision Layer (Rule-Based Logic)
- Applies domain-specific rules
- Aggregates confidence scores
- Produces a final moderation verdict

This ensures **better accuracy, transparency, and control**.

---

## 🏗️ System Architecture

Image Input
↓
NudeNet Detection
↓
Label-wise Confidence Scores
↓
Rule-based Aggregation
↓
Final Verdict (SAFE / NSFW / REVIEW)


---

## 🧪 Classification Logic

### 🔴 NSFW (Explicit Content)
- Exposed genitalia or anus
- High-confidence exposed female breasts
- Cumulative explicit score exceeds threshold

### 🟡 REVIEW (Ambiguous Content)
- Multiple soft signals detected
- Borderline confidence levels
- Requires human verification

### 🟢 SAFE (Allowed Content)
- No detections
- Contextual or non-sexual exposure
- Scores below defined thresholds

---

## 📂 Project Structure

NSFW-moderation/
│
├── App/
│ ├── init.py
│ ├── classifier.py # Core NSFW detection & rule logic
│ ├── main.py # FastAPI entry point
│ └── tmp_uploads/ # Temporary image storage
│
├── .gitignore
├── requirements.txt
├── render.yaml
└── README.md


⚠️ **Note:**  
Model files (`.onnx`) are intentionally **not committed** due to GitHub size limits.  
NudeNet automatically downloads required models at runtime.

---

## ⚙️ Core Detection Strategy

- **Explicit body parts** → high weight
- **Soft body parts** → cumulative weight
- **Threshold-based decision** to reduce false positives

This avoids cases like:
- Beach photos flagged as NSFW
- Fitness or medical images misclassified
- Single soft detection causing rejection

---

## 📦 Example API Output

### NSFW Image
```json
```json
{
  "verdict": "NSFW"
}
```
### Safe Image
```json
{
  "verdict": "SAFE"
}
```
### Reviewed Image
```json
{
  "verdict": "REVIEW"
}
```

## 🚀 Key Features

✅ Lazy model loading (memory efficient)

✅ Rule-based false positive reduction

✅ Clear moderation outcomes

✅ FastAPI-based architecture

✅ Easy to extend with new rules

## ⚠️ Limitations

Scene-level context understanding is limited

Cultural interpretations of nudity may vary

Video moderation not included (image-only)

## 🔧 Future Enhancements

Context-aware detection using CLIP / ViT

Human-in-the-loop moderation

Video frame analysis

Confidence calibration with real datasets

## 🧑‍💻 Tech Stack

Python 3

FastAPI

NudeNet

ONNX Runtime

Rule-based decision engine

## 📌 Use Cases

Social media moderation

Marketplace image screening

Content safety pipelines

Automated pre-moderation systems

## 📜 Disclaimer

This project is intended for educational and research purposes.
Final moderation accuracy depends on model behavior and threshold configuration.

## ⭐ Final Note

This project demonstrates:

Practical ML integration

Engineering judgment

Explainable moderation decisions

Real-world content safety challenges