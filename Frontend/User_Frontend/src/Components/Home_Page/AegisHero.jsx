import React from 'react';
import heroVideo from '../../assets/Hero1.mp4';

export default function AegisHero() {
  return (
    <section className="relative w-full overflow-hidden bg-slate-900 leading-none block -mt-px">
      {/* Reduced height container: 200px mobile -> 260px tablet -> 320px desktop */}
      <div className="relative w-full h-[200px] sm:h-[260px] md:h-[300px] lg:h-[330px] overflow-hidden mt-0.5">
        <video
          autoPlay
          loop
          muted
          playsInline
          preload="auto"
          className="w-full h-full object-cover object-center block"
        >
          <source src={heroVideo} type="video/mp4" />
        </video>

        {/* Transparent Clickable Overlay Targets Matching Video Buttons */}
        <div className="absolute inset-0 flex items-center justify-center pointer-events-none">
          <div className="w-full max-w-4xl mx-auto px-4 flex flex-col items-center">
            {/* Reduced spacer height to match the shorter banner */}
            <div className="h-10 sm:h-16 md:h-20" />

            <div className="flex items-center gap-3 sm:gap-4 pointer-events-auto">
              <button
                type="button"
                onClick={() => console.log('Discover Loans Clicked')}
                className="w-28 sm:w-36 md:w-44 h-7 sm:h-9 md:h-10 rounded-lg cursor-pointer opacity-0 hover:opacity-10 hover:bg-white transition-opacity duration-150"
                aria-label="Discover Eligible Loans"
              />
              <button
                type="button"
                onClick={() => console.log('AI Security Clicked')}
                className="w-32 sm:w-40 md:w-48 h-7 sm:h-9 md:h-10 rounded-lg cursor-pointer opacity-0 hover:opacity-10 hover:bg-white transition-opacity duration-150"
                aria-label="Learn About Our AI Security"
              />
            </div>
          </div>
        </div>
      </div>
    </section>
  );
}