export function Logo({ className }: { className?: string }) {
  return (
    <svg
      viewBox="0 0 48 48"
      fill="none"
      xmlns="http://www.w3.org/2000/svg"
      className={className}
      aria-hidden="true"
    >
      <polygon
        points="24,4 44,16 44,36 24,44 4,36 4,16"
        stroke="#4CAF50"
        strokeWidth="1.5"
        fill="#161616"
      />
      <polygon
        points="24,12 36,20 36,32 24,38 12,32 12,20"
        stroke="#66BB6A"
        strokeWidth="1"
        fill="none"
        opacity="0.7"
      />
      <line
        x1="12"
        y1="20"
        x2="36"
        y2="32"
        stroke="#4CAF50"
        strokeWidth="0.75"
        opacity="0.4"
      />
      <line
        x1="36"
        y1="20"
        x2="12"
        y2="32"
        stroke="#4CAF50"
        strokeWidth="0.75"
        opacity="0.4"
      />
    </svg>
  );
}
