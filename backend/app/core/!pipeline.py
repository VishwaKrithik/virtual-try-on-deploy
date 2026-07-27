import torch
from diffusers import StableDiffusionControlNetInpaintPipeline, ControlNetModel
from transformers import pipeline
from app.core.config import settings


class ModelManager:
    def __init__(self):
        self.device = "cuda" if torch.cuda.is_available() else "cpu"
        self.dtype = torch.float16 if self.device == "cuda" else torch.float32

        print(self.device)

        print(f"[INFO] Using device: {self.device}")
        if self.device == "cpu":
            print("[WARNING] CUDA not detected. Inference will be very slow.")

        print("[INFO] Loading ControlNet...")
        self.controlnet = ControlNetModel.from_pretrained(
            settings.CONTROLNET_MODEL,
            torch_dtype=self.dtype
        ).to(self.device)

        print("[INFO] Loading Inpainting Pipeline...")
        self.pipe = StableDiffusionControlNetInpaintPipeline.from_pretrained(
            settings.INPAINT_MODEL,
            controlnet=self.controlnet,
            torch_dtype=self.dtype,
            variant="fp16" if self.device == "cuda" else None
        ).to(self.device)

        print("[INFO] Loading IP-Adapter...")
        self.pipe.load_ip_adapter(
            settings.IP_ADAPTER_REPO,
            subfolder=settings.IP_ADAPTER_SUBFOLDER,
            weight_name=settings.IP_ADAPTER_WEIGHT
        )

        print("[INFO] Loading Depth Estimator...")
        self.depth_estimator = pipeline(
            "depth-estimation",
            model=settings.DEPTH_MODEL
        )


model_manager = ModelManager()