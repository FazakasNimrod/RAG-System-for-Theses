import axios from "axios";

const API_URL = "http://127.0.0.1:5000/search/";

export const searchElasticsearch = async ({
  query,
  year,
  sort,
  isPhrase,
  department,
}) => {
  const params = {};
  if (query) params.q = query;
  if (year) params.year = year;
  if (sort) params.sort = sort;
  if (isPhrase) params.phrase = "true";
  if (department) params.department = department;

  try {
    const response = await axios.get(API_URL, { params });
    return response.data;
  } catch (error) {
    console.error("Error fetching search results:", error);
    return [];
  }
};

export const searchElasticsearchSemantic = async ({
  query,
  year,
  sort,
  limit = 10,
  department,
}) => {
  const params = {};
  if (query) params.q = query;
  if (year) params.year = year;
  if (sort) params.sort = sort;
  if (limit) params.limit = limit;
  if (department) params.department = department;

  try {
    const response = await axios.get(`${API_URL}semantic`, { params });
    return response.data;
  } catch (error) {
    console.error("Error fetching semantic search results:", error);
    return [];
  }
};
