import React from 'react';

/**
 * CrisisPulseLogo - Bespoke vector emblem based on the wireframe globe & pulse waveform.
 * Harmonized to look razor-sharp in both light and dark modes with subtle pulse animations.
 */
export default function CrisisPulseLogo({ size = 38, className = '' }) {
  return (
    <svg
      width={size}
      height={size}
      viewBox="0 0 100 100"
      fill="none"
      xmlns="http://www.w3.org/2000/svg"
      className={`crisis-pulse-svg ${className}`}
      aria-label="CrisisPulse Emblem"
    >
      <defs>
        {/* Subtle glow filter for the pulse wave */}
        <filter id="cp-pulse-glow" x="-20%" y="-20%" width="140%" height="140%">
          <feDropShadow dx="0" dy="1" stdDeviation="1.5" floodColor="#f25f4c" floodOpacity="0.35" />
        </filter>
        <linearGradient id="cp-pulse-gradient" x1="0%" y1="0%" x2="100%" y2="0%">
          <stop offset="0%" stopColor="#f87171" />
          <stop offset="50%" stopColor="#ef4444" />
          <stop offset="100%" stopColor="#f97316" />
        </linearGradient>
      </defs>

      {/* Background Soft Disc for high contrast & elegance */}
      <circle
        cx="50"
        cy="50"
        r="47"
        className="cp-globe-backdrop"
      />

      {/* Globe Wireframe - Teal / Slate Rings */}
      {/* Outer Meridian Circle */}
      <circle
        cx="50"
        cy="50"
        r="38"
        stroke="currentColor"
        strokeWidth="2.2"
        className="cp-globe-grid"
      />

      {/* Inner Elliptical Longitudes (3D Wireframe Globe) */}
      <ellipse
        cx="50"
        cy="50"
        rx="22"
        ry="38"
        stroke="currentColor"
        strokeWidth="1.8"
        className="cp-globe-grid cp-globe-grid-mid"
      />
      <ellipse
        cx="50"
        cy="50"
        rx="9"
        ry="38"
        stroke="currentColor"
        strokeWidth="1.6"
        className="cp-globe-grid cp-globe-grid-inner"
      />
      
      {/* Prime Meridian vertical line */}
      <line
        x1="50"
        y1="12"
        x2="50"
        y2="88"
        stroke="currentColor"
        strokeWidth="1.2"
        strokeDasharray="2 3"
        className="cp-globe-grid cp-globe-axis"
      />

      {/* Dynamic EKG / Seismograph Crisis Pulse Waveform */}
      {/* Path spans from left, strikes through globe with an intense heartbeat spike, then levels out with terminal node */}
      <path
        d="M 6 50 L 26 50 L 33 22 L 44 80 L 53 38 L 59 50 L 90 50"
        fill="none"
        stroke="url(#cp-pulse-gradient)"
        strokeWidth="3.4"
        strokeLinecap="round"
        strokeLinejoin="round"
        filter="url(#cp-pulse-glow)"
        className="cp-pulse-line"
      />

      {/* Telemetry Sensor Node / Focal Ping Dot */}
      <circle
        cx="90"
        cy="50"
        r="4.2"
        fill="#f97316"
        className="cp-pulse-node"
      />
      <circle
        cx="90"
        cy="50"
        r="2"
        fill="#ffffff"
      />
    </svg>
  );
}
