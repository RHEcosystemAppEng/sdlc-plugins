# Repository Impact Map — TC-9003: SBOM Comparison View

## Field Inheritance

| Field | Value | Inherited From |
|---|---|---|
| Priority | Critical | TC-9003 |
| Fix Versions | RHTPA 1.5.0 | TC-9003 |

All tasks inherit Priority: Critical and Fix Versions: RHTPA 1.5.0 from the parent feature TC-9003.

## Workflow Mode

**Direct-to-main** — All tasks target `main` branch.

**Rationale:** The backend changes are purely additive (new `GET /api/v2/sbom/compare` endpoint with no schema migrations, no breaking changes to existing endpoints, no new database tables). The frontend changes are also primarily additive (new comparison page and route). The only modification to existing code is adding selection checkboxes and a "Compare selected" button to the SBOM list page, which does not alter existing behavior. Cross-repo feature branches are impractical since trustify-backend and trustify-ui are separate repositories with independent deployment cycles. Natural task ordering (backend first, then frontend) handles coordination.

## Repository: trustify-backend

### Impact Summary
New SBOM comparison module following the existing `model/ + service/ + endpoints/` pattern within `modules/fundamental/src/sbom/`.

### Files Created
| File | Task | Purpose |
|---|---|---|
| `modules/fundamental/src/sbom/model/comparison.rs` | Task 1 | Comparison result model types |
| `modules/fundamental/src/sbom/service/compare.rs` | Task 2 | Comparison diffing service logic |
| `modules/fundamental/src/sbom/endpoints/compare.rs` | Task 3 | HTTP handler for comparison endpoint |
| `tests/api/sbom_compare.rs` | Task 3 | Integration tests |

### Files Modified
| File | Task | Change |
|---|---|---|
| `modules/fundamental/src/sbom/model/mod.rs` | Task 1 | Export comparison module |
| `modules/fundamental/src/sbom/service/mod.rs` | Task 2 | Export compare service module |
| `modules/fundamental/src/sbom/endpoints/mod.rs` | Task 3 | Register /compare route |

### API Changes
| Endpoint | Task | Type | Description |
|---|---|---|---|
| `GET /api/v2/sbom/compare?left={id1}&right={id2}` | Task 3 | NEW | Returns structured diff between two SBOMs |

### Architecture Notes
- No new database tables — diff is computed on-the-fly from existing package and advisory data
- Follows existing module pattern: model types -> service logic -> endpoint handler
- Reuses existing SbomService, PackageService, and AdvisoryService for data access

## Repository: trustify-ui

### Impact Summary
New comparison page with supporting API layer, plus minor enhancement to the existing SBOM list page for compare entry point.

### Files Created
| File | Task | Purpose |
|---|---|---|
| `src/hooks/useSbomComparison.ts` | Task 4 | React Query hook for comparison API |
| `src/pages/SbomComparePage/SbomComparePage.tsx` | Task 5 | Main comparison page component |
| `src/pages/SbomComparePage/components/ComparisonToolbar.tsx` | Task 5 | Header toolbar with SBOM selectors |
| `src/pages/SbomComparePage/components/DiffSection.tsx` | Task 5 | Reusable expandable diff section |
| `src/pages/SbomComparePage/SbomComparePage.test.tsx` | Task 5 | Comparison page unit tests |
| `tests/mocks/fixtures/sbom-comparison.json` | Task 6 | Mock comparison data |
| `tests/e2e/sbom-compare.spec.ts` | Task 6 | E2E tests for comparison workflow |

### Files Modified
| File | Task | Change |
|---|---|---|
| `src/api/models.ts` | Task 4 | Add comparison TypeScript interfaces |
| `src/api/rest.ts` | Task 4 | Add fetchSbomComparison() client function |
| `src/routes.tsx` | Task 6 | Register /sbom/compare route |
| `src/pages/SbomListPage/SbomListPage.tsx` | Task 6 | Add row selection and Compare button |

### Architecture Notes
- Follows existing page structure: page directory with main component + components/ subdirectory
- API layer follows existing pattern: models.ts types -> rest.ts client -> hooks/ React Query hook
- Reuses existing SeverityBadge, FilterToolbar, and useSboms from the codebase

## Task Dependency Graph

```
Task 1 (backend model)
  └─> Task 2 (backend service)
        └─> Task 3 (backend endpoint + tests)
              └─> Task 4 (frontend API layer)  [cross-repo dependency]
                    └─> Task 5 (frontend comparison page)
                          └─> Task 6 (frontend route + list integration)
```

## Risk Assessment
- **Performance**: Comparison of SBOMs with 2000+ packages may approach the 1s p95 target. The service should use efficient set operations (HashMaps by package name) rather than nested iterations.
- **Large diffs**: The Figma design specifies virtualized lists for >100 changed packages. Task 5 should consider react-window or similar for table virtualization.
- **Cross-repo coordination**: Backend must be deployed before frontend comparison page is useful. Deployment ordering is the responsibility of the release process.
