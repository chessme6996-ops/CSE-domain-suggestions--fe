"use client";
import { useState } from "react";

export default function PredictForm({ values, setValues }) {
  const [result, setResult] = useState("");
  const [loading, setLoading] = useState(false);

  async function handlePredict() {
    const entries = Object.values(values);
    if (entries.length !== 14 || entries.some(v => v === "")) {
      setResult("Please fill all inputs");
      return;
    }

    setLoading(true);
    try {
      const apiUrl = process.env.NEXT_PUBLIC_API_URL || "http://127.0.0.1:8000";
      const response = await fetch(`${apiUrl}/predict`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ values: entries.map(Number) })
      });

      if (!response.ok) throw new Error("Server error");
      const data = await response.json();
      setResult(data.predicted_role || "Prediction failed");
    } catch (err) {
      setResult("API Error: Backend offline");
    } finally {
      setLoading(false);
    }
  }

  return (
    <div className="text-center mt-10">
      <button
        onClick={handlePredict}
        disabled={loading}
        className={`px-6 py-3 bg-black text-white rounded-lg text-lg transition-all ${
          loading ? "opacity-50 cursor-not-allowed" : "hover:bg-gray-800"
        }`}
      >
        {loading ? "Predicting..." : "Predict Career"}
      </button>
      <div className="mt-6 p-4 bg-gray-100 rounded-lg inline-block min-w-[200px]">
        <h3 className="text-sm uppercase tracking-wider text-gray-500">Result</h3>
        <p className="text-2xl font-bold text-blue-600">
          {result || "Waiting for input..."}
        </p>
      </div>
    </div>
  );
}
