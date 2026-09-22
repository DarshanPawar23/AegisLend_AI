import React from 'react';

function Login_Footer() {
  return (
    <footer className="w-full bg-[#0d2137] text-slate-300 select-none">
      {/* Top Bar: Navigation Links & Security Guarantee */}
      <div className="w-full px-6 lg:px-12 py-3.5 flex flex-col md:flex-row items-center justify-between gap-3 border-b border-slate-700/60 text-xs sm:text-[13px] font-medium tracking-wide">
        
        {/* Nav Links */}
        <div className="flex flex-wrap items-center justify-center gap-6 sm:gap-9 text-slate-300">
          <a href="#about" className="hover:text-white transition-colors duration-200">
            About Us
          </a>
          <a href="#support" className="hover:text-white transition-colors duration-200">
            Contact Support
          </a>
          <a href="#privacy" className="hover:text-white transition-colors duration-200">
            Privacy Policy
          </a>
          <a href="#terms" className="hover:text-white transition-colors duration-200">
            Terms of Use
          </a>
        </div>

        {/* Right Label */}
        <div className="flex items-center gap-1.5 text-slate-200">
          <a href="#security" className="hover:text-teal-300 transition-colors duration-200 font-medium">
            Security Guarantee
          </a>
        </div>
      </div>

      {/* Bottom Bar: Copyright & Compliance Trust Badge */}
      <div className="w-full px-6 lg:px-12 py-2.5 flex flex-col sm:flex-row items-center justify-between gap-2.5 text-[11px] sm:text-xs text-slate-400">
        
        {/* Dynamic / Exact Copyright */}
        <p className="font-normal text-center sm:text-left">
          &copy; {new Date().getFullYear()} AegisLend AI Ecosystem. All rights reserved.
        </p>

        {/* Bank-Grade Security Certification Pill */}
        <div className="inline-flex items-center gap-2 bg-white/95 px-2.5 py-1 rounded border border-slate-200 shadow-xs">
          {/* Shield Checkmark Icon */}
          <svg
            className="w-3.5 h-3.5 text-emerald-600"
            viewBox="0 0 24 24"
            fill="currentColor"
          >
            <path
              fillRule="evenodd"
              d="M12.516 2.17a.75.75 0 00-1.032 0 11.209 11.209 0 01-7.877 3.08.75.75 0 00-.722.515A12.74 12.74 0 002.25 9.75c0 5.942 4.064 10.933 9.563 12.348a.749.749 0 00.374 0c5.499-1.415 9.563-6.406 9.563-12.348 0-1.39-.223-2.73-.635-3.985a.75.75 0 00-.722-.516l-.143.001c-2.996 0-5.717-1.17-7.734-3.08zm3.094 8.016a.75.75 0 10-1.22-.872l-3.236 4.53L9.53 12.22a.75.75 0 00-1.06 1.06l2.25 2.25a.75.75 0 001.14-.094l3.75-5.25z"
              clipRule="evenodd"
            />
          </svg>

          {/* Secured Text */}
          <div className="flex flex-col text-left leading-none">
            <span className="text-[7.5px] font-bold tracking-tight text-slate-500 uppercase">
              Secured by
            </span>
            <span className="text-[8.5px] font-black tracking-tight text-slate-800">
              Hybrid IDS & Behavioral ML
            </span>
          </div>
        </div>

      </div>
    </footer>
  );
}

export default Login_Footer;
