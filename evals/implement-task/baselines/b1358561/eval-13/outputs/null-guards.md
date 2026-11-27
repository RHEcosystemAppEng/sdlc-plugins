# Defensive Property Access Analysis — TC-9211

Source rule: implement-task SKILL.md, Step 6, "Defensive property access on external data". When code consumes data from another module, it must guard optional and nullable properties before using them, with the language's idiomatic pattern. In Rust that means `if let` / `match` / `.unwrap_or_default()` / `.map_or()`. `.unwrap()`, `.expect()`, and indexing are never used.

## Why guards are required here

`AdvisoryIngestResult` is produced by `IngestorService::ingest_advisory()` in a **different crate** (`modules/ingestor/src/service/mod.rs`). The fundamental module consumes it, so the data crosses a module boundary:
- The producer owns the schema and can change it on its own schedule.
- Its fields are explicitly `Option<T>` for all aggregate data, and each one can be `None` in normal operation: no CVE references, no package-level detail, no severity metadata.
- The task requires that the extractor "must handle all nullable fields gracefully without panicking". The output `VulnerabilitySummary` has only non-optional fields, so every `None` has to become a concrete default at this boundary.

## Field-by-field analysis

| Field (input) | Type | When `None` | Guard | Output default |
|---|---|---|---|---|
| `cves` | `Option<Vec<String>>` | Advisory has no CVE references | `result.cves.clone().unwrap_or_default()` (or `result.cves.unwrap_or_default()` if the result is taken by value) | `cve_list = vec![]`, `cve_count = 0` |
| `affected_packages` | `Option<Vec<AffectedPackage>>` | No package-level detail | `result.affected_packages.as_deref().map_or(0, <[_]>::len)`, which counts without cloning the packages | `affected_package_count = 0` |
| `severity_counts` | `Option<HashMap<String, u32>>` | Severity metadata absent | `result.severity_counts.clone().unwrap_or_default()` | `severity_breakdown = HashMap::new()` |

Derived field:

| Field (output) | Rule | Why |
|---|---|---|
| `cve_count` | Computed **from the already-guarded `cve_list`** with `u32::try_from(cve_list.len()).context(...)?` | Deriving the count from the guarded list means `cve_count == cve_list.len()` holds whatever the input was (`None`, `Some(vec![])`, or populated). Computing it from `result.cves` separately would mean guarding the same field twice, with room for the two to drift. `try_from` replaces `as u32` so an overflow is surfaced as an `AppError` instead of being truncated silently |
| `affected_package_count` | Same `u32::try_from(..).context(..)?` conversion | Same reason: no silent truncation, and no panic |

## Guard patterns chosen, and why

1. **`.unwrap_or_default()` for owned collections (`cves`, `severity_counts`).** This is the most idiomatic Rust for "None → empty collection". `Vec` and `HashMap` both implement `Default`, so it cannot panic. It also matches the task's notes exactly: "use an empty Vec" and "use an empty HashMap".
2. **`.as_deref().map_or(0, <[_]>::len)` for `affected_packages`.** Only the count is needed, so borrowing the slice avoids cloning `AffectedPackage` values. The `None` case maps straight to `0`.
3. **No `if let` chains.** Every field has a natural default, so `unwrap_or_default`/`map_or` express the defaulting in one expression and keep the guards independent. `if let`/`match` would only be warranted if a `None` field needed different behavior, such as logging. The task does not ask for that.
4. **Each field is guarded independently.** No guard depends on another field, so mixed `Some`/`None` inputs default per field, as the "mixed Some/None" test requirement expects.
5. **Forbidden patterns:** `result.cves.unwrap()`, `.expect(..)`, `result.cves.as_ref().unwrap().len()`, `cves[0]`, and `x.len() as u32`. Each of these either panics on `None` or truncates silently.

## Nested and partial-data considerations

- **Elements inside the collections.** Rust's type system guarantees that a `Vec<String>` cannot contain null elements and a `HashMap<String, u32>` cannot contain null values, so no per-element guard is needed. The extractor never reads properties *inside* `AffectedPackage` (it only counts entries), so the optional fields of `AffectedPackage` itself need no guards. If a later change read, for example, `pkg.version: Option<String>`, that access would need its own guard.
- **`Some(vec![])` vs `None`.** Both give the same output (empty list, count 0). That is acceptable because the task does not ask to distinguish them, and the test for `cve_count` consistency covers both.
- **Upstream type verification (Step 4).** Before implementing, confirm with `mcp__serena_backend__find_symbol("AdvisoryIngestResult", include_body=true)` that the fields really are `Option<...>` as the task describes. If one turns out to be non-optional, such as a plain `Vec`, the guard for it would not compile as written and would be adjusted. If the upstream type is more nullable than described, for example `Option<Vec<Option<String>>>`, add `.into_iter().flatten()` to drop inner `None`s. That would be a deviation to report in the Jira comment.
- **Other consumers (Step 9, check 13 caller-site).** Grep for other users of `AdvisoryIngestResult` to confirm that defaulting `None` to empty or zero matches how existing consumers treat these fields.

## Test coverage of the guards

| Guard path | Test |
|---|---|
| All fields `Some` | `extract_summary_fully_populated` |
| All fields `None` → zeroed summary (`== VulnerabilitySummary::default()`) | `extract_summary_all_none` |
| Each field `None` while the others are `Some` | `extract_summary_mixed_fields` (3 cases, parameterized with `rstest` if the project already uses it) |
| `cve_count == cve_list.len()` for `None`, empty, one, and many | `extract_summary_cve_count_matches_list` |
