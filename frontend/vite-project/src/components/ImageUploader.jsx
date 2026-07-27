import React from "react";

export default function ImageUploader({ label, file, preview, onChange }) {
  return (
    <div className="card">
      <label className="upload-label">{label}</label>
      <input
        type="file"
        accept="image/*"
        onChange={(e) => onChange(e.target.files?.[0] || null)}
      />

      <div className="preview-box">
        {preview ? (
          <img src={preview} alt={label} className="preview-image" />
        ) : (
          <p>No image selected</p>
        )}
      </div>

      <p className="file-name">{file ? file.name : "No file chosen"}</p>
    </div>
  );
}