# Criterion 6: Existing package list endpoint tests continue to pass (backward compatible)

**Verdict: PASS**

## Reasoning

The change only adds a field to the response. No existing field is removed, renamed, or retyped. The endpoint route, parameters (`offset`, `limit`), and return type are unchanged. Clients that ignore unknown fields are unaffected.

## Evidence

- `summary.rs` adds one field and leaves the existing fields (`id`, `name`, `version`, `license`) untouched.
- `service/mod.rs` maps every existing field through unchanged (`id`, `name`, `version`, `license`).
- `endpoints/list.rs` keeps the same `.list(params.offset, params.limit)` call. Only a comment was added.
- CI status: the eval reports that all checks pass.

## Caveat

The documented repository structure has no existing package-specific integration test file. `tests/api/` contains only `sbom.rs`, `advisory.rs`, and `search.rs`. The backward-compatibility verdict therefore rests on the change being additive and on CI passing. If any existing test builds `PackageSummary` with a struct literal, the new required field would break compilation. CI being green suggests that is not the case.
