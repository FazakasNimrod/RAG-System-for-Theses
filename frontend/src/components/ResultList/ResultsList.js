import React, { useState } from "react";
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
              <AbstractContent
                abstract={abstract}
                highlight={highlight?.abstract}
              />
              <p className="result-keywords">
                <strong>Keywords:</strong>{" "}
                <KeywordsList
                  originalKeywords={keywords}
                  highlightedKeywords={highlight?.keywords}
                />
              </p>
              <button onClick={() => handleGoToPDF(_id)}>Go to PDF</button>
            </li>
          );
        })}
      </ul>
    </div>
  );
};

const AbstractContent = ({ abstract, highlight }) => {
  const [expanded, setExpanded] = useState(false);
  const toggleExpanded = () => setExpanded(!expanded);

  const needsExpandButton = highlight || abstract.length > 200;

  let displayContent;

  if (expanded) {
    if (highlight) {
      const highlightTerms = new Set();
      highlight.forEach((fragment) => {
        const matches = fragment.match(/<em>(.*?)<\/em>/g);
        if (matches) {
          matches.forEach((match) => {
            const term = match.replace(/<\/?em>/g, "").toLowerCase();
            highlightTerms.add(term);
          });
        }
      });

      let highlightedAbstract = abstract;
      highlightTerms.forEach((term) => {
        const regex = new RegExp(`\\b${term}\\b`, "gi");
        highlightedAbstract = highlightedAbstract.replace(
          regex,
          (match) => `<em>${match}</em>`
        );
      });

      displayContent = highlightedAbstract;
    } else {
      displayContent = abstract;
    }
  } else {
    displayContent = highlight
      ? highlight.join(" ")
      : truncateText(abstract, 200);
  }

  return (
    <div className="result-abstract-container">
      <p className="result-abstract">
        <strong>Abstract:</strong>{" "}
        <span
          dangerouslySetInnerHTML={{
            __html: displayContent,
          }}
        />
        {!expanded && needsExpandButton && "... "}
        {expanded && needsExpandButton && " "}
        {needsExpandButton && (
          <button className="toggle-abstract-btn" onClick={toggleExpanded}>
            {expanded ? "Show Less" : "Show More"}
          </button>
        )}
      </p>
    </div>
  );
};

function truncateText(text, maxLength) {
  if (text.length <= maxLength) return text;
  return text.substring(0, maxLength);
}

const KeywordsList = ({ originalKeywords, highlightedKeywords }) => {
  if (!originalKeywords || originalKeywords.length === 0) {
    return "None";
  }

  if (!highlightedKeywords || highlightedKeywords.length === 0) {
    return originalKeywords.join(", ");
  }

  const highlightTerms = new Map();
  highlightedKeywords.forEach((hwk) => {
    const matches = hwk.match(/<em>(.*?)<\/em>/g);
    if (matches) {
      matches.forEach((match) => {
        const term = match.replace(/<\/?em>/g, "").toLowerCase();
        highlightTerms.set(term, true);
      });
    }
  });

  const displayKeywords = originalKeywords.map((keyword) => {
    const lowercaseKeyword = keyword.toLowerCase();

    for (const term of highlightTerms.keys()) {
      if (lowercaseKeyword.includes(term)) {
        const regex = new RegExp(term, "gi");
        return keyword.replace(regex, (match) => `<em>${match}</em>`);
      }
    }

    return keyword;
  });

  return (
    <span dangerouslySetInnerHTML={{ __html: displayKeywords.join(", ") }} />
  );
};

export default ResultsList;
