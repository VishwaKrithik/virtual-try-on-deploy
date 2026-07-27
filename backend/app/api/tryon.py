from fastapi import APIRouter, UploadFile, File, Form, HTTPException
from fastapi.responses import Response
from PIL import Image
from io import BytesIO

from app.utils.image_utils import pil_to_base64, bytes_to_base64
from app.services.inference import VTONInferenceService
from app.schemas.tryon import TryOnResponse


router = APIRouter()
inference_service = VTONInferenceService()


@router.post("/generate")
async def generate_tryon(
    person_image: UploadFile = File(...),
    garment_image: UploadFile = File(...),
    steps: int = Form(50),
    guidance_scale: float = Form(7),
    controlnet_scale: float = Form(0.45),
    ip_adapter_scale: float = Form(1.05),
    seed: int = Form(42)
):
    try:
        person_bytes = await person_image.read()
        garment_bytes = await garment_image.read()

        person_pil = Image.open(BytesIO(person_bytes)).convert("RGB")
        garment_pil = Image.open(BytesIO(garment_bytes)).convert("RGB")

        outputs = inference_service.run_tryon(
            person_raw=person_pil,
            garment_raw=garment_pil,
            steps=steps,
            guidance_scale=guidance_scale,
            controlnet_scale=controlnet_scale,
            ip_adapter_scale=ip_adapter_scale,
            seed=seed
        )

        return TryOnResponse(
            final_output=bytes_to_base64(outputs["final_output"]),
            resized_person=bytes_to_base64(outputs["resized_person"]),
            resized_garment=bytes_to_base64(outputs["resized_garment"]),
            depth_map=bytes_to_base64(outputs["depth_map"]),
            mask=bytes_to_base64(outputs["mask"])
        )

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# router = APIRouter()


# @router.post("/tryon", response_model=TryOnResponse)
# async def tryon_endpoint(
#     person_image: UploadFile = File(...),
#     garment_image: UploadFile = File(...),
#     steps: int = Form(50),
#     guidance_scale: float = Form(7.0),
#     controlnet_scale: float = Form(0.45),
#     ip_adapter_scale: float = Form(1.05),
#     seed: int = Form(42),
# ):
#     try:
#         person_bytes = await person_image.read()
#         garment_bytes = await garment_image.read()

#         person_pil = Image.open(BytesIO(person_bytes)).convert("RGB")
#         garment_pil = Image.open(BytesIO(garment_bytes)).convert("RGB")

#         outputs = run_tryon(
#             model_manager=model_manager,
#             person_raw=person_pil,
#             garment_raw=garment_pil,
#             steps=steps,
#             guidance_scale=guidance_scale,
#             controlnet_scale=controlnet_scale,
#             ip_adapter_scale=ip_adapter_scale,
#             seed=seed,
#         )

#         return TryOnResponse(
#             final_output=pil_to_base64(outputs["final_output"]),
#             resized_person=pil_to_base64(outputs["resized_person"]),
#             resized_garment=pil_to_base64(outputs["resized_garment"]),
#             depth_map=pil_to_base64(outputs["depth_map"]),
#             mask=pil_to_base64(outputs["mask"]),
#         )

#     except Exception as e:
#         raise HTTPException(status_code=500, detail=str(e))
