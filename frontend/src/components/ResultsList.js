import React from "react";
import "./ResultsList.css";

const ResultsList = ({ results }) => {
  if (!results) {
    return (
      <p className="error-message">An error occurred while fetching results.</p>
    );
  }

  if (results.length === 0) {
    return <p className="no-results">No results found.</p>;
  }

  const handleGoToPDF = (_id) => {
    window.open(`http://localhost:5000/${_id}`, "_blank");
  };

  return (
    <div className="result-lists">
      <ul className="result-items">
        {results.map((result) => {
          const { _id, _source, highlight } = result;
          const { abstract, author, keywords, year, supervisor } = _source;

          return (
            <li key={_id} className="result-item">
              <h3 className="result-author">
                {author} ({year})
              </h3>
              <p className="result-supervisor">
                <strong>Supervisor:</strong>{" "}
                {Array.isArray(supervisor) ? supervisor.join(", ") : supervisor}
              </p>
              <p className="result-abstract">
                <strong>Abstract:</strong>{" "}
                <span
                  dangerouslySetInnerHTML={{
                    __html: highlight?.abstract
                      ? highlight.abstract.join(" ")
                      : abstract,
                  }}
                />
              </p>
              <p className="result-keywords">
                <strong>Keywords:</strong>{" "}
                {highlight?.keywords
                  ? highlight.keywords.join(", ")
                  : keywords.join(", ")}
              </p>
              <button onClick={() => handleGoToPDF(_id)}>Go to PDF</button>
            </li>
          );
        })}
      </ul>
    </div>
  );
};

export default ResultsList;
