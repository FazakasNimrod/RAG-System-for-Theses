import React, { useState, useEffect, useCallback } from "react";
import StatisticsSidebar from "../../components/StatisticsSidebar/StatisticsSidebar";
import StatisticsDisplay from "../../components/StatisticsDisplay/StatisticsDisplay";
import { getStatistics } from "../../services/statisticsService";
import "./StatisticsPage.css";

const StatisticsPage = () => {
  const [statistics, setStatistics] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  const [department, setDepartment] = useState(null);
  const [year, setYear] = useState(null);
  const [supervisor, setSupervisor] = useState(null);

  const fetchStatistics = useCallback(async () => {
    setLoading(true);
    setError(null);

    try {
      const data = await getStatistics({
        department,
        year,
        supervisor,
      });

      if (data.success) {
        setStatistics(data);
      } else {
        setError(data.error || "Failed to fetch statistics");
      }
    } catch (err) {
      setError("Failed to fetch statistics");
      console.error("Error fetching statistics:", err);
    } finally {
      setLoading(false);
    }
  }, [department, year, supervisor]);

  useEffect(() => {
    fetchStatistics();
  }, [fetchStatistics]);

  const handleFilterChange = (newFilters) => {
    setDepartment(newFilters.department);
    setYear(newFilters.year);
    setSupervisor(newFilters.supervisor);
  };

  const clearFilters = () => {
    setDepartment(null);
    setYear(null);
    setSupervisor(null);
  };

  return (
    <div className="statistics-page">
      <StatisticsSidebar
        department={department}
        year={year}
        supervisor={supervisor}
        onFilterChange={handleFilterChange}
        onClearFilters={clearFilters}
      />

      <div className="statistics-content">
        <div className="statistics-header">
          <h1>Thesis Statistics</h1>
          {(department || year || supervisor) && (
            <div className="active-filters">
              <span className="filters-label">Active Filters:</span>
              {department && (
                <span className="filter-tag">
                  Department:{" "}
                  {department === "cs" ? "Computer Science" : "Informatics"}
                </span>
              )}
              {year && <span className="filter-tag">Year: {year}</span>}
              {supervisor && (
                <span className="filter-tag">Supervisor: {supervisor}</span>
              )}
            </div>
          )}
        </div>

        {loading && (
          <div className="loading-container">
            <div className="loading-spinner"></div>
            <p>Loading statistics...</p>
          </div>
        )}

        {error && (
          <div className="error-container">
            <div className="error-message">
              <h3>Error Loading Statistics</h3>
              <p>{error}</p>
              <button onClick={fetchStatistics} className="retry-btn">
                Try Again
              </button>
            </div>
          </div>
        )}

        {!loading && !error && statistics && (
          <StatisticsDisplay statistics={statistics} />
        )}
      </div>
    </div>
  );
};

export default StatisticsPage;
