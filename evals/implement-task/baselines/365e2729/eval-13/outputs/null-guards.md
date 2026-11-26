# Defensive Property Access Analysis — TC-9211

## Why guards are required

`AdvisoryIngestResult` comes from another module: the `ingestor` crate (`modules/ingestor/src/service/mod.rs`), produced by `IngestorService::ingest_advisory()`. The new code in `fundamental` consumes it. The skill's "Defensive property access on external data" rule applies to every access path that crosses this module boundary. The ingestor owns the schema and may return partial results, and its schema can change on its own. The task makes all three aggregate fields `Option<T>` and requires that the extractor "must handle all nullable fields gracefully without panicking".

In Rust, the main risks are `.unwrap()` and `.expect()` on `Option`, and indexing (`v[0]`, `map["critical"]`), because all of these panic. The guard pattern is the idiomatic combinators `.unwrap_or_default()`, `.map_or(...)`, `.as_ref()`/`.as_deref()` and `if let`, as named in the skill guidance.

## Field-by-field analysis

| Field (upstream type) | Accessed for | Guard needed? | Guard pattern | Default when `None` |
|---|---|---|---|---|
| `cves: Option<Vec<String>>` | `cve_list` contents and `cve_count` | **Yes** | `result.cves.as_deref().map(<[String]>::to_vec).unwrap_or_default()` (or `result.cves.clone().unwrap_or_default()`) | `Vec::new()`, so `cve_count = 0` |
| `affected_packages: Option<Vec<AffectedPackage>>` | count only (`affected_package_count`) | **Yes** | `result.affected_packages.as_ref().map_or(0, Vec::len)` | `0` |
| `severity_counts: Option<HashMap<String, u32>>` | `severity_breakdown` | **Yes** | `result.severity_counts.clone().unwrap_or_default()` | `HashMap::new()` |
| `AffectedPackage` inner fields | not accessed | No | Only the length of the vec is used, so no nested access needs guarding. If a future change reads package fields, guard those too. | n/a |
| `HashMap<String, u32>` values | copied as-is | No | The whole map is passed through. No key lookups, so no `map[key]` panic risk. If specific keys were read, use `.get(k).copied().unwrap_or(0)`. | n/a |
| Elements of `cves` (`String`) | copied as-is | No | Non-optional `String` values, so there is no nullable access. | n/a |

## Pattern choices and reasons

1. **`unwrap_or_default()` for `cves` and `severity_counts`.** The output struct needs owned, non-optional `Vec<String>` and `HashMap<String, u32>`. `Default` for both is the empty collection, which is exactly what the Implementation Notes ask for ("use an empty `Vec`" / "use an empty `HashMap`"). It is concise, panic-free and shows intent clearly.
2. **`.as_ref().map_or(0, Vec::len)` for `affected_packages`.** Only the count is needed. Borrowing with `as_ref()` avoids cloning a vector of possibly large `AffectedPackage` structs. `map_or(0, ...)` gives the required `0` for `None` in a single expression.
3. **Borrow with `&AdvisoryIngestResult`, not owned.** The caller keeps ownership of the ingest result, which might also be used for other things. Guards work on references (`as_ref`/`as_deref`), and data is cloned only where the output must own it.
4. **Derive `cve_count` from the defaulted `cve_list`.** Defaulting happens first, then `cve_count = cve_list.len()`. This makes the "cve_count matches cve_list length" criterion true by construction in all cases: `None`, `Some(vec![])` and `Some(non-empty)`. Computing the count separately from `result.cves` would add a second access path that could drift.
5. **Safe `usize` to `u32` conversion.** `len()` returns `usize`, and the output fields are `u32`. A plain `as u32` would silently truncate on overflow. Use `u32::try_from(len)` and map the error to `AppError` with `.context(...)`, which fits the method's `Result<T, AppError>` return type. Saturating with `.unwrap_or(u32::MAX)` is an acceptable alternative if the team wants an infallible path. Neither option panics.
6. **Explicitly avoided:** `result.cves.unwrap()`, `result.cves.expect(..)`, `result.affected_packages.unwrap().len()`, `result.severity_counts.as_ref().unwrap()`, `if result.cves.is_some() { result.cves.as_ref().unwrap() ... }` (an is_some/unwrap split that is fragile under refactoring), and any `map["key"]` indexing.

## `Some(empty)` vs `None`

`Some(vec![])` and `None` produce the same output (an empty list and a 0 count). No special branch is needed, and tests cover both, so the equivalence is intentional and verified.

## Test coverage of the guards

- All `None`: the summary equals `VulnerabilitySummary::default()`, with every field zeroed or empty.
- Mixed: each field is `None` in turn while the others are `Some`. Only the `None` field takes its default, which proves the guards are independent.
- Fully populated: the values pass through exactly, so the guards do not change present data.
- `cve_count` consistency across `None`, `Some(vec![])`, one entry and several entries.
