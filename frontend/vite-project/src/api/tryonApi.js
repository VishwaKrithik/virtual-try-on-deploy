import axios from "axios";

const API = axios.create({
  baseURL: "http://127.0.0.1:8000/generate",
});

export const generateTryOn = async ({
  personImage,
  garmentImage,
  steps,
  guidanceScale,
  controlnetScale,
  ipAdapterScale,
  seed,
}) => {
  const formData = new FormData();
  formData.append("person_image", personImage);
  formData.append("garment_image", garmentImage);
  formData.append("steps", steps);
  formData.append("guidance_scale", guidanceScale);
  formData.append("controlnet_scale", controlnetScale);
  formData.append("ip_adapter_scale", ipAdapterScale);
  formData.append("seed", seed);

  const response = await API.post("/", formData, {
    headers: {
      "Content-Type": "multipart/form-data",
    },
  });

  return response.data;
};