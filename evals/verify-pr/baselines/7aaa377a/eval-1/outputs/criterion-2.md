## Criterion 2: `GET /api/v2/package?license=MIT,Apache-2.0` returns packages with either license

**Verdict: PASS**

### Analysis

This criterion requires that comma-separated license values are treated as a union filter, returning packages that match any of the specified licenses.

### Evidence from the PR diff

**1. Comma splitting (list.rs)**

The `validate_license_param` function explicitly splits on commas and trims whitespace:

```rust
let identifiers: Vec<String> = license.split(',').map(|s| s.trim().to_string()).collect();
```

For the input `"MIT,Apache-2.0"`, this produces `["MIT", "Apache-2.0"]`. Each identifier is then validated individually against the SPDX expression parser.

**2. OR-based filtering (service/mod.rs)**

The service layer uses `Condition::any()` with `is_in`:

```rust
Condition::any()
    .add(package_license::Column::License.is_in(licenses.iter().cloned()))
```

`Condition::any()` produces an OR condition, and `is_in` generates a SQL `WHERE license IN ('MIT', 'Apache-2.0')` clause. This correctly returns the union of packages matching either license.

**3. Integration test coverage (tests/api/package.rs)**

The test `test_list_packages_multi_license_filter` seeds three packages:
- pkg-a with MIT
- pkg-b with Apache-2.0
- pkg-c with GPL-3.0-only

Then requests `?license=MIT,Apache-2.0` and asserts:
- Status is 200 OK
- Exactly 2 items returned (pkg-a and pkg-b, not pkg-c)
- All returned items have license equal to either "MIT" or "Apache-2.0"

This directly validates the union-filter behavior.

### Conclusion

The implementation correctly parses comma-separated license values into a list, validates each independently, and applies an OR-based database filter that returns the union of matching packages. The test confirms that only packages matching at least one of the specified licenses are returned.
