# AgriAssist Backend — AI Smart Farming Assistant

This is the **Backend** module of the AgriAssist college mini project.

## 1. Project Overview

AgriAssist is an AI-powered smart farming assistant. It lets a user upload a
photo of a crop leaf, predicts the crop and disease using a machine learning
model, and returns treatment, fertilizer, weather, and chatbot assistance.

The project is split across four team members:

| Member  | Responsibility |
|---------|-----------------|
| Mona    | Machine Learning (model training + `predict.py`) |
| Shivani | Database |
| Ojaswi  | Frontend |
| **You** | **Backend (this folder)** |

## 2. Backend Responsibilities

This backend is a **FastAPI** application that:

- Accepts image uploads
- Calls Mona's ML prediction function (does not train or modify it)
- Returns treatment and fertilizer recommendations (no database — in-memory logic)
- Provides an AI chatbot via the Groq API
- Provides live weather data via OpenWeatherMap
- Exposes a health check endpoint

It does **not** contain any database code, frontend code, or ML training code.

## 3. Folder Structure

```text
backend/
│
├── __init__.py
├── main.py                 # FastAPI app entry point
├── requirements.txt
├── .env.example
├── .gitignore
├── README.md
│
├── routers/                 # API route definitions
│   ├── upload.py
│   ├── predict.py
│   ├── treatment.py
│   ├── fertilizer.py
│   ├── chatbot.py
│   └── weather.py
│
├── services/                 # Business logic
│   ├── ml_service.py
│   ├── treatment_service.py
│   ├── fertilizer_service.py
│   ├── chatbot_service.py
│   └── weather_service.py
│
├── schemas/                  # Pydantic request/response models
│   ├── prediction.py
│   ├── chatbot.py
│   └── recommendation.py
│
├── utils/
│   └── file_utils.py         # Upload validation & saving helpers
│
├── ml/                        # Mona's ML files go here (see ml/README.md)
│   └── README.md
│
└── static/
    └── uploads/                # Uploaded images are stored here
```

## 4. Installation

You need **Python 3.10+** installed.

Clone/download the project, then move into the folder that **contains** the
`backend/` folder (the project root — this is important for the run command
to work).

## 5. Virtual Environment Setup

From the project root (the folder containing `backend/`):

```bash
python -m venv venv
```

Activate it:

- **Windows (PowerShell):**
  ```bash
  venv\Scripts\activate
  ```
- **macOS / Linux:**
  ```bash
  source venv/bin/activate
  ```

## 6. Installing Requirements

```bash
pip install -r backend/requirements.txt
```

## 7. `.env` Setup

Copy the example file and fill in your own keys:

```bash
cp backend/.env.example backend/.env
```

Then edit `backend/.env`:

```env
GROQ_API_KEY=your_groq_api_key_here
GROQ_MODEL=llama-3.1-8b-instant
OPENWEATHER_API_KEY=your_openweathermap_api_key_here
ALLOWED_ORIGINS=http://localhost:5173
```

> `.env` is already listed in `.gitignore` — never commit real API keys.

## 8. How to Run the Backend

From the **project root** (the folder that contains `backend/`):

```bash
python -m uvicorn backend.main:app --reload --port 8000
```

The server will start at: `http://localhost:8000`

## 9. Swagger / API Docs

- Swagger UI: `http://localhost:8000/docs`
- ReDoc: `http://localhost:8000/redoc`

## 10. API Endpoints

| Method | Endpoint         | Description                                |
|--------|------------------|---------------------------------------------|
| POST   | `/api/upload`    | Upload a leaf image                          |
| POST   | `/api/predict`   | Predict crop + disease from an image         |
| POST   | `/api/treatment` | Get treatment/prevention advice              |
| POST   | `/api/fertilizer`| Get fertilizer/nutrient advice               |
| POST   | `/api/chat`      | Chat with the AI assistant (Groq)             |
| GET    | `/api/weather`   | Get current weather for a city                |
| GET    | `/health`        | Health check                                   |

Example: `POST /api/treatment`
```json
{
  "crop": "Corn",
  "disease": "Common Rust"
}
```

Example: `GET /api/weather?city=Indore`

## 11. Mona's ML Integration

The backend never trains or redefines the ML model. It dynamically imports
Mona's `predict_image()` function from `backend/ml/predict.py` and calls it
with the path of the uploaded image.

Expected function contract:

```python
def predict_image(image_path: str) -> dict:
    return {
        "crop": "Corn",
        "disease": "Common Rust",
        "confidence": 98.45
    }
```

If the ML files are missing, `POST /api/predict` returns a clean
`503 Service Unavailable` JSON error instead of crashing the whole app.

## 12. How to Place ML Files

Once Mona provides her files, copy them into `backend/ml/`:

```text
backend/ml/
├── fine_tuned_best.keras
├── class_mapping.json
└── predict.py
```

No backend code changes are required — `/api/predict` will start working
automatically.

## 13. Frontend Integration

The frontend (built by Ojaswi) should:

1. Run on `http://localhost:5173` (already whitelisted in CORS via `.env`)
2. Call `POST /api/upload` or `POST /api/predict` with `multipart/form-data`,
   using a form field named `file`
3. Call the other endpoints with standard `application/json` bodies
4. Read uploaded images back from `http://localhost:8000/static/uploads/<filename>`

## 14. Common Errors and Solutions

| Problem | Likely Cause | Solution |
|---|---|---|
| `ModuleNotFoundError: No module named 'backend'` | Running uvicorn from the wrong folder | Run the command from the project root, **not** from inside `backend/` |
| `503 Service Unavailable` on `/api/predict` | Mona's ML files aren't in `backend/ml/` yet | Add `fine_tuned_best.keras`, `class_mapping.json`, and `predict.py` to `backend/ml/` |
| `500` error on `/api/chat` | Missing/invalid `GROQ_API_KEY` or `GROQ_MODEL` | Check your `backend/.env` file |
| `404` on `/api/weather` | Invalid city name | Double check spelling, e.g. `?city=Indore` |
| CORS errors in the browser console | Frontend origin not in `ALLOWED_ORIGINS` | Update `ALLOWED_ORIGINS` in `backend/.env` to match your frontend's URL |
| `400 Bad Request` on upload | Wrong file type | Only `.jpg`, `.jpeg`, `.png` are accepted |
