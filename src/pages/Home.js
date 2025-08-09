import React from "react";
import FileUpload from "../components/FileUpload";
import { useNavigate } from "react-router-dom";

const Home = () => {
  const navigate = useNavigate();

  return (
    <div className="min-h-screen bg-gradient-to-br from-gray-50 to-blue-100 flex flex-col items-center justify-center px-4">
      <div className="text-center max-w-2xl">
        <h1 className="text-4xl md:text-5xl font-bold text-gray-800 mb-4">
          📈 StockPulse
        </h1>
        <p className="text-lg text-gray-600 mb-8">
          Upload your personal stock portfolio and get insightful analytics and AI-powered financial summaries.
        </p>
        
        <div className="bg-white shadow-xl rounded-2xl p-6 mb-6">
          <FileUpload />
        </div>
        <button
          onClick={() => navigate("/dashboard")}
          className="mt-4 px-6 py-3 bg-blue-600 hover:bg-blue-700 text-white font-semibold rounded-xl transition duration-200"
        >
          Go to Dashboard →
        </button>
      </div>
    </div>
  );
};



export default Home;
