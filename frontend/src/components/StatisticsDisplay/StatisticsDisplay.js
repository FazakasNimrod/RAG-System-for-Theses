import React from "react";
import "./StatisticsDisplay.css";

const StatisticsDisplay = ({ statistics }) => {
  const { total_documents, statistics: stats } = statistics;

  return (
    <div className="statistics-display">
      <div className="stats-overview">
        <div className="stat-card total">
          <div className="stat-number">{total_documents}</div>
          <div className="stat-label">Total Theses</div>
        </div>

        <div className="stat-card">
          <div className="stat-number">{stats.supervisors_count || 0}</div>
          <div className="stat-label">Unique Supervisors</div>
        </div>

        <div className="stat-card">
          <div className="stat-number">
            {stats.year_range?.max - stats.year_range?.min + 1 || 0}
          </div>
          <div className="stat-label">Year Range</div>
          <div className="stat-subtitle">
            {stats.year_range?.min} - {stats.year_range?.max}
          </div>
        </div>

        <div className="stat-card">
          <div className="stat-number">
            {stats.average_abstract_length || 0}
          </div>
          <div className="stat-label">Avg Abstract Length</div>
          <div className="stat-subtitle">characters</div>
        </div>
      </div>

      <div className="stats-grid">
        <div className="stats-section">
          <h3>Distribution by Year</h3>
          <div className="year-chart">
            {Object.entries(stats.by_year || {})
              .sort(([a], [b]) => parseInt(b) - parseInt(a))
              .map(([year, count]) => (
                <div key={year} className="year-bar">
                  <div className="year-label">{year}</div>
                  <div className="bar-container">
                    <div
                      className="bar"
                      style={{
                        width: `${
                          (count / Math.max(...Object.values(stats.by_year))) *
                          100
                        }%`,
                      }}
                    >
                      <span className="bar-count">{count}</span>
                    </div>
                  </div>
                </div>
              ))}
          </div>
        </div>

        {Object.keys(stats.by_department || {}).length > 1 && (
          <div className="stats-section">
            <h3>Distribution by Department</h3>
            <div className="department-chart">
              {Object.entries(stats.by_department || {}).map(
                ([dept, count]) => (
                  <div key={dept} className="department-item">
                    <div className="department-name">
                      {dept === "cs" ? "Computer Science" : "Informatics"}
                    </div>
                    <div className="department-bar">
                      <div
                        className="bar"
                        style={{
                          width: `${(count / total_documents) * 100}%`,
                        }}
                      >
                        <span className="bar-count">{count}</span>
                      </div>
                    </div>
                    <div className="department-percentage">
                      {((count / total_documents) * 100).toFixed(1)}%
                    </div>
                  </div>
                )
              )}
            </div>
          </div>
        )}

        <div className="stats-section">
          <h3>Top Supervisors</h3>
          <div className="supervisor-list">
            {Object.entries(stats.by_supervisor || {})
              .sort(([, a], [, b]) => b - a)
              .slice(0, 10)
              .map(([supervisor, count]) => (
                <div key={supervisor} className="supervisor-item">
                  <div className="supervisor-name">{supervisor}</div>
                  <div className="supervisor-count">{count} theses</div>
                </div>
              ))}
          </div>
        </div>

        <div className="stats-section">
          <h3>Most Common Keywords</h3>
          <div className="keywords-cloud">
            {Object.entries(stats.top_keywords || {})
              .slice(0, 12)
              .map(([keyword, count]) => (
                <div
                  key={keyword}
                  className="keyword-tag"
                  style={{
                    fontSize: `${Math.min(
                      1.5,
                      0.8 +
                        (count /
                          Math.max(...Object.values(stats.top_keywords))) *
                          0.7
                    )}rem`,
                  }}
                >
                  {keyword} ({count})
                </div>
              ))}
          </div>
        </div>
      </div>
    </div>
  );
};

export default StatisticsDisplay;
