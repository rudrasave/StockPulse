import React, { useEffect, useState } from 'react';
import { fetchSummary } from '../services/api';

const PortfolioSummary = () => {
  const [summary, setSummary] = useState(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const loadSummary = async () => {
      try {
        const data = await fetchSummary();
        setSummary(data);
      } catch (err) {
        console.error("Failed to fetch summary:", err);
      } finally {
        setLoading(false);
      }
    };
    loadSummary();
  }, []);

  if (loading) return <p className="text-center">Loading summary...</p>;
  if (!summary) return <p className="text-center text-red-500">No summary data found.</p>;

  return (
    <div className="bg-white shadow-md rounded p-4 mt-4">
      <h2 className="text-xl font-semibold mb-4">📊 Portfolio Summary</h2>
      <div className="grid grid-cols-1 sm:grid-cols-3 gap-4 mb-4">
        <div className="p-4 border rounded">
          <p className="text-gray-500">Total Investment</p>
          <p className="text-lg font-bold">₹ {summary.total_investment.toLocaleString()}</p>
        </div>
        <div className="p-4 border rounded">
          <p className="text-gray-500">Total Gain/Loss</p>
          <p className={`text-lg font-bold ${summary.total_gain >= 0 ? 'text-green-600' : 'text-red-600'}`}>
            ₹ {summary.total_gain.toLocaleString()}
          </p>
        </div>
        <div className="p-4 border rounded">
          <p className="text-gray-500">Current Value</p>
          <p className="text-lg font-bold">₹ {summary.current_value.toLocaleString()}</p>
        </div>
      </div>

      <h3 className="text-md font-semibold mb-2">Top Holdings</h3>
      <table className="min-w-full text-sm text-left border">
        <thead className="bg-gray-100">
          <tr>
            <th className="p-2">Symbol</th>
            <th className="p-2">Quantity</th>
            <th className="p-2">Gain/Loss</th>
          </tr>
        </thead>
        <tbody>
          {summary.top_holdings.map((stock, idx) => (
            <tr key={idx} className="border-t">
              <td className="p-2">{stock.symbol}</td>
              <td className="p-2">{stock.quantity}</td>
              <td className={`p-2 ${stock.gain >= 0 ? 'text-green-600' : 'text-red-600'}`}>
                ₹ {stock.gain.toLocaleString()}
              </td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
};

export default PortfolioSummary;
