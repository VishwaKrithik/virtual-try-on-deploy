import React, { useState } from "react";
import ImageUploader from "../components/ImageUploader";
import SettingsPanel from "../components/SettingsPanel";
import OutputGallery from "../components/OutputGallery";
import { generateTryOn } from "../api/tryonApi";

export default function TryOnPage() {
  const [personFile, setPersonFile] = useState(null);
  const [garmentFile, setGarmentFile] = useState(null);

  const [personPreview, setPersonPreview] = useState(null);
  const [garmentPreview, setGarmentPreview] = useState(null);

  const [steps, setSteps] = useState(50);
  const [guidanceScale, setGuidanceScale] = useState(7.0);
  const [controlnetScale, setControlnetScale] = useState(0.45);
  const [ipAdapterScale, setIpAdapterScale] = useState(1.05);
  const [seed, setSeed] = useState(42);

  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");
  const [outputs, setOutputs] = useState({
    final_output: null,
    resized_person: null,
    resized_garment: null,
    depth_map: null,
    mask: null,
  });

  const handlePersonChange = (file) => {
    setPersonFile(file);
    setPersonPreview(file ? URL.createObjectURL(file) : null);
  };

  const handleGarmentChange = (file) => {
    setGarmentFile(file);
    setGarmentPreview(file ? URL.createObjectURL(file) : null);
  };

  const handleGenerate = async () => {
    if (!personFile || !garmentFile) {
      setError("Please upload both images.");
      return;
    }

    setLoading(true);
    setError("");

    try {
      const data = await generateTryOn({
        personImage: personFile,
        garmentImage: garmentFile,
        steps,
        guidanceScale,
        controlnetScale,
        ipAdapterScale,
        seed,
      });

      setOutputs(data);
    } catch (err) {
      setError(err?.response?.data?.detail || "Generation failed.");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="page">
      <div className="header">
        <h1>Virtual Try-On Studio</h1>
        <p>Upload a person image and a garment image to generate a try-on result.</p>
      </div>

      {error && <div className="error-box">{error}</div>}

      <div className="top-grid">
        <ImageUploader
          label="Person Image"
          file={personFile}
          preview={personPreview}
          onChange={handlePersonChange}
        />

        <ImageUploader
          label="Garment Image"
          file={garmentFile}
          preview={garmentPreview}
          onChange={handleGarmentChange}
        />

        <SettingsPanel
          steps={steps}
          setSteps={setSteps}
          guidanceScale={guidanceScale}
          setGuidanceScale={setGuidanceScale}
          controlnetScale={controlnetScale}
          setControlnetScale={setControlnetScale}
          ipAdapterScale={ipAdapterScale}
          setIpAdapterScale={setIpAdapterScale}
          seed={seed}
          setSeed={setSeed}
          onGenerate={handleGenerate}
          loading={loading}
          disabled={!personFile || !garmentFile}
        />
      </div>

      <OutputGallery outputs={outputs} />
    </div>
  );
}