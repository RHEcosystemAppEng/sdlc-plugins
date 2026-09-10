// SYNTHETIC TEST DATA — PackageCard with planted layout thrashing (F6)
import React, { useRef } from 'react';

interface Package {
  id: number;
  name: string;
}

interface PackageCardProps {
  packages: Package[];
}

export function PackageCard({ packages }: PackageCardProps) {
  const cardRef = useRef<(HTMLDivElement | null)[]>([]);

  return (
    <div className="package-grid">
      {packages.map((pkg, i) => {
        // F6: Layout Thrashing — DOM read/write interleaved in map()
        const height = cardRef.current[i]?.offsetHeight;
        if (height && height < 200) {
          cardRef.current[i]!.style.height = '200px';
        }
        return (
          <div key={pkg.id} ref={(el) => (cardRef.current[i] = el)}>
            {pkg.name}
          </div>
        );
      })}
    </div>
  );
}
