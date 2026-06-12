# performance-analyze-module evals

Evaluates the performance analysis skill's ability to detect anti-patterns, validate findings, enforce the progress completion gate, and halt on missing prerequisites.

## Test cases

| ID | Name | Tests |
|---|---|---|
| 1 | Frontend-only happy path | Frontend detection + validation + report (≥2 confirmed findings) |
| 2 | Hybrid analysis | Frontend + backend detection, query ledger, cross-layer analysis |
| 3 | Progress gate enforcement | Pre-seeded progress with Step 6.5 pending — gate completes step with findings ≥ 1 |
| 4 | False positive rejection | SeaORM `load_one` batch call vs true N+1 — validation discards false positive |
| 5 | Missing config halt | No performance config → halt, suggest `performance-setup` |
| 6 | Missing baseline halt | Config present, baseline missing → halt, suggest `performance-baseline` |

## Output layout

Evals use the same flat pattern as `performance-setup` evals. All artifacts are written under the target repository tree:

```
outputs/
└── mock-repo/                    # or mock-backend/ for eval 4
    ├── performance-config.json
    └── performance/
        ├── baselines/
        └── analysis/
            ├── analysis-progress.json
            ├── findings-validation.json
            ├── workflow-analysis-report.md
            └── query-ledger.json
```

Stop-path evals (5–6) write halt messages to `outputs/response.md` and must not produce analysis artifacts.

## Fixtures

- `files/mock-repo/` — React+Vite frontend with planted anti-patterns in `.tsx` files
- `files/mock-backend/` — Rust/actix-web backend with planted issues in `.rs` files
- Config files at `files/mock-repo/performance/config-*.json` and `files/mock-backend/performance/config-backend-only.json`
- Baseline data at `files/mock-repo/performance/baselines/` and `files/mock-backend/performance/baselines/`
- Pre-seeded progress file at `files/pre-seeded-progress.json` (Eval 3)
- Unused-import target at `files/mock-repo/src/utils/unused-imports.ts` (Eval 3 Step 6.5)

## Planted patterns

| Location | Step | Pattern |
|---|---|---|
| `Dashboard.tsx` | 6.2 | N+1 fetch in loop |
| `Dashboard.tsx` / `HeavyChart.tsx` | 6.9 | Missing lazy loading |
| `Dashboard.tsx` | 6.5 | Unused imports from `unused-imports.ts` |
| `useProducts.ts` | 6.1 | Over-fetching (3 of 12 fields used) |
| `products.rs::list_products` | 7.4 | Missing pagination |
| `products.rs::get_product_details` | 7.3 | True N+1 sequential queries |
| `product.rs::load_product_vendors` | 7.3 | False positive (SeaORM `load_one` batch) |

## Running

```
/sdlc-workflow:run-evals Run evals for performance-analyze-module.
Evals path: evals/performance-analyze-module/evals.json
Workspace: /tmp/performance-analyze-module-eval
```

## Notes

- Evals use grep-based detection (no Serena) — assertions account for Medium confidence
- No live SQL, Jira, or server startup — all fixture-based
- Eval 4 specifically tests the Step 9.1-B2 technology-specific invalidator for SeaORM batch semantics
- Phase 0 (first end-to-end run + baseline commit) is required before assertion hardening beyond current checks
