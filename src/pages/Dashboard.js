// src/pages/Dashboard.js

import React, { useEffect, useState } from "react";
import PortfolioSummary from "../components/PortfolioSummary";
import ChartDisplay from "../components/ChartDisplay";
import AIChatBox from "../components/AIChatBox";
import { fetchSummary, fetchChartData } from "../services/api";

const Dashboard = () => {
  const [summary, setSummary] = useState(null);
  const [chartData, setChartData] = useState(null);

  useEffect(() => {
    const loadDashboardData = async () => {
      try {
        const summaryRes = await fetchSummary();
        const chartRes = await fetchChartData();
        setSummary(summaryRes);
        setChartData(chartRes);
      } catch (error) {
        console.error("Failed to load dashboard data:", error);
      }
    };

    loadDashboardData();
  }, []);

  return (
    <div className="p-6">
      <h1 className="text-3xl font-bold mb-6">📊 Portfolio Dashboard</h1>

      {/* Summary Section */}
      {summary ? (
        <PortfolioSummary summary={summary} />
      ) : (
        <p className="text-gray-500">Loading summary...</p>
      )}

      {/* Charts Section */}
      {chartData ? (
        <div className="mt-8">
          <ChartDisplay data={chartData} />
        </div>
      ) : (
        <p className="text-gray-500 mt-8">Loading charts...</p>
      )}

      {/* AI Chat Section */}
      <div className="mt-10">
        <h2 className="text-2xl font-semibold mb-4">💬 Ask AI About Your Portfolio</h2>
        <AIChatBox />
      </div>
    </div>
  );
};

export default Dashboard;
