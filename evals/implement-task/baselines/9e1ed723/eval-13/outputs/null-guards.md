# Defensive Property Access Analysis — TC-9211

This analysis applies the "Defensive property access on external data" rule from implement-task Step 6:

> When consuming data produced by another module... add null/undefined guards before accessing
> nested properties... Use the language's idiomatic guard pattern (e.g. `if let` /
> `.unwrap_or_default()` in Rust).

## Why guards are required here

`AdvisoryIngestResult` is produced by a **different crate**: `modules/ingestor`, through `IngestorService::ingest_advisory()`. It is consumed in `modules/fundamental`, so the data crosses a module boundary.
- The producer's schema explicitly marks every aggregate field as `Option<T>`.
- The task description documents real-world cases where each field is `None`.
- The ingestor crate can evolve independently. A field that is always `Some` today may stop being so later.

In Rust, the compiler will not let you read a `Vec` directly through an `Option`. The real risk is that someone writes `.unwrap()` or `.expect()` on these fields, or `result.cves.as_ref().unwrap().len()`, which **panics** on `None`. The task explicitly requires "without panicking". So the rule is: **no `unwrap()`, `expect()`, or `[]` indexing on any of these fields.** Every access goes through a default-producing combinator.

## Field-by-field analysis

| Field (source type) | Guard needed? | When `None` occurs | Guard pattern | Output on `None` |
|---|---|---|---|---|
| `cves: Option<Vec<String>>` | **Yes** | The advisory has no CVE references | `result.cves.clone().unwrap_or_default()` (or `result.cves.unwrap_or_default()` if the result is taken by value) | `cve_list = vec![]`, `cve_count = 0` |
| `affected_packages: Option<Vec<AffectedPackage>>` | **Yes** | The advisory has no package-level detail | `result.affected_packages.as_ref().map_or(0, Vec::len)`, converted with `u32::try_from` | `affected_package_count = 0` |
| `severity_counts: Option<HashMap<String, u32>>` | **Yes** | Severity metadata is absent | `result.severity_counts.clone().unwrap_or_default()` | `severity_breakdown = HashMap::new()` |
| Derived `cve_count` | Indirect | Follows `cves` | Computed from the **already-defaulted** `cve_list.len()`. It is never computed separately from the `Option`. | `0` |

### `cves`
- **Pattern**: `unwrap_or_default()`. `Vec<String>: Default`, so this gives an empty vec. It is the idiomatic Rust equivalent of `(rem.cves ?? [])`.
- **Why this pattern**: the field is needed both as the list and as the count. Unwrapping it into one owned `Vec` first and then deriving `cve_count = cve_list.len()` keeps one source of truth. That guarantees the acceptance criterion `cve_count == cve_list.len()` for every input: `None`, `Some(vec![])`, and `Some(non-empty)`.
- **Anti-pattern to avoid**: computing the count and the list along two separate paths, for example `cves.as_ref().map(|v| v.len()).unwrap_or(0)` alongside `cves.clone().unwrap_or_default()`. They agree today, but the two paths can drift apart.

### `affected_packages`
- **Pattern**: `as_ref().map_or(0, Vec::len)`. Only the count is needed, so it borrows instead of cloning the `Vec<AffectedPackage>`. An `if let Some(pkgs) = &result.affected_packages { pkgs.len() } else { 0 }` is equivalent and also acceptable.
- **Nested access**: no fields of `AffectedPackage` are read, so no inner guards are needed. If a future change reads nested optional fields, for example `pkg.version: Option<String>`, it should use `filter_map` / `as_deref()`. It must not unwrap those fields.

### `severity_counts`
- **Pattern**: `unwrap_or_default()`. `HashMap<String, u32>: Default` gives an empty map.
- The values are `u32` (not `Option<u32>`), so the inner values need no guard. Entries are copied as they are. The summary does not invent missing severity keys such as `"critical": 0`, because the task says only "use an empty HashMap".

## Numeric conversion guard (related, non-null)

`Vec::len()` returns `usize`, but the output fields are `u32`. A plain `as u32` would silently truncate above `u32::MAX`. The plan uses `u32::try_from(len)` with `.context(...)` instead. That turns the impossible-in-practice overflow into an `AppError`, never a panic or a wrong count. It also fits the method's `Result<VulnerabilitySummary, AppError>` signature.

## Guard pattern summary

```rust
let cve_list = result.cves.clone().unwrap_or_default();                  // None -> []
let cve_count = u32::try_from(cve_list.len()).context("...")?;           // derived, consistent
let affected_package_count = u32::try_from(
    result.affected_packages.as_ref().map_or(0, Vec::len),               // None -> 0
).context("...")?;
let severity_breakdown = result.severity_counts.clone().unwrap_or_default(); // None -> {}
```

## Pattern choices

- **`unwrap_or_default()` over `unwrap_or(Vec::new())`**: it is shorter and uses the type's own `Default`, and it allocates nothing on the `None` path.
- **`map_or` / `if let` over `match`**: these are equivalent, but less verbose for a single default.
- **No `unwrap()` or `expect()`**: they would violate the "without panicking" requirement.
- **Non-optional output struct**: downstream consumers such as the email digest never need to guard again, because the null handling happens once, at the module boundary.

## Test coverage of the guards

| Guard | Test |
|---|---|
| All three `None` | `extract_summary_all_none` checks that the result equals `VulnerabilitySummary::default()` |
| Each field defaults on its own | `extract_summary_mixed_fields`, with several Some/None combinations |
| `Some(empty)` behaves like `None` | `extract_summary_some_empty_collections` |
| `cve_count` stays consistent with `cve_list` | `extract_summary_cve_count_matches_list` (None, empty, 3 items) |
| Happy path is unchanged by the guards | `extract_summary_fully_populated` |
