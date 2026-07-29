# Criterion 2: GET /api/v2/package?license=MIT,Apache-2.0 returns packages with either license

## Verdict: PASS

## Reasoning

The implementation satisfies this criterion through comma-separated value handling in the validation and filtering pipeline:

### Query Parameter Parsing (list.rs)

When a request arrives at `GET /api/v2/package?license=MIT,Apache-2.0`, the `license` field of `PackageListParams` is populated with `Some("MIT,Apache-2.0")` as a single string.

### Comma Separation and Validation (list.rs)

The `validate_license_param("MIT,Apache-2.0")` function:
1. Splits the input on commas: `"MIT,Apache-2.0".split(',')` produces `["MIT", "Apache-2.0"]`
2. Trims whitespace from each token via `.map(|s| s.trim().to_string())`
3. Validates each token individually with `spdx::Expression::parse(id)` -- both "MIT" and "Apache-2.0" are valid SPDX identifiers
4. Returns `Ok(vec!["MIT".to_string(), "Apache-2.0".to_string()])`

### Service Layer Filtering (service/mod.rs)

The validated identifiers `["MIT", "Apache-2.0"]` are passed to `PackageService::list()`. The filter logic:
1. Constructs `Condition::any().add(package_license::Column::License.is_in(licenses.iter().cloned()))`, which generates an SQL `WHERE package_license.license IN ('MIT', 'Apache-2.0')` clause
2. The use of `Condition::any()` with `is_in()` produces a union (OR) semantic -- packages matching either license are returned
3. The `InnerJoin` on `PackageLicense` ensures only packages with a license record are matched

### Test Coverage

The test `test_list_packages_multi_license_filter` directly validates this criterion:
- Seeds 3 packages: pkg-a (MIT), pkg-b (Apache-2.0), pkg-c (GPL-3.0-only)
- Queries `GET /api/v2/package?license=MIT,Apache-2.0`
- Asserts `StatusCode::OK`
- Asserts `body.items.len() == 2` (MIT + Apache-2.0, excluding GPL-3.0-only)
- Asserts `body.items.iter().all(|p| p.license == "MIT" || p.license == "Apache-2.0")` (union of matching licenses)

### Conclusion

The implementation correctly handles comma-separated license values by splitting, validating each independently, and using SQL `IN` clause semantics to return the union of packages matching any of the specified licenses.
