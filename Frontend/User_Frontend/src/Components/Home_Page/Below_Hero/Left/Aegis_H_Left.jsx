import React, { useState, useEffect } from 'react';
import agentVideo from '../../../../assets/Jai.webm';

const loanProducts = [
  {
    id: 'personal',
    title: 'Personal Loan',
    rate: 'Starting @ 10.49% p.a.',
    maxAmount: 'Up to ₹40 Lakhs',
    tenure: 'Flexible 12–72 Months',
    badge: 'Instant Disbursal',
    accentColor: 'text-sky-600',
    hoverBorder: 'hover:border-sky-400',
    accentBg: 'bg-sky-50',
    buttonColor: 'bg-sky-600 hover:bg-sky-700',
    icon: (
      <svg className="w-5 h-5 text-sky-600" fill="none" viewBox="0 0 24 24" stroke="currentColor">
        <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M17 9V7a2 2 0 00-2-2H5a2 2 0 00-2 2v6a2 2 0 002 2h2m2 4h10a2 2 0 002-2v-6a2 2 0 00-2-2H9a2 2 0 00-2 2v6a2 2 0 002 2zm7-5a2 2 0 11-4 0 2 2 0 014 0z" />
      </svg>
    )
  },
  {
    id: 'home',
    title: 'Home Loan',
    rate: 'Starting @ 8.40% p.a.',
    maxAmount: 'Up to ₹5 Crores',
    tenure: 'Up to 30 Years',
    badge: 'Lowest EMI',
    accentColor: 'text-teal-600',
    hoverBorder: 'hover:border-teal-400',
    accentBg: 'bg-teal-50',
    buttonColor: 'bg-teal-600 hover:bg-teal-700',
    icon: (
      <svg className="w-5 h-5 text-teal-600" fill="none" viewBox="0 0 24 24" stroke="currentColor">
        <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M3 12l2-2m0 0l7-7 7 7M5 10v10a1 1 0 001 1h3m10-11l2 2m-2-2v10a1 1 0 01-1 1h-3m-6 0a1 1 0 001-1v-4a1 1 0 011-1h2a1 1 0 011 1v4a1 1 0 001 1m-6 0h6" />
      </svg>
    )
  },
  {
    id: 'education',
    title: 'Education Loan',
    rate: 'Starting @ 9.15% p.a.',
    maxAmount: 'Up to ₹1.5 Crores',
    tenure: 'Moratorium + 15 Yrs',
    badge: '100% Financing',
    accentColor: 'text-emerald-600',
    hoverBorder: 'hover:border-emerald-400',
    accentBg: 'bg-emerald-50',
    buttonColor: 'bg-emerald-600 hover:bg-emerald-700',
    icon: (
      <svg className="w-5 h-5 text-emerald-600" fill="none" viewBox="0 0 24 24" stroke="currentColor">
        <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M12 14l9-5-9-5-9 5 9 5zm0 0l6.16-3.422a12.083 12.083 0 01.665 6.479A11.952 11.952 0 0012 20.055a11.952 11.952 0 00-6.824-2.998 12.078 12.078 0 01.665-6.479L12 14zm-4 6v-7.5" />
      </svg>
    )
  },
  {
    id: 'business',
    title: 'Business Loan',
    rate: 'Starting @ 11.25% p.a.',
    maxAmount: 'Up to ₹75 Lakhs',
    tenure: 'Collateral Free',
    badge: 'Fast-Track Capital',
    accentColor: 'text-indigo-600',
    hoverBorder: 'hover:border-indigo-400',
    accentBg: 'bg-indigo-50',
    buttonColor: 'bg-indigo-600 hover:bg-indigo-700',
    icon: (
      <svg className="w-5 h-5 text-indigo-600" fill="none" viewBox="0 0 24 24" stroke="currentColor">
        <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M21 13.255A23.931 23.931 0 0112 15c-3.183 0-6.22-.62-9-1.745M16 6V4a2 2 0 00-2-2h-4a2 2 0 00-2 2v2m4 6h.01M5 20h14a2 2 0 002-2V8a2 2 0 00-2-2H5a2 2 0 00-2 2v10a2 2 0 002 2z" />
      </svg>
    )
  },
  {
    id: 'vehicle',
    title: 'Vehicle Loan',
    rate: 'Starting @ 8.75% p.a.',
    maxAmount: '100% On-Road Funding',
    tenure: 'Up to 84 Months',
    badge: 'Pre-Approved',
    accentColor: 'text-cyan-600',
    hoverBorder: 'hover:border-cyan-400',
    accentBg: 'bg-cyan-50',
    buttonColor: 'bg-cyan-600 hover:bg-cyan-700',
    icon: (
      <svg className="w-5 h-5 text-cyan-600" fill="none" viewBox="0 0 24 24" stroke="currentColor">
        <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M8 17h.01M16 17h.01M5 11l2-5h10l2 5m-14 0h14m-14 0v5a1 1 0 001 1h1m12-6v5a1 1 0 01-1 1h-1m-10 0h8" />
      </svg>
    )
  },
  {
    id: 'gold',
    title: 'Gold Loan',
    rate: 'Starting @ 8.90% p.a.',
    maxAmount: 'Instant Cash/Transfer',
    tenure: 'Same-Day Vault Release',
    badge: 'Zero Processing Fee',
    accentColor: 'text-amber-600',
    hoverBorder: 'hover:border-amber-400',
    accentBg: 'bg-amber-50',
    buttonColor: 'bg-amber-600 hover:bg-amber-700',
    icon: (
      <svg className="w-5 h-5 text-amber-600" fill="none" viewBox="0 0 24 24" stroke="currentColor">
        <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M12 8c-1.657 0-3 .895-3 2s1.343 2 3 2 3 .895 3 2-1.343 2-3 2m0-8c1.11 0 2.08.402 2.599 1M12 8V7m0 1v8m0 0v1m0-1c-1.11 0-2.08-.402-2.599-1M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
      </svg>
    )
  }
];

export default function Aegis_H_Left() {
  const [activeSlide, setActiveSlide] = useState(0);
  const [isPaused, setIsPaused] = useState(false);
  const totalSlides = Math.ceil(loanProducts.length / 2);

  useEffect(() => {
    if (isPaused) return;
    const interval = setInterval(() => {
      setActiveSlide((prev) => (prev + 1) % totalSlides);
    }, 4500);
    return () => clearInterval(interval);
  }, [isPaused, totalSlides]);

  return (
    <div className="w-full bg-white p-6 sm:p-8 rounded-2xl border border-slate-200/90 shadow-sm flex flex-col justify-between">
      {/* 50/50 Grid Layout */}
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-8 items-stretch">
        
        {/* Left 50%: Standalone AI Banking Concierge Card */}
        <div className="flex flex-col justify-between bg-slate-50/70 border border-slate-200/90 rounded-2xl p-6 relative overflow-hidden">
          <div>
            <div className="flex items-center gap-2 mb-2.5">
              <span className="relative flex h-2.5 w-2.5">
                <span className="animate-ping absolute inline-flex h-full w-full rounded-full bg-teal-400 opacity-75" />
                <span className="relative inline-flex rounded-full h-2.5 w-2.5 bg-teal-600" />
              </span>
              <span className="text-[11px] font-bold text-teal-700 tracking-wider uppercase">
                AI Digital Lending Concierge
              </span>
            </div>

            <h2 className="text-2xl sm:text-[1.75rem] font-extrabold text-[#0d2137] tracking-tight leading-tight">
              Your Intelligent Lending Partner
            </h2>

            <p className="mt-2 text-xs sm:text-sm text-slate-600 leading-relaxed">
              Agentic AI continuously evaluates your financial profile against active bank criteria to issue real-time eligibility with zero friction.
            </p>
          </div>

          {/* Large Video & Chat Interaction Box */}
          <div className="mt-6 bg-white border border-slate-200/90 rounded-xl p-5 shadow-xs flex flex-col sm:flex-row items-center gap-5">
            {/* Expanded Jai Avatar Viewport */}
            <div className="relative w-44 h-44 sm:w-52 sm:h-52 flex-shrink-0 rounded-xl overflow-hidden bg-slate-950 border border-slate-300 shadow-md">
              <video
                autoPlay
                loop
                muted
                playsInline
                preload="auto"
                className="w-full h-full object-cover object-center pointer-events-none"
              >
                <source src={agentVideo} type="video/webm" />
              </video>
              <div className="absolute top-2 left-2 flex items-center gap-1.5 px-2 py-0.5 rounded-full bg-black/65 backdrop-blur-sm border border-white/15 text-[9px] font-bold text-emerald-400">
                <span className="w-1.5 h-1.5 rounded-full bg-emerald-400 animate-pulse" />
                LIVE AGENT
              </div>
            </div>

            {/* Structured Dialog & Actions */}
            <div className="flex-1 flex flex-col justify-between self-stretch space-y-3.5">
              <div className="p-3.5 rounded-xl bg-slate-50 border border-slate-200/80">
                <div className="flex items-center justify-between mb-1.5">
                  <span className="text-xs font-bold text-slate-900">Jai — Banking Officer</span>
                  <span className="text-[10px] font-bold text-teal-700 bg-teal-50 border border-teal-200 px-1.5 py-0.5 rounded">
                    Verified
                  </span>
                </div>
                <p className="text-xs text-slate-600 font-medium leading-relaxed">
                  "Ready to inspect pre-approved limits, custom tenures, and interest structures for your portfolio."
                </p>
              </div>

              <div className="flex flex-col gap-2">
                <button
                  type="button"
                  className="w-full inline-flex items-center justify-center gap-2 px-5 py-2.5 rounded-xl bg-[#0e3b64] hover:bg-[#082845] text-white text-xs font-bold shadow-sm transition-all duration-150 active:scale-95 cursor-pointer"
                >
                  <svg className="w-4 h-4" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2.2" d="M8 12h.01M12 12h.01M16 12h.01M21 12c0 4.418-4.03 8-9 8a9.863 9.863 0 01-4.255-.949L3 20l1.395-3.72C3.512 15.042 3 13.574 3 12c0-4.418 4.03-8 9-8s9 3.582 9 8z" />
                  </svg>
                  Start Chat Session
                </button>
                <span className="text-[10px] text-slate-400 font-medium text-center">
                  Instant response • Bank-grade encrypted
                </span>
              </div>
            </div>
          </div>
        </div>

        {/* Right 50%: Standalone Loan Products & Interactive Slider */}
        <div 
          className="flex flex-col justify-between bg-slate-50/70 border border-slate-200/90 rounded-2xl p-6"
          onMouseEnter={() => setIsPaused(true)}
          onMouseLeave={() => setIsPaused(false)}
        >
          <div>
            <div className="flex items-center justify-between mb-4">
              <div>
                <h3 className="text-xl sm:text-2xl font-extrabold text-[#0d2137] tracking-tight">
                  Our Loan Products
                </h3>
                <p className="text-xs text-slate-500">
                  Select a product to view verified eligibility and terms
                </p>
              </div>

              {/* Slider Controls */}
              <div className="flex items-center gap-2">
                <button
                  type="button"
                  onClick={() => setActiveSlide((prev) => (prev === 0 ? totalSlides - 1 : prev - 1))}
                  className="w-8 h-8 rounded-full border border-slate-300 bg-white hover:bg-slate-100 flex items-center justify-center text-slate-700 font-bold transition-colors cursor-pointer shadow-xs"
                  aria-label="Previous Slide"
                >
                  ‹
                </button>
                <div className="flex items-center gap-1.5 px-1">
                  {Array.from({ length: totalSlides }).map((_, idx) => (
                    <button
                      key={idx}
                      onClick={() => setActiveSlide(idx)}
                      className={`h-1.5 rounded-full transition-all duration-300 ${
                        activeSlide === idx ? 'w-5 bg-teal-600' : 'w-1.5 bg-slate-300'
                      }`}
                      aria-label={`Go to slide ${idx + 1}`}
                    />
                  ))}
                </div>
                <button
                  type="button"
                  onClick={() => setActiveSlide((prev) => (prev + 1) % totalSlides)}
                  className="w-8 h-8 rounded-full border border-slate-300 bg-white hover:bg-slate-100 flex items-center justify-center text-slate-700 font-bold transition-colors cursor-pointer shadow-xs"
                  aria-label="Next Slide"
                >
                  ›
                </button>
              </div>
            </div>

            {/* Slider Container */}
            <div className="overflow-hidden mt-4">
              <div 
                className="flex transition-transform duration-500 ease-out"
                style={{ transform: `translateX(-${activeSlide * 100}%)` }}
              >
                {Array.from({ length: totalSlides }).map((_, slideIndex) => {
                  const slideItems = loanProducts.slice(slideIndex * 2, slideIndex * 2 + 2);
                  return (
                    <div key={slideIndex} className="w-full flex-shrink-0 grid grid-cols-1 sm:grid-cols-2 gap-4 px-0.5">
                      {slideItems.map((loan) => (
                        <div
                          key={loan.id}
                          className={`group relative bg-white border border-slate-200/90 rounded-2xl p-5 shadow-xs transition-all duration-300 ${loan.hoverBorder} hover:shadow-lg hover:-translate-y-1 flex flex-col justify-between`}
                        >
                          <div>
                            <div className="flex items-center justify-between gap-2 mb-3">
                              <div className={`w-10 h-10 rounded-xl ${loan.accentBg} flex items-center justify-center`}>
                                {loan.icon}
                              </div>
                              <span className="text-[10px] font-bold px-2 py-0.5 rounded-full bg-slate-100 text-slate-600 group-hover:bg-teal-50 group-hover:text-teal-700 transition-colors">
                                {loan.badge}
                              </span>
                            </div>

                            <h4 className="text-base font-bold text-slate-900 group-hover:text-teal-700 transition-colors">
                              {loan.title}
                            </h4>

                            <div className="mt-3 space-y-1.5 border-t border-slate-100 pt-3 text-xs">
                              <div className="flex justify-between items-center">
                                <span className="text-slate-500 font-medium">Interest Rate</span>
                                <span className={`font-bold ${loan.accentColor}`}>{loan.rate}</span>
                              </div>
                              <div className="flex justify-between items-center">
                                <span className="text-slate-500 font-medium">Maximum Limit</span>
                                <span className="font-semibold text-slate-800">{loan.maxAmount}</span>
                              </div>
                              <div className="flex justify-between items-center">
                                <span className="text-slate-500 font-medium">Tenure Period</span>
                                <span className="font-semibold text-slate-800">{loan.tenure}</span>
                              </div>
                            </div>
                          </div>

                          <button
                            type="button"
                            className={`mt-5 w-full py-2.5 rounded-xl ${loan.buttonColor} text-white text-xs font-bold tracking-wide shadow-xs transition-all duration-150 active:scale-95 cursor-pointer`}
                          >
                            Check Eligibility
                          </button>
                        </div>
                      ))}
                    </div>
                  );
                })}
              </div>
            </div>
          </div>
        </div>

      </div>

      {/* Embedded 4-Step Process Indicator */}
      <div className="mt-8 pt-6 border-t border-slate-100">
        <h4 className="text-xs font-bold text-slate-500 uppercase tracking-widest mb-6 text-center">
          How It Works
        </h4>

        <div className="relative flex items-center justify-between max-w-3xl mx-auto px-4 sm:px-8">
          <div className="absolute top-4 left-10 right-10 h-[2px] bg-slate-200 z-0" />

          {[
            { step: '1', title: 'Authenticate' },
            { step: '2', title: 'Get Recommendations' },
            { step: '3', title: 'Apply Securely' },
            { step: '4', title: 'Quick Decision' }
          ].map((item, idx) => (
            <div key={idx} className="flex flex-col items-center gap-2 z-10 relative">
              <div className="w-8 h-8 rounded-full bg-white border-2 border-teal-600 text-teal-700 flex items-center justify-center text-xs font-bold shadow-xs">
                ✓
              </div>
              <span className="text-[11px] sm:text-xs font-semibold text-slate-700 text-center whitespace-nowrap">
                {item.step}. {item.title}
              </span>
            </div>
          ))}
        </div>
      </div>
    </div>
  );
}