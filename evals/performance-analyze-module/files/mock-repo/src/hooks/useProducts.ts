<!-- SYNTHETIC TEST DATA — Over-fetching hook for eval -->
import { useQuery } from '@tanstack/react-query';

interface ProductResponse {
  id: string;
  name: string;
  description: string;
  price: number;
  inventory: { quantity: number; warehouse_location: string };
  created_at: string;
  updated_at: string;
  category: string;
  tags: string[];
  vendor_id: string;
  sku: string;
  weight_kg: number;
}

// PLANTED ANTI-PATTERN: Over-fetching (Step 6.1)
// Fetches 12 fields but Dashboard only uses id, name, price (3 of 12)
export function useProducts() {
  const { data, isLoading } = useQuery({
    queryKey: ['products'],
    queryFn: () => fetch('/api/v2/products').then(r => r.json()),
  });

  return {
    products: (data || []) as ProductResponse[],
    isLoading,
  };
}
