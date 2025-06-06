import React from "react";
import WordCloud from "../WordCloud/WordCloud";
import TopicPieChart from "../TopicPieChart/TopicPieChart";
import "./StatisticsDisplay.css";

const StatisticsDisplay = ({ statistics }) => {
  const { total_documents, statistics: stats, filters_applied } = statistics;

  const getSelectedSupervisorCount = () => {
    if (!filters_applied?.supervisor) return total_documents;
    return stats.by_supervisor?.[filters_applied.supervisor] || total_documents;
  };

  const supervisorThesesCount = getSelectedSupervisorCount();

  return (
    <div className="statistics-display">
      <div className="stats-overview">
        <div className="stat-card total">
          <div className="stat-number">{supervisorThesesCount}</div>
          <div className="stat-label">
            {filters_applied?.supervisor
              ? `Theses supervised by ${filters_applied.supervisor}`
              : "Total Theses"}
          </div>
        </div>

        {!filters_applied?.supervisor ? (
          <div className="stat-card">
            <div className="stat-number">{stats.supervisors_count || 0}</div>
            <div className="stat-label">Unique Supervisors</div>
          </div>
        ) : (
          Object.keys(stats.by_department || {}).length > 0 && (
            <div className="stat-card">
              <div className="stat-number">
                {Object.keys(stats.by_department).length}
              </div>
              <div className="stat-label">
                {Object.keys(stats.by_department).length === 1
                  ? "Department"
                  : "Departments"}
              </div>
              <div className="stat-subtitle">
                {Object.entries(stats.by_department || {})
                  .map(
                    ([dept, count]) =>
                      `${dept === "cs" ? "CS" : "Info"}: ${count}`
                  )
                  .join(", ")}
              </div>
            </div>
          )
        )}

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
        {/* Topic Distribution Pie Chart and Top Supervisors - Only show when supervisor is NOT selected */}
        {!filters_applied?.supervisor && (
          <>
            <TopicPieChart
              department={filters_applied?.department}
              year={filters_applied?.year}
              supervisor={filters_applied?.supervisor}
            />

            <div className="stats-section">
              <h3>Top Supervisors</h3>
              <div
                className="supervisor-list"
                style={{ maxHeight: "100%", overflowY: "auto" }}
              >
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
          </>
        )}

        {filters_applied?.supervisor ? (
          <>
            <div className="stats-section">
              <h3>Supervisor Information</h3>
              <div className="supervisor-info">
                <div className="supervisor-detail">
                  <strong>Name:</strong> {filters_applied.supervisor}
                </div>
                <div className="supervisor-detail">
                  <strong>Total Theses Supervised:</strong>{" "}
                  {supervisorThesesCount}
                </div>
              </div>
            </div>

            <div className="stats-section">
              <h3>Theses by Year</h3>
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
                              (count /
                                Math.max(...Object.values(stats.by_year))) *
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
              {Object.keys(stats.by_year || {}).length === 0 && (
                <div className="no-data-message">
                  No thesis data found for this supervisor.
                </div>
              )}
            </div>

            <div className="stats-section word-cloud-section">
              <h3>Research Areas Word Cloud</h3>
              <div className="word-cloud-description">
                <p>
                  Interactive visualization of research keywords and topics.
                  Hover over words to see frequency details.
                </p>
              </div>
              {stats.keyword_cloud_data &&
              stats.keyword_cloud_data.length > 0 ? (
                <WordCloud
                  data={stats.keyword_cloud_data}
                  height={450}
                  className="supervisor-word-cloud"
                />
              ) : (
                <div className="no-data-message">
                  No research keywords found for this supervisor.
                </div>
              )}
            </div>

            <div className="stats-section recent-theses">
              <h3>Recent Theses Supervised</h3>
              <div className="thesis-list">
                {(stats.recent_theses || [])
                  .slice(0, 6)
                  .map((thesis, index) => (
                    <div key={index} className="thesis-item">
                      <div className="thesis-header">
                        <div className="thesis-author">{thesis.author}</div>
                        <div className="thesis-year">{thesis.year}</div>
                      </div>
                      <div className="thesis-details">
                        <div className="thesis-department">
                          {thesis.department === "cs"
                            ? "Computer Science"
                            : "Informatics"}
                        </div>
                      </div>
                      {thesis.hash_code && (
                        <button
                          className="view-pdf-btn"
                          onClick={() =>
                            window.open(
                              `http://localhost:5000/${thesis.hash_code}`,
                              "_blank"
                            )
                          }
                        >
                          View PDF
                        </button>
                      )}
                    </div>
                  ))}
                {(!stats.recent_theses || stats.recent_theses.length === 0) && (
                  <div className="no-theses-message">
                    No recent theses found for this supervisor.
                  </div>
                )}
              </div>
            </div>
          </>
        ) : (
          <>
            {/* Only show Distribution by Year if no specific year is selected */}
            {!filters_applied?.year && (
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
                                (count /
                                  Math.max(...Object.values(stats.by_year))) *
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
            )}

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

            <div className="stats-section word-cloud-section">
              <h3>Research Trends - Keyword Cloud</h3>
              {stats.keyword_cloud_data &&
              stats.keyword_cloud_data.length > 0 ? (
                <WordCloud
                  data={stats.keyword_cloud_data}
                  height={500}
                  className="main-word-cloud"
                />
              ) : (
                <div className="no-data-message">
                  No research keywords found for the selected filters.
                </div>
              )}
              <div className="word-cloud-legend">
                <p className="legend-text">
                  💡 <strong>Tip:</strong> Hover over keywords to see exact
                  frequencies. The size reflects how commonly these topics
                  appear in theses.
                </p>
              </div>
            </div>

            <div className="stats-section recent-theses">
              <h3>Recent Theses</h3>
              <div className="thesis-list">
                {(stats.recent_theses || [])
                  .slice(0, 8)
                  .map((thesis, index) => (
                    <div key={index} className="thesis-item">
                      <div className="thesis-header">
                        <div className="thesis-author">{thesis.author}</div>
                        <div className="thesis-year">{thesis.year}</div>
                      </div>
                      <div className="thesis-details">
                        <div className="thesis-department">
                          {thesis.department === "cs"
                            ? "Computer Science"
                            : "Informatics"}
                        </div>
                        {Array.isArray(thesis.supervisor) ? (
                          <div className="thesis-supervisor">
                            Supervisor: {thesis.supervisor.join(", ")}
                          </div>
                        ) : thesis.supervisor ? (
                          <div className="thesis-supervisor">
                            Supervisor: {thesis.supervisor}
                          </div>
                        ) : null}
                      </div>
                      {thesis.hash_code && (
                        <button
                          className="view-pdf-btn"
                          onClick={() =>
                            window.open(
                              `http://localhost:5000/${thesis.hash_code}`,
                              "_blank"
                            )
                          }
                        >
                          View PDF
                        </button>
                      )}
                    </div>
                  ))}
                {(!stats.recent_theses || stats.recent_theses.length === 0) && (
                  <div className="no-theses-message">
                    No recent theses found for the selected filters.
                  </div>
                )}
              </div>
            </div>
          </>
        )}
      </div>
    </div>
  );
};

export default StatisticsDisplay;
