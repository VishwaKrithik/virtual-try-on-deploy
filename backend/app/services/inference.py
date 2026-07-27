import io
import modal
from PIL import Image
from services.image_preprocess import (
    ImagePreprocessor
)



class VTONInferenceService:
    def __init__(self):
        self.processor = ImagePreprocessor()
        self.GPUClass = modal.Cls.from_name(
            "vton-gpu-pipeline-app", "VTONRunner"
        )

    def run_tryon(
        self,
        person_raw: bytes,
        garment_raw: bytes,
        steps: int = 50,
        guidance_scale: float = 7,
        controlnet_scale: float = 0.45,
        ip_adapter_scale: float = 1.05,
        seed: int = 42
    ) -> bytes:

        prompt = (
            "a realistic photo of the same person wearing the exact upper-body garment from the reference image, "
            "preserve the original pants, preserve the original lower body clothing, "
            "do not change trousers, do not generate matching pants, "
            "preserve the person's pose, body shape, and identity, "
            "accurate garment color, accurate fabric, exact sleeve length from the reference garment, "
            "do not extend sleeves, do not shorten sleeves, "
            "natural clothing fit, realistic folds, realistic fashion photo"
        )

        negative_prompt = (
            "cartoon, illustration, 3d render, plastic texture, flat lighting, overexposed, "
            "artifact, ghosting, blurry, floating fabric, extra limbs, bad anatomy"
        )

        processed = self.processor.preprocess(person_raw, garment_raw)
        orig_w, orig_h = processed["orig_size"]

        # Testing preprocessing steps

        # with open("debug_person.png", "wb") as f:
        #     f.write(processed["person_bytes"])

        # with open("debug_garment.png", "wb") as f:
        #     f.write(processed["garment_bytes"])

        # with open("debug_mask.png", "wb") as f:
        #     f.write(processed["mask_bytes"])

        # print("Original size:", processed["orig_size"])

        # person_img = Image.open(io.BytesIO(processed["person_bytes"])).convert("RGB")
        # mask_img = Image.open(io.BytesIO(processed["mask_bytes"])).convert("L")  # Convert to grayscale

        # # Option A: Red Semi-Transparent Overlay (Best for checking mask boundary)
        # # Creates a red highlight over the target try-on region
        # overlay = Image.new("RGB", person_img.size, (255, 0, 0))  # Red tint
        # highlighted_person = Image.composite(overlay, person_img, mask_img)
        # debug_overlay = Image.blend(person_img, highlighted_person, alpha=0.5)
        # debug_overlay.save("debug_person_masked_overlay.png")

        # # Option B: Direct Cutout / Blackout (Best for seeing exactly what the model sees)
        # # Replaces masked region with black
        # black_bg = Image.new("RGB", person_img.size, (0, 0, 0))
        # cutout_person = Image.composite(black_bg, person_img, mask_img)
        # cutout_person.save("debug_person_cutout.png")

        # print("Saved masked debug images: debug_person_masked_overlay.png & debug_person_cutout.png")


        gpu_runner = self.GPUClass()
        outputs = gpu_runner.run_gpu_inference.remote(
            person_bytes = processed["person_bytes"],
            garment_bytes = processed["garment_bytes"],
            mask_bytes = processed["mask_bytes"],
            orig_w = orig_w,
            orig_h = orig_h,
            prompt = prompt,
            negative_prompt=negative_prompt,
            steps = steps,
            guidance_scale = guidance_scale,
            controlnet_scale = controlnet_scale,
            ip_adapter_scale = ip_adapter_scale,
            seed = seed
        )

        # with open("debug_depth_map.png", "wb") as f:
        #     f.write(result_dict["depth_map"])
        # with open("debug_mask_image.png", "wb") as f:
        #     f.write(result_dict["mask_image"])
        # with open("debug_raw_diffusion.png", "wb") as f:
        #     f.write(result_dict["raw_diffusion"])
            
        # print("Debug images saved to disk!")

        # 3. Return only the final output to the FastAPI router
        return {
            "depth_map": outputs["depth_map"],
            "mask": outputs["mask_image"],
            "final_output": outputs["final_output"],
            "resized_garment": processed["garment_bytes"],
            "resized_person": processed["person_bytes"]
        }

        return result_bytes






# def run_tryon(
#     # model_manager,
#     person_raw: Image.Image,
#     garment_raw: Image.Image,
#     steps: int,
#     guidance_scale: float,
#     controlnet_scale: float,
#     ip_adapter_scale: float,
#     seed: int,
# ):

#     person_img, (orig_w, orig_h) = resize_person_image(person_raw)
#     garment_img = resize_garment_image(clean_garment_raw)
#     clean_garment_raw = remove_garment_background(garment_raw)
#     mask_blurred = build_torso_mask(person_img)
#     # pose_map = build_depth_map(person_img, model_manager.depth_estimator)

#     model_manager.pipe.set_ip_adapter_scale(ip_adapter_scale)

    # prompt = (
    #     "a realistic photo of the same person wearing the exact upper-body garment from the reference image, "
    #     "preserve the original pants, preserve the original lower body clothing, "
    #     "do not change trousers, do not generate matching pants, "
    #     "preserve the person's pose, body shape, and identity, "
    #     "accurate garment color, accurate fabric, exact sleeve length from the reference garment, "
    #     "do not extend sleeves, do not shorten sleeves, "
    #     "natural clothing fit, realistic folds, realistic fashion photo"
    # )

    # negative_prompt = (
    #     "cartoon, illustration, 3d render, plastic texture, flat lighting, overexposed, "
    #     "artifact, ghosting, blurry, floating fabric, extra limbs, bad anatomy"
    # )

#     generator = torch.Generator(device=model_manager.device).manual_seed(seed)

#     # result = model_manager.pipe(
#     #     prompt=prompt,
#     #     negative_prompt=negative_prompt,
#     #     image=person_img,
#     #     mask_image=mask_blurred,
#     #     # control_image=pose_map,
#     #     ip_adapter_image=garment_img,
#     #     num_inference_steps=steps,
#     #     controlnet_conditioning_scale=controlnet_scale,
#     #     guidance_scale=guidance_scale,
#     #     generator=generator,
#     # ).images[0]

#     final_output = Image.composite(result, person_img, mask_blurred)
#     final_output = final_output.resize((orig_w, orig_h), Image.LANCZOS)

#     return {
#         "final_output": final_output,
#         "resized_person": person_img,
#         "resized_garment": garment_img,
#         # "depth_map": pose_map,
#         "mask": mask_blurred,
#     }

    # negative_prompt = (
    #     "change pants, recolor pants, matching pants, suit set, co-ord set, full outfit replacement, "
    #     "replace lower body clothing, long sleeves when short sleeve, short sleeves when long sleeve, "
    #     "sleeve extension, jacket, blazer, hoodie, coat, extra clothing layers, duplicated clothing, "
    #     "garment distortion, warped fabric, floating cloth, detached sleeves, incorrect garment structure, "
    #     "extra arms, extra legs, extra fingers, bad anatomy, distorted limbs, unrealistic proportions, "
    #     "cartoon, anime, illustration, 3d render, cgi, plastic texture, "
    #     "low resolution, blurry, jpeg artifacts, ghosting"
    # )

    # mask_blurred = build_upper_garment_mask(
    #     person_img,
    #     protect_lower_body=False,
    #     include_arms=False,
    # )

  # prompt = (
    #     "a person wearing this EXACT garment, RAW photo, 8k uhd, dslr, "
    #     "soft cinematic lighting, highly detailed, realistic fabric texture and drape"
    # )
