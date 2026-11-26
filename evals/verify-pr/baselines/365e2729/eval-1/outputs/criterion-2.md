# Criterion 2: `GET /api/v2/package?license=MIT,Apache-2.0` returns packages with either license

**Verdict: PASS**

## Code that implements it

`modules/fundamental/src/package/endpoints/list.rs`, in `validate_license_param`, splits the value on commas and trims each part:
```rust
let identifiers: Vec<String> = license.split(',').map(|s| s.trim().to_string()).collect();
```
Each identifier is validated, and the whole list is returned as a `Vec<String>`.

`modules/fundamental/src/package/service/mod.rs` turns that list into one `IN` clause:
```rust
Condition::any()
    .add(package_license::Column::License.is_in(licenses.iter().cloned()))
```
`License IN ('MIT', 'Apache-2.0')` matches packages with either license, which gives the union.

## Test coverage

`tests/api/package.rs::test_list_packages_multi_license_filter` seeds MIT, Apache-2.0 and GPL-3.0-only packages, then calls `?license=MIT,Apache-2.0`. It asserts:
- the status is `200 OK`
- `items.len() == 2`
- every item is either MIT or Apache-2.0, so the GPL package is excluded

This matches the test requirement "comma-separated license filter returns union of matching packages".

## Caveats (non-blocking)

- The `INNER JOIN` on `package_license` has no `DISTINCT` or `GROUP BY`. A package with several license rows that all match could be returned twice and counted twice in `total`. The test seeds only single-license packages, so it would not catch this. The criterion as written is still met.
- `Condition::any()` wraps a single `is_in`, so it adds nothing. It is harmless.
