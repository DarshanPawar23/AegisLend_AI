import React from 'react';

export default function Aegis_H_Right() {
  return (
    <div className="w-full bg-white p-6 lg:p-8 rounded-2xl border border-slate-200/80 shadow-sm flex flex-col justify-between">
      <div>
        <h2 className="text-xl sm:text-2xl font-bold text-slate-900 tracking-tight text-center mb-6">
          Why Choose AegisLend AI?
        </h2>

        {/* 3 Core Tech Pillars */}
        <div className="grid grid-cols-1 sm:grid-cols-3 gap-6 text-center">
          
          {/* Pillar 1 */}
          <div className="flex flex-col items-center">
            <div className="w-16 h-16 rounded-2xl bg-teal-50/80 border border-teal-100 flex items-center justify-center mb-3">
              <svg className="w-8 h-8 text-teal-600" viewBox="0 0 24 24" fill="none" stroke="currentColor">
                <rect x="4" y="4" width="16" height="16" rx="3" strokeWidth="1.8" />
                <circle cx="9" cy="10" r="1.5" fill="currentColor" />
                <circle cx="15" cy="10" r="1.5" fill="currentColor" />
                <path d="M9 15c1 1 3 1 4 0" strokeWidth="1.8" strokeLinecap="round" />
              </svg>
            </div>
            <h3 className="text-xs sm:text-sm font-bold text-slate-800 leading-tight">
              AI-Powered Personalization
            </h3>
            <p className="mt-1.5 text-[11px] text-slate-500 leading-normal">
              Continuous agentic profiling evaluates real credit readiness for accurate terms.
            </p>
          </div>

          {/* Pillar 2 */}
          <div className="flex flex-col items-center">
            <div className="w-16 h-16 rounded-2xl bg-sky-50/80 border border-sky-100 flex items-center justify-center mb-3">
              <svg className="w-8 h-8 text-[#0e3b64]" viewBox="0 0 24 24" fill="none" stroke="currentColor">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="1.8" d="M12 11c0 3.517-1.009 6.799-2.753 9.571m-3.44-2.04l.054-.09A13.916 13.916 0 008 11a4 4 0 118 0c0 1.017-.07 2.019-.203 3m-2.118 6.844A21.88 21.88 0 0015.171 17m3.839 1.132c.645-2.266.99-4.659.99-7.132A8 8 0 004 11a7.978 7.978 0 001.408 4.5" />
              </svg>
            </div>
            <h3 className="text-xs sm:text-sm font-bold text-slate-800 leading-tight">
              Secure & Risk-Aware Authentication
            </h3>
            <p className="mt-1.5 text-[11px] text-slate-500 leading-normal">
              Multi-modal zero-trust protocols secure your identity and verified bank accounts.
            </p>
          </div>

          {/* Pillar 3 */}
          <div className="flex flex-col items-center">
            <div className="w-16 h-16 rounded-2xl bg-emerald-50/80 border border-emerald-100 flex items-center justify-center mb-3">
              <svg className="w-8 h-8 text-emerald-600" viewBox="0 0 24 24" fill="none" stroke="currentColor">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="1.8" d="M9 12l2 2 4-4m5.618-4.016A11.955 11.955 0 0112 2.944a11.955 11.955 0 01-8.618 3.04A12.02 12.02 0 003 9c0 5.591 3.824 10.29 9 11.622 5.176-1.332 9-6.03 9-11.622 0-1.042-.133-2.052-.382-3.016z" />
              </svg>
            </div>
            <h3 className="text-xs sm:text-sm font-bold text-slate-800 leading-tight">
              Continuous Session Protection
            </h3>
            <p className="mt-1.5 text-[11px] text-slate-500 leading-normal">
              Behavioral telemetry and active monitoring shield every phase of loan settlement.
            </p>
          </div>

        </div>
      </div>

      {/* Bottom Legal & Bank Security Badge */}
      <div className="mt-8 pt-5 border-t border-slate-100 flex flex-wrap items-center justify-between gap-3 text-[11px] text-slate-500">
        <div className="flex items-center gap-4">
          <a href="#" className="hover:text-slate-900 transition-colors">About Us</a>
          <a href="#" className="hover:text-slate-900 transition-colors">Contact Support</a>
          <a href="#" className="hover:text-slate-900 transition-colors">Privacy Policy</a>
          <a href="#" className="hover:text-slate-900 transition-colors">Terms of Use</a>
        </div>

        <div className="inline-flex items-center gap-2 px-3 py-1 rounded-md bg-emerald-50 border border-emerald-200 text-emerald-800 font-semibold text-[10px]">
          <span className="w-2 h-2 rounded-full bg-emerald-500 animate-pulse" />
          Secured by Hybrid IDS & Behavioral ML
        </div>
      </div>
    </div>
  );
}