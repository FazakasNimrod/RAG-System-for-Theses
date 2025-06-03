import React, { useState, useEffect, useCallback } from "react";
import {
  PieChart,
  Pie,
  Cell,
  ResponsiveContainer,
  Tooltip,
  Legend,
} from "recharts";
import "./TopicPieChart.css";

const CATEGORY_COLORS = {
  "Artificial Intelligence & Machine Learning": "#FF6B6B",
  "Web & Mobile Application Development": "#4ECDC4",
  "IoT, Embedded Systems & Hardware": "#45B7D1",
  "Healthcare & Bioinformatics": "#96CEB4",
  "Education Technology & Gamification": "#FFEAA7",
  "Security & Network Systems": "#DDA0DD",
  "Business & Management Systems": "#98D8C8",
};

const BACKUP_COLORS = [
  "#FF6B6B",
  "#4ECDC4",
  "#45B7D1",
  "#96CEB4",
  "#FFEAA7",
  "#DDA0DD",
  "#98D8C8",
  "#FF9F43",
  "#74B9FF",
  "#A29BFE",
  "#FD79A8",
  "#FDCB6E",
];

const TopicPieChart = ({ department, year, supervisor }) => {
  const [chartData, setChartData] = useState([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);

  const loadTopicData = useCallback(async () => {
    setLoading(true);
    setError(null);

    try {
      const response = await fetch("/categorized_theses.txt");
      if (!response.ok) {
        throw new Error("Failed to load categorized theses data");
      }

      const textData = await response.text();
      const lines = textData
        .trim()
        .split("\n")
        .filter((line) => line.trim());

      const filteredData = lines.filter((line) => {
        const parts = line.split(" - ");
        if (parts.length !== 2) return false;

        const [authorYearDept] = parts;
        const authorYearDeptParts = authorYearDept.split(", ");

        if (authorYearDeptParts.length < 3) return false;

        const thesisYear = parseInt(authorYearDeptParts[1]);
        const thesisDept = authorYearDeptParts[2];

        if (department) {
          const deptFilter = department === "cs" ? "cs" : "info";
          if (thesisDept !== deptFilter) return false;
        }

        if (year && thesisYear !== year) {
          return false;
        }

        return true;
      });

      const topicCounts = {};
      filteredData.forEach((line) => {
        const category = line.split(" - ")[1];
        topicCounts[category] = (topicCounts[category] || 0) + 1;
      });

      const chartDataResult = Object.entries(topicCounts).map(
        ([topic, count], index) => {
          const color =
            CATEGORY_COLORS[topic] ||
            BACKUP_COLORS[index % BACKUP_COLORS.length];
          console.log(`Topic: "${topic}" -> Color: ${color}`);
          return {
            name: topic,
            value: count,
            color: color,
          };
        }
      );

      chartDataResult.sort((a, b) => b.value - a.value);

      console.log("Final chart data:", chartDataResult);

      setChartData(chartDataResult);
    } catch (err) {
      console.error("Error loading topic data:", err);
      setError(err.message);
    } finally {
      setLoading(false);
    }
  }, [department, year]);

  useEffect(() => {
    loadTopicData();
  }, [loadTopicData]);

  if (supervisor) {
    return null;
  }

  const CustomTooltip = ({ active, payload }) => {
    if (active && payload && payload.length) {
      const data = payload[0];
      const percentage = (
        (data.value / chartData.reduce((sum, item) => sum + item.value, 0)) *
        100
      ).toFixed(1);

      return (
        <div className="custom-tooltip">
          <p className="tooltip-title">{data.name}</p>
          <p className="tooltip-value">
            Count: {data.value} ({percentage}%)
          </p>
        </div>
      );
    }
    return null;
  };

  const CustomLabel = ({
    cx,
    cy,
    midAngle,
    innerRadius,
    outerRadius,
    value,
  }) => {
    const total = chartData.reduce((sum, item) => sum + item.value, 0);
    const percentage = ((value / total) * 100).toFixed(1);

    if (percentage < 5) return null;

    const RADIAN = Math.PI / 180;
    const radius = innerRadius + (outerRadius - innerRadius) * 0.5;
    const x = cx + radius * Math.cos(-midAngle * RADIAN);
    const y = cy + radius * Math.sin(-midAngle * RADIAN);

    return (
      <text
        x={x}
        y={y}
        textAnchor={x > cx ? "start" : "end"}
        dominantBaseline="central"
        className="pie-label"
      >
        {`${percentage}%`}
      </text>
    );
  };

  if (loading) {
    return (
      <div className="stats-section">
        <h3>Research Topics Distribution</h3>
        <div className="topic-loading-container">
          <div className="topic-loading-spinner"></div>
          <p className="topic-loading-text">Loading topic distribution...</p>
        </div>
      </div>
    );
  }

  if (error) {
    return (
      <div className="stats-section">
        <h3>Research Topics Distribution</h3>
        <div className="topic-error-container">
          <p className="topic-error-text">Error loading topic data: {error}</p>
          <p className="topic-error-hint">
            Make sure the categorized_theses.txt file is available in the public
            folder.
          </p>
        </div>
      </div>
    );
  }

  if (chartData.length === 0) {
    return (
      <div className="stats-section">
        <h3>Research Topics Distribution</h3>
        <div className="topic-no-data-container">
          <p className="topic-no-data-text">
            No theses found for the selected filters.
          </p>
        </div>
      </div>
    );
  }

  return (
    <div className="stats-section topic-pie-chart">
      <h3>Research Topics Distribution</h3>
      <div className="topic-description">
        <p className="topic-description-text">
          Distribution of {chartData.reduce((sum, item) => sum + item.value, 0)}{" "}
          theses across research topics
          {department &&
            ` in ${department === "cs" ? "Computer Science" : "Informatics"}`}
          {year && ` for year ${year}`}
        </p>
      </div>

      <ResponsiveContainer
        width="100%"
        height={550}
        className="topic-chart-container"
      >
        <PieChart>
          <Pie
            data={chartData}
            cx="50%"
            cy="40%"
            labelLine={false}
            label={CustomLabel}
            outerRadius={170}
            dataKey="value"
            strokeWidth={2}
            stroke="#fff"
          >
            {chartData.map((entry, index) => (
              <Cell key={`cell-${index}`} fill={entry.color} />
            ))}
          </Pie>
          <Tooltip content={<CustomTooltip />} />
          <Legend
            verticalAlign="bottom"
            height={120}
            wrapperStyle={{
              paddingTop: "15px",
              fontSize: "12px",
              lineHeight: "2",
            }}
            formatter={(value, entry) => (
              <span className="legend-item" style={{ color: entry.color }}>
                {value} ({entry.payload.value})
              </span>
            )}
          />
        </PieChart>
      </ResponsiveContainer>
    </div>
  );
};

export default TopicPieChart;
