import React, { useState } from "react";
import "./SideBar.css";

const Sidebar = ({
  year,
  setYear,
  sort,
  setSort,
  isPhrase,
  setIsPhrase,
  limit,
  setLimit,
  department,
  setDepartment,
  searchSupervisors,
  setSearchSupervisors,
  onFilter,
  hidePhraseOption = false,
  hideSortOption = false,
  showLimitOption = false,
  showSupervisorOption = false,
}) => {
  const [departments] = useState([
    { id: "cs", name: "Computer Science" },
    { id: "informatics", name: "Informatics" },
  ]);

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

      {setDepartment && (
        <div className="filter-section">
          <label htmlFor="department-filter">Department</label>
          <select
            id="department-filter"
            value={department || ""}
            onChange={(e) => setDepartment(e.target.value || null)}
          >
            <option value="">All Departments</option>
            {departments.map((dept) => (
              <option key={dept.id} value={dept.id}>
                {dept.name}
              </option>
            ))}
          </select>
        </div>
      )}

      {!hideSortOption && setSort && (
        <div className="filter-section">
          <label htmlFor="sort-order">Sort By Year</label>
          <select
            id="sort-order"
            value={sort}
            onChange={(e) => setSort(e.target.value)}
          >
            <option value="relevance">Relevance (Default)</option>
            <option value="desc">Newest First</option>
            <option value="asc">Oldest First</option>
          </select>
        </div>
      )}

      {!hidePhraseOption && setIsPhrase && (
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
      )}

      {showSupervisorOption && setSearchSupervisors && (
        <div className="filter-section">
          <label className="search-mode-label">Search Target</label>
          <div className="radio-group">
            <div className="radio-option">
              <input
                type="checkbox"
                id="search-supervisors"
                checked={searchSupervisors}
                onChange={(e) => setSearchSupervisors(e.target.checked)}
              />
              <label htmlFor="search-supervisors">
                Search Supervisors Only
              </label>
            </div>
          </div>
        </div>
      )}

      {showLimitOption && setLimit && (
        <div className="filter-section">
          <label htmlFor="result-limit">Result Limit</label>
          <select
            id="result-limit"
            value={limit}
            onChange={(e) => setLimit(parseInt(e.target.value))}
          >
            <option value="5">5 results</option>
            <option value="10">10 results</option>
            <option value="20">20 results</option>
            <option value="50">50 results</option>
            <option value="100">100 results</option>
          </select>
        </div>
      )}

      <button className="apply-filters-btn" onClick={onFilter}>
        Apply Filters
      </button>
    </div>
  );
};

export default Sidebar;
