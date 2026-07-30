# Criterion 2: `GET /api/v2/package?license=MIT,Apache-2.0` returns packages with either license

## Verdict: PASS

## Reasoning

### What was checked

This criterion requires that the endpoint supports comma-separated license values and returns the union of packages matching any of the specified licenses.

### Evidence from the diff

**1. Comma splitting (`modules/fundamental/src/package/endpoints/list.rs`):**

The `validate_license_param` function splits the input on commas and trims whitespace:

```rust
let identifiers: Vec<String> = license.split(',').map(|s| s.trim().to_string()).collect();
```

For input `"MIT,Apache-2.0"`, this produces `["MIT", "Apache-2.0"]`.

**2. Per-identifier validation:**

Each identifier in the split list is validated independently through `spdx::Expression::parse`. Both "MIT" and "Apache-2.0" are valid SPDX identifiers, so both pass validation.

**3. Union filter (`modules/fundamental/src/package/service/mod.rs`):**

The filter uses `Condition::any()` with `is_in`:

```rust
Condition::any()
    .add(package_license::Column::License.is_in(licenses.iter().cloned()))
```

`is_in` generates a SQL `WHERE license IN ('MIT', 'Apache-2.0')` clause, which matches packages with either license. `Condition::any()` ensures this is an OR-style match.

**4. Test coverage (`tests/api/package.rs`):**

The test `test_list_packages_multi_license_filter` directly verifies this criterion:
- Seeds packages with MIT, Apache-2.0, and GPL-3.0-only licenses
- Requests `GET /api/v2/package?license=MIT,Apache-2.0`
- Asserts response status is 200 OK
- Asserts exactly 2 items returned (MIT and Apache-2.0, excluding GPL-3.0-only)
- Asserts all returned items have license equal to either "MIT" or "Apache-2.0"

### Conclusion

The code correctly splits comma-separated license values, validates each individually, and applies a SQL IN clause that returns the union of matching packages. The test provides direct verification of this behavior. Criterion satisfied.
