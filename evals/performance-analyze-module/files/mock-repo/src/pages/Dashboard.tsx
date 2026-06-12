<!-- SYNTHETIC TEST DATA — Dashboard page with planted anti-patterns for eval -->
import React from 'react';
import { HeavyChart } from '../components/HeavyChart';
import { useProducts } from '../hooks/useProducts';
// PLANTED ANTI-PATTERN: Unused imports (Step 6.5)
import { formatCurrency, parseTimestamp, deepClone, DEFAULT_PAGE_SIZE } from '../utils/unused-imports';

interface Product {
  id: string;
  name: string;
  price: number;
}

// PLANTED ANTI-PATTERN: N+1 fetch in loop (Step 6.2)
async function loadProductDetails(products: Product[]) {
  const details = [];
  for (const product of products) {
    const response = await fetch(`/api/v2/products/${product.id}`);
    const data = await response.json();
    details.push(data);
  }
  return details;
}

// PLANTED ANTI-PATTERN: Missing lazy loading (Step 6.9)
// HeavyChart is imported statically instead of React.lazy
export default function Dashboard() {
  const { products } = useProducts();

  React.useEffect(() => {
    if (products.length > 0) {
      loadProductDetails(products);
    }
  }, [products]);

  return (
    <div>
      <h1>Dashboard</h1>
      <HeavyChart data={products} />
      <ul>
        {products.map((p: Product) => (
          <li key={p.id}>{p.name} - ${p.price}</li>
        ))}
      </ul>
    </div>
  );
}
