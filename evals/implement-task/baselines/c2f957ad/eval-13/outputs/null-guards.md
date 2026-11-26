# Defensive Property Access Analysis — TC-9211

## Why guards are needed

`AdvisoryIngestResult` is produced by a different crate (`modules/ingestor`,
`IngestorService::ingest_advisory()`) and consumed in `modules/fundamental`. This is a
module boundary: per the implement-task skill's "Defensive property access on external
data" rule, every nested/aggregate property access on that data must be guarded, because
the producer's schema allows absence and may evolve independently. Here the type signature
itself declares absence (`Option<T>`) for all three aggregate fields, and the task explicitly
requires "handle all nullable fields gracefully without panicking".

In Rust the compiler forbids using an `Option<Vec<_>>` as a `Vec<_>` directly, so the risk
is not a null dereference but a *panic* from a careless `.unwrap()` / `.expect()` / indexing,
or a silent truncation from `as u32`. The guards below remove every panic path.

## Field-by-field analysis

| Field (upstream) | Type | When `None` | Output field(s) | Guard | Default |
|---|---|---|---|---|---|
| `cves` | `Option<Vec<String>>` | advisory has no CVE references | `cve_list`, `cve_count` | `result.cves.as_deref().map(<[String]>::to_vec).unwrap_or_default()` (borrowed) or `result.cves.unwrap_or_default()` (owned) | `Vec::new()`, count 0 |
| `affected_packages` | `Option<Vec<AffectedPackage>>` | no package-level detail | `affected_package_count` | `result.affected_packages.as_ref().map_or(0, Vec::len)` | 0 |
| `severity_counts` | `Option<HashMap<String, u32>>` | severity metadata absent | `severity_breakdown` | `result.severity_counts.clone().unwrap_or_default()` (borrowed) or `.unwrap_or_default()` (owned) | `HashMap::new()` |

### `cves`
- Guard: `unwrap_or_default()` after converting the borrowed slice to an owned `Vec`.
- `cve_count` is **derived from the already-guarded `cve_list.len()`** rather than computed
  separately from `result.cves`. That way both fields come from one source of truth, and the
  acceptance criterion `cve_count == cve_list.len()` holds by construction, including the
  `None` and `Some(vec![])` cases.

### `affected_packages`
- Only the count is needed, so no `AffectedPackage` contents are cloned or touched.
  `as_ref().map_or(0, Vec::len)` borrows, returns 0 for `None`, and never reads into elements.
- Since no nested `AffectedPackage` fields are read, no further guards are needed inside the
  elements. If a later change reads e.g. `pkg.version`, and that field is `Option`, it must be
  guarded the same way (`pkg.version.as_deref().unwrap_or("")` or filtered out).

### `severity_counts`
- `unwrap_or_default()` gives an empty `HashMap` for `None`. Values are copied through
  unchanged; no key lookups like `map["critical"]` are done (indexing a `HashMap` with a
  missing key panics). If a later change needs a particular severity, use
  `map.get("critical").copied().unwrap_or(0)`.

## Numeric conversion guard

`Vec::len()` returns `usize`, but the output fields are `u32`. A plain `len as u32` silently
truncates on overflow, and `u32::try_from(len).unwrap()` panics. Use a saturating conversion:

```rust
fn to_u32(n: usize) -> u32 { u32::try_from(n).unwrap_or(u32::MAX) }
```

This won't come up for realistic CVE or package counts, but it keeps the "never panics"
guarantee complete. (Before adding the helper, grep `common/` for an existing one and reuse it.)

## Guard pattern choice: why these idioms

- **`Option::unwrap_or_default()`**: the idiomatic Rust guard that the skill names
  (`.unwrap_or_default()`). It maps `None` to `Default::default()` (empty `Vec` / `HashMap`),
  which is exactly the default the task asks for in its Implementation Notes.
- **`Option::map_or(0, ...)`**: computes a derived value (a count) without a full
  `unwrap_or_default()` + allocation, and keeps the zero default explicit.
- **`as_ref()` / `as_deref()`**: lets the method take `&AdvisoryIngestResult` so the caller
  keeps ownership. No moves happen out of borrowed data.
- **Not used**: `.unwrap()`, `.expect()`, `if let Some(x) = ... else { panic!() }`, slice or
  map indexing (`v[0]`, `m["k"]`), and unchecked `as` casts. Each of these can panic or
  silently corrupt data.
- An equivalent `match`/`if let` form would also be acceptable, but the combinator form is
  shorter, matches common Rust style, and keeps each field's defaulting rule on one line.

## Output-side guarantee

`VulnerabilitySummary` has **no `Option` fields** and derives `Default`. Downstream
consumers (the email digest renderer) therefore never need their own null guards. The
`Option`-handling stays at this single boundary instead of spreading to every consumer.

## Test coverage for the guards

| Guard path | Test |
|---|---|
| All `Some` | fully-populated test: exact `assert_eq!` on the whole struct |
| All `None` | all-None test: `assert_eq!(summary, VulnerabilitySummary::default())` |
| Each `None` independently | mixed test: three cases, each with one field `Some` and the others `None` |
| `Some(vec![])` vs `None` for cves | cve_count consistency test: both give `cve_count == 0`, `cve_list == vec![]` |
| `cve_count == cve_list.len()` | consistency test over 0 / 1 / 5 / `None` inputs |
