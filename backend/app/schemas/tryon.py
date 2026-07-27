from pydantic import BaseModel


class TryOnResponse(BaseModel):
    final_output: str
    resized_person: str
    resized_garment: str
    depth_map: str
    mask: str