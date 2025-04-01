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

export const getPdfByHashCode = (hashCode) => {
  if (!hashCode) return null;

  const pdfStorageUrl = "http://localhost:5000";
  return `${pdfStorageUrl}/${hashCode}`;
};

export const getDocumentLink = (reference) => {
  const identifier = reference.hash_code || reference.id;
  return getPdfByHashCode(identifier);
};
