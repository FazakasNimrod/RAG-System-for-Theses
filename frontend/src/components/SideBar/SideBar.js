import React from "react";
import "./SideBar.css";

const Sidebar = ({ year, setYear, sort, setSort, onFilter }) => {
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

      <button className="apply-filters-btn" onClick={onFilter}>
        Apply Filters
      </button>
    </div>
  );
};

export default Sidebar;
