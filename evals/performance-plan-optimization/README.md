# performance-plan-optimization evals

Evaluates the optimization planning skill's ability to read analysis reports, apply the decision framework, generate optimization plans, and produce mock Jira artifacts.

See [IMPROVEMENT-PLAN.md](IMPROVEMENT-PLAN.md) for the gate workflow and backlog.

## Test cases

| ID | Name | Tests |
|---|---|---|
| 1 | Mixed recommendations with db-migration | 6 findings with mixed dispositions. Verifies plan + Jira mock output, task count range (3–6), db-migration labels, CAUTION safeguards, deferred/rejected documentation, hedged impact language, and layer labels. |
| 2 | Zero actionable findings | All 3 findings discarded during validation. Skill halts with `outputs/response.md`; no plan or Jira artifacts. |
| 3 | Unvalidated report | `validation_run` is false. Skill halts at validation check with `outputs/response.md`; no plan or Jira artifacts. |

## Fixtures

- `files/config-fullstack.json` — Full-stack performance config (actix-web + SeaORM backend, `backend.path: ../mock-backend`)
- `files/analysis-report-mixed.md` — Mock analysis report with 6 findings (mixed dispositions)
- `files/findings-validation-mixed.json` — Validation artifact with 5 Confirmed + 1 Downgraded
- `files/analysis-report-zero.md` — Mock analysis report with all findings discarded
- `files/findings-validation-zero.json` — Validation artifact with 3 Discarded findings
- `files/findings-validation-unvalidated.json` — Validation artifact with `validation_run: false`
- `files/conventions-rust.md` — Rust/SeaORM migration conventions for db-migration task generation
- `files/mock-repo/` — Frontend source stubs for Step 5 grep (F2 N+1, F6 layout thrashing)
- `files/mock-backend/` — Backend source stubs for Step 5 grep (F1 over-fetch, F3 missing index, F4 deep chain, F5 unused JOIN)

## Running

```
/sdlc-workflow:run-evals performance-plan-optimization
```

Evals path: `evals/performance-plan-optimization/evals.json`

## Notes

- All evals mock Jira output to JSON files instead of calling Jira MCP
- Outputs use the skill's canonical layout under `outputs/mock-repo/performance/`
- Stop-path evals write halt messages to `outputs/response.md` (graders read files, not chat)
- db-migration script generation (Step 5.5) is not asserted until gate passes and migration assertions are added
