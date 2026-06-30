// SYNTHETIC TEST DATA — Planted unused exports for Step 6.5 eval
export function formatCurrency(value: number): string {
  return `$${value.toFixed(2)}`;
}

export function parseTimestamp(iso: string): Date {
  return new Date(iso);
}

export function deepClone<T>(obj: T): T {
  return JSON.parse(JSON.stringify(obj));
}

export const DEFAULT_PAGE_SIZE = 25;
