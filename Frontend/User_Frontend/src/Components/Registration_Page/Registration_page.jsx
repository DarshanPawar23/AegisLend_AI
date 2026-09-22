import React, { useState, useEffect, useRef } from 'react';
import { useNavigate } from 'react-router-dom';
import Login_Header from '../Login_Page/Login_Header';
import Login_Footer from '../Login_Page/Login_Footer';

export default function Registration_Page() {
  const navigate = useNavigate();
  const videoRef = useRef(null);
  const otpInputsRef = useRef([]);
  const mpinInputsRef = useRef([]);
  const confirmMpinInputsRef = useRef([]);
  const API_URL = import.meta.env.VITE_API_URL;

  const [currentStep, setCurrentStep] = useState(1);
  const [loading, setLoading] = useState(false);
  const [errorMessage, setErrorMessage] = useState('');

  const [formData, setFormData] = useState({
    account_number: '',
    mobile_number: '',
    first_name: '',
    last_name: '',
    date_of_birth: ''
  });

  const [registrationId, setRegistrationId] = useState(null);
  const [otp, setOtp] = useState(['', '', '', '', '', '']);
  const [timer, setTimer] = useState(30);
  const [canResend, setCanResend] = useState(false);

  const [mpin, setMpin] = useState(['', '', '', '', '', '']);
  const [confirmMpin, setConfirmMpin] = useState(['', '', '', '', '', '']);
  const [showMpinDigits, setShowMpinDigits] = useState(false);

  useEffect(() => {
    if (videoRef.current) {
      videoRef.current.muted = true;
      videoRef.current.defaultMuted = true;
      videoRef.current.play().catch(() => {});
    }
  }, []);

  useEffect(() => {
    let interval = null;
    if (currentStep === 2 && timer > 0) {
      interval = setInterval(() => {
        setTimer((prev) => prev - 1);
      }, 1000);
    } else if (timer === 0) {
      setCanResend(true);
      clearInterval(interval);
    }
    return () => clearInterval(interval);
  }, [currentStep, timer]);

  const handleInputChange = (e) => {
    const { name, value } = e.target;
    setFormData((prev) => ({ ...prev, [name]: value }));
  };

  const handleVerifyAccount = async (e) => {
    e.preventDefault();
    setLoading(true);
    setErrorMessage('');

    try {
      const response = await fetch(
        `${API_URL}/api/user/registration/verify-account`,
        {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json'
          },
          body: JSON.stringify(formData)
        }
      );

      const data = await response.json();

      if (!response.ok || !data.success) {
        throw new Error(
          data.message || 'Account verification failed. Check your bank details.'
        );
      }

      setRegistrationId(data.registration_id);
      setCurrentStep(2);
      setTimer(30);
      setCanResend(false);
      setOtp(['', '', '', '', '', '']);
    } catch (err) {
      setErrorMessage(err.message || 'Unable to verify account details.');
    } finally {
      setLoading(false);
    }
  };

  const handleOtpChange = (index, value) => {
    if (!/^\d*$/.test(value)) return;
    const newOtp = [...otp];
    newOtp[index] = value.slice(-1);
    setOtp(newOtp);

    if (value && index < 5) {
      otpInputsRef.current[index + 1]?.focus();
    }
  };

  const handleOtpKeyDown = (index, e) => {
    if (e.key === 'Backspace' && !otp[index] && index > 0) {
      otpInputsRef.current[index - 1]?.focus();
    }
  };

  const handleVerifyOtp = async (e) => {
    e.preventDefault();
    const enteredOtp = otp.join('');
    if (enteredOtp.length !== 6) {
      setErrorMessage('Please enter a complete 6-digit OTP code.');
      return;
    }

    setLoading(true);
    setErrorMessage('');

    try {
      const response = await fetch(
        `${API_URL}/api/user/registration/verify-phone`,
        {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json'
          },
          body: JSON.stringify({
            registration_id: registrationId,
            otp: enteredOtp
          })
        }
      );

      const data = await response.json();

      if (!response.ok || !data.success) {
        throw new Error(data.message || 'Phone verification failed.');
      }
      setCurrentStep(3);
      setOtp(['', '', '', '', '', '']);
    } catch (err) {
      setErrorMessage(err.message || 'Invalid or expired OTP code.');
    } finally {
      setLoading(false);
    }
  };

  const handleResendOtp = async () => {
    if (!canResend || loading) return;
    setLoading(true);
    setErrorMessage('');

    try {
      const response = await fetch(
        `${API_URL}/api/user/registration/resend-otp`,
        {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json'
          },
          body: JSON.stringify({
            registration_id: registrationId
          })
        }
      );

      const data = await response.json();

      if (!response.ok || !data.success) {
        throw new Error(data.message || 'Failed to resend OTP.');
      }

      setOtp(['', '', '', '', '', '']);
      setTimer(30);
      setCanResend(false);
      otpInputsRef.current[0]?.focus();
    } catch (err) {
      setErrorMessage(err.message || 'Failed to resend OTP. Please try again shortly.');
    } finally {
      setLoading(false);
    }
  };

  const handleMpinChange = (index, value) => {
    if (!/^\d*$/.test(value)) return;
    const newMpin = [...mpin];
    newMpin[index] = value.slice(-1);
    setMpin(newMpin);

    if (value && index < 5) {
      mpinInputsRef.current[index + 1]?.focus();
    } else if (value && index === 5) {
      confirmMpinInputsRef.current[0]?.focus();
    }
  };

  const handleMpinKeyDown = (index, e) => {
    if (e.key === 'Backspace' && !mpin[index] && index > 0) {
      mpinInputsRef.current[index - 1]?.focus();
    }
  };

  const handleConfirmMpinChange = (index, value) => {
    if (!/^\d*$/.test(value)) return;
    const newConfirmMpin = [...confirmMpin];
    newConfirmMpin[index] = value.slice(-1);
    setConfirmMpin(newConfirmMpin);

    if (value && index < 5) {
      confirmMpinInputsRef.current[index + 1]?.focus();
    }
  };

  const handleConfirmMpinKeyDown = (index, e) => {
    if (e.key === 'Backspace' && !confirmMpin[index] && index > 0) {
      confirmMpinInputsRef.current[index - 1]?.focus();
    }
  };

  const handleSetupMpin = async (e) => {
    e.preventDefault();
    const primaryMpin = mpin.join('');
    const confirmedMpin = confirmMpin.join('');

    if (primaryMpin.length !== 6 || confirmedMpin.length !== 6) {
      setErrorMessage('Please enter and confirm all 6 digits of your MPIN.');
      return;
    }

    if (primaryMpin !== confirmedMpin) {
      setErrorMessage('MPIN and Confirm MPIN do not match. Please verify.');
      return;
    }

    setLoading(true);
    setErrorMessage('');

    try {
      const response = await fetch(
        `${API_URL}/api/user/registration/setup-mpin`,
        {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json'
          },
          body: JSON.stringify({
            registration_id: registrationId,
            mpin: primaryMpin,
            confirm_mpin: confirmedMpin
          })
        }
      );

      const data = await response.json();

      if (!response.ok || !data.success) {
        throw new Error(data.message || 'Failed to setup MPIN.');
      }

      setCurrentStep(4);
    } catch (err) {
      setErrorMessage(err.message || 'Error occurred while finalizing MPIN setup.');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="min-h-screen flex flex-col bg-[#f5f8fb] text-slate-900 select-none">
      <Login_Header />

      <main className="relative flex-1 flex items-center justify-center overflow-hidden py-10 px-4 sm:px-8">
        <div className="absolute inset-0 pointer-events-none z-0">
          <div className="absolute inset-0 bg-[#f7fafc]" />
          <div className="absolute top-0 inset-x-0 h-[450px] bg-gradient-to-b from-white via-[#f1f6fa] to-[#eaf3f7]" />
          <div className="absolute inset-0 opacity-[0.25] bg-[radial-gradient(#94a3b8_1px,transparent_1px)] [background-size:24px_24px]" />
          <div className="absolute -top-24 left-[5%] w-[480px] h-[480px] rounded-full bg-teal-200/20 blur-3xl" />
          <div className="absolute top-1/3 -right-24 w-[450px] h-[450px] rounded-full bg-sky-200/20 blur-3xl" />
        </div>

        <div className="relative z-10 w-full max-w-[1360px] mx-auto grid grid-cols-1 xl:grid-cols-12 gap-8 lg:gap-12 items-center my-auto">
          
          <div className="xl:col-span-7 flex flex-col">
            <div className="flex flex-wrap items-center gap-3 mb-4">
              <div className="inline-flex items-center gap-2 px-3.5 py-1.5 rounded-full bg-white border border-slate-200/90 shadow-2xs">
                <span className="w-2 h-2 rounded-full bg-teal-500" />
                <span className="text-[11px] font-extrabold uppercase tracking-wider text-slate-700">
                  New Account Setup
                </span>
              </div>
              <div className="inline-flex items-center gap-2 px-3.5 py-1.5 rounded-full bg-[#0b2942] text-white shadow-2xs">
                <span className="text-[11px] font-bold uppercase tracking-wider text-slate-100">
                  Safe • Secure • Simple
                </span>
              </div>
            </div>

            <div className="mb-5">
              <h1 className="text-3xl sm:text-4xl lg:text-5xl font-black leading-tight text-[#0d2137]">
                Start your journey with{' '}
                <span className="text-teal-600">AegisLend AI</span>
              </h1>
              <p className="mt-2 text-sm sm:text-base text-slate-600 max-w-[560px]">
                Verify your bank account, secure your identity, and get access to personalized lending solutions in just a few simple steps.
              </p>
            </div>

            <div className="relative w-full aspect-16/10 rounded-2xl overflow-hidden shadow-2xl shadow-slate-900/10 border border-slate-200/90 bg-white">
              <video
                ref={videoRef}
                src="/assets/Registration_vid.mp4"
                autoPlay
                loop
                muted
                playsInline
                className="w-full h-full object-cover object-center pointer-events-none"
              />
              <div className="absolute top-4 left-4 inline-flex items-center gap-2 px-3 py-1.5 rounded-xl bg-white/95 backdrop-blur-md border border-slate-200/80 shadow-md">
                <span className="w-2 h-2 rounded-full bg-emerald-500 animate-pulse" />
                <span className="text-[10px] font-black uppercase tracking-wider text-slate-800">
                  AI Agent Assisting
                </span>
              </div>
            </div>

            <div className="grid grid-cols-3 gap-3 mt-4">
              <div className="rounded-xl border border-slate-200/90 bg-white/95 px-3 py-2.5 shadow-2xs flex items-center gap-2.5">
                <div className="w-8 h-8 rounded-lg bg-teal-50 flex items-center justify-center shrink-0">
                  <svg className="w-4 h-4 text-teal-700" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
                    <path d="M12 22s8-4 8-10V5l-8-3-8 3v7c0 6 8 10 8 10z" />
                  </svg>
                </div>
                <div>
                  <p className="text-xs font-bold text-slate-800 leading-tight">Your Data is Protected</p>
                  <p className="text-[10px] text-slate-500 font-medium">Bank-grade security</p>
                </div>
              </div>

              <div className="rounded-xl border border-slate-200/90 bg-white/95 px-3 py-2.5 shadow-2xs flex items-center gap-2.5">
                <div className="w-8 h-8 rounded-lg bg-teal-50 flex items-center justify-center shrink-0">
                  <svg className="w-4 h-4 text-teal-700" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
                    <rect x="3" y="11" width="18" height="11" rx="2" ry="2" />
                    <path d="M7 11V7a5 5 0 0 1 10 0v4" />
                  </svg>
                </div>
                <div>
                  <p className="text-xs font-bold text-slate-800 leading-tight">Verified Customers Only</p>
                  <p className="text-[10px] text-slate-500 font-medium">Secure account linking</p>
                </div>
              </div>

              <div className="rounded-xl border border-slate-200/90 bg-white/95 px-3 py-2.5 shadow-2xs flex items-center gap-2.5">
                <div className="w-8 h-8 rounded-lg bg-teal-50 flex items-center justify-center shrink-0">
                  <svg className="w-4 h-4 text-teal-700" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
                    <polygon points="13 2 3 14 12 14 11 22 21 10 12 10 13 2" />
                  </svg>
                </div>
                <div>
                  <p className="text-xs font-bold text-slate-800 leading-tight">Fast & Hassle-Free</p>
                  <p className="text-[10px] text-slate-500 font-medium">Get started quickly</p>
                </div>
              </div>
            </div>
          </div>

          <div className="xl:col-span-5 flex justify-center xl:justify-end">
            <div className="w-full max-w-[480px] bg-white rounded-3xl border border-slate-200/90 shadow-2xl shadow-slate-300/50 p-8 sm:p-9 relative overflow-hidden">
              <div className="absolute top-0 inset-x-0 h-1.5 bg-gradient-to-r from-[#0b2942] via-teal-500 to-[#0b2942]" />

              <div className="flex flex-col items-center text-center mb-6">
                <div className="w-12 h-12 rounded-2xl bg-[#0b2942] flex items-center justify-center shadow-lg shadow-[#0b2942]/20 mb-2.5 ring-1 ring-teal-400/30">
                  <svg className="w-6 h-6 text-teal-300" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="1.8">
                    <path d="M12 22s8-4 8-10V5l-8-3-8 3v7c0 6 8 10 8 10z" fill="rgba(45,212,191,0.12)" />
                    <circle cx="12" cy="11" r="2.5" />
                  </svg>
                </div>
                <div className="flex items-baseline text-2xl font-black text-[#0d2137]">
                  <span>AegisLend</span>
                  <span className="ml-1 text-teal-600">AI</span>
                </div>
                <p className="text-xs font-semibold text-slate-500 mt-0.5">
                  Create Your Account
                </p>

                <div className="grid grid-cols-4 gap-2 w-full mt-5 text-center">
                  {[
                    { stepNum: 1, label: 'Account Verification' },
                    { stepNum: 2, label: 'Phone Verification' },
                    { stepNum: 3, label: 'Set MPIN' },
                    { stepNum: 4, label: 'Complete Registration' }
                  ].map((s) => (
                    <div key={s.stepNum} className="flex flex-col items-center">
                      <span className={`w-6 h-6 rounded-full flex items-center justify-center text-[10px] font-bold transition-all ${
                        currentStep >= s.stepNum ? 'bg-teal-600 text-white' : 'bg-slate-100 text-slate-400'
                      }`}>
                        {s.stepNum}
                      </span>
                      <span className={`text-[9.5px] font-bold mt-1 leading-tight ${
                        currentStep === s.stepNum ? 'text-slate-900 font-extrabold' : 'text-slate-400'
                      }`}>
                        {s.label}
                      </span>
                    </div>
                  ))}
                </div>
              </div>

              {errorMessage && (
                <div className="mb-4 p-3 rounded-xl bg-red-50 border border-red-200 text-red-700 text-xs font-medium">
                  {errorMessage}
                </div>
              )}

              {currentStep === 1 && (
                <form onSubmit={handleVerifyAccount} className="space-y-3.5">
                  <div>
                    <label className="block mb-1 text-xs font-bold text-slate-700">Bank Account Number</label>
                    <input
                      type="text"
                      name="account_number"
                      value={formData.account_number}
                      onChange={handleInputChange}
                      placeholder="Enter your bank account number"
                      maxLength={20}
                      className="w-full h-11 px-4 rounded-xl border border-slate-300 bg-slate-50/60 text-sm text-slate-900 outline-none transition focus:bg-white focus:border-teal-600 focus:ring-4 focus:ring-teal-600/10"
                      required
                    />
                  </div>

                  <div>
                    <label className="block mb-1 text-xs font-bold text-slate-700">Registered Mobile Number</label>
                    <input
                      type="tel"
                      name="mobile_number"
                      value={formData.mobile_number}
                      onChange={handleInputChange}
                      placeholder="Enter your mobile number"
                      maxLength={15}
                      className="w-full h-11 px-4 rounded-xl border border-slate-300 bg-slate-50/60 text-sm text-slate-900 outline-none transition focus:bg-white focus:border-teal-600 focus:ring-4 focus:ring-teal-600/10"
                      required
                    />
                  </div>

                  <div className="grid grid-cols-2 gap-3">
                    <div>
                      <label className="block mb-1 text-xs font-bold text-slate-700">First Name</label>
                      <input
                        type="text"
                        name="first_name"
                        value={formData.first_name}
                        onChange={handleInputChange}
                        placeholder="Enter first name"
                        maxLength={50}
                        className="w-full h-11 px-3.5 rounded-xl border border-slate-300 bg-slate-50/60 text-sm text-slate-900 outline-none transition focus:bg-white focus:border-teal-600 focus:ring-4 focus:ring-teal-600/10"
                        required
                      />
                    </div>
                    <div>
                      <label className="block mb-1 text-xs font-bold text-slate-700">Last Name</label>
                      <input
                        type="text"
                        name="last_name"
                        value={formData.last_name}
                        onChange={handleInputChange}
                        placeholder="Enter last name"
                        maxLength={50}
                        className="w-full h-11 px-3.5 rounded-xl border border-slate-300 bg-slate-50/60 text-sm text-slate-900 outline-none transition focus:bg-white focus:border-teal-600 focus:ring-4 focus:ring-teal-600/10"
                        required
                      />
                    </div>
                  </div>

                  <div>
                    <label className="block mb-1 text-xs font-bold text-slate-700">Date of Birth</label>
                    <input
                      type="date"
                      name="date_of_birth"
                      value={formData.date_of_birth}
                      onChange={handleInputChange}
                      className="w-full h-11 px-4 rounded-xl border border-slate-300 bg-slate-50/60 text-sm text-slate-700 outline-none transition focus:bg-white focus:border-teal-600 focus:ring-4 focus:ring-teal-600/10"
                      required
                    />
                  </div>

                  <button
                    type="submit"
                    disabled={loading}
                    className="w-full h-12 mt-2 rounded-xl bg-[#0b2942] hover:bg-[#071e31] text-white font-bold text-sm tracking-wide shadow-lg shadow-[#0b2942]/15 active:scale-[0.99] transition cursor-pointer flex items-center justify-center gap-2"
                  >
                    {loading ? (
                      <span className="w-5 h-5 border-2 border-white/30 border-t-white rounded-full animate-spin" />
                    ) : (
                      <>
                        <span>Verify Account</span>
                        <svg className="w-4 h-4" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
                          <path d="M5 12h14M13 6l6 6-6 6" />
                        </svg>
                      </>
                    )}
                  </button>
                </form>
              )}

              {currentStep === 2 && (
                <form onSubmit={handleVerifyOtp} className="space-y-4">
                  <div className="text-center">
                    <p className="text-xs text-slate-600">
                      We sent a verification code to <span className="font-bold text-slate-900">{formData.mobile_number}</span>
                    </p>
                  </div>

                  <div>
                    <div className="flex items-center justify-between mb-1.5">
                      <label className="text-xs font-bold text-slate-700">Enter 6-Digit OTP</label>
                      <button
                        type="button"
                        onClick={handleResendOtp}
                        disabled={!canResend || loading}
                        className={`text-xs font-bold ${canResend ? 'text-teal-700 hover:text-teal-900 cursor-pointer' : 'text-slate-400 cursor-not-allowed'}`}
                      >
                        {canResend ? 'Resend OTP' : `Resend in ${timer}s`}
                      </button>
                    </div>

                    <div className="grid grid-cols-6 gap-2">
                      {otp.map((digit, index) => (
                        <input
                          key={index}
                          ref={(el) => (otpInputsRef.current[index] = el)}
                          type="text"
                          inputMode="numeric"
                          maxLength={1}
                          value={digit}
                          onChange={(e) => handleOtpChange(index, e.target.value)}
                          onKeyDown={(e) => handleOtpKeyDown(index, e)}
                          className="h-11 w-full text-center rounded-xl border border-slate-300 bg-white text-base font-bold text-slate-900 outline-none transition focus:border-teal-600 focus:ring-4 focus:ring-teal-600/10"
                        />
                      ))}
                    </div>
                  </div>

                  <div className="flex gap-3">
                    <button
                      type="button"
                      onClick={() => {
                        setErrorMessage('');
                        setCurrentStep(1);
                      }}
                      className="w-1/3 h-12 rounded-xl border border-slate-300 hover:bg-slate-50 text-slate-700 font-bold text-sm transition cursor-pointer"
                    >
                      Back
                    </button>
                    <button
                      type="submit"
                      disabled={loading}
                      className="w-2/3 h-12 rounded-xl bg-[#0b2942] hover:bg-[#071e31] text-white font-bold text-sm tracking-wide shadow-lg shadow-[#0b2942]/15 active:scale-[0.99] transition cursor-pointer flex items-center justify-center gap-2"
                    >
                      {loading ? (
                        <span className="w-5 h-5 border-2 border-white/30 border-t-white rounded-full animate-spin" />
                      ) : (
                        <span>Verify Phone</span>
                      )}
                    </button>
                  </div>
                </form>
              )}

              {currentStep === 3 && (
                <form onSubmit={handleSetupMpin} className="space-y-4">
                  <div className="text-center">
                    <p className="text-xs text-slate-600">
                      Set a 6-digit MPIN for fast and secure login to your account.
                    </p>
                  </div>

                  <div>
                    <div className="flex items-center justify-between mb-1.5">
                      <label className="text-xs font-bold text-slate-700">Set 6-Digit MPIN</label>
                      <button
                        type="button"
                        onClick={() => setShowMpinDigits(!showMpinDigits)}
                        className="text-xs font-semibold text-teal-700 hover:text-teal-900 cursor-pointer"
                      >
                        {showMpinDigits ? 'Hide Digits' : 'Show Digits'}
                      </button>
                    </div>

                    <div className="grid grid-cols-6 gap-2">
                      {mpin.map((digit, index) => (
                        <input
                          key={index}
                          ref={(el) => (mpinInputsRef.current[index] = el)}
                          type={showMpinDigits ? 'text' : 'password'}
                          inputMode="numeric"
                          maxLength={1}
                          value={digit}
                          onChange={(e) => handleMpinChange(index, e.target.value)}
                          onKeyDown={(e) => handleMpinKeyDown(index, e)}
                          className="h-11 w-full text-center rounded-xl border border-slate-300 bg-white text-base font-bold text-slate-900 outline-none transition focus:border-teal-600 focus:ring-4 focus:ring-teal-600/10"
                        />
                      ))}
                    </div>
                  </div>

                  <div>
                    <label className="block mb-1.5 text-xs font-bold text-slate-700">Confirm 6-Digit MPIN</label>
                    <div className="grid grid-cols-6 gap-2">
                      {confirmMpin.map((digit, index) => (
                        <input
                          key={index}
                          ref={(el) => (confirmMpinInputsRef.current[index] = el)}
                          type={showMpinDigits ? 'text' : 'password'}
                          inputMode="numeric"
                          maxLength={1}
                          value={digit}
                          onChange={(e) => handleConfirmMpinChange(index, e.target.value)}
                          onKeyDown={(e) => handleConfirmMpinKeyDown(index, e)}
                          className="h-11 w-full text-center rounded-xl border border-slate-300 bg-white text-base font-bold text-slate-900 outline-none transition focus:border-teal-600 focus:ring-4 focus:ring-teal-600/10"
                        />
                      ))}
                    </div>
                  </div>

                  <div className="flex items-center gap-2.5 rounded-xl border border-slate-200 bg-slate-50/90 px-3.5 py-2.5">
                    <svg className="w-4 h-4 shrink-0 text-teal-700" viewBox="0 0 24 24" fill="currentColor">
                      <path d="M12 2L4 5v6c0 5.1 3.4 9.7 8 11 4.6-1.3 8-5.9 8-11V5l-8-3zm0 4l5 1.9V11c0 3.4-2 6.6-5 7.9-3-1.3-5-4.5-5-7.9V7.9L12 6z" />
                    </svg>
                    <p className="text-[10.5px] leading-tight text-slate-600">
                      Never share your 6-digit MPIN or OTP with bank representatives.
                    </p>
                  </div>

                  <button
                    type="submit"
                    disabled={loading}
                    className="w-full h-12 mt-2 rounded-xl bg-[#0b2942] hover:bg-[#071e31] text-white font-bold text-sm tracking-wide shadow-lg shadow-[#0b2942]/15 active:scale-[0.99] transition cursor-pointer flex items-center justify-center gap-2"
                  >
                    {loading ? (
                      <span className="w-5 h-5 border-2 border-white/30 border-t-white rounded-full animate-spin" />
                    ) : (
                      <>
                        <span>Complete MPIN Setup</span>
                        <svg className="w-4 h-4" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
                          <path d="M5 12h14M13 6l6 6-6 6" />
                        </svg>
                      </>
                    )}
                  </button>
                </form>
              )}

              {currentStep === 4 && (
                <div className="text-center py-4 space-y-4">
                  <div className="w-14 h-14 rounded-full bg-emerald-50 text-emerald-600 border border-emerald-200 flex items-center justify-center mx-auto shadow-xs">
                    <svg className="w-7 h-7" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2.5">
                      <polyline points="20 6 9 17 4 12" />
                    </svg>
                  </div>

                  <div>
                    <h3 className="text-lg font-black text-slate-900">Registration Complete!</h3>
                    <p className="text-xs text-slate-600 mt-1 max-w-[320px] mx-auto">
                      Your bank identity and 6-digit MPIN credentials have been saved. You can now log into your account.
                    </p>
                  </div>

                  <div className="rounded-xl border border-slate-200/80 bg-slate-50/80 p-3 text-xs text-slate-600 flex justify-between items-center">
                    <span className="font-semibold">Account Number:</span>
                    <span className="font-bold text-slate-800 tracking-wider">
                      •••• •••• {formData.account_number.slice(-4)}
                    </span>
                  </div>

                  <button
                    type="button"
                    onClick={() => navigate('/login')}
                    className="w-full h-12 rounded-xl bg-[#0b2942] hover:bg-[#071e31] text-white font-bold text-sm tracking-wide shadow-lg shadow-[#0b2942]/15 active:scale-[0.99] transition cursor-pointer flex items-center justify-center gap-2"
                  >
                    <span>Proceed to Login</span>
                    <svg className="w-4 h-4" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
                      <path d="M5 12h14M13 6l6 6-6 6" />
                    </svg>
                  </button>
                </div>
              )}

              <div className="mt-5 pt-4 border-t border-slate-100 text-center text-xs">
                <span className="text-slate-500">Already have an account? </span>
                <button
                  type="button"
                  onClick={() => navigate('/login')}
                  className="font-bold text-teal-700 hover:underline cursor-pointer"
                >
                  Login
                </button>
              </div>
            </div>
          </div>

        </div>
      </main>

      <Login_Footer />
    </div>
  );
}