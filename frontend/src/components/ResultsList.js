import React from "react";

const ResultsList = ({ results }) => {
  if (!results) {
    return <p>An error occurred while fetching results.</p>;
  }

  if (results.length === 0) {
    return <p>No results found.</p>;
  }

  return (
    <ul>
      {results.map((result) => {
        const { _id, _source, highlight } = result;
        const { abstract, author, keywords, year } = _source;

        return (
          <li key={_id}>
            <h3>
              {author} ({year})
            </h3>
            <p>
              <strong>Abstract:</strong>{" "}
              {highlight?.abstract
                ? highlight.abstract.join(" ")
                : abstract}
            </p>
            <p>
              <strong>Keywords:</strong>{" "}
              {highlight?.keywords
                ? highlight.keywords.join(", ")
                : keywords.join(", ")}
            </p>
          </li>
        );
      })}
    </ul>
  );
};

export default ResultsList;
