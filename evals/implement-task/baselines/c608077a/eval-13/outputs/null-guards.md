# Defensive Property Access Analysis — TC-9211

## Why guards are required

`AdvisoryIngestResult` is produced by a **different module** (`modules/ingestor`, by
`IngestorService::ingest_advisory()`) and consumed in `modules/fundamental`. The data
crosses a module boundary, so the implement-task skill's "Defensive property access on
external data" rule applies:
- The producer's schema explicitly allows absence. Every aggregate field is `Option<T>`.
- The producer can change independently, for example by returning partial results for advisories without CVE references, package detail, or severity metadata.
- The consumer contract (`VulnerabilitySummary`) is **non-optional**, so every `Option` has to be collapsed to a concrete default at the boundary.

Rust doesn't have null pointers, so the risk isn't a null dereference. The risk is a
**panic** from `.unwrap()`, `.expect()`, or `[i]` indexing, or from silently wrong
data. Truncating `as u32` casts are one example of the second. The guards below remove both.

## Field-by-field analysis

| Upstream field | Type | When it's `None` | Needs guard? | Guard pattern | Default produced |
|---|---|---|---|---|---|
| `cves` | `Option<Vec<String>>` | Advisory has no CVE references | **Yes** | `result.cves.clone().unwrap_or_default()` | `cve_list = vec![]` |
| (derived) `cve_count` | from `cve_list` | — | Yes, consistency guard | `saturating_u32(cve_list.len())`, computed **from the already-defaulted list** | `0` |
| `affected_packages` | `Option<Vec<AffectedPackage>>` | No package-level detail | **Yes** | `result.affected_packages.as_ref().map_or(0, Vec::len)` | `affected_package_count = 0` |
| `severity_counts` | `Option<HashMap<String, u32>>` | Severity metadata absent | **Yes** | `result.severity_counts.clone().unwrap_or_default()` | `severity_breakdown = HashMap::new()` |
| Length → `u32` conversion | `usize` → `u32` | Not a nullability issue, but an overflow/truncation hazard | Yes | `u32::try_from(n).unwrap_or(u32::MAX)` | saturates instead of wrapping |

Any other fields on `AdvisoryIngestResult` (IDs, etc.) aren't read by the extractor, so they
don't need guards. I'd confirm this with `find_symbol("AdvisoryIngestResult", include_body=true)`.
If the real struct has other `Option` fields the summary needs, the same patterns apply.

## Guard patterns chosen and why

### 1. `cves` → `.clone().unwrap_or_default()`
```rust
let cve_list: Vec<String> = result.cves.clone().unwrap_or_default();
```
- The CVE strings end up in the output (`cve_list`), so an owned `Vec` is needed. Cloning the `Option` and then defaulting is the idiomatic one-liner.
- `unwrap_or_default()` is total. It can't panic, and `None` becomes `Vec::new()`, exactly as the Implementation Notes require ("use an empty Vec").
- Alternative: if the method took `AdvisoryIngestResult` by value, `result.cves.unwrap_or_default()` would avoid the clone. I chose `&AdvisoryIngestResult` so callers keep the result, for example to persist it and also email it.

### 2. `cve_count` is derived, not read separately
```rust
let cve_count = saturating_u32(cve_list.len());
```
- The acceptance criterion "cve_count matches the length of the cve_list" is guaranteed **by construction**, because the count is computed from the same, already-guarded list. The `None` case gives `0` automatically, and the `Some(vec![])` case also gives `0`.
- I don't use a separate `if let Some(c) = &result.cves { c.len() } else { 0 }` branch, because two code paths could drift apart.

### 3. `affected_packages` → `.as_ref().map_or(0, Vec::len)`
```rust
let affected_package_count = saturating_u32(result.affected_packages.as_ref().map_or(0, Vec::len));
```
- Only the **count** is needed, so `.as_ref()` borrows the inner `Vec` with no clone. Cloning a `Vec<AffectedPackage>` just to count it would be wasteful.
- `map_or(0, Vec::len)` handles `None → 0` in one expression and can't panic.
- Equivalent alternatives: `result.affected_packages.as_deref().map_or(0, <[_]>::len)` or `result.affected_packages.as_ref().map(Vec::len).unwrap_or(0)`. `map_or` is the most direct of these.

### 4. `severity_counts` → `.clone().unwrap_or_default()`
```rust
let severity_breakdown: HashMap<String, u32> = result.severity_counts.clone().unwrap_or_default();
```
- The map is copied into the output, so it needs an owned value. `None` becomes `HashMap::new()`, as required ("use an empty HashMap").
- I never index into the map (`map["critical"]` panics if the key is missing). Downstream consumers that need a specific level should use `.get("critical").copied().unwrap_or(0)`. That convention goes in the struct's doc comment and PR notes, but this task only passes the map through.

### 5. `usize → u32` conversion → `u32::try_from(..).unwrap_or(u32::MAX)`
- `Vec::len()` returns `usize`, and the output fields are `u32`. `len as u32` would silently wrap on more than 4,294,967,295 items. That isn't realistic, but the saturating conversion costs nothing and keeps the "never wrong, never panics" guarantee. Clippy's `cast_possible_truncation` lint would also flag `as`.

## Patterns explicitly avoided

| Avoided | Reason |
|---|---|
| `result.cves.unwrap()` / `.expect("...")` | Panics on `None`, which violates the "without panicking" criterion |
| `result.cves.as_ref().unwrap().len()` | Same panic risk |
| `result.severity_counts.unwrap()["high"]` | Double panic risk: the Option and the missing key |
| `if result.cves.is_some() { result.cves.clone().unwrap() ... }` | Check-then-unwrap is non-idiomatic and gets fragile under refactoring |
| `len() as u32` | Silent truncation |
| Making `VulnerabilitySummary` fields `Option<T>` | Pushes the nullability problem onto every email consumer and contradicts the Implementation Notes |
| Returning `Err(AppError)` when a field is `None` | `None` is a valid upstream state (documented in the task), not an error |

## Independence of defaults

Each guard is a separate expression over a separate field, so a `None` in one field
can't affect the others. This is what the "mixed Some/None" test requirement checks:

| cves | affected_packages | severity_counts | Result |
|---|---|---|---|
| Some | Some | Some | all values carried through |
| None | Some | Some | `cve_count 0`, `cve_list []`, others intact |
| Some | None | Some | `affected_package_count 0`, others intact |
| Some | Some | None | `severity_breakdown {}`, others intact |
| None | None | None | `VulnerabilitySummary::default()` |

`Some(vec![])` / `Some(HashMap::new())` give the same output as `None`. Both mean "nothing to report",
and a dedicated test covers this.

## Test coverage of the guards

- `test_extract_summary_all_none`: every guard takes its `None` branch, and the result equals `VulnerabilitySummary::default()`.
- `test_extract_summary_mixed_fields` (one case per field): each guard's `None` branch runs alone, with value assertions on the other two fields.
- `test_extract_summary_fully_populated`: every guard takes its `Some` branch, with exact value equality.
- `test_cve_count_matches_cve_list_len`: covers `None`, empty, one CVE, and several CVEs, asserting `cve_count as usize == cve_list.len()` and the exact list contents.
