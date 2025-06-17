import axios from "axios";

const API_URL = "http://127.0.0.1:5000/search/";

export const getStatistics = async ({
  department = null,
  year = null,
  supervisor = null,
}) => {
  const params = {};
  if (department) params.department = department;
  if (year) params.year = year;
  if (supervisor) params.supervisor = supervisor;

  console.log("Getting statistics with params:", params);

  try {
    const response = await axios.get(`${API_URL}statistics`, { params });
    console.log("Statistics response:", response.data);
    return response.data;
  } catch (error) {
    console.error("Error fetching statistics:", error);

    if (!department && !year && !supervisor) {
      try {
        console.log("Trying with empty string parameters...");
        const response = await axios.get(`${API_URL}statistics`, {
          params: {
            department: "",
            year: "",
            supervisor: "",
          },
        });
        console.log("Alternative request succeeded:", response.data);
        return response.data;
      } catch (altError) {
        console.error("Alternative request also failed:", altError);
      }
    }

    throw error;
  }
};

export const getUniqueSupervisors = async (department = null, year = null) => {
  const params = {};
  if (department) params.department = department;
  if (year) params.year = year;

  console.log("Getting supervisors with params:", params);

  try {
    const response = await axios.get(`${API_URL}statistics/supervisors`, {
      params,
    });
    console.log("Supervisors response:", response.data);
    return response.data;
  } catch (error) {
    console.error("Error fetching supervisors:", error);
    return [];
  }
};

export const getUniqueYears = async (department = null) => {
  const params = {};
  if (department) params.department = department;

  console.log("Getting years with params:", params);

  try {
    const response = await axios.get(`${API_URL}statistics/years`, { params });
    console.log("Years response:", response.data);
    return response.data;
  } catch (error) {
    console.error("Error fetching years:", error);
    return [];
  }
};
