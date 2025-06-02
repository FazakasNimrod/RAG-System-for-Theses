import React from "react";
import { TagCloud } from "react-tagcloud";
import "./WordCloud.css";

const WordCloud = ({ data, width = 600, height = 400, className = "" }) => {
  if (!data || data.length === 0) {
    return (
      <div className={`word-cloud-container ${className}`}>
        <div className="word-cloud-empty">
          <p>No keywords available</p>
        </div>
      </div>
    );
  }

  const transformedData = data.map((item) => ({
    value: item.text,
    count: item.value,
    key: item.text,
  }));

  const colorOptions = {
    luminosity: "bright",
    hue: ["blue", "green", "red", "orange", "purple", "pink"],
  };

  const customRenderer = (tag, size, color) => (
    <span
      key={tag.key}
      style={{
        fontSize: `${size}px`,
        color: color,
        margin: "3px",
        padding: "2px 4px",
        display: "inline-block",
        borderRadius: "3px",
        transition: "all 0.2s ease",
        fontWeight: "500",
        fontFamily: "Arial, sans-serif",
      }}
      className="tag-cloud-word"
      title={`${tag.value}: ${tag.count} thesis${tag.count !== 1 ? "es" : ""}`}
      onMouseEnter={(e) => {
        e.target.style.fontWeight = "bold";
        e.target.style.backgroundColor = "rgba(0, 123, 255, 0.1)";
      }}
      onMouseLeave={(e) => {
        e.target.style.fontWeight = "500";
        e.target.style.backgroundColor = "transparent";
      }}
    >
      {tag.value}
    </span>
  );

  return (
    <div className={`word-cloud-container ${className}`}>
      <div
        className="word-cloud-wrapper"
        style={{
          width: "100%",
          height: height,
          display: "flex",
          alignItems: "center",
          justifyContent: "center",
          padding: "20px",
          boxSizing: "border-box",
        }}
      >
        <TagCloud
          tags={transformedData}
          minSize={12}
          maxSize={48}
          colorOptions={colorOptions}
          renderer={customRenderer}
          className="tag-cloud"
        />
      </div>
    </div>
  );
};

export default WordCloud;
