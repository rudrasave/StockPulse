// src/components/ChartDisplay.js
import React, { useEffect, useState } from "react";
import { fetchChartData } from "../services/api";
import {
  BarChart,
  Bar,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  ResponsiveContainer,
  Legend,
  LineChart,
  Line,
} from "recharts";

const ChartDisplay = () => {
  const [data, setData] = useState([]);

  useEffect(() => {
    const getData = async () => {
      const chartData = await fetchChartData();
      setData(chartData);
    };
    getData();
  }, []);

  if (!data || data.length === 0) return <p>Loading charts...</p>;

  return (
    <div className="p-4">
      <h2 className="text-xl font-semibold mb-4">📊 Portfolio Performance</h2>
      <div className="mb-6 h-72">
        <ResponsiveContainer width="100%" height="100%">
          <BarChart data={data}>
            <CartesianGrid strokeDasharray="3 3" />
            <XAxis dataKey="stock" />
            <YAxis />
            <Tooltip />
            <Legend />
            <Bar dataKey="gain" fill="#4ade80" name="Gain" />
            <Bar dataKey="loss" fill="#f87171" name="Loss" />
          </BarChart>
        </ResponsiveContainer>
      </div>

      <div className="h-72">
        <ResponsiveContainer width="100%" height="100%">
          <LineChart data={data}>
            <CartesianGrid strokeDasharray="3 3" />
            <XAxis dataKey="stock" />
            <YAxis />
            <Tooltip />
            <Legend />
            <Line type="monotone" dataKey="value" stroke="#3b82f6" name="Total Value" />
          </LineChart>
        </ResponsiveContainer>
      </div>
    </div>
  );
};

export default ChartDisplay;
