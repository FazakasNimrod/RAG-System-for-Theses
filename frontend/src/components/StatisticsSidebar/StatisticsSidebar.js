import React, { useState, useEffect } from "react";
import {
  getUniqueSupervisors,
  getUniqueYears,
} from "../../services/statisticsService";
import "./StatisticsSidebar.css";

const StatisticsSidebar = ({
  department,
  year,
  supervisor,
  onFilterChange,
  onClearFilters,
}) => {
  const [supervisors, setSupervisors] = useState([]);
  const [years, setYears] = useState([]);
  const [loadingSupervisors, setLoadingSupervisors] = useState(false);
  const [loadingYears, setLoadingYears] = useState(false);

  const departments = [
    { id: "cs", name: "Computer Science" },
    { id: "informatics", name: "Informatics" },
  ];

  useEffect(() => {
    const fetchSupervisors = async () => {
      setLoadingSupervisors(true);
      try {
        console.log(`Fetching supervisors for department: ${department}`);
        const data = await getUniqueSupervisors(department);
        console.log(`Received ${data.length} supervisors:`, data);
        setSupervisors(data);
      } catch (error) {
        console.error("Error fetching supervisors:", error);
        setSupervisors([]);
      } finally {
        setLoadingSupervisors(false);
      }
    };

    fetchSupervisors();
  }, [department]);

  useEffect(() => {
    const fetchYears = async () => {
      setLoadingYears(true);
      try {
        console.log(`Fetching years for department: ${department}`);
        const data = await getUniqueYears(department);
        console.log(`Received ${data.length} years:`, data);
        setYears(data);
      } catch (error) {
        console.error("Error fetching years:", error);
        setYears([]);
      } finally {
        setLoadingYears(false);
      }
    };

    fetchYears();
  }, [department]);

  const handleDepartmentChange = (newDepartment) => {
    const dept = newDepartment === "" ? null : newDepartment;
    onFilterChange({
      department: dept,
      year: null,
      supervisor: null,
    });
  };

  const handleYearChange = (newYear) => {
    const yearValue = newYear === "" ? null : parseInt(newYear);
    onFilterChange({
      department,
      year: yearValue,
      supervisor,
    });
  };

  const handleSupervisorChange = (newSupervisor) => {
    const supervisorValue = newSupervisor === "" ? null : newSupervisor;
    onFilterChange({
      department,
      year,
      supervisor: supervisorValue,
    });
  };

  const hasActiveFilters = department || year || supervisor;

  return (
    <div className="statistics-sidebar">
      <h3>Filters</h3>

      <div className="filter-section">
        <label htmlFor="department-filter">Department</label>
        <select
          id="department-filter"
          value={department || ""}
          onChange={(e) => handleDepartmentChange(e.target.value)}
        >
          <option value="">All Departments</option>
          {departments.map((dept) => (
            <option key={dept.id} value={dept.id}>
              {dept.name}
            </option>
          ))}
        </select>
      </div>

      <div className="filter-section">
        <label htmlFor="year-filter">Year</label>
        <select
          id="year-filter"
          value={year || ""}
          onChange={(e) => handleYearChange(e.target.value)}
          disabled={loadingYears}
        >
          <option value="">All Years</option>
          {years.map((yearOption) => (
            <option key={yearOption} value={yearOption}>
              {yearOption}
            </option>
          ))}
        </select>
        {loadingYears && <div className="loading-text">Loading years...</div>}
      </div>

      <div className="filter-section">
        <label htmlFor="supervisor-filter">Supervisor</label>
        <select
          id="supervisor-filter"
          value={supervisor || ""}
          onChange={(e) => handleSupervisorChange(e.target.value)}
          disabled={loadingSupervisors}
        >
          <option value="">All Supervisors</option>
          {supervisors.map((supervisorOption) => (
            <option key={supervisorOption} value={supervisorOption}>
              {supervisorOption}
            </option>
          ))}
        </select>
        {loadingSupervisors && (
          <div className="loading-text">Loading supervisors...</div>
        )}
      </div>

      {hasActiveFilters && (
        <div className="filter-actions">
          <button className="clear-all-btn" onClick={onClearFilters}>
            Clear All Filters
          </button>
        </div>
      )}
    </div>
  );
};

export default StatisticsSidebar;
