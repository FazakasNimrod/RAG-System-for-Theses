import axios from "axios";

const API_URL = "http://127.0.0.1:5000/search";

export const fetchAvailableModels = async () => {
  try {
    const response = await axios.get(`${API_URL}/models`);
    return response.data;
  } catch (error) {
    console.error("Error fetching available models:", error);
    throw error;
  }
};

export const askQuestion = async (
  query,
  model = "llama3.2:3b",
  topK = 5,
  department = null
) => {
  try {
    const response = await axios.post(`${API_URL}/rag`, {
      query,
      model,
      top_k: topK,
      department,
    });
    return response.data;
  } catch (error) {
    console.error("Error asking question:", error);
    throw error;
  }
};
