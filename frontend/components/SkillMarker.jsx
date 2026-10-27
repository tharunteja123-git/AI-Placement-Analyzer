export default function SkillMarker({ skill, kind, index }) {
  const color = kind === "matched" ? "#BDEBD2" : "#FFC7CF";
  return (
    <li
      className="marker rounded px-2 py-1 text-[0.95rem] font-medium"
      style={{
        "--mk": color,
        "--delay": `${0.5 + index * 0.06}s`,
        boxDecorationBreak: "clone",
      }}
    >
      {skill}
    </li>
  );
}

