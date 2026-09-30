// SYNTHETIC TEST DATA — PackageList with planted N+1 fetch pattern (F2)
import React, { useEffect, useState } from 'react';

interface Package {
  id: number;
  name: string;
}

export default function PackageList() {
  const [packages, setPackages] = useState<Package[]>([]);
  const [packageDetails, setPackageDetails] = useState<unknown[]>([]);

  useEffect(() => {
    fetch('/api/v1/packages')
      .then((res) => res.json())
      .then(setPackages);
  }, []);

  // F2: N+1 Frontend Query — sequential fetches in forEach loop
  useEffect(() => {
    packages.forEach(async (pkg) => {
      const details = await fetch(`/api/v1/packages/${pkg.id}`);
      setPackageDetails((prev) => [...prev, await details.json()]);
    });
  }, [packages]);

  return (
    <div>
      <h1>Packages</h1>
      <ul>
        {packageDetails.map((detail, index) => (
          <li key={index}>{JSON.stringify(detail)}</li>
        ))}
      </ul>
    </div>
  );
}
