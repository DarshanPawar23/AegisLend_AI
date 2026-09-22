import React from 'react';

function Login_Animation() {
  return (
    <div className="flex flex-col items-center justify-center p-6 text-center select-none animate-fade-in">
      {/* Dynamic Security Verification Scanner */}
      <div className="relative w-20 h-20 mb-5 flex items-center justify-center">
        <span className="absolute inset-0 rounded-full border-2 border-teal-500/20 animate-ping duration-1000" />
        <span className="absolute inset-1 rounded-full border-2 border-t-teal-600 border-r-transparent border-b-sky-700 border-l-transparent animate-spin" />
        
        <div className="w-12 h-12 rounded-xl bg-slate-900 flex items-center justify-center shadow-lg shadow-teal-900/30">
          <svg className="w-6 h-6 text-teal-400" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
            <path d="M12 22s8-4 8-10V5l-8-3-8 3v7c0 6 8 10 8 10z" fill="rgba(13,148,136,0.15)" />
            <path d="M9 12l2 2 4-4" strokeLinecap="round" strokeLinejoin="round" />
          </svg>
        </div>
      </div>

      <h3 className="text-base font-bold text-slate-800 tracking-tight">Authenticating Session</h3>
      <p className="text-xs text-slate-500 font-medium mt-1">Verifying MPIN & Hybrid ML Behavior Profile...</p>
      
      {/* Bank Progress Pill */}
      <div className="w-36 h-1.5 bg-slate-100 rounded-full overflow-hidden mt-4">
        <div className="h-full bg-gradient-to-r from-teal-500 to-sky-600 rounded-full animate-pulse w-3/4" />
      </div>
    </div>
  );
}

export default Login_Animation;