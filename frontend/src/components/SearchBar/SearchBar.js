import React from "react";
import "./SearchBar.css";

const SearchBar = ({
  query,
  setQuery,
  onSearch,
  searchSupervisors = false,
  setSearchSupervisors = null,
}) => {
  const handleKeyPress = (e) => {
    if (e.key === "Enter") {
      onSearch();
    }
  };

  return (
    <div className="search-bar-container">
      <div className="search-bar">
        <input
          type="text"
          placeholder={
            searchSupervisors ? "Search supervisors..." : "Search theses..."
          }
          value={query}
          onChange={(e) => setQuery(e.target.value)}
          onKeyPress={handleKeyPress}
        />
        <button onClick={onSearch}>Search</button>
      </div>

      {/* Search Mode Toggle - only show if setSearchSupervisors is provided */}
      {setSearchSupervisors && (
        <div className="search-mode-toggle">
          <label className="search-mode-label">
            <input
              type="checkbox"
              checked={searchSupervisors}
              onChange={(e) => setSearchSupervisors(e.target.checked)}
              className="search-mode-checkbox"
            />
            <span className="search-mode-text">Search supervisors only</span>
          </label>
        </div>
      )}
    </div>
  );
};

export default SearchBar;
