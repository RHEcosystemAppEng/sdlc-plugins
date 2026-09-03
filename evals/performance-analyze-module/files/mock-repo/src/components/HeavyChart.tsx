<!-- SYNTHETIC TEST DATA — Large component missing React.memo for eval -->
import React from 'react';

interface ChartProps {
  data: Array<{ id: string; name: string; price: number }>;
}

// PLANTED ANTI-PATTERN: Missing memoization (Step 6.6)
// This component receives complex props without React.memo
export function HeavyChart({ data }: ChartProps) {
  // Expensive render: iterates full dataset on every render
  const sorted = [...data].sort((a, b) => b.price - a.price);
  const labels = sorted.map(d => d.name);
  const values = sorted.map(d => d.price);

  return (
    <div className="chart-container">
      <svg viewBox="0 0 400 200">
        {values.map((v, i) => (
          <rect key={i} x={i * 40} y={200 - v} width={30} height={v} fill="#4A90D9" />
        ))}
      </svg>
      <div className="labels">
        {labels.map((l, i) => (
          <span key={i}>{l}</span>
        ))}
      </div>
    </div>
  );
}
