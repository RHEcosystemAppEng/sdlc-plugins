# Defensive Property Access Analysis — TC-9211

## Why guards are needed

`AdvisoryIngestResult` is produced by a **different crate** (`modules/ingestor`, through
`IngestorService::ingest_advisory()`) and consumed in `modules/fundamental`. Data that crosses
this module boundary needs guards, as the implement-task skill's "Defensive property access on external data" rule requires:
- The producer's schema explicitly allows absence: every aggregate field is `Option<T>`.
- The task description says each field "may be `None`" in real scenarios: advisories without CVE references, without package-level detail, or without severity metadata.
- The ingestor can change independently. Code that assumes `Some` today could start panicking after an upstream change that compiles cleanly.
- The acceptance criteria require "without panicking". So `.unwrap()`, `.expect()`, and indexing (`[0]`, `map["critical"]`) are banned on these paths.

In Rust, the compiler already forces you to handle `Option`. The real risk is a "lazy" handling such as `.unwrap()` or `.expect("always set")`, which compiles fine and then panics at runtime. The guards below handle `None` without panicking.

## Field-by-field analysis

| Field | Upstream type | Needs guard? | Guard pattern | Default | Rationale |
|---|---|---|---|---|---|
| `cves` | `Option<Vec<String>>` | **Yes** | `result.cves.clone().unwrap_or_default()` | `Vec::new()` | The output needs an owned `Vec<String>`. `unwrap_or_default` gives an empty list for `None` and never panics. |
| `cve_count` (derived) | from `cves` | **Yes, indirectly** | `cve_list.len()`, computed **after** the guard | `0` | Deriving from the already-defaulted list guarantees `cve_count == cve_list.len()` (AC4) in every case, including `None` and `Some(vec![])`. It is never computed from the raw `Option`. |
| `affected_packages` | `Option<Vec<AffectedPackage>>` | **Yes** | `result.affected_packages.as_ref().map_or(0, Vec::len)` | `0` | Only the count is needed. `as_ref()` borrows instead of cloning the whole package vector, and `map_or` gives 0 for `None`. No nested `AffectedPackage` fields are read, so no inner guards are needed. |
| `severity_counts` | `Option<HashMap<String, u32>>` | **Yes** | `result.severity_counts.clone().unwrap_or_default()` | `HashMap::new()` | The output needs an owned map. The default is an empty map. Keys are copied as-is, with no `map["critical"]` indexing, which would panic on a missing key. |
| Length → `u32` conversion | `usize` | **Yes (numeric)** | `u32::try_from(len).unwrap_or(u32::MAX)` | saturates | `len as u32` silently truncates on overflow. `try_from` with a saturating fallback has no panic and no wraparound. The case is unrealistic but cheap to make correct. |

## Guard patterns used (idiomatic Rust)

```rust
// Owned collection needed -> clone the inner value, default on None
let cve_list = result.cves.clone().unwrap_or_default();
let severity_breakdown = result.severity_counts.clone().unwrap_or_default();

// Only a derived scalar needed -> borrow, then map with a fallback
let affected_package_count = result.affected_packages.as_ref().map_or(0, Vec::len);

// Derived invariant computed from the guarded value, not the raw Option
let cve_count = u32::try_from(cve_list.len()).unwrap_or(u32::MAX);
```

Why these patterns and not others:
- **`unwrap_or_default()`** is the idiomatic Rust guard for an optional collection. It is the skill's stated Rust pattern and needs no hand-written default literal. It works because `Vec<String>` and `HashMap<String, u32>` both implement `Default`.
- **`.as_ref().map_or(0, Vec::len)`** avoids cloning a potentially large `Vec<AffectedPackage>` just to count it.
- **`if let Some(..)`** would also work, but needs more lines for the same result. The combinators keep each guard to one line next to the field it protects.
- **Banned**: `.unwrap()`, `.expect(..)`, `unwrap_unchecked`, `[index]`, `map[&key]`, and `as u32` truncation.
- **Owned-input alternative**: if callers can pass `AdvisoryIngestResult` by value, use `result.cves.unwrap_or_default()` directly with no clone. Choose between the two by checking the call sites with `find_referencing_symbols`.

## Fields that do NOT need guards

- **`AffectedPackage` inner fields**: not accessed. Only the vector length is used. If a future version reports per-package detail (e.g. names), each inner `Option` field would need its own guard.
- **Output `VulnerabilitySummary` fields**: deliberately non-`Option`, with `#[derive(Default)]`. Downstream email-rendering code can then read `summary.cve_list.join(", ")` or `summary.severity_breakdown.get("critical").copied().unwrap_or(0)` without guarding again. The extractor is the single normalization point.

## Semantic edge cases

| Input | Result | Note |
|---|---|---|
| `cves: None` | `cve_list: []`, `cve_count: 0` | as specified |
| `cves: Some(vec![])` | `cve_list: []`, `cve_count: 0` | treated the same as None; tested |
| `affected_packages: None` | `affected_package_count: 0` | as specified |
| `affected_packages: Some(vec![])` | `0` | tested |
| `severity_counts: None` | `{}` | as specified |
| `severity_counts: Some({})` | `{}` | tested |
| All None | `VulnerabilitySummary::default()` | asserted by full struct equality |
| Mixed | each field defaults independently | one test per None position |

No deduplication or filtering of CVE IDs is done. The task does not require it, and doing it would change `cve_count` semantics beyond the specification. Tests must not assert uniqueness, because the requirements do not state it.

## Test coverage of the guards

Each guard is covered by a test that asserts **values**, using full `VulnerabilitySummary` equality rather than only `len()`:
1. All `Some` → exact populated summary.
2. All `None` → `== VulnerabilitySummary::default()`. This proves there is no panic and all values are zeroed.
3. Mixed: exactly one field `Some` per case (three cases). This proves the defaults are independent.
4. `cve_count == cve_list.len()` across `None`, `Some(vec![])`, and non-empty lists.
