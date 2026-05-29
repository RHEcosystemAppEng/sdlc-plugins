# Implementation Plan for TC-9201

## Task Summary

Add an advisory severity aggregation service method and REST endpoint that returns counts per severity level (Critical, High, Medium, Low) and a total for a given SBOM.

## Parsed Task Fields

- **Jira ID**: TC-9201
- **Repository**: trustify-backend
- **Target Branch**: main
- **Target PR**: none (default flow -- create new branch and PR)
- **Bookend Type**: none (normal implementation)
- **Dependencies**: None
- **Linked Issues**: is incorporated by TC-9001
- **webUrl**: `https://redhat.atlassian.net/browse/TC-9201`

## Branch Strategy

- Branch name: `TC-9201` (named after Jira issue ID per conventions)
- Base branch: `main` (from Target Branch field)
- Commands:
  ```
  git checkout main
  git pull
  git checkout -b TC-9201
  ```

## Files to Create

1. **`modules/fundamental/src/advisory/model/severity_summary.rs`** -- SeveritySummary response struct
2. **`modules/fundamental/src/advisory/endpoints/severity_summary.rs`** -- GET handler for `/api/v2/sbom/{id}/advisory-summary`
3. **`tests/api/advisory_summary.rs`** -- Integration tests for the new endpoint

## Files to Modify

1. **`modules/fundamental/src/advisory/service/advisory.rs`** -- Add `severity_summary` method to AdvisoryService
2. **`modules/fundamental/src/advisory/endpoints/mod.rs`** -- Register the new route
3. **`modules/fundamental/src/advisory/model/mod.rs`** -- Add `pub mod severity_summary;` to register new model module

## Files NOT Modified (confirmed)

- **`server/src/main.rs`** -- No changes needed; routes auto-mount via module registration

## Pre-Implementation Inspection Plan

Using Serena instance `serena_backend` (from Repository Registry):

1. `mcp__serena_backend__get_symbols_overview` on:
   - `modules/fundamental/src/advisory/service/advisory.rs` -- understand existing `fetch`, `list`, `search` method signatures
   - `modules/fundamental/src/advisory/endpoints/get.rs` -- understand endpoint handler pattern
   - `modules/fundamental/src/advisory/endpoints/mod.rs` -- understand route registration pattern
   - `modules/fundamental/src/advisory/model/summary.rs` -- see `AdvisorySummary` struct and its `severity` field
   - `modules/fundamental/src/advisory/model/mod.rs` -- see existing module registrations
   - `entity/src/sbom_advisory.rs` -- understand the join table structure

2. `mcp__serena_backend__find_symbol` with `include_body=true` on:
   - `AdvisoryService::fetch` -- to replicate the method pattern
   - `AdvisoryService::list` -- to replicate the method pattern
   - `AdvisorySummary` struct -- to see the `severity` field type and access pattern

3. `mcp__serena_backend__find_referencing_symbols` on:
   - `AdvisoryService` -- to confirm adding a method won't break existing consumers

4. Sibling analysis (convention conformance) on:
   - `modules/fundamental/src/advisory/endpoints/get.rs` and `list.rs` -- endpoint patterns
   - `modules/fundamental/src/sbom/endpoints/get.rs` -- cross-module endpoint pattern for comparison
   - `tests/api/advisory.rs` and `tests/api/sbom.rs` -- test patterns

5. Documentation file identification:
   - `README.md` at repo root
   - `docs/api.md` -- REST API reference
   - `docs/architecture.md` -- system architecture
   - `CONVENTIONS.md` at repo root

## Implementation Order

1. Create the `SeveritySummary` model struct (file-1)
2. Register the model module in `model/mod.rs` (file-4)
3. Add the `severity_summary` service method (file-3)
4. Create the endpoint handler (file-2)
5. Register the route in `endpoints/mod.rs` (file-5)
6. Write integration tests (file-6)
7. Run `cargo test` to verify
8. Self-verification checks (scope, sensitive patterns, data-flow trace, contract/sibling parity)

## Commit Message

```
feat(api): add advisory severity aggregation endpoint

Add GET /api/v2/sbom/{id}/advisory-summary endpoint that returns
severity counts (critical, high, medium, low, total) for advisories
linked to a given SBOM. Includes SeveritySummary model, service
method with deduplication by advisory ID, endpoint handler, and
integration tests.

Implements TC-9201
```

With trailer: `--trailer="Assisted-by: Claude Code"`

Full command:
```
git commit --trailer="Assisted-by: Claude Code" -m "feat(api): add advisory severity aggregation endpoint

Add GET /api/v2/sbom/{id}/advisory-summary endpoint that returns
severity counts (critical, high, medium, low, total) for advisories
linked to a given SBOM. Includes SeveritySummary model, service
method with deduplication by advisory ID, endpoint handler, and
integration tests.

Implements TC-9201"
```

## PR Creation

```
git push -u origin TC-9201
gh pr create --base main --title "feat(api): add advisory severity aggregation endpoint" --body "## Summary
- Add SeveritySummary response model with critical, high, medium, low, and total count fields
- Add severity_summary service method to AdvisoryService with deduplication by advisory ID
- Add GET /api/v2/sbom/{id}/advisory-summary endpoint handler
- Add integration tests covering valid SBOM, non-existent SBOM (404), empty advisories, and deduplication

## Jira
Implements [TC-9201](https://redhat.atlassian.net/browse/TC-9201)"
```

## Jira Updates (Step 11)

1. **Set Git Pull Request custom field** (`customfield_10875`) on TC-9201 with the PR URL in ADF format (inlineCard)
2. **Add comment** to TC-9201 with:
   - PR link
   - Summary of changes (SeveritySummary model, service method, endpoint, tests)
   - No deviations from plan
   - Footer: sdlc-workflow/implement-task version link
3. **Transition** TC-9201 to In Review

## Self-Verification Checklist

- [ ] Scope containment: `git diff --name-only` matches Files to Modify + Files to Create
- [ ] Untracked file check: verify all new files are staged
- [ ] Sensitive pattern check: no passwords, API keys, or secrets in diff
- [ ] Documentation currency: check if `docs/api.md` needs updating for new endpoint
- [ ] Duplication check: search for existing severity aggregation logic
- [ ] Data-flow trace: request -> Path extraction -> service call -> DB query -> aggregation -> JSON response (complete)
- [ ] Contract verification: SeveritySummary implements Serialize/Deserialize
- [ ] Sibling parity: handler matches pattern of get.rs/list.rs, service method matches fetch/list pattern
- [ ] CI checks from CONVENTIONS.md: run all extracted commands
