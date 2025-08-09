// src/services/api.js
const BASE_URL = process.env.REACT_APP_API_URL || "http://localhost:5000";

export const uploadPortfolio = async (file) => {
  const formData = new FormData();
  formData.append("file", file);

  const res = await fetch(`${BASE_URL}/upload`, {
    method: "POST",
    body: formData,
  });

  return res.json();
};

export const fetchSummary = async () => {
  const res = await fetch(`${BASE_URL}/summary`);
  return res.json();
};

export const fetchChartData = async () => {
  const res = await fetch(`${BASE_URL}/charts`);
  return res.json();
};

export const askAI = async (query) => {
  const res = await fetch(`${BASE_URL}/ask`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ query }),
  });
  return res.json();
};
