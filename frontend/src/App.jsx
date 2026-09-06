import React from "react";
import { BrowserRouter as Router, Routes, Route, Navigate } from "react-router-dom";
import Navbar from "./components/Navbar";
import LiveQAPage from "./pages/LiveQAPage";

export default function App() {
  return (
    <Router>
      <div className="min-h-screen bg-slate-50 text-slate-900 flex flex-col font-sans">
        <Navbar />
        <main className="max-w-7xl w-full mx-auto p-8 flex-1">
          <Routes>
            <Route path="/" element={<LiveQAPage />} />
            <Route path="*" element={<Navigate to="/" replace />} />
          </Routes>
        </main>
        <footer className="text-center py-6 text-slate-400 text-xs border-t border-slate-200 bg-white">
          Automated QA Service — Powered by Local LLM Inference
        </footer>
      </div>
    </Router>
  );
}

