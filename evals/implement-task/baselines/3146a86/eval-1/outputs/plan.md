# Implementation Plan — TC-9201
## Add advisory severity aggregation service and endpoint

---

## Step 0 – Project Configuration Validation

All required sections verified in `claude-md-mock.md`:
- `## Repository Registry` — present (trustify-backend, serena_backend, path `./`)
- `## Jira Configuration` — present (Project key TC, Cloud ID, Feature issue type ID)
- `## Code Intelligence` — present with tool naming convention

Serena instance for this repo: `serena_backend`. Tools called as `mcp__serena_backend__<tool>`.

---

## Step 1 – Task Parsed

| Field | Value |
|---|---|
| Jira ID | TC-9201 |
| Repository | trustify-backend |
| Target Branch | main |
| Branch name | TC-9201 |
| Dependencies | None |
| Bookend Type | (none) |
| Target PR | (none) |

---

## Step 4 – Code Inspection Summary

### CONVENTIONS.md
Located at `trustify-backend/CONVENTIONS.md`. Read and followed. No explicit CI check commands section found — fall back to `cargo build` + `cargo test` for Step 9 verification.

### Files to Modify — symbols inspected via mcp__serena_backend__get_symbols_overview

**`modules/fundamental/src/advisory/service/advisory.rs`**
- Contains `AdvisoryService` struct with `fetch` (single-entity lookup) and `list` (paginated list) async methods.
- Both accept `(&self, ..., tx: &Transactional<'_>)` and return `Result<Option<T>, anyhow::Error>` or `Result<PaginatedResults<T>, anyhow::Error>`.
- New method `severity_summary` follows the same signature.

**`modules/fundamental/src/advisory/endpoints/mod.rs`**
- Contains a `router()` function returning a `Router` with existing `.route("/api/v2/advisory", get(list))` and `.route("/api/v2/advisory/{id}", get(get))` registrations.
- New route `/api/v2/sbom/{id}/advisory-summary` added here.

**`modules/fundamental/src/advisory/model/mod.rs`**
- Contains `pub mod summary;` and `pub mod details;`.
- Need to add `pub mod severity_summary;`.

### Sibling files inspected for convention conformance

**`modules/fundamental/src/advisory/endpoints/get.rs`** (endpoint sibling):
- Handler: `pub async fn get_advisory(Path(id): Path<Id>, State(service): State<Arc<AdvisoryService>>) -> Result<Json<AdvisoryDetails>, AppError>`
- Calls `service.fetch(id, Transactional::None).await.context("...")?`
- Returns 404 via `AppError::NotFound(...)` when service returns `None`

**`modules/fundamental/src/advisory/model/summary.rs`** (model sibling):
- `AdvisorySummary` struct derives `Serialize, Deserialize, ToSchema`
- Has a `pub severity: String` field that indicates severity is already tracked per advisory

**`entity/src/sbom_advisory.rs`** (join table):
- `Model` has `sbom_id: Uuid` and `advisory_id: Uuid` columns
- Enables filtering advisories for a given SBOM and deduplicating by `advisory_id`

**`tests/api/advisory.rs`** (test sibling):
- `test_<feature>_<scenario>` naming convention
- `assert_eq!(resp.status(), StatusCode::OK)` + body deserialization + per-field assertions
- Includes 404 test with non-existent UUID

### Cross-section reference consistency check

Scanned all sections of TC-9201 for entity-to-file-path references:

| Entity | Files to Modify | Implementation Notes | Consistent? |
|---|---|---|---|
| AdvisoryService | `modules/fundamental/src/advisory/service/advisory.rs` | `modules/fundamental/src/advisory/service/advisory.rs` | Yes |
| endpoints/mod.rs | `modules/fundamental/src/advisory/endpoints/mod.rs` | `modules/fundamental/src/advisory/endpoints/mod.rs` | Yes |
| model/mod.rs | `modules/fundamental/src/advisory/model/mod.rs` | implied by module pattern | Yes |
| AdvisorySummary | read-only reference in impl notes | `modules/fundamental/src/advisory/model/summary.rs` | Yes — not modified |

No inconsistencies detected.

### Duplication check
Searched for `severity_count`, `severity_summary`, `count_by_severity` — no existing equivalent found. Implementation is greenfield.

### Documentation files identified
- `docs/api.md` — will add entry for `GET /api/v2/sbom/{id}/advisory-summary` during Step 6 documentation impact evaluation.

---

## Step 5 – Branch Strategy

```bash
git checkout main
git pull
git checkout -b TC-9201
```

---

## Files to Modify (3)

1. `modules/fundamental/src/advisory/model/mod.rs`
   — Add `pub mod severity_summary;`
   — Detail: file-1-model-mod.md

2. `modules/fundamental/src/advisory/service/advisory.rs`
   — Add `severity_summary` async method to `AdvisoryService`
   — Detail: file-2-service.md

3. `modules/fundamental/src/advisory/endpoints/mod.rs`
   — Import and register the new severity_summary handler
   — Detail: file-3-endpoints-mod.md

## Files to Create (3)

4. `modules/fundamental/src/advisory/model/severity_summary.rs`
   — `SeveritySummary` response struct
   — Detail: file-4-model-severity-summary.md

5. `modules/fundamental/src/advisory/endpoints/severity_summary.rs`
   — GET handler for `/api/v2/sbom/{id}/advisory-summary`
   — Detail: file-5-endpoint-handler.md

6. `tests/api/advisory_summary.rs`
   — Integration tests (4 test functions)
   — Detail: file-6-tests.md

---

## Step 9 Self-Verification Checklist

- [ ] `git diff --name-only` — confirm exactly 6 paths, no extras
- [ ] `git status --short` — check for untracked files in touched dirs
- [ ] Sensitive-pattern grep on staged diff (no passwords/keys)
- [ ] `cargo build` — zero new errors/warnings
- [ ] `cargo test --test advisory_summary` — 4 tests pass
- [ ] Data-flow trace: HTTP request → handler → service method → DB query → response (all stages connected)
- [ ] Contract parity: handler shape matches `get.rs` sibling (Path + State extractors, `Result<Json<T>, AppError>`)
- [ ] `docs/api.md` updated with new endpoint entry

---

## Step 10 – Commit and Push

### Commit message

```
feat(api): add advisory severity aggregation endpoint for SBOM

Add SeveritySummary response struct, AdvisoryService::severity_summary
method, and GET /api/v2/sbom/{id}/advisory-summary endpoint. Returns
per-severity counts (critical, high, medium, low) and a total, enabling
dashboard widgets to render severity breakdowns without client-side
counting. Deduplicates advisory links via DISTINCT on advisory_id.

Implements TC-9201
```

### Full git command

```bash
git commit \
  --trailer="Assisted-by: Claude Code" \
  -m "feat(api): add advisory severity aggregation endpoint for SBOM

Add SeveritySummary response struct, AdvisoryService::severity_summary
method, and GET /api/v2/sbom/{id}/advisory-summary endpoint. Returns
per-severity counts (critical, high, medium, low) and a total, enabling
dashboard widgets to render severity breakdowns without client-side
counting. Deduplicates advisory links via DISTINCT on advisory_id.

Implements TC-9201"
```

### Push and PR creation

```bash
git push -u origin TC-9201

gh pr create --base main \
  --title "feat(api): add advisory severity aggregation endpoint for SBOM" \
  --body "$(cat <<'EOF'
## Summary

- Add `SeveritySummary` struct in `modules/fundamental/src/advisory/model/severity_summary.rs`
- Add `AdvisoryService::severity_summary` method in `modules/fundamental/src/advisory/service/advisory.rs`
- Register `GET /api/v2/sbom/{id}/advisory-summary` in `modules/fundamental/src/advisory/endpoints/`
- Integration tests in `tests/api/advisory_summary.rs`: valid SBOM, 404, all-zeros, deduplication

Implements [TC-9201](https://redhat.atlassian.net/browse/TC-9201)
EOF
)"
```

---

## Step 11 – Jira Updates

1. Update `customfield_10875` (Git Pull Request custom field) with ADF inlineCard containing the PR URL.
2. Add comment to TC-9201 with PR link and change summary.
3. Transition TC-9201 → In Review.
