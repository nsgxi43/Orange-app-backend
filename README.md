# Orange App Backend

AI-powered backend that detects oranges in an uploaded image, draws bounding boxes, calculates average size, and estimates spoilage percentage using Gemini Vision.

Built with FastAPI + Roboflow + Google Gemini.

---

## Features

- Image upload API (FastAPI)
- Orange detection using Roboflow (Fruit2 model)
- Bounding-box extraction
- Average orange size calculation (pixels)
- Gemini Vision health classification:
  - healthy_orange
  - rotten_orange
  - fungus_orange
- Automatic spoilage percentage
- Annotated output image
- JSON API response

---

## High-Level Architecture

Image Upload  
↓  
Roboflow Detection (oranges + boxes)  

↓  
Gemini Vision classification  
↓  
Metrics calculation (avg size + spoilage %)  
↓  
JSON Report

---

## 📁 Project Structure

```
Orange_app/
│
├── app/
│ ├── main.py 
│ ├── analysis.py
│ ├── crop.py 
│ ├── gemini.py
│ └── init.py
│
├── annotated.jpg -> box output
├── .env -> add the api keys here
├── requirements.txt
└── README.md
```

---

## Setup

### 1. Clone repository

```bash
git clone https://github.com/nsgxi43/Orange-app-backend.git
cd Orange-app-backend
```

### 2. Create virtual environment
```bash
python3 -m venv venv
source venv/bin/activate
```

### 3. Install dependencies
```bash
pip install -r requirements.txt
```

### 4. Create .env
```bash
nano .env
```

Add:
```
ROBOFLOW_API_KEY=your_roboflow_key
GEMINI_API_KEY=your_gemini_key
```

### 5. Run server
```bash
uvicorn app.main:app --reload
```

Open:
http://127.0.0.1:8000/docs

Use `/analyze` endpoint to upload image.

## API Response Example
```json
{
  "total_oranges_detected": 92,
  "oranges_seen_by_gemini": 78,
  "average_size_px": 31.08,
  "spoilage_percentage": 0.0,
  "health_report": [
    { "box": 0, "status": "healthy_orange" }
  ]
}
```

## Tech Stack

- FastAPI
- Roboflow
- Google Gemini Vision
- Python 3.10+

## Notes

- Gemini only evaluates crops it receives.
- Spoilage percentage: `(non_healthy / oranges_seen_by_gemini) × 100`
