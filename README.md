
# 🎭 AI Meme Generator (FastAPI)

An **AI-powered Meme Generator** built with **FastAPI**, **SQLAlchemy**, and **Pillow**.
It automatically selects the best meme template using semantic similarity and generates captions — or lets users provide their own text.

---

## 🚀 Features

* ✅ FastAPI backend with Swagger UI
* 🧠 AI-based meme template selection (Sentence Transformers)
* ✍️ Auto caption generation or custom text input
* 🖼️ Meme rendering using Pillow
* 🗄️ SQLite database (no setup needed)
* 📂 Local image template ingestion
* 🧪 Easy testing via `/docs`

---

## 📁 Project Structure

```
meme-generator/
│
├── app/
│   ├── main.py              # FastAPI app entry point
│   ├── database.py          # Database configuration
│   ├── models.py            # SQLAlchemy models
│   ├── schemas.py           # Pydantic schemas
│   ├── crud.py               # Database operations
│   ├── renderer.py           # Meme image renderer
│   ├── ai_engine.py          # AI caption + template selection
│   └── ingest_templates.py   # Template ingestion script
│
├── templates_dataset/        # Meme image templates
├── generated_output/         # Generated memes
├── meme.db                   # SQLite database
├── requirements.txt
└── README.md
```

---

## 🛠️ Installation

### 1️⃣ Clone the repository

```bash
git clone https://github.com/yourusername/meme-generator.git
cd meme-generator
```

### 2️⃣ Create & activate virtual environment

```bash
python -m venv venv
```

**Windows**

```bash
venv\Scripts\activate
```

**Mac / Linux**

```bash
source venv/bin/activate
```

### 3️⃣ Install dependencies

```bash
pip install -r requirements.txt
```

---

## 📥 Ingest Meme Templates

Place meme images (`.jpg`, `.png`) inside `templates_dataset/`, then run:

```bash
python -m app.ingest_templates
```

This:

* Stores template metadata in `meme.db`
* Creates vector embeddings for AI selection

---

## ▶️ Run the Server

```bash
uvicorn app.main:app --reload
```

Server runs at:

```
http://127.0.0.1:8000
```

---

## 📚 API Documentation

Open Swagger UI:

```
http://127.0.0.1:8000/docs
```

---

## 🧪 Generate a Meme (POST)

### Endpoint

```
POST /generate-meme
```

### Example Request Body

```json
{
  "prompt": "superhero meme",
  "top_text": "When code works",
  "bottom_text": "Without errors"
}
```

✅ If `top_text` & `bottom_text` are omitted, AI will generate captions automatically.

---

## 🖼️ Output

* Generated meme images are saved in:

```
generated_output/
```

* API response includes the image path and metadata.

---

## ❌ Common Notes

* ❗ **`GET /` returns 404 by design** — use `/docs`
* ❌ Docker is **NOT required**
* ⚠️ Ensure `assets/impact.ttf` exists for text rendering

---

## 🧠 Tech Stack

* **FastAPI**
* **SQLAlchemy**
* **Pydantic v2**
* **Sentence-Transformers**
* **Pillow**
* **SQLite**

---

## 📌 Future Improvements

* Web frontend (React / Next.js)
* Meme preview endpoint
* Cloud storage
* Multiple layouts
* User accounts

---

## 📄 License

MIT License


