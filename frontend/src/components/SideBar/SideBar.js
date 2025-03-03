import React from "react";
import "./SideBar.css";

const Sidebar = ({
  year,
  setYear,
  sort,
  setSort,
  isPhrase,
  setIsPhrase,
  onFilter,
}) => {
  return (
    <div className="sidebar">
      <h3>Filters</h3>
      <div className="filter-section">
        <label htmlFor="year-filter">Year</label>
        <input
          id="year-filter"
          type="number"
          placeholder="Filter by year"
          value={year}
          onChange={(e) => setYear(e.target.value)}
        />
      </div>

      <div className="filter-section">
        <label htmlFor="sort-order">Sort Order</label>
        <select
          id="sort-order"
          value={sort}
          onChange={(e) => setSort(e.target.value)}
        >
          <option value="desc">Descending</option>
          <option value="asc">Ascending</option>
        </select>
      </div>

      <div className="filter-section">
        <label className="search-mode-label">Search Mode</label>
        <div className="radio-group">
          <div className="radio-option">
            <input
              type="radio"
              id="regular-search"
              name="search-mode"
              checked={!isPhrase}
              onChange={() => setIsPhrase(false)}
            />
            <label htmlFor="regular-search">Regular Search</label>
          </div>
          <div className="radio-option">
            <input
              type="radio"
              id="phrase-search"
              name="search-mode"
              checked={isPhrase}
              onChange={() => setIsPhrase(true)}
            />
            <label htmlFor="phrase-search">Exact Phrase</label>
          </div>
        </div>
      </div>

      <button className="apply-filters-btn" onClick={onFilter}>
        Apply Filters
      </button>
    </div>
  );
};

export default Sidebar;
