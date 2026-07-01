## Criterion 2: `GET /api/v2/package?license=MIT,Apache-2.0` returns packages with either license

### Evidence

**Endpoint layer (`list.rs`):**
- `validate_license_param` splits the license string on commas: `license.split(',').map(|s| s.trim().to_string()).collect()`.
- For input `"MIT,Apache-2.0"`, this produces `vec!["MIT", "Apache-2.0"]`.
- Each identifier is validated individually via `spdx::Expression::parse`.

**Service layer (`service/mod.rs`):**
- The filter uses `Condition::any()` with `is_in(licenses.iter().cloned())`.
- `Condition::any()` produces an OR condition, and `is_in` generates a SQL `IN ('MIT', 'Apache-2.0')` clause.
- This correctly returns the union of packages matching either license.

**Test (`tests/api/package.rs`):**
- `test_list_packages_multi_license_filter` seeds three packages: `pkg-a` (MIT), `pkg-b` (Apache-2.0), `pkg-c` (GPL-3.0-only).
- Queries `GET /api/v2/package?license=MIT,Apache-2.0`.
- Asserts `resp.status() == StatusCode::OK`.
- Asserts `body.items.len() == 2` (MIT + Apache-2.0, excluding GPL-3.0-only).
- Asserts `body.items.iter().all(|p| p.license == "MIT" || p.license == "Apache-2.0")`.

### Verdict: PASS

The comma-separated parsing in `validate_license_param` combined with the `is_in` filter in the service layer correctly returns the union of packages matching any of the specified licenses. The test validates this behavior with three distinct licenses, confirming the GPL-3.0-only package is excluded.
