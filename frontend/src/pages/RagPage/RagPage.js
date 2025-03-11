import React, { useState, useEffect } from "react";
import { fetchAvailableModels, askQuestion } from "../../services/ragService";
import "./RagPage.css";

const RagPage = () => {
  const [query, setQuery] = useState("");
  const [answer, setAnswer] = useState(null);
  const [loading, setLoading] = useState(false);
  const [initialLoading, setInitialLoading] = useState(true);
  const [error, setError] = useState(null);
  const [models, setModels] = useState([]);
  const [selectedModel, setSelectedModel] = useState("");
  const [numDocs, setNumDocs] = useState(5);

  useEffect(() => {
    const getModels = async () => {
      try {
        setInitialLoading(true);
        const availableModels = await fetchAvailableModels();
        setModels(availableModels);

        if (availableModels.length > 0) {
          const defaultModel =
            availableModels.find((m) => m.id === "llama3.2:3b") ||
            availableModels[0];
          setSelectedModel(defaultModel.id);
        }
      } catch (err) {
        setError(
          "Failed to load available models. Please ensure Ollama is running correctly."
        );
        console.error("Error fetching models:", err);
      } finally {
        setInitialLoading(false);
      }
    };

    getModels();
  }, []);

  const handleSubmit = async (e) => {
    e.preventDefault();

    if (!query.trim()) {
      return;
    }

    setLoading(true);
    setError(null);
    setAnswer(null);

    try {
      const response = await askQuestion(query, selectedModel, numDocs);
      setAnswer(response);
    } catch (err) {
      setError(
        "An error occurred while processing your question. Please ensure Ollama is running and try again."
      );
      console.error("Error asking question:", err);
    } finally {
      setLoading(false);
    }
  };

  const handleKeyPress = (e) => {
    if (e.key === "Enter" && !e.shiftKey) {
      e.preventDefault();
      handleSubmit(e);
    }
  };

  return (
    <div className="rag-page">
      <div className="rag-sidebar">
        <h3>Settings</h3>

        <div className="sidebar-section">
          <label htmlFor="model-selector">Model</label>
          <select
            id="model-selector"
            value={selectedModel}
            onChange={(e) => setSelectedModel(e.target.value)}
            disabled={loading || initialLoading || models.length === 0}
          >
            {models.length === 0 && <option value="">Loading models...</option>}
            {models.map((model) => (
              <option key={model.id} value={model.id}>
                {model.name}
              </option>
            ))}
          </select>
          {selectedModel && models.length > 0 && (
            <div className="model-description">
              {models.find((m) => m.id === selectedModel)?.description}
            </div>
          )}
        </div>

        <div className="sidebar-section">
          <label htmlFor="num-docs">Number of Documents</label>
          <select
            id="num-docs"
            value={numDocs}
            onChange={(e) => setNumDocs(Number(e.target.value))}
            disabled={loading || initialLoading}
          >
            <option value={3}>3 documents</option>
            <option value={5}>5 documents</option>
            <option value={8}>8 documents</option>
            <option value={10}>10 documents</option>
          </select>
        </div>

        <div className="ollama-status">
          <span
            className={models.length > 0 ? "status-online" : "status-offline"}
          >
            {models.length > 0 ? "Ollama: Connected" : "Ollama: Not connected"}
          </span>
        </div>
      </div>

      <div className="rag-content">
        <h1>Ask Research Questions</h1>

        <form onSubmit={handleSubmit} className="question-form">
          <textarea
            value={query}
            onChange={(e) => setQuery(e.target.value)}
            onKeyPress={handleKeyPress}
            placeholder="Ask a research question..."
            rows={4}
            disabled={loading || initialLoading || models.length === 0}
            className="non-resizable"
          />
          <button
            type="submit"
            disabled={
              loading || initialLoading || !query.trim() || models.length === 0
            }
          >
            {loading ? "Processing..." : "Ask Question"}
          </button>
        </form>

        {initialLoading && (
          <div className="loading-container">
            <div className="loading-spinner"></div>
            <p>Establishing connection with Ollama...</p>
          </div>
        )}

        {loading && !initialLoading && (
          <div className="loading-container">
            <div className="loading-spinner"></div>
            <p>
              Generating answer with{" "}
              {models.find((m) => m.id === selectedModel)?.name ||
                selectedModel}
              ...
            </p>
          </div>
        )}

        {error && <div className="error-message">{error}</div>}

        {models.length === 0 && !initialLoading && !error && (
          <div className="warning-message">
            <h3>Ollama Connection Required</h3>
            <p>
              This feature requires Ollama to be running locally. Please make
              sure you have Ollama installed and running with your models.
            </p>
            <p>
              Download Ollama:{" "}
              <a
                href="https://ollama.ai/download"
                target="_blank"
                rel="noopener noreferrer"
              >
                https://ollama.ai/download
              </a>
            </p>
            <p>
              Then run:{" "}
              <code>ollama pull llama3.2:3b llama3.2:1b llama3.1:8b</code>
            </p>
          </div>
        )}

        {answer && !loading && (
          <div className="answer-container">
            <div className="answer-header">
              <h2>Answer</h2>
              <span className="model-badge">Generated by {answer.model}</span>
            </div>

            <div className="answer-content">{answer.answer}</div>

            <div className="references-section">
              <h3>References</h3>
              <ul className="reference-list">
                {answer.references.map((ref, index) => (
                  <li key={index} className="reference-item">
                    <div className="reference-header">
                      <span className="reference-author">
                        {ref.author} ({ref.year})
                      </span>
                      <span className="reference-score">
                        Relevance: {ref.score.toFixed(2)}
                      </span>
                    </div>
                    <p className="reference-snippet">{ref.abstract_snippet}</p>
                    <button
                      className="view-document-btn"
                      onClick={() =>
                        window.open(`http://localhost:5000/${ref.id}`, "_blank")
                      }
                    >
                      View Document
                    </button>
                  </li>
                ))}
              </ul>
            </div>
          </div>
        )}
      </div>
    </div>
  );
};

export default RagPage;
