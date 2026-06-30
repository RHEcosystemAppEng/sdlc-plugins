<!-- SYNTHETIC TEST DATA — Package list page with planted GET API call for tracing eval -->
import { useQuery } from '@tanstack/react-query';

export default function Packages() {
  const { data: packages } = useQuery({
    queryKey: ['packages'],
    queryFn: () => fetch('/api/v2/packages').then(r => r.json()),
  });
  return <div>{JSON.stringify(packages)}</div>;
}
