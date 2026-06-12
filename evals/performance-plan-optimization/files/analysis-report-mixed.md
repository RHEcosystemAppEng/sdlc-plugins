<!-- SYNTHETIC TEST DATA — DO NOT USE IN PRODUCTION -->

# Performance Analysis Report

**Generated:** 2026-06-09T10:30:00Z
**Workflow:** package-listing
**Baseline Date:** 2026-06-08T14:00:00Z
**Validation Artifact:** `performance/analysis/findings-validation.json`
**Validation Status:** passed

---

## Workflow Metrics

| Metric | Current (p95) | Target | Status |
|---|---|---|---|
| LCP (Largest Contentful Paint) | 3400 ms | 2500 ms | Needs Improvement |
| FCP (First Contentful Paint) | 2200 ms | 1800 ms | Needs Improvement |
| DOM Interactive | 4800 ms | 3500 ms | Needs Improvement |
| Total Load Time | 6100 ms | 4000 ms | Needs Improvement |

---

## Bundle Composition

**Total JavaScript Size:** 1080 KB
**Third-Party Libraries:** 800 KB (74%)
**Application Code:** 280 KB (26%)

**Top Third-Party Libraries by Size:**

| Library | Size | Used In |
|---|---|---|
| chart.js | 350 KB | /packages/:id |
| lodash | 120 KB | /packages, /packages/:id |
| moment.js | 95 KB | /packages |

---

## Finding Validation Summary

**Validation Step:** Step 9.1 re-verified all findings against source code before report generation.

| # | Finding | Anti-Pattern | Step | Disposition | Confidence | Severity | Timeline | Notes |
|---|---|---|---|---|---|---|---|---|
| F1 | API response includes 50KB of unused advisory metadata | Over-Fetching | 8.A | Confirmed | Medium | Low | 1-4 hours | Response includes full advisory objects but frontend only uses id and title |
| F2 | Sequential fetch calls for package details in listing loop | N+1 Frontend Query | 6.3 | Confirmed | High | Low | 1-3 days | 5 sequential fetches in useEffect loop instead of batch endpoint |
| F3 | Missing index on advisories.package_id column | Missing Index | 7.6.4 | Confirmed | High | High | 1-4 hours | WHERE clause filters on package_id without index; sequential scan on 120K rows |
| F4 | 3-level deep service chain through advisory resolver | Deep Service Chain | 7.6.2 | Downgraded | Medium | Low | 1-3 days | Chain depth verified but effective query count lower than estimated |
| F5 | Unused LEFT JOIN on package_metadata table | Unused JOINs | 7.6.5 | Confirmed | Medium | Low | 1-4 hours | JOIN fetches metadata but handler only returns name and version |
| F6 | DOM reads/writes interleaved in package card render loop | Layout Thrashing | 6.4 | Confirmed | Medium | Low | 0.5-1 day | offsetHeight read followed by style.height write inside map() |

**Validation Statistics:**
- Findings submitted: 6
- Confirmed: 5 (83%)
- Confirmed (Low Confidence): 0 (0%)
- Downgraded: 1 (17%)
- Discarded: 0 (0%)

---

## Anti-Pattern Analysis

### Over-Fetching

**Severity:** Low
**Confidence:** Medium (Grep -- response field analysis)
**Instances Found:** 1
**Estimated Impact:** ~50 KB payload reduction per request, estimated up to 12% load time improvement

**Description:**
The backend API returns full advisory objects in the package listing response, but the frontend only destructures `id` and `title` from each advisory. The remaining fields (description, cvss_score, affected_versions, references, timestamps) are transferred but never rendered.

**Detected Instances:**

1. **src/handlers/packages.rs:19**
   **Finding ID:** F1
   ```rust
   let advisories = advisory::Entity::find()
       .filter(advisory::Column::PackageId.eq(pkg_id))
       .all(&db)
       .await?;
   // Returns full Advisory model with 12 fields
   ```
   **Issue:** Response includes 12 fields per advisory but frontend uses only 2 (id, title). Approx 50KB unused data per listing page.
   **Recommended Fix:** Create a `AdvisoryBriefDto` with only `id` and `title`, or implement field projection in the query.
   **Verification Checklist:**
   - [ ] Confirm frontend destructuring pattern in PackageList.tsx
   - [ ] Verify no other consumer uses the full advisory fields
   **Validation Status:** Confirmed
   **Confidence:** Medium -- "Detection: Grep, Evidence: Response schema vs frontend usage, Risk: Low => Final: Medium"
   **Severity:** Low
   **Timeline:** 1-4 hours

---

### N+1 Frontend Query

**Severity:** Low
**Confidence:** High (Grep -- clear sequential fetch pattern)
**Instances Found:** 1
**Estimated Impact:** Estimated up to 35% improvement in DOM Interactive time by batching 5 sequential requests

**Description:**
The package listing page fetches individual package details in a useEffect loop, creating 5 sequential network requests where a single batch request would suffice.

**Detected Instances:**

1. **src/pages/PackageList.tsx:21**
   **Finding ID:** F2
   ```tsx
   useEffect(() => {
     packages.forEach(async (pkg) => {
       const details = await fetch(`/api/v1/packages/${pkg.id}`);
       setPackageDetails(prev => [...prev, await details.json()]);
     });
   }, [packages]);
   ```
   **Issue:** 5 sequential fetch calls in forEach loop. Each call waits for the previous to complete due to state update pattern.
   **Recommended Fix:** Use `Promise.all()` with a batch endpoint `/api/v1/packages?ids=1,2,3,4,5` or parallelize with `Promise.all(packages.map(...))`.
   **Verification Checklist:**
   - [ ] Verify the forEach pattern is not already parallelized
   - [ ] Check if a batch endpoint exists
   **Validation Status:** Confirmed
   **Confidence:** High -- "Detection: Grep, Evidence: Sequential forEach with await, Risk: Low => Final: High"
   **Severity:** Low
   **Timeline:** 1-3 days

---

### Missing Database Indexes

**Severity:** High
**Confidence:** High (Grep -- migration file analysis)
**Instances Found:** 1
**Estimated Impact:** Estimated up to 22% improvement in backend response time (p95); index lookup vs sequential scan on 120K rows

**Description:**
The `advisories` table is queried with a WHERE clause on `package_id`, but no index exists on that column. This causes PostgreSQL to perform a sequential scan on 120,000 rows.

**Detected Instances:**

1. **Table:** `advisories`
   **Column:** `package_id`
   **Table Source:** `migration/src/m20260101_000001_create_advisories.rs`
   **Used In:** Advisory lookup by package (`src/handlers/advisories.rs:10`)
   **Query Type:** WHERE filter
   **Loop Multiplier:** 1 (single query per request)
   **Finding ID:** F3
   **Estimated Impact:** Sequential scan on 120,000 rows vs. index lookup
   **Recommended Fix:**
   ```sql
   CREATE INDEX idx_advisories_package_id ON advisories(package_id);
   ```
   **Verification Checklist:**
   - [ ] Verify no existing index covers this column
   - [ ] Run EXPLAIN ANALYZE on the query before and after
   **Validation Status:** Confirmed
   **Confidence:** High -- "Detection: Grep, Evidence: Migration files show no index, Risk: Medium => Final: High"
   **Severity:** High
   **Timeline:** 1-4 hours

---

### Deep Service Chain

**Severity:** Low
**Confidence:** Medium (Grep -- call graph analysis)
**Instances Found:** 1
**Estimated Impact:** Estimated up to 8% improvement in response time by flattening call chain

**Description:**
The advisory resolution endpoint passes through 3 service layers, each adding a database query. While the chain is real, the effective query count after downgrade is lower than initially estimated.

**Detected Instances:**

1. **src/handlers/advisories.rs:11**
   **Finding ID:** F4
   ```rust
   pub async fn get_advisories(db: &DatabaseConnection, pkg_id: i32) -> Result<Vec<Advisory>> {
       let pkg = package::Entity::find_by_id(pkg_id).one(&db).await?;
       let advisories = advisory_service::resolve_advisories(&db, &pkg).await?;
       let enriched = enrichment_service::enrich(&db, &advisories).await?;
       Ok(enriched)
   }
   ```
   **Issue:** 3-level chain: handler -> advisory_service -> enrichment_service, each with DB queries
   **Recommended Fix:** Combine queries into a single JOIN query or use batch loading
   **Verification Checklist:**
   - [ ] Trace full call chain to count actual queries
   - [ ] Verify enrichment queries cannot be batched
   **Validation Status:** Downgraded
   **Confidence:** Medium -- "Detection: Grep, Evidence: Call chain verified but effective count lower, Risk: Medium => Final: Medium"
   **Severity:** Low (downgraded from Medium)
   **Timeline:** 1-3 days

---

### Unused Table Joins

**Severity:** Low
**Confidence:** Medium (Grep -- query and response analysis)
**Instances Found:** 1
**Estimated Impact:** Estimated up to 3% improvement in query time by removing unnecessary JOIN

**Description:**
The package listing query includes a LEFT JOIN on `package_metadata` but the handler only returns `name` and `version` from the packages table. The joined metadata fields are never accessed.

**Detected Instances:**

1. **Endpoint:** GET /api/v1/packages
   **Handler:** src/handlers/packages.rs:7
   **Finding ID:** F5
   **Query:**
   ```rust
   let packages = package::Entity::find()
       .find_also_related(package_metadata::Entity)
       .all(&db)
       .await?;
   // Only pkg.name and pkg.version used in response
   ```
   **Unused Join:** `package_metadata` (via find_also_related)
   **Reason:** No fields from `package_metadata` accessed in SELECT or response schema
   **Join Type:** LEFT JOIN
   **Table Size:** 45,000 rows
   **Index Status:** Indexed on foreign key
   **Estimated Overhead:** 3ms per query
   **Call Frequency:** single
   **Total Impact:** 3ms per request
   **Recommended Fix:**
   ```rust
   let packages = package::Entity::find()
       .all(&db)
       .await?;
   ```
   **Verification Checklist:**
   - [ ] Confirm package_metadata fields are not used anywhere in response construction
   - [ ] Verify no downstream logic depends on the joined data
   **Validation Status:** Confirmed
   **Confidence:** Medium -- "Detection: Grep, Evidence: Response construction analysis, Risk: Low => Final: Medium"
   **Severity:** Low
   **Timeline:** 1-4 hours

---

### Layout Thrashing

**Severity:** Low
**Confidence:** Medium (Grep -- DOM read/write pattern)
**Instances Found:** 1
**Estimated Impact:** Estimated up to 40% improvement in render performance for package card list by batching DOM operations

**Description:**
The package card rendering loop interleaves DOM reads and writes, forcing the browser to perform layout recalculation on each iteration.

**Detected Instances:**

1. **src/components/PackageCard.tsx:20**
   **Finding ID:** F6
   ```tsx
   {packages.map((pkg, i) => {
     const height = cardRef.current[i]?.offsetHeight; // DOM read
     if (height && height < 200) {
       cardRef.current[i].style.height = '200px'; // DOM write
     }
     return <PackageCardItem key={pkg.id} package={pkg} />;
   })}
   ```
   **Issue:** `offsetHeight` read followed by `style.height` write inside `map()` loop. Each iteration triggers forced synchronous layout.
   **Recommended Fix:** Batch all reads first using `requestAnimationFrame` or `ResizeObserver`, then apply writes in a separate pass.
   **Verification Checklist:**
   - [ ] Confirm the interleaved read/write pattern exists in production code
   - [ ] Verify the component renders in a list context
   **Validation Status:** Confirmed
   **Confidence:** Medium -- "Detection: Grep, Evidence: Clear read-write interleave in loop, Risk: Low => Final: Medium"
   **Severity:** Low
   **Timeline:** 0.5-1 day

---

## Backend Source Code Analysis

**Backend Repository:** package-listing-api (actix-web)
**Analysis Coverage:** 3 endpoints analyzed
**Serena Status:** Grep fallback

### Backend Anti-Patterns Detected

See findings F1, F3, F4, F5 above for backend-specific anti-patterns (Over-Fetching, Missing Index, Deep Service Chain, Unused JOINs).

---

## Recommended Optimizations

**Note:** Optimizations are categorized by layer (Frontend / Backend / Integration) when backend analysis is available.

### Tactical Optimizations

| Priority | Optimization | Confidence | Severity | Timeline | Prerequisite | Estimated Impact | Effort |
|---|---|---|---|---|---|---|---|
| 1 | F6: Batch DOM reads/writes in PackageCard render loop | Medium | Low | 0.5-1 day | None | Estimated up to 40% render improvement | Low |
| 2 | F2: Replace sequential fetches with batch/parallel pattern | High | Low | 1-3 days | None | Estimated up to 35% DOM Interactive improvement | Medium |
| 3 | F3: Add index on advisories.package_id | High | High | 1-4 hours | None | Estimated up to 22% backend p95 improvement | Low |
| 4 | F1: Create AdvisoryBriefDto for listing endpoint | Medium | Low | 1-4 hours | None | Estimated up to 12% load time improvement | Low |
| 5 | F4: Flatten advisory resolution service chain | Medium | Low | 1-3 days | F3 | Estimated up to 8% response time improvement | Medium |
| 6 | F5: Remove unused package_metadata JOIN | Medium | Low | 1-4 hours | None | Estimated up to 3% query time improvement | Low |

### Strategic / Architectural Optimizations

No strategic/architectural optimizations identified -- tactical fixes are sufficient to reach target SLAs.

---

## Executive Summary

**Overall Performance Rating:** Needs Improvement

**Key Findings:**
- Frontend N+1 fetch pattern causes 5 sequential requests on package listing page
- Missing database index on advisories.package_id causes sequential scans on 120K rows
- Layout thrashing in package card rendering degrades render performance
- Backend over-fetching transfers ~50KB of unused advisory data per request

**Top 3 Optimization Opportunities:**
1. Layout Thrashing fix (F6) -- Estimated up to 40% render improvement
2. N+1 Frontend Query fix (F2) -- Estimated up to 35% DOM Interactive improvement
3. Missing Index fix (F3) -- Estimated up to 22% backend p95 improvement

---

## Next Steps

1. Review this report with the team and prioritize optimizations
2. Create optimization plan and Jira Epic/Tasks using `/sdlc-workflow:performance-plan-optimization`
3. After implementing optimizations, re-run `/sdlc-workflow:performance-baseline` to capture new baseline and measure improvements
