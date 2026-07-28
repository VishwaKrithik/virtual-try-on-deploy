# 👕 AI Virtual Try-On

An AI-powered Virtual Try-On application that allows users to upload a photo of themselves and virtually try different clothing items using deep learning image generation.

## 🌐 Live Demo

🔗 https://virtual-try-on-deploy.vercel.app/

---

## ✨ Features

- 📸 Upload a person image
- 👔 Upload a garment image
- 🤖 AI-powered virtual clothing generation
- ⚡ Fast and responsive React interface
- 🎯 Face-aware image preprocessing
- 🖼️ High-quality generated outputs
- 🔄 Real-time communication with the backend API

---

## 🏗️ Project Architecture

```
Frontend (React + Vite)
        │
        ▼
 FastAPI Backend
        │
        ▼
Image Preprocessing
(OpenCV + Haar Cascade)
        │
        ▼
Virtual Try-On Model
        │
        ▼
Generated Image
```

---

## 🛠️ Tech Stack

### Frontend

- React 19
- Vite
- Axios
- CSS

### Backend

- FastAPI
- Python
- OpenCV
- Pillow
- Modal
- Uvicorn
- Pydantic

---

## 📂 Project Structure

```
virtual-try-on/

├── frontend/
│   └── vite-project/
│       ├── src/
│       ├── public/
│       └── package.json
│
├── backend/
│   ├── app/
│   │   ├── api/
│   │   ├── core/
│   │   ├── schemas/
│   │   ├── services/
│   │   └── utils/
│   ├── requirements.txt
│   └── modal_vton.py
│
└── README.md
```

---

## 🚀 Running Locally

### Clone the repository

```bash
git clone https://github.com/your-username/your-repository.git

cd your-repository
```

---

### Frontend

```bash
cd frontend/vite-project

npm install

npm run dev
```

Runs on

```
http://localhost:5173
```

---

### Backend

```bash
cd backend

pip install -r requirements.txt
```

Run the server

```bash
uvicorn app.main:app --reload
```

Runs on

```
http://localhost:8000
```

---

## 📸 How It Works

1. Upload a photo of yourself.
2. Upload the clothing image.
3. The backend preprocesses the person image.
4. The AI Virtual Try-On model generates the final result.
5. The generated image is returned to the frontend for viewing.

---

## 🔬 Image Processing Pipeline

- Image upload
- Face detection using Haar Cascade
- Image preprocessing
- Virtual Try-On inference
- Post-processing
- Result generation

---

## 📁 API

### Health Check

```
GET /
```

Response

```json
{
  "status": "Backend VTON is running"
}
```

---

## Future Improvements

- Multiple clothing categories
- Better pose estimation
- Clothing segmentation
- Background preservation
- Batch image processing
- User authentication
- History of generated results

---

## Screenshots

> Add screenshots or GIFs of the application here.

Example:

```
Home Page

Upload Interface

Generated Output
```

---

## Author

**Vishwa Krithik S**
**Sandeep Vijay**
**Shreya Venghatesh**
**Vishnu Charan M**

AI & Data Science Undergraduate

Interested in Artificial Intelligence, Computer Vision, and Generative AI.

---

## License

This project is intended for educational and research purposes.
