# Criterion 5: Response serialization includes the new field in JSON output

**Verdict: PASS**

## What was checked
- `modules/fundamental/src/package/model/summary.rs`: the new field is added to `PackageSummary`.
- `modules/fundamental/src/package/endpoints/list.rs`: the handler returns `Json<PaginatedResults<PackageSummary>>`.
- `modules/fundamental/src/package/service/mod.rs`: the service fills in the field.

## What was found
`PackageSummary` is already the JSON response type of `GET /api/v2/package`, wrapped in `Json<PaginatedResults<...>>`, so it must already derive `Serialize`. The new field is a plain `pub i64` with no `#[serde(skip)]` or other attribute that would hide it, so serde includes it in the JSON output automatically. The service sets the field on every item it returns.

The only change to `list.rs` is a trailing comment (`// vulnerability_count now included in response`). The comment does nothing, and no other code change is needed for serialization. Not changing `list.rs` beyond that is acceptable.

## Caveat
The field is serialized, but its value is always 0 (see Criterion 3). This criterion covers only whether the field appears in the output, and it does.
