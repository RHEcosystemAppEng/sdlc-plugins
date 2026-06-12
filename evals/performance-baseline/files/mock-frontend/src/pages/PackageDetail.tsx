<!-- SYNTHETIC TEST DATA — Package detail page with GET + POST API calls for tracing eval -->
import { useParams } from 'react-router-dom';
import { useQuery } from '@tanstack/react-query';

export default function PackageDetail() {
  const { id } = useParams();
  const { data } = useQuery({
    queryKey: ['package', id],
    queryFn: () => fetch(`/api/v2/packages/${id}`).then(r => r.json()),
  });

  async function scanVulnerabilities() {
    await fetch(`/api/v2/packages/${id}/vulnerabilities`, { method: 'POST' });
  }

  return <div>{JSON.stringify(data)}<button onClick={scanVulnerabilities}>Scan</button></div>;
}
