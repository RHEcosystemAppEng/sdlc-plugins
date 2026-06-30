# Impact Map: TC-9003 — SBOM Comparison View

## trustify-backend

### New Files
| File | Created By Task | Purpose |
|---|---|---|
| `modules/fundamental/src/sbom/model/comparison.rs` | Task 2 | Comparison response model structs |
| `modules/fundamental/src/sbom/service/comparison.rs` | Task 3 | SBOM diff computation service |
| `modules/fundamental/src/sbom/endpoints/compare.rs` | Task 4 | GET /api/v2/sbom/compare handler |
| `tests/api/sbom_compare.rs` | Task 5 | Integration tests for comparison endpoint |

### Modified Files
| File | Modified By Task(s) | Change |
|---|---|---|
| `modules/fundamental/src/sbom/model/mod.rs` | Task 2 | Export comparison model module |
| `modules/fundamental/src/sbom/service/mod.rs` | Task 3 | Export comparison service module |
| `modules/fundamental/src/sbom/endpoints/mod.rs` | Task 4 | Register /compare route |
| `tests/Cargo.toml` | Task 5 | Add test module reference |

### API Changes
| Endpoint | Method | Task | Description |
|---|---|---|---|
| `/api/v2/sbom/compare?left={id1}&right={id2}` | GET | Task 4 | NEW: Returns structured SBOM comparison diff |

## trustify-ui

### New Files
| File | Created By Task | Purpose |
|---|---|---|
| `src/hooks/useSbomComparison.ts` | Task 6 | React Query hook for comparison API |
| `src/pages/SbomComparePage/SbomComparePage.tsx` | Task 7 | Main comparison page component |
| `src/pages/SbomComparePage/components/DiffSection.tsx` | Task 7 | Expandable diff section component |
| `src/pages/SbomComparePage/components/SbomSelector.tsx` | Task 7 | SBOM selector dropdown component |
| `src/pages/SbomComparePage/SbomComparePage.test.tsx` | Task 8 | Unit tests for comparison page |
| `tests/mocks/fixtures/sbom-comparison.json` | Task 8 | Mock comparison response fixture |

### Modified Files
| File | Modified By Task(s) | Change |
|---|---|---|
| `src/api/models.ts` | Task 6 | Add comparison TypeScript interfaces |
| `src/api/rest.ts` | Task 6 | Add compareSboms() API client function |
| `src/routes.tsx` | Task 7 | Add /sbom/compare route |
| `src/App.tsx` | Task 7 | Add lazy import for SbomComparePage |
| `tests/mocks/handlers.ts` | Task 8 | Add MSW handler for comparison endpoint |
