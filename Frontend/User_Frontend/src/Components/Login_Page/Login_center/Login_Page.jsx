import React, { useEffect, useRef, useState } from 'react';
import { useNavigate } from 'react-router-dom';
import Login_Header from '../Login_Header';
import Login_Footer from '../Login_Footer';
import Login_Animation from './Login_Animation';

const API_URL = import.meta.env.VITE_API_URL || 'http://127.0.0.1:8000';

function Login_Page() {
  const navigate = useNavigate();
  const [accountNumber, setAccountNumber] = useState('');
  const [mpin, setMpin] = useState('');
  const [showMpin, setShowMpin] = useState(false);
  const [otp, setOtp] = useState(['', '', '', '', '', '']);
  const [isAuthenticating, setIsAuthenticating] = useState(false);
  const [requiresOtp, setRequiresOtp] = useState(false);
  const [loginOtpId, setLoginOtpId] = useState(null);
  const [errorMessage, setErrorMessage] = useState('');
  const [showLocationModal, setShowLocationModal] = useState(false);
  const [locationCoords, setLocationCoords] = useState({ latitude: null, longitude: null });

  const [showAd, setShowAd] = useState(true);
  const [adFadeOut, setAdFadeOut] = useState(false);

  const otpInputsRef = useRef([]);
  const agentVideoRef = useRef(null);
  const adVideoRef = useRef(null);

  useEffect(() => {
    const video = agentVideoRef.current;
    if (!video) return;

    video.muted = true;
    video.defaultMuted = true;
    video.play().catch(() => {});
  }, []);

  useEffect(() => {
    const video = adVideoRef.current;
    if (!video || !showAd) return;

    video.muted = true;
    video.defaultMuted = true;
    video.play().catch(() => {});

    const handleTimeUpdate = () => {
      if (video.duration && video.currentTime >= video.duration - 1.2) {
        setAdFadeOut(true);
      }
    };

    video.addEventListener('timeupdate', handleTimeUpdate);
    return () => video.removeEventListener('timeupdate', handleTimeUpdate);
  }, [showAd]);

  const handleAdEnded = () => {
    setAdFadeOut(true);
    setTimeout(() => {
      setShowAd(false);
    }, 500);
  };

  const skipAd = () => {
    setAdFadeOut(true);
    setTimeout(() => {
      setShowAd(false);
    }, 400);
  };

  const requestDeviceLocation = () => {
    return new Promise((resolve) => {
      if (!navigator.geolocation) {
        setErrorMessage('Geolocation is not supported by this browser.');
        setShowLocationModal(true);
        resolve({ latitude: null, longitude: null });
        return;
      }

      const success = (position) => {
        const coords = {
          latitude: position.coords.latitude,
          longitude: position.coords.longitude
        };
        console.log('Device Location:', coords);
        setLocationCoords(coords);
        setShowLocationModal(false);
        setErrorMessage('');
        resolve(coords);
      };

      const failure = (error) => {
        console.error('Geolocation Error:', error.code, error.message);

        if (error.code === 1) {
          setErrorMessage('Location permission was denied. Please allow location access for localhost.');
          setShowLocationModal(true);
          resolve({ latitude: null, longitude: null });
          return;
        }

        navigator.geolocation.getCurrentPosition(
          success,
          (secondError) => {
            console.error('High Accuracy Geolocation Error:', secondError.code, secondError.message);
            setErrorMessage('Unable to detect your device location. Please enable Windows location services and allow location access for localhost.');
            setShowLocationModal(true);
            resolve({ latitude: null, longitude: null });
          },
          {
            enableHighAccuracy: true,
            timeout: 15000,
            maximumAge: 0
          }
        );
      };

      navigator.geolocation.getCurrentPosition(
        success,
        failure,
        {
          enableHighAccuracy: false,
          timeout: 10000,
          maximumAge: 60000
        }
      );
    });
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

  const handleKeyDown = (index, e) => {
    if (e.key === 'Backspace' && !otp[index] && index > 0) {
      otpInputsRef.current[index - 1]?.focus();
    }
  };

  const executeLoginRequest = async (coords) => {
    setErrorMessage('');
    setIsAuthenticating(true);

    try {
      if (!requiresOtp) {
        const response = await fetch(`${API_URL}/api/user/login`, {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({
            account_number: accountNumber,
            mpin: mpin,
            device_id: 'WEB_CLIENT',
            device_name: navigator.userAgent,
            user_agent: navigator.userAgent,
            latitude: coords.latitude,
            longitude: coords.longitude,
            city: null,
            country: null
          })
        });

        const text = await response.text();
        let data = {};
        try {
          data = text ? JSON.parse(text) : {};
        } catch {
          throw new Error('Server returned an unreadable response.');
        }

        if (!response.ok || !data.success) {
          throw new Error(data.message || data.detail || 'Login failed. Please verify credentials.');
        }

        if (data.requires_otp || data.login_otp_id) {
          setLoginOtpId(data.login_otp_id);
          setRequiresOtp(true);
          setIsAuthenticating(false);
        } else {
          setTimeout(() => {
            navigate('/');
          }, 1200);
        }
      } else {
        const enteredOtp = otp.join('');
        if (enteredOtp.length !== 6) {
          throw new Error('Please enter all 6 digits of the OTP.');
        }

        const response = await fetch(`${API_URL}/api/user/login/verify-otp`, {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({
            login_otp_id: loginOtpId,
            otp: enteredOtp,
            device_id: 'WEB_CLIENT',
            device_name: navigator.userAgent,
            user_agent: navigator.userAgent,
            latitude: coords.latitude,
            longitude: coords.longitude,
            city: null,
            country: null
          })
        });

        const text = await response.text();
        let data = {};
        try {
          data = text ? JSON.parse(text) : {};
        } catch {
          throw new Error('Server returned an unreadable response.');
        }

        if (!response.ok || !data.success) {
          throw new Error(data.message || data.detail || 'OTP verification failed.');
        }

        setTimeout(() => {
          navigate('/');
        }, 1200);
      }
    } catch (err) {
      setIsAuthenticating(false);
      setErrorMessage(err.message || 'Authentication error occurred.');
    }
  };

  const handleLogin = async (e) => {
    e.preventDefault();
    setErrorMessage('');

    let coords = locationCoords;
    if (coords.latitude === null || coords.longitude === null) {
      coords = await requestDeviceLocation();
    }

    if (coords.latitude === null || coords.longitude === null) {
      setIsAuthenticating(false);
      setErrorMessage('Location permission is required to authenticate securely.');
      setShowLocationModal(true);
      return;
    }

    console.log('Sending login with location:', coords);
    await executeLoginRequest(coords);
  };

  return (
    <div className="min-h-screen flex flex-col bg-[#f5f8fb] text-slate-900 select-none relative">
      <Login_Header />

      <main className="relative flex-1 flex items-center justify-center overflow-hidden">
        <div className="absolute inset-0 pointer-events-none z-0">
          <div className="absolute inset-0 bg-[#f7fafc]" />
          <div className="absolute top-0 inset-x-0 h-[450px] bg-gradient-to-b from-white via-[#f1f6fa] to-[#eaf3f7]" />
          <div className="absolute inset-0 opacity-[0.25] bg-[radial-gradient(#94a3b8_1px,transparent_1px)] [background-size:24px_24px]" />
          <div className="absolute -top-24 left-[5%] w-[480px] h-[480px] rounded-full bg-teal-200/20 blur-3xl" />
          <div className="absolute top-1/3 -right-24 w-[450px] h-[450px] rounded-full bg-sky-200/20 blur-3xl" />
        </div>

        <div className="relative z-10 w-full max-w-[1340px] mx-auto px-6 sm:px-10 lg:px-12 py-8 my-auto">
          <div className="grid grid-cols-1 xl:grid-cols-12 gap-8 lg:gap-12 items-center">
            
            <div className="xl:col-span-7 flex flex-col">
              <div className="flex flex-wrap items-center gap-3 mb-4">
                <div className="inline-flex items-center gap-2 px-3.5 py-1.5 rounded-full bg-white border border-slate-200/90 shadow-2xs">
                  <span className="relative flex h-2 w-2">
                    <span className="animate-ping absolute inline-flex h-full w-full rounded-full bg-emerald-400 opacity-75" />
                    <span className="relative inline-flex rounded-full h-2 w-2 bg-emerald-500" />
                  </span>
                  <span className="text-[11px] font-extrabold uppercase tracking-wider text-slate-700">
                    24/7 AI Virtual Desk
                  </span>
                </div>

                <div className="inline-flex items-center gap-2 px-3.5 py-1.5 rounded-full bg-[#0b2942] text-white shadow-2xs">
                  <svg className="w-3.5 h-3.5 text-teal-300" viewBox="0 0 24 24" fill="currentColor">
                    <path d="M12 2L4 5v6.2c0 5.1 3.5 9.8 8 10.8 4.5-1 8-5.7 8-10.8V5l-8-3z" />
                  </svg>
                  <span className="text-[11px] font-bold uppercase tracking-wider text-slate-100">
                    Aegis-Guard Verified
                  </span>
                </div>
              </div>

              <div className="mb-5">
                <h1 className="text-3xl sm:text-4xl lg:text-5xl font-black leading-tight text-[#0d2137]">
                  Banking assistance,{' '}
                  <span className="text-teal-600">built around you.</span>
                </h1>
                <p className="mt-2 text-sm sm:text-base text-slate-600 max-w-[560px]">
                  Meet your AegisLend AI virtual banking assistant — loan approvals, secure account authentication, and digital servicing whenever you need it.
                </p>
              </div>

              <div className="relative w-full aspect-16/10 rounded-2xl overflow-hidden shadow-2xl shadow-slate-900/10 border border-slate-200/90 bg-white">
                <video
                  ref={agentVideoRef}
                  src="/assets/aegis_agent.mp4"
                  autoPlay
                  loop
                  muted
                  playsInline
                  className="w-full h-full object-cover object-center pointer-events-none"
                />

                <div className="absolute inset-x-0 bottom-0 h-20 bg-gradient-to-t from-[#0b2942]/20 to-transparent pointer-events-none" />

                <div className="absolute top-4 left-4 inline-flex items-center gap-2 px-3 py-1.5 rounded-xl bg-white/95 backdrop-blur-md border border-slate-200/80 shadow-md">
                  <span className="w-2 h-2 rounded-full bg-emerald-500 animate-pulse" />
                  <span className="text-[10px] font-black uppercase tracking-wider text-slate-800">
                    Agent Online
                  </span>
                </div>
              </div>

              <div className="grid grid-cols-3 gap-3 mt-4">
                <FeatureCard
                  title="24/7 AI Support"
                  subtitle="Available Anytime"
                  icon="support"
                />
                <FeatureCard
                  title="Instant Lending"
                  subtitle="Fast Track Decision"
                  icon="loan"
                />
                <FeatureCard
                  title="Zero-Trust Vault"
                  subtitle="AES-256 Protected"
                  icon="security"
                />
              </div>
            </div>

            <div className="xl:col-span-5 flex justify-center xl:justify-end">
              <div className="w-full max-w-[440px] bg-white rounded-3xl border border-slate-200/90 shadow-2xl shadow-slate-300/50 p-8 sm:p-9 relative overflow-hidden">
                <div className="absolute top-0 inset-x-0 h-1.5 bg-gradient-to-r from-[#0b2942] via-teal-500 to-[#0b2942]" />

                {isAuthenticating ? (
                  <Login_Animation />
                ) : (
                  <>
                    <div className="flex flex-col items-center text-center mb-7">
                      <div className="w-13 h-13 rounded-2xl bg-[#0b2942] flex items-center justify-center shadow-lg shadow-[#0b2942]/20 mb-3 ring-1 ring-teal-400/30">
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
                        Secure Account Access
                      </p>
                    </div>

                    {errorMessage && (
                      <div className="mb-4 p-3 rounded-xl bg-red-50 border border-red-200 text-red-700 text-xs font-medium text-center">
                        {errorMessage}
                      </div>
                    )}

                    <form onSubmit={handleLogin} className="space-y-4">
                      <div>
                        <label className="block mb-1.5 text-xs font-bold text-slate-700">
                          Bank Account Number
                        </label>
                        <input
                          type="text"
                          value={accountNumber}
                          onChange={(e) => setAccountNumber(e.target.value)}
                          placeholder="Enter your account number"
                          maxLength={20}
                          disabled={requiresOtp}
                          className="w-full h-11 px-4 rounded-xl border border-slate-300 bg-slate-50/60 text-sm text-slate-900 placeholder:text-slate-400 outline-none transition focus:bg-white focus:border-teal-600 focus:ring-4 focus:ring-teal-600/10 disabled:bg-slate-100 disabled:text-slate-500"
                          required
                        />
                      </div>

                      <div>
                        <label className="block mb-1.5 text-xs font-bold text-slate-700">
                          MPIN or Password
                        </label>
                        <div className="relative">
                          <input
                            type={showMpin ? 'text' : 'password'}
                            value={mpin}
                            onChange={(e) => setMpin(e.target.value)}
                            placeholder="Enter your MPIN or Password"
                            maxLength={6}
                            disabled={requiresOtp}
                            className="w-full h-11 px-4 pr-11 rounded-xl border border-slate-300 bg-slate-50/60 text-sm text-slate-900 placeholder:text-slate-400 outline-none transition focus:bg-white focus:border-teal-600 focus:ring-4 focus:ring-teal-600/10 disabled:bg-slate-100 disabled:text-slate-500"
                            required
                          />
                          <button
                            type="button"
                            onClick={() => setShowMpin(!showMpin)}
                            disabled={requiresOtp}
                            className="absolute right-3 top-1/2 -translate-y-1/2 text-slate-400 hover:text-slate-700 p-1 cursor-pointer"
                          >
                            {showMpin ? (
                              <svg className="w-4 h-4" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
                                <path d="M1 12s4-8 11-8 11 8 11 8-4 8-11 8-11-8-11-8z" />
                                <circle cx="12" cy="12" r="3" />
                              </svg>
                            ) : (
                              <svg className="w-4 h-4" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
                                <path d="M17.94 17.94A10.07 10.07 0 0 1 12 20c-7 0-11-8-11-8a18.45 18.45 0 0 1 5.06-5.94" />
                                <path d="M9.9 4.24A9.12 9.12 0 0 1 12 4c7 0 11 8 11 8a18.5 18.5 0 0 1-2.16 3.19" />
                                <line x1="1" y1="1" x2="23" y2="23" />
                              </svg>
                            )}
                          </button>
                        </div>
                      </div>

                      {requiresOtp && (
                        <div>
                          <div className="flex items-center justify-between mb-1.5">
                            <label className="text-xs font-bold text-slate-700">
                              Enter OTP
                            </label>
                            <button type="button" className="text-xs font-bold text-teal-700 hover:text-teal-900 cursor-pointer">
                              Resend OTP
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
                                onKeyDown={(e) => handleKeyDown(index, e)}
                                className="h-11 w-full text-center rounded-xl border border-slate-300 bg-white text-base font-bold text-slate-900 outline-none transition focus:border-teal-600 focus:ring-4 focus:ring-teal-600/10"
                              />
                            ))}
                          </div>
                        </div>
                      )}

                      <div className="flex items-center gap-2.5 rounded-xl border border-slate-200 bg-slate-50/90 px-3.5 py-2.5">
                        <svg className="w-4 h-4 shrink-0 text-teal-700" viewBox="0 0 24 24" fill="currentColor">
                          <path d="M12 2L4 5v6c0 5.1 3.4 9.7 8 11 4.6-1.3 8-5.9 8-11V5l-8-3zm0 4l5 1.9V11c0 3.4-2 6.6-5 7.9-3-1.3-5-4.5-5-7.9V7.9L12 6z" />
                        </svg>
                        <p className="text-[10.5px] leading-tight text-slate-600">
                          Encrypted end-to-end via Aegis-Guard Zero Trust Protocol.
                        </p>
                      </div>

                      <button
                        type="submit"
                        className="w-full h-12 rounded-xl bg-[#0b2942] hover:bg-[#071e31] text-white font-bold text-sm tracking-wide shadow-lg shadow-[#0b2942]/15 active:scale-[0.99] transition cursor-pointer flex items-center justify-center gap-2"
                      >
                        <span>{requiresOtp ? 'Verify OTP & Authenticate' : 'Authenticate Securely'}</span>
                        <svg className="w-4 h-4" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2.2">
                          <path d="M5 12h14M13 6l6 6-6 6" />
                        </svg>
                      </button>
                    </form>

                    <div className="mt-5 pt-4 border-t border-slate-100 text-center text-xs">
                      <a href="#forgot-mpin" className="font-semibold text-slate-600 hover:text-teal-700">
                        Forgot MPIN?
                      </a>
                      <div className="mt-1.5 text-slate-500">
                        No MPIN set?{' '}
                        <button
                          type="button"
                          onClick={() => navigate('/registration')}
                          className="font-bold text-teal-700 hover:underline cursor-pointer inline-block"
                        >
                          Register Account
                        </button>
                      </div>
                    </div>
                  </>
                )}
              </div>
            </div>

          </div>
        </div>
      </main>

      <Login_Footer />

      {showLocationModal && (
        <div className="fixed inset-0 z-[100] bg-slate-900/60 backdrop-blur-xs flex items-center justify-center p-4">
          <div className="bg-white rounded-2xl max-w-sm w-full p-6 shadow-2xl border border-slate-100 flex flex-col items-center text-center">
            <div className="w-12 h-12 rounded-full bg-teal-50 text-teal-600 flex items-center justify-center mb-3">
              <svg className="w-6 h-6" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
                <path d="M12 2C8.13 2 5 5.13 5 9c0 5.25 7 13 7 13s7-7.75 7-13c0-3.87-3.13-7-7-7z" />
                <circle cx="12" cy="9" r="2.5" />
              </svg>
            </div>
            <h3 className="text-base font-bold text-slate-900">Enable Device Location</h3>
            <p className="text-xs text-slate-500 mt-1 mb-5">
              AegisLend bank security requires your device location to verify against unauthorized account intrusion.
            </p>
            <div className="flex gap-2.5 w-full">
              <button
                type="button"
                onClick={() => setShowLocationModal(false)}
                className="flex-1 py-2.5 rounded-xl border border-slate-200 text-slate-600 text-xs font-bold hover:bg-slate-50 transition"
              >
                Cancel
              </button>
              <button
                type="button"
                onClick={async () => {
                  setErrorMessage('');
                  const coords = await requestDeviceLocation();
                  if (coords.latitude !== null && coords.longitude !== null) {
                    setShowLocationModal(false);
                  }
                }}
                className="flex-1 py-2.5 rounded-xl bg-[#0b2942] hover:bg-[#071e31] text-white text-xs font-bold transition"
              >
                Allow Location
              </button>
            </div>
          </div>
        </div>
      )}

      {showAd && (
        <div
          className={`fixed inset-0 z-50 bg-[#071c2e] flex items-center justify-center transition-opacity duration-700 ${
            adFadeOut ? 'opacity-0 pointer-events-none' : 'opacity-100'
          }`}
        >
          <div className="relative w-full h-full max-w-[1600px] flex items-center justify-center">
            <video
              ref={adVideoRef}
              src="/assets/aegislend_ad.mp4"
              muted
              playsInline
              onEnded={handleAdEnded}
              className="w-full h-full object-contain"
            />

            <button
              type="button"
              onClick={skipAd}
              className="absolute top-8 right-8 px-5 py-2 rounded-full bg-black/40 hover:bg-black/60 border border-white/20 text-white text-xs font-bold backdrop-blur-md transition cursor-pointer"
            >
              Skip Intro
            </button>
          </div>
        </div>
      )}
    </div>
  );
}

function FeatureCard({ title, subtitle, icon }) {
  return (
    <div className="rounded-xl border border-slate-200/90 bg-white/95 px-3 py-2.5 shadow-2xs flex items-center gap-2.5">
      <div className="w-8 h-8 rounded-lg bg-teal-50 flex items-center justify-center shrink-0">
        {icon === 'support' && (
          <svg className="w-4 h-4 text-teal-700" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
            <circle cx="12" cy="12" r="10" />
            <polyline points="12 6 12 12 16 14" />
          </svg>
        )}
        {icon === 'loan' && (
          <svg className="w-4 h-4 text-teal-700" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
            <path d="M12 2v20M17 5H9.5a3.5 3.5 0 000 7h5a3.5 3.5 0 010 7H6" />
          </svg>
        )}
        {icon === 'security' && (
          <svg className="w-4 h-4 text-teal-700" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
            <path d="M12 22s8-4 8-10V5l-8-3-8 3v7c0 6 8 10 8 10z" />
          </svg>
        )}
      </div>
      <div>
        <p className="text-xs font-bold text-slate-800 leading-tight">{title}</p>
        <p className="text-[10px] text-slate-500 font-medium">{subtitle}</p>
      </div>
    </div>
  );
}

export default Login_Page;