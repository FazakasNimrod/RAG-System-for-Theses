import React, { useState } from "react";
import "./ResultsList.css";

const ResultsList = ({ results }) => {
  // Early return for empty results or error
  if (!results) {
    return (
      <p className="error-message">An error occurred while fetching results.</p>
    );
  }

  if (results.length === 0) {
    return <p className="no-results">No results found.</p>;
  }

  const handleGoToPDF = (_id) => {
    // Open the PDF in a new tab
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

// Abstract content component with inline show more/less button
const AbstractContent = ({ abstract, highlight }) => {
  const [expanded, setExpanded] = useState(false);
  const toggleExpanded = () => setExpanded(!expanded);

  // Determine if we need a "Show More" button
  // We need it if: there are highlights (as they're partial) OR the abstract is long
  const needsExpandButton = highlight || abstract.length > 200;

  // If we have highlighted content, preserve highlighting in the full abstract
  let displayContent;

  if (expanded) {
    // When expanded, we still want to show highlights
    if (highlight) {
      // Extract terms that should be highlighted
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

      // Apply highlighting to the full abstract
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
    // When collapsed, show highlight fragments if available or truncated abstract
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

// Helper function to truncate text to a specified length
function truncateText(text, maxLength) {
  if (text.length <= maxLength) return text;
  return text.substring(0, maxLength);
}

// Component to handle keywords display with highlighting
const KeywordsList = ({ originalKeywords, highlightedKeywords }) => {
  if (!originalKeywords || originalKeywords.length === 0) {
    return "None";
  }

  // If no highlighted keywords, just return the originals
  if (!highlightedKeywords || highlightedKeywords.length === 0) {
    return originalKeywords.join(", ");
  }

  // Create a map of the original keywords for quick lookup
  const keywordMap = new Map();

  // Create a map of terms that should be highlighted
  // (extract the text content from the highlighted HTML)
  const highlightTerms = new Map();
  highlightedKeywords.forEach((hwk) => {
    // Extract the text inside <em> tags if present
    const matches = hwk.match(/<em>(.*?)<\/em>/g);
    if (matches) {
      matches.forEach((match) => {
        const term = match.replace(/<\/?em>/g, "").toLowerCase();
        highlightTerms.set(term, true);
      });
    }
  });

  // Convert original keywords to highlighted versions if needed
  const displayKeywords = originalKeywords.map((keyword) => {
    const lowercaseKeyword = keyword.toLowerCase();

    // Check if this keyword or part of it should be highlighted
    for (const term of highlightTerms.keys()) {
      if (lowercaseKeyword.includes(term)) {
        // Create a highlighted version by wrapping the matching part in <em>
        const regex = new RegExp(term, "gi");
        return keyword.replace(regex, (match) => `<em>${match}</em>`);
      }
    }

    return keyword;
  });

  // Return as HTML
  return (
    <span dangerouslySetInnerHTML={{ __html: displayKeywords.join(", ") }} />
  );
};

export default ResultsList;
