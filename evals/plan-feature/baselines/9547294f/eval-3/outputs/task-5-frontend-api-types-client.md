# Task 5 — Add API types and client function for SBOM comparison

## Repository
trustify-ui

## Target Branch
TC-9003

## Description
Add TypeScript interfaces for the SBOM comparison API response and the API client function to call the backend comparison endpoint. This provides the data layer that the comparison page components will consume via React Query.

## Files to Modify
- `src/api/models.ts` — Add TypeScript interfaces: SbomComparisonResult, AddedPackage, RemovedPackage, VersionChange, NewVulnerability, ResolvedVulnerability, LicenseChange
- `src/api/rest.ts` — Add `fetchSbomComparison(leftId: string, rightId: string): Promise<SbomComparisonResult>` function

## Files to Create
- `src/hooks/useSbomComparison.ts` — React Query hook `useSbomComparison(leftId?: string, rightId?: string)` that calls fetchSbomComparison and is enabled only when both IDs are provided

## Implementation Notes

### TypeScript interfaces

Define interfaces matching the backend response shape exactly:

```typescript
export interface SbomComparisonResult {
  added_packages: AddedPackage[];
  removed_packages: RemovedPackage[];
  version_changes: VersionChange[];
  new_vulnerabilities: NewVulnerability[];
  resolved_vulnerabilities: ResolvedVulnerability[];
  license_changes: LicenseChange[];
}

export interface AddedPackage {
  name: string;
  version: string;
  license: string;
  advisory_count: number;
}

// ... similar for other sub-types
```

### API client function

Follow the existing pattern in `src/api/rest.ts` (e.g., `fetchSboms()`):

```typescript
export const fetchSbomComparison = (leftId: string, rightId: string): Promise<SbomComparisonResult> => {
  return client.get(`/api/v2/sbom/compare`, { params: { left: leftId, right: rightId } })
    .then((response) => response.data);
};
```

### React Query hook

Follow the existing hook pattern in `src/hooks/useSboms.ts`:

```typescript
export const useSbomComparison = (leftId?: string, rightId?: string) => {
  return useQuery({
    queryKey: ["sbom-comparison", leftId, rightId],
    queryFn: () => fetchSbomComparison(leftId!, rightId!),
    enabled: !!leftId && !!rightId,
  });
};
```

### Backend API contracts

- `GET /api/v2/sbom/compare?left={id}&right={id}` — response shape: `SbomComparisonResult` as defined above (see `modules/fundamental/src/sbom/endpoints/compare.rs` in trustify-backend)

Verify these contracts against the backend repo during implementation using the implement-task cross-repo API verification step.

### Reuse candidates

- `src/api/rest.ts::fetchSboms` — existing API client function pattern for GET requests with Axios
- `src/api/models.ts` — existing TypeScript interface definitions for API types
- `src/hooks/useSboms.ts` — existing React Query hook pattern with useQuery
- `src/hooks/useSbomById.ts` — existing hook with single-entity query pattern
- `src/api/client.ts` — Axios instance with base URL and auth interceptors

Per CONVENTIONS.md: use React Query (TanStack Query) for server state; API client functions go in `src/api/rest.ts`; hooks go in `src/hooks/`.
Applies: task modifies `src/api/rest.ts` matching the convention's TypeScript API layer scope.

## Acceptance Criteria
- [ ] TypeScript interfaces compile and match the backend SbomComparisonResult response shape
- [ ] fetchSbomComparison function calls the correct endpoint with left and right query parameters
- [ ] useSbomComparison hook is disabled when either ID is missing
- [ ] useSbomComparison hook returns comparison data when both IDs are provided

## Test Requirements
- [ ] Unit test: useSbomComparison hook returns data with MSW mock for the comparison endpoint
- [ ] Unit test: useSbomComparison hook is not enabled when leftId is undefined
- [ ] Unit test: useSbomComparison hook is not enabled when rightId is undefined

## Dependencies
- Depends on: Task 1 — Create feature branch TC-9003 from main
- Depends on: Task 3 — Add SBOM comparison REST endpoint (API contract dependency)

---
Priority: Critical
Fix Versions: RHTPA 1.5.0
Labels: ai-generated-jira

[sdlc-workflow] Description digest: sha256-md:e7b1d5c9f4a0683b2e8f1c5d7a9b3e6f0c4d8a2b5e7f9c1d3a6b8e0f4c2d5a7b
