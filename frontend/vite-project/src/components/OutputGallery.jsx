import React from "react";

function OutputCard({ title, src }) {
  return (
    <div className="card">
      <h3>{title}</h3>
      <div className="preview-box">
        {src ? <img src={src} alt={title} className="preview-image" /> : <p>No output yet</p>}
      </div>
    </div>
  );
}

export default function OutputGallery({ outputs }) {
  return (
    <div className="output-grid">
      <OutputCard title="Final Output" src={outputs.final_output} />
      <OutputCard title="Resized Person" src={outputs.resized_person} />
      <OutputCard title="Resized Garment" src={outputs.resized_garment} />
      <OutputCard title="Depth Map" src={outputs.depth_map} />
      <OutputCard title="Mask" src={outputs.mask} />
    </div>
  );
}