import React from 'react';
import { useNavigate } from 'react-router-dom';

export default function AegisHeader() {
  const navigate = useNavigate();

  return (
    <header className="w-full bg-white border-b border-slate-200/90 sticky top-0 z-50 shadow-sm">
      <div className="w-full px-6 lg:px-12 py-3 flex items-center justify-between gap-4">
        
        {/* Left Section: Shield Logo + Title + Tagline */}
        <div className="flex items-center gap-5 sm:gap-7">
          <div 
            onClick={() => navigate('/')} 
            className="flex items-center gap-3.5 group select-none cursor-pointer"
          >
            {/* Shield Icon Container with AI Neural Node Styling */}
            <div className="relative w-11 h-12 rounded-xl bg-gradient-to-b from-[#0e2a47] to-[#08182b] flex items-center justify-center shadow-md shadow-sky-950/20 group-hover:scale-105 transition-transform duration-300 ring-1 ring-sky-500/30">
              <svg
                className="w-7 h-7 text-sky-400 group-hover:text-teal-300 transition-colors duration-300"
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

            {/* Brand Text */}
            <div className="flex items-baseline tracking-tight font-extrabold text-2xl sm:text-[1.65rem] text-[#0d2137]">
              <span>AegisLend</span>
              <span className="ml-1.5 text-teal-600 font-black tracking-normal">AI</span>
            </div>
          </div>

          {/* Divider */}
          <div className="hidden md:block h-7 w-[1.5px] bg-slate-200" />

          {/* Subtitle / Tagline */}
          <p className="hidden md:inline-block text-sm lg:text-[0.95rem] font-medium text-slate-600 tracking-normal">
            An Intelligent and Secure Digital Lending Ecosystem
          </p>
        </div>

        {/* Right Section: Status Indicator & Professional Button */}
        <div className="flex items-center gap-6 lg:gap-8">
          {/* Live Secure Connection Indicator */}
          <div className="hidden sm:flex items-center gap-2.5">
            <span className="relative flex h-2.5 w-2.5">
              <span className="animate-ping absolute inline-flex h-full w-full rounded-full bg-teal-400 opacity-75" />
              <span className="relative inline-flex rounded-full h-2.5 w-2.5 bg-teal-500 shadow-sm shadow-teal-500/50" />
            </span>
            <span className="text-xs font-bold uppercase tracking-wider text-slate-600">
              Secure Account Login
            </span>
          </div>

          {/* Login Button with Subtext */}
          <div className="flex flex-col items-center">
            <button
              type="button"
              onClick={() => navigate('/login')}
              className="group relative flex items-center justify-center gap-2.5 px-7 py-2 rounded-lg border-2 border-teal-600 bg-white hover:bg-teal-600 text-teal-700 hover:text-white font-bold text-xs uppercase tracking-wider shadow-sm transition-all duration-200 active:scale-95 cursor-pointer"
            >
              <svg
                className="w-4 h-4 text-teal-600 group-hover:text-white transition-colors duration-200"
                viewBox="0 0 24 24"
                fill="none"
                stroke="currentColor"
                strokeWidth="2.2"
                strokeLinecap="round"
                strokeLinejoin="round"
              >
                <rect x="3" y="11" width="18" height="11" rx="2" ry="2" />
                <path d="M7 11V7a5 5 0 0 1 10 0v4" />
              </svg>
              <span>Login</span>
            </button>

            <span className="text-[10px] font-medium text-slate-500 tracking-tight mt-1 select-none">
              Existing Bank Customers Only
            </span>
          </div>
        </div>

      </div>
    </header>
  );
}