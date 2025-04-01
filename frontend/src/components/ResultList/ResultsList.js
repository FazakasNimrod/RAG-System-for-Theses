import React, { useState } from "react";
import { getPdfUrl } from "../../services/elasticsearchService";
import "./ResultsList.css";

const ResultsList = ({ results, showScores = false }) => {
  if (!results) {
    return (
      <p className="error-message">An error occurred while fetching results.</p>
    );
  }

  if (results.length === 0) {
    return <p className="no-results">No results found.</p>;
  }

  const handleGoToPDF = (hash_code) => {
    const pdfUrl = getPdfUrl(hash_code);
    if (pdfUrl) {
      window.open(pdfUrl, "_blank");
    } else {
      console.error("Invalid hash code:", hash_code);
    }
  };

  return (
    <div className="result-lists">
      <ul className="result-items">
        {results.map((result) => {
          const { _id, _source, highlight, _score } = result;
          const { abstract, author, keywords, year, supervisor, hash_code } =
            _source;

          return (
            <li key={_id} className="result-item">
              <div className="result-header">
                <h3 className="result-author">
                  {author} ({year})
                </h3>
                {showScores && _score !== undefined && (
                  <span className="result-score">
                    Similarity Score: {_score.toFixed(2)}
                  </span>
                )}
              </div>
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
              <button onClick={() => handleGoToPDF(hash_code)}>
                Go to PDF
              </button>
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

function truncateText(text, maxLength) {
  if (text.length <= maxLength) return text;
  return text.substring(0, maxLength);
}

export default ResultsList;
