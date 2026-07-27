# Criterion 2: `GET /api/v2/package?license=MIT,Apache-2.0` returns packages with either license

## Verdict: PASS

## Reasoning

### What the criterion requires

When multiple license identifiers are provided as a comma-separated list in the `license` query parameter, the endpoint must return packages matching any of the specified licenses (union/OR semantics).

### Evidence from the diff

**1. Comma splitting in validation (list.rs)**

The `validate_license_param` function splits the input on commas:

```rust
let identifiers: Vec<String> = license.split(',').map(|s| s.trim().to_string()).collect();
```

For input `"MIT,Apache-2.0"`, this produces `vec!["MIT", "Apache-2.0"]`. Each identifier is individually validated against the SPDX parser, ensuring both `MIT` and `Apache-2.0` are recognized.

**2. OR-semantics in the query (service/mod.rs)**

The filter uses `Condition::any()` with `is_in`:

```rust
query = query.filter(
    Condition::any()
        .add(package_license::Column::License.is_in(licenses.iter().cloned()))
);
```

`Condition::any()` produces an OR clause in SeaORM. The `is_in` with `["MIT", "Apache-2.0"]` generates SQL equivalent to `WHERE license IN ('MIT', 'Apache-2.0')`, which returns rows matching either license. This correctly implements union semantics.

**3. Test coverage (tests/api/package.rs)**

The test `test_list_packages_multi_license_filter` verifies this criterion:
- Seeds packages with MIT, Apache-2.0, and GPL-3.0-only licenses
- Calls `GET /api/v2/package?license=MIT,Apache-2.0`
- Asserts the response status is 200 OK
- Asserts exactly 2 items are returned (MIT and Apache-2.0, not GPL-3.0-only)
- Asserts all returned items have a license that is either MIT or Apache-2.0

### Conclusion

The comma-separated parsing produces a list of identifiers, and the `Condition::any()` + `is_in` query correctly returns the union of packages matching any of the specified licenses. The integration test confirms the behavior end-to-end. The criterion is satisfied.
