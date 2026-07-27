import os
from dotenv import load_dotenv

load_dotenv()


class Settings:
    APP_NAME: str = os.getenv("APP_NAME", "Virtual Try-On API")
    APP_HOST: str = os.getenv("APP_HOST", "127.0.0.1")
    APP_PORT: int = int(os.getenv("APP_PORT", 8000))
    FRONTEND_ORIGIN: str = os.getenv("FRONTEND_ORIGIN", "http://localhost:5173")

    CONTROLNET_MODEL: str = os.getenv("CONTROLNET_MODEL", "lllyasviel/sd-controlnet-depth")
    INPAINT_MODEL: str = os.getenv("INPAINT_MODEL", "runwayml/stable-diffusion-inpainting")
    IP_ADAPTER_REPO: str = os.getenv("IP_ADAPTER_REPO", "h94/IP-Adapter")
    IP_ADAPTER_SUBFOLDER: str = os.getenv("IP_ADAPTER_SUBFOLDER", "models")
    IP_ADAPTER_WEIGHT: str = os.getenv("IP_ADAPTER_WEIGHT", "ip-adapter-plus_sd15.bin")
    DEPTH_MODEL: str = os.getenv("DEPTH_MODEL", "Intel/dpt-large")


settings = Settings()