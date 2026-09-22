import React from 'react';
import { useNavigate } from 'react-router-dom';

export default function LoginHeader() {
  const navigate = useNavigate();

  return (
    <header className="w-full bg-white border-b border-slate-200 sticky top-0 z-50 shadow-xs select-none">
      <div className="w-full px-6 lg:px-12 py-3 flex items-center justify-between gap-4">
        
        {/* Left Section: Back Button + Logo + Title + Tagline */}
        <div className="flex items-center gap-3 sm:gap-5">
          {/* Back Navigation Button to Home "/" */}
          <button
            type="button"
            onClick={() => navigate('/')}
            className="flex items-center justify-center w-9 h-9 rounded-lg border border-slate-200 bg-slate-50 hover:bg-slate-100 hover:border-slate-300 text-slate-600 hover:text-[#0d2137] transition-all duration-200 cursor-pointer shadow-xs active:scale-95"
            title="Back to Home"
            aria-label="Back to Home"
          >
            <svg
              className="w-5 h-5"
              viewBox="0 0 24 24"
              fill="none"
              stroke="currentColor"
              strokeWidth="2.2"
              strokeLinecap="round"
              strokeLinejoin="round"
            >
              <path d="M19 12H5M12 19l-7-7 7-7" />
            </svg>
          </button>

          {/* Brand Logo & Name */}
          <div 
            onClick={() => navigate('/')} 
            className="flex items-center gap-3 group cursor-pointer"
          >
            {/* Shield Logo with Brain/Node Silhouette */}
            <div className="relative w-10 h-11 rounded-xl bg-[#0e2a47] flex items-center justify-center shadow-md shadow-sky-950/20 group-hover:scale-105 transition-transform duration-300 ring-1 ring-sky-500/30">
              <svg
                className="w-6 h-6 text-sky-400 group-hover:text-teal-300 transition-colors duration-300"
                viewBox="0 0 24 24"
                fill="none"
                stroke="currentColor"
                strokeWidth="1.8"
                strokeLinecap="round"
                strokeLinejoin="round"
              >
                <path d="M12 22s8-4 8-10V5l-8-3-8 3v7c0 6 8 10 8 10z" fill="rgba(14, 165, 233, 0.12)" />
                <circle cx="12" cy="11" r="2.5" fill="currentColor" />
                <path d="M12 8.5V6" strokeWidth="1.5" />
                <path d="M12 16v-2.5" strokeWidth="1.5" />
                <path d="M8.5 11H6" strokeWidth="1.5" />
                <path d="M18 11h-2.5" strokeWidth="1.5" />
              </svg>
            </div>

            {/* Brand Title */}
            <div className="flex items-baseline tracking-tight font-extrabold text-2xl text-[#0d2137]">
              <span>AegisLend</span>
              <span className="ml-1 text-teal-600 font-black">AI</span>
            </div>
          </div>

          {/* Divider */}
          <div className="hidden md:block h-6 w-[1px] bg-slate-200 ml-2" />

          {/* Subtitle / Tagline */}
          <p className="hidden md:inline-block text-sm font-medium text-slate-600">
            An Intelligent and Secure Digital Lending Ecosystem
          </p>
        </div>

        {/* Right Section: Compact Secure Lock Indicator */}
        <div className="flex flex-col items-end">
          <div className="flex items-center gap-1.5 text-[#0d2137]">
            <svg
              className="w-3.5 h-3.5 text-teal-600"
              viewBox="0 0 24 24"
              fill="currentColor"
            >
              <path fillRule="evenodd" d="M12 1.5a5.25 5.25 0 00-5.25 5.25v3a3 3 0 00-3 3v6.75a3 3 0 003 3h10.5a3 3 0 003-3v-6.75a3 3 0 00-3-3v-3c0-2.9-2.35-5.25-5.25-5.25zm3.75 8.25v-3a3.75 3.75 0 10-7.5 0v3h7.5z" clipRule="evenodd" />
            </svg>
            <span className="text-xs font-semibold tracking-tight text-slate-800">
              Secure Account Login
            </span>
          </div>
          <span className="text-[10px] font-medium text-slate-400 tracking-tight select-none">
            Existing Bank Customers Only
          </span>
        </div>

      </div>
    </header>
  );
}