"use client";
import {useState,useEffect} from "react";
const size=168;
const stroke=12;
const radius=(size-stroke)/2;
const circumference=2*Math.PI*radius;

export function scoreVerdict(score){
    if (score >= 75) return "Strong match";
    if (score >= 50) return "Partial match";
    return "Significant gaps";
    }
export default function ScoreRing({score}) {
    const target=Math.min(100, Math.max(0, Math.round(score)));
    const[shown,setshown]=useState(0);
    const[drawn,setDrawn]=useState(false);
    useEffect(()=>{
        const reduced=wnidow.matchMedia("(prefers-reduced-motion: reduce)").matches;
        if (reduced){
            setshown(target);
            setDrawn(true);
            return;
        } 
        setDrawn(true);
        const start=performance.now();
        const duration=1200;
        let frame=0;
        const tick=(now)=>{
            const t=Math.min(1,(now-start)/duration)
            const eased=1-Math.pow(1-t,3);
            setshown(Math.round(eased*target));
            if(t<1) frame=requestAnimationFrame(tick);
        };
        frame=requestAnimationFrame(tick);
        return ()=> cancelAnimationFrame(frame);
    },[target]);
const offset= drawn ? circumference * (1-target/100):circumference;
return (
    <div 
    className="relative shrink-0"
      style={{ width: size, height: size}}
      role="img"
      aria-label={`Match score ${target} out of 100`}
    >
      <svg width={size} height={size} className="-rotate-90">
        <circle cx={size / 2} cy={size / 2} r={radius} fill="none" stroke="#D9DEE8" strokeWidth={stroke} />
        <circle
          cx={size / 2}
          cy={size / 2}
          r={radius}
          fill="none"
          stroke="#2B3FD6"
          strokeWidth={stroke}
          strokeLinecap="round"
          strokeDasharray={circumference}
          strokeDashoffset={offset}
          style={{ transition: "stroke-dashoffset 1.2s cubic-bezier(0.22, 1, 0.36, 1)" }}
        />
      </svg>
      <div className="absolute inset-0 flex flex-col items-center justify-center">
        <span className="font-display text-5xl font-bold leading-none">{shown}</span>
        <span className="mt-1 text-sm text-slate">out of 100</span>
      </div>
    </div>
  );
}
