from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from api.tryon import router as tryon_router


app = FastAPI(
    title="Virtual Try-On Backend API",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)

@app.get("/")
def root():
    return {
        "status": "Backend VTON is running"
    }

app.include_router(tryon_router, tags=["Virtual Try-On"])







# from fastapi import FastAPI
# import uvicorn
# from fastapi.middleware.cors import CORSMiddleware

# from app.api.tryon import router as tryon_router
# from app.core.config import settings


# app = FastAPI(title=settings.APP_NAME)

# app.add_middleware(
#     CORSMiddleware,
#     allow_origins=[settings.FRONTEND_ORIGIN],
#     allow_credentials=True,
#     allow_methods=["*"],
#     allow_headers=["*"],
# )

# app.include_router(tryon_router, prefix="/api/v1", tags=["Try-On"])


# @app.get("/")
# def root():
#     return {"message": "Virtual Try-On API is running"}

# if __name__ == "__main__":
#     uvicorn.run(
#         "main:app",
#         host="0.0.0.0",
#         port=8000,
#         reload=True
#     )