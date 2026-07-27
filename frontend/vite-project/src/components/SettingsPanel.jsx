import React from "react";

export default function SettingsPanel({
  steps,
  setSteps,
  guidanceScale,
  setGuidanceScale,
  controlnetScale,
  setControlnetScale,
  ipAdapterScale,
  setIpAdapterScale,
  seed,
  setSeed,
  onGenerate,
  loading,
  disabled,
}) {
  return (
    <div className="card">
      <h2>Generation Settings</h2>

      <label>Inference Steps: {steps}</label>
      <input
        type="range"
        min="20"
        max="80"
        step="1"
        value={steps}
        onChange={(e) => setSteps(Number(e.target.value))}
      />

      <label>Guidance Scale: {guidanceScale}</label>
      <input
        type="range"
        min="1"
        max="12"
        step="0.1"
        value={guidanceScale}
        onChange={(e) => setGuidanceScale(Number(e.target.value))}
      />

      <label>ControlNet Scale: {controlnetScale}</label>
      <input
        type="range"
        min="0.1"
        max="1.5"
        step="0.05"
        value={controlnetScale}
        onChange={(e) => setControlnetScale(Number(e.target.value))}
      />

      <label>IP-Adapter Scale: {ipAdapterScale}</label>
      <input
        type="range"
        min="0.1"
        max="2"
        step="0.05"
        value={ipAdapterScale}
        onChange={(e) => setIpAdapterScale(Number(e.target.value))}
      />

      <label>Seed</label>
      <input
        type="number"
        value={seed}
        onChange={(e) => setSeed(Number(e.target.value))}
      />

      <button onClick={onGenerate} disabled={disabled || loading}>
        {loading ? "Processing..." : "Generate Try-On"}
      </button>
    </div>
  );
}