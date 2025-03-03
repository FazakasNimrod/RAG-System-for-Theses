import axios from "axios";

const API_URL = "http://127.0.0.1:5000/search/";

export const searchElasticsearch = async ({ query, year, sort, isPhrase }) => {
  const params = {};
  if (query) params.q = query;
  if (year) params.year = year;
  if (sort) params.sort = sort;
  if (isPhrase) params.phrase = "true";

  try {
    const response = await axios.get(API_URL, { params });
    return response.data;
  } catch (error) {
    console.error("Error fetching search results:", error);
    return [];
  }
};
