import io
import modal
import torch
from PIL import Image
# from rembg import remove, new_session

def download_all_gpu_models():
    from diffusers import StableDiffusionControlNetInpaintPipeline, ControlNetModel
    from transformers import pipeline
    # from rembg import new_session

    # 1. Pre-download U2Net background removal model (~170MB)
    # new_session("u2net")

    # 2. ControlNet & Diffusion models
    controlnet = ControlNetModel.from_pretrained(
        "lllyasviel/sd-controlnet-depth",
        torch_dtype=torch.float16
    )

    pipe = StableDiffusionControlNetInpaintPipeline.from_pretrained(
        "runwayml/stable-diffusion-inpainting",
        controlnet=controlnet,
        torch_dtype=torch.float16,
        variant="fp16"
    )

    pipe.load_ip_adapter(
        "h94/IP-Adapter",
        subfolder="models",
        weight_name="ip-adapter-plus_sd15.bin"
    )

    pipeline(task="depth-estimation", model="Intel/dpt-large")


gpu_image = (
    modal.Image.debian_slim(python_version="3.11")
    .pip_install(
        "torch",
        "diffusers",
        "accelerate",
        "pillow",
        "einops",
        "transformers",
        # "rembg",
        # "onnxruntime-gpu"  # Runs rembg on GPU
    ).run_function(download_all_gpu_models)
)


app = modal.App("vton-gpu-pipeline-app", image=gpu_image)

# debug_volume = modal.Volume.from_name("vton-debug-volume", create_if_missing=True)

# @app.cls(gpu="A100", timeout=300, volumes={"/debug": debug_volume})
@app.cls(gpu="A10G", timeout=300)
class VTONRunner:
    @modal.enter()
    def setup_gpu_models(self):
        from diffusers import StableDiffusionControlNetInpaintPipeline, ControlNetModel
        from transformers import pipeline
        # from rembg import new_session

        # Reuse session across calls for faster inference
        # self.rembg_session = new_session("u2net")

        self.depth_estimator = pipeline(
            task="depth-estimation", 
            model="Intel/dpt-large", 
            device=0
        )

        controlnet = ControlNetModel.from_pretrained(
            "lllyasviel/sd-controlnet-depth",
            torch_dtype=torch.float16
        )

        self.pipe = StableDiffusionControlNetInpaintPipeline.from_pretrained(
            "runwayml/stable-diffusion-inpainting",
            controlnet=controlnet,
            torch_dtype=torch.float16,
            variant="fp16"
        ).to("cuda")

        self.pipe.load_ip_adapter(
            "h94/IP-Adapter",
            subfolder="models",
            weight_name="ip-adapter-plus_sd15.bin"
        )

    # Your background removal helper inside Modal GPU
    # def remove_garment_background(self, garment_raw: Image.Image) -> Image.Image:
    #     # bg_removed = remove(garment_raw, session=self.rembg_session)
    #     white_bg = Image.new("RGB", garment_raw.size, (255, 255, 255))
    #     white_bg.paste(garment_raw, mask=garment_raw.split()[3])
    #     return white_bg

    def build_depth_map(self, person_img: Image.Image) -> Image.Image:
        depth_image = self.depth_estimator(person_img)["depth"]
        return depth_image.convert("RGB")

    @modal.method()
    def run_gpu_inference(
        self, 
        person_bytes: bytes, 
        garment_bytes: bytes, 
        mask_bytes: bytes, 
        orig_w: int,
        orig_h: int,
        prompt: str = "A person wearing garment",
        negative_prompt: str = "",
        steps: int = 50,
        guidance_scale: float = 7,
        controlnet_scale: float = 0.45,
        ip_adapter_scale: float = 1.05,
        seed: int = 42,
    ) -> bytes:
        person_img = Image.open(io.BytesIO(person_bytes)).convert("RGB")
        garment_img = Image.open(io.BytesIO(garment_bytes)).convert("RGB")
        mask_img = Image.open(io.BytesIO(mask_bytes)).convert("L")

        # 1. Clean garment background on GPU instantly
        # garment_clean = self.remove_garment_background(garment_raw)

        # person_img.save("/debug/received_person.png")
        # garment_img.save("/debug/received_garment.png")
        # mask_img.save("/debug/received_mask.png")
        
        # # Commit changes so files are written to cloud storage immediately
        # debug_volume.commit()
        # print("Debug images successfully saved to Modal Volume at /debug!")

        # 2. Generate Depth Map
        depth_map = self.build_depth_map(person_img)

        # 3. Dynamic IP-Adapter scale & Seed
        self.pipe.set_ip_adapter_scale(ip_adapter_scale)
        generator = torch.Generator(device="cuda").manual_seed(seed)

        # 4. Diffusion Pipeline Execution
        result = self.pipe(
            prompt=prompt,
            negative_prompt=negative_prompt,
            image=person_img,
            mask_image=mask_img,
            control_image=depth_map,
            ip_adapter_image=garment_img,
            num_inference_steps=steps,
            guidance_scale=guidance_scale,
            controlnet_conditioning_scale=controlnet_scale,
            generator=generator
            # strength=0.8
        ).images[0]

        final_output = Image.composite(result, person_img, mask_img)
        final_output = final_output.resize((orig_w, orig_h), Image.LANCZOS)

        def img_to_bytes(img: Image.Image) -> bytes:
            buf = io.BytesIO()
            img.save(buf, format="PNG")
            return buf.getvalue()

        return {
            "final_output": img_to_bytes(final_output),
            "raw_diffusion": img_to_bytes(result),
            "depth_map": img_to_bytes(depth_map),
            "mask_image": img_to_bytes(mask_img)
        }

        buffer = io.BytesIO()
        final_output.save(buffer, format="PNG")
        return buffer.getvalue()