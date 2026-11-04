# Defensive Property Access Analysis: TC-9211

## Context

`extract_vulnerability_summary()` lives in the **fundamental** module. It consumes `AdvisoryIngestResult`, which the **ingestor** module (`modules/ingestor/src/service/mod.rs`) produces via `IngestorService::ingest_advisory()`. That data crosses a module boundary. Per the implement-task skill's "Defensive property access on external data" rule, every nested access must be guarded:

- The producer's schema already allows absence (`Option<T>`).
- The producer may return partial results, i.e. `Some(vec![])` versus `None`.
- The producer may evolve independently. For example, more fields could become `Option` later, and the guard style below keeps working.

In Rust, `None` cannot be accessed by accident unless code calls `.unwrap()`, `.expect()`, or indexes, or pattern-matches only on `Some`. So in Rust the "guard" means: **never unwrap; always collapse `Option` to a concrete default with an idiomatic combinator.**

## Field-by-field analysis

| Field (upstream type) | Needs a guard? | Failure mode without a guard | Guard pattern | Output value when `None` |
|---|---|---|---|---|
| `cves: Option<Vec<String>>` | **Yes** | `result.cves.unwrap()` panics on advisories with no CVE refs. `result.cves.as_ref().unwrap().len()` panics too. | `result.cves.clone().unwrap_or_default()`, then derive the count from the defaulted list | `cve_list = vec![]`, `cve_count = 0` |
| `affected_packages: Option<Vec<AffectedPackage>>` | **Yes** | `.unwrap().len()` panics for advisories without package-level detail | `result.affected_packages.as_ref().map_or(0, Vec::len)`. This borrows only, with no clone of the `AffectedPackage` items, since only the count is needed. | `affected_package_count = 0` |
| `severity_counts: Option<HashMap<String, u32>>` | **Yes** | `.unwrap()` panics when severity metadata is absent. Also, `map["critical"]` indexing panics on a missing key even when the map is `Some`. | `result.severity_counts.clone().unwrap_or_default()`. Never index by key; downstream readers use `.get(k).copied().unwrap_or(0)`. | `severity_breakdown = HashMap::new()` |
| Derived: `usize → u32` length conversion | **Yes** (secondary) | `len as u32` silently truncates above `u32::MAX`, which could break `cve_count == cve_list.len()`. | `u32::try_from(len)` mapped to `AppError` via `.context(...)`, using the method's existing `Result` return | not applicable (only an error for absurd sizes) |
| Elements inside `cves` (`String`) | No | Rust `String` cannot be null. An empty string is valid data, and filtering it isn't in the spec. | none (passed through unchanged) | n/a |
| Elements inside `affected_packages` (`AffectedPackage`) | No | Only `.len()` is used, so no inner fields are dereferenced | none | n/a |
| Values inside `severity_counts` (`u32`) | No | Primitive, never null | none | n/a |

## Chosen guard patterns and why

### 1. `Option<Vec<T>>` that I need to own → `.clone().unwrap_or_default()`

```rust
let cve_list: Vec<String> = result.cves.clone().unwrap_or_default();
```

- `unwrap_or_default()` is the idiomatic Rust form of "`?? []`". `Vec::default()` is an empty vec, so the call is total and can never panic.
- `.clone()` is needed because the method takes `&AdvisoryIngestResult`, and the CVE strings must be owned by the output struct. If the signature took ownership instead, this would be `result.cves.unwrap_or_default()` with no clone.
- I prefer this to a `match` or an `if let` block because it is one expression, has no branch to forget, and is the pattern the skill names explicitly.

### 2. `Option<Vec<T>>` where only the length matters → `.as_ref().map_or(0, Vec::len)`

```rust
let affected_package_count = u32::try_from(
    result.affected_packages.as_ref().map_or(0, Vec::len),
).context("affected package count exceeds u32::MAX")?;
```

- `as_ref()` turns `&Option<Vec<_>>` into `Option<&Vec<_>>`, so nothing is moved or cloned. Cloning a vec of `AffectedPackage` structs just to count them would be wasteful.
- `map_or(0, Vec::len)` supplies the default (0) and the projection in one total expression.
- An equivalent alternative is `result.affected_packages.as_deref().map_or(0, <[_]>::len)`. I prefer `as_ref()` for readability.

### 3. `Option<HashMap<K, V>>` → `.clone().unwrap_or_default()`, and never index

```rust
let severity_breakdown: HashMap<String, u32> =
    result.severity_counts.clone().unwrap_or_default();
```

- `HashMap::default()` is an empty map. That matches the Implementation Notes: "When `severity_counts` is `None`, use an empty `HashMap`".
- There is a second hazard: `HashMap` indexing with `map["high"]` panics on a missing key. The extractor copies the map wholesale and never indexes it. Tests and any future consumers should use `.get("high").copied().unwrap_or(0)`.

### 4. Count consistency by construction

```rust
let cve_count = u32::try_from(cve_list.len()).context("CVE count exceeds u32::MAX")?;
```

`cve_count` is computed from the already-defaulted `cve_list`, not from `result.cves` in a separate branch. That makes the acceptance criterion "cve_count matches the length of cve_list" an invariant of the code rather than something two code paths must keep in sync. For example, a buggy version could compute the count via `result.cves.as_ref().map_or(0, Vec::len)` while the list was built another way.

### 5. Checked integer conversion instead of `as`

`as u32` never panics, but it silently wraps for lengths above `u32::MAX`, which would break the count invariant. `u32::try_from` plus `?` uses the method's existing `Result<_, AppError>` contract, so the function stays panic-free and correct. In practice this path is unreachable for real advisories.

## Patterns that are explicitly forbidden in this change

| Pattern | Why |
|---|---|
| `result.cves.unwrap()` / `.expect("...")` | Panics on `None`, which the spec says is a normal case |
| `result.cves.as_ref().unwrap().len()` | Same panic, hidden behind a borrow |
| `result.severity_counts.unwrap()["critical"]` | Two panic sources: a `None` map, and a missing key |
| `result.cves.unwrap_or_default().len() as u32` (separately from building the list) | Duplicates the defaulting logic, and the count could drift from the list |
| `if result.cves.is_some() { result.cves.as_ref().unwrap() ... }` | Check-then-unwrap. It is fragile under refactoring; use combinators or `if let` instead. |

## `None` vs `Some(empty)` semantics

The spec treats `None` as "no data", which defaults to 0 or empty. The producer may also emit `Some(vec![])` or `Some(HashMap::new())`. Both shapes produce the identical zeroed `VulnerabilitySummary`, because `unwrap_or_default()` and `map_or(0, len)` yield the same value in both cases. The test `extract_summary_empty_some_collections` covers this. The output type deliberately has no `Option`, so downstream email rendering never needs its own null checks: the guarding is centralized at the module boundary.

## Test coverage of guards

| Guard | Test(s) |
|---|---|
| `cves` `None` → `[]`, count 0 | all-None test; mixed cases with `cves=None`; cve_count consistency test with the `None` case |
| `affected_packages` `None` → 0 | all-None test; mixed cases with `affected_packages=None` |
| `severity_counts` `None` → `{}` | all-None test; mixed cases with `severity_counts=None` |
| Independent defaulting | parameterized mixed Some/None test asserting the full expected struct per case |
| `Some(empty)` equals `None` | `extract_summary_empty_some_collections` |
| Count invariant | `extract_summary_cve_count_matches_list_len` (None, empty, 1, 5 items) |
