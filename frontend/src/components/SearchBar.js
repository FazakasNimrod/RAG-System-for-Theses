import React from "react";
import "./SearchBar.css";

const SearchBar = ({ query, setQuery, onSearch }) => {
  // Handle key press events
  const handleKeyPress = (e) => {
    // Check if Enter key was pressed
    if (e.key === "Enter") {
      onSearch();
    }
  };

  return (
    <div className="search-bar">
      <input
        type="text"
        placeholder="Search..."
        value={query}
        onChange={(e) => setQuery(e.target.value)}
        onKeyPress={handleKeyPress}
      />
      <button onClick={onSearch}>Search</button>
    </div>
  );
};

export default SearchBar;
