# Virtual Try-On Application

A full-stack application for AI-powered virtual garment fitting. Users can upload target person images and clothing items to generate realistic virtual try-on previews.

🌐 **Live Demo:** [https://virtual-try-on-deploy.vercel.app/](https://virtual-try-on-deploy.vercel.app/)

---

## 🏗 Repository Structure

```text
virtual-try-on-deploy/
├── backend/
│   ├── app/
│   │   ├── api/             # FastAPI API endpoints (tryon.py)
│   │   ├── core/            # Pipeline configuration & orchestration
│   │   ├── schemas/         # Pydantic models & validation
│   │   ├── services/        # Preprocessing, face detection, inference logic
│   │   └── utils/           # Image utility helpers
│   ├── modal_vton.py        # Modal serverless GPU backend deployment
│   ├── main.py              # Application entry point
│   └── requirements.txt     # Python dependencies
│
└── frontend/
    └── vite-project/        # React + Vite application
        ├── src/
        │   ├── api/         # Axios/Fetch integration (tryonApi.js)
        │   ├── components/  # React components (ImageUploader, Gallery, Settings)
        │   └── pages/       # Application views (TryOnPage)
        ├── package.json     # Node dependencies & scripts
        └── vite.config.js   # Vite configuration
