# Defensive Property Access Analysis — TC-9211

## Why guards are needed

`AdvisoryIngestResult` is produced by a different crate (`modules/ingestor`, built by `IngestorService::ingest_advisory()`) and consumed in `modules/fundamental`. Because the data crosses a module boundary, the producer's schema can change independently. The task also states that every aggregate field can be absent. The implement-task skill ("Defensive property access on external data") requires idiomatic null guards before accessing these fields. In Rust that means handling `Option` explicitly, using `if let`, `.map_or`, `.unwrap_or_default()` and similar. It never means `.unwrap()`, `.expect()`, or indexing.

## Field-by-field analysis

| Field (upstream type) | Can be `None` when | Unsafe access to avoid | Guard pattern | Resulting default |
|---|---|---|---|---|
| `cves: Option<Vec<String>>` | advisory has no CVE references | `result.cves.unwrap()`, `result.cves.as_ref().unwrap().len()`, `result.cves.unwrap()[0]` | `result.cves.clone().unwrap_or_default()` | `cve_list = vec![]`, `cve_count = 0` |
| `affected_packages: Option<Vec<AffectedPackage>>` | advisory has no package-level detail | `result.affected_packages.unwrap().len()` | `result.affected_packages.as_ref().map_or(0, \|p\| saturating_u32(p.len()))` | `affected_package_count = 0` |
| `severity_counts: Option<HashMap<String, u32>>` | severity metadata is absent | `result.severity_counts.unwrap()`, `map["critical"]` (indexing panics on a missing key) | `result.severity_counts.clone().unwrap_or_default()` | `severity_breakdown = HashMap::new()` |

### `cves`

- **Pattern**: `.clone().unwrap_or_default()`. `Vec<String>: Default` gives an empty vec. The function borrows `&AdvisoryIngestResult`, so it clones the inner vec only when one is present. `Option<Vec>::clone()` on `None` is free.
- **Consistency guard**: `cve_count` is computed from the defaulted `cve_list.len()`, not from a separate read of `result.cves`. That makes AC #4 (`cve_count == cve_list.len()`) true by construction, because there is only one source of truth.
- **Alternative considered**: `result.cves.as_deref().unwrap_or(&[]).to_vec()`. It is equivalent but noisier. `unwrap_or_default` is the idiomatic choice.

### `affected_packages`

- **Pattern**: `.as_ref().map_or(0, |pkgs| ...)`. Only the length is needed, so `.as_ref()` borrows the vec without cloning any `AffectedPackage` values.
- **No nested access**: the extractor never reads fields inside `AffectedPackage`, so it needs no deeper guards. If a later change reads nested optional fields such as `pkg.version: Option<String>`, it must use the same pattern (`pkg.version.as_deref().unwrap_or("")`, or `filter_map`).

### `severity_counts`

- **Pattern**: `.clone().unwrap_or_default()`. This produces an empty `HashMap`.
- **Secondary guard**: downstream code (and tests) must read severities with `.get("critical").copied().unwrap_or(0)`, never `map["critical"]`. `Index` on a `HashMap` panics when the key is missing, and a `Some(map)` can still lack a particular severity key.
- The keys are passed through unchanged. Normalising them (e.g. lowercasing) is not in the task, so it is not added.

## Additional (non-`Option`) panic sources guarded

| Risk | Guard | Why |
|---|---|---|
| `usize` → `u32` conversion for `cve_count` / `affected_package_count` | `u32::try_from(len).unwrap_or(u32::MAX)`, via a private `saturating_u32` helper | `len as u32` silently truncates on 64-bit for more than 4,294,967,295 items. `try_from(...).unwrap()` would panic. Saturating is the safe and explicit choice. The case is unrealistic but costs nothing to handle. |
| Indexing into lists (`cves[0]`) | Not used. Iterate or use `.first()` if ever needed. | Indexing an empty `Vec` panics. |

## Semantics: `None` vs `Some(empty)`

Both produce the same output: an empty collection and a count of 0. That is intentional. A digest email does not need to tell "no data" apart from "zero items". The tests include `Some(vec![])` and `Some(HashMap::new())` rows to show the two are equivalent. If product later needs that distinction, the output struct would need a flag. That would contradict the "non-optional fields" requirement, so it is not added now.

## Why not use `Option` in the output?

The Implementation Notes require `VulnerabilitySummary` to have non-optional fields with sensible defaults. Resolving the `Option`s once, at the module boundary inside `extract_vulnerability_summary`, means:

1. Email rendering and other consumers never need their own null checks.
2. The defaulting rule is defined in exactly one place. `VulnerabilitySummary::default()` equals the all-`None` result, and the test asserts this.
3. The function cannot panic on missing data. It contains no `unwrap`/`expect`/indexing on upstream values, and the only `unwrap_or*` calls are total.

## Test coverage of the guards

| Guard | Test(s) |
|---|---|
| `cves` `None` → empty and 0 | `all_none_fields_yield_zeroed_summary`, mixed row 2/3, `cve_count_matches_cve_list_length[None]` |
| `affected_packages` `None` → 0 | `all_none_fields_yield_zeroed_summary`, mixed rows 1/3 |
| `severity_counts` `None` → empty map | `all_none_fields_yield_zeroed_summary`, mixed rows 1/2 |
| Independent defaulting | `mixed_some_none_fields_default_independently` (each row has exactly one field `Some`) |
| Count/list consistency | `cve_count_matches_cve_list_length` (`None`, `Some([])`, 1 item, 3 items) |
