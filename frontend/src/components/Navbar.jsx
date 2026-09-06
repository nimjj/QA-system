import React from "react";
import { Sparkles } from "lucide-react";

export default function Navbar() {
  return (
    <header className="border-b border-slate-200 bg-white sticky top-0 z-40 px-8 py-3.5 flex flex-wrap justify-between items-center gap-4 shadow-sm">
      <div className="flex items-center gap-3">
        <div className="w-9 h-9 rounded-lg bg-slate-900 text-white flex items-center justify-center font-bold text-base shadow">
          QA
        </div>
        <div>
          <h1 className="font-bold text-base text-slate-900 leading-tight flex items-center gap-2">
            Automated QA Intelligence
            <span className="text-[11px] font-semibold px-2 py-0.5 rounded-full bg-slate-100 text-slate-700 border border-slate-200">
              Stateless Architecture
            </span>
          </h1>
          <p className="text-xs text-slate-500">Local LLM Scorecard Evaluation</p>
        </div>
      </div>
      <nav className="flex items-center gap-1 bg-slate-100 p-1 rounded-lg border border-slate-200">
        <div className="flex items-center gap-1.5 px-3.5 py-1.5 rounded-md text-xs font-semibold bg-white text-slate-900 shadow-sm border border-slate-200/80">
          <Sparkles size={13} /> Live QA Test
        </div>
      </nav>
    </header>
  );
}
