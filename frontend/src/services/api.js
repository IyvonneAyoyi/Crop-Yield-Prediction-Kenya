import axios from "axios";
import.meta.env.VITE_API_URL

// FastAPI base URL
const api = axios.create({
  baseURL: import.meta.env.VITE_API_URL || "http://127.0.0.1:8000",
  headers: {
    "Content-Type": "application/json",
  },
});

// GET AVAILABLE CROPS
export const getCrops = async () => {
  const response = await api.get("/crops");
  return response.data.crops;
};

// GET AVAILABLE COUNTIES
export const getCounties = async () => {
  const response = await api.get("/counties");
  return response.data.counties;
};

// PREDICT YIELD
export const predictYield = async (predictionData) => {
  const response = await api.post("/predict", predictionData);
  return response.data;
};

export default api;