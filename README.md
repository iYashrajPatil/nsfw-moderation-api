# 🛡️ Multi-Modal NSFW Content Moderation API  
*(Image · Text · Video | Lightweight · Open-Source · CPU-Only)*

A **production-ready, multi-modal content moderation system** designed for **social media platforms**.  
It classifies **images, text, and videos** into **SAFE**, **REVIEW**, or **NSFW** using **lightweight open-source models**, rule-based logic, and confidence scoring.

This project focuses on **practical, deployable content moderation**, not just raw machine-learning output.

---

## 📌 Problem Statement

Platforms handling user-generated content (social media, forums, marketplaces, short-video apps) must automatically detect **explicit, abusive, or inappropriate content** to ensure safety, compliance, and user trust.

Pure ML-only moderation systems often suffer from:

- ❌ High false positives (beach, gym, medical, sports content)
- ❌ Poor explainability
- ❌ Expensive GPU requirements
- ❌ Difficult deployment & scaling
- ❌ No clear escalation strategy for ambiguous content

---

## 💡 Solution Overview

This system implements a **multi-layered moderation pipeline** that combines:

- ✅ **Image Moderation** → NudeNet + rule-based scoring  
- ✅ **Text Moderation** → TF-IDF + Logistic Regression + keyword rules  
- ✅ **Video Moderation** → Frame sampling + image moderation reuse  
- ✅ **Central Orchestration** → Unified verdicts & confidence scoring  
- ✅ **Production Logging** → Auditable moderation decisions  

Each input is classified into:

SAFE | REVIEW | NSFW


with a **confidence score (0.0 – 1.0)**.

---

## 🧠 System Architecture

                ┌──────────────────────┐
                │   FastAPI Server     │
                └─────────┬────────────┘
                          │
                ┌─────────▼────────────┐
                │  Moderation Engine   │
                └───────┬───────┬──────┘
                        │       │
        ┌───────────────▼───┐   ▼
        │ Image Moderator    │  Text Moderator
        │ (NudeNet + Rules)  │  (TF-IDF + Rules)
        └───────────────┬───┘
                        ▼
                Video Moderator
           (Frame Sampling + Image Moderator)


- **Single verdict format**
- **Modular & extensible**
- **CPU-only inference**
- **No paid APIs**
- **Offline / self-hosted**

---

## 🧪 Moderation Logic

### 🖼️ Image Moderation
- Uses **NudeNet (ONNX, CPU-only)**
- Detects explicit & suggestive body parts
- Applies **rule-based aggregation** to reduce false positives
- Verdicts based on configurable thresholds

### ✍️ Text Moderation
- Hybrid approach:
  - TF-IDF + Logistic Regression (trained on public datasets)
  - Keyword-based rule scoring
- Designed for:
  - Sexual content
  - Abusive language
  - Toxic comments
- Conservative aggregation → **REVIEW instead of over-blocking**

### 🎞️ Video Moderation
- No heavy video neural networks
- Uses **frame sampling (1 frame every 2 seconds)**
- Reuses **existing image moderator**
- Aggregates frame-level decisions
- Early-exit optimization for obvious NSFW content

---

## 📤 Output Format (Consistent Across Modalities)

```json
{
  "type": "image | text | video",
  "verdict": "SAFE | REVIEW | NSFW",
  "confidence": 0.0
}
```
## 🚀 Getting Started
1️⃣ Install Dependencies

pip install -r requirements.txt

2️⃣ Run the API

python -m uvicorn App.main:app --reload

3️⃣ Test via Swagger UI

http://127.0.0.1:8000/docs

NSFW_MODERATION/
│
├── App/
│   ├── classifier.py              # Image moderation (NudeNet)
│   ├── text_moderator/             # Text moderation module
│   ├── video_moderator/            # Video moderation module
│   ├── moderation_engine.py        # Central orchestrator
│   ├── logger.py                   # Central logging config
│   ├── main.py                     # FastAPI app
│   ├── models/                     # Trained ML models
│   ├── tmp_uploads/                # Temporary files (gitignored)
│   └── logs/
│       └── moderation.log          # Moderation logs
│
├── requirements.txt
├── README.md
└── .gitignore

## 📊 Logging & Observability

All moderation decisions are logged with:

- Input type
- Verdict
- Confidence
- Error details (if any)

This enables:

- Auditing moderation behavior
- Debugging false positives
- Compliance reporting
- Production monitoring

## ⚠️ Limitations (Honest Disclosure)

- Very short explicit flashes in videos may be missed
- Sarcasm & deep context in text may require human review
- Designed for social media moderation, not adult platforms
###### These are intentional trade-offs for speed, cost, and deployability.

## 🧑‍💻 Ideal Use Cases

- Social media platforms
- Content upload moderation
- Reels / Shorts / Stories filtering
- Marketplace image safety checks
- Academic & internship projects
- Open-source moderation research

## 📜 License

- This project uses only free & open-source components and is intended for ethical, public-platform content moderation.