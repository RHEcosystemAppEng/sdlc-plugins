# Criterion 2: `GET /api/v2/package?license=MIT,Apache-2.0` returns packages with either license

**Verdict: PASS**

## Reasoning

1. **Comma separation** — `validate_license_param` does `license.split(',').map(|s| s.trim().to_string())`, producing `["MIT", "Apache-2.0"]`. Whitespace around commas (e.g. `MIT, Apache-2.0`) is also tolerated by the `trim()`.
2. **Validation** — both identifiers are valid SPDX expressions, so validation passes and the vector is returned.
3. **Union semantics** — the service builds `Condition::any()` with `package_license::Column::License.is_in(["MIT", "Apache-2.0"])`. `IN (...)` is an OR across the values, so a package matches if its license is MIT **or** Apache-2.0 (union, not intersection).
4. **Test evidence** — `test_list_packages_multi_license_filter` seeds MIT, Apache-2.0 and GPL-3.0-only packages, requests `?license=MIT,Apache-2.0`, and asserts status 200, exactly 2 items, and that each item is MIT or Apache-2.0 (GPL excluded).

## Notes (informational, not blocking)
- Because the filter uses an INNER JOIN on the `package_license` mapping, a package that has *both* MIT and Apache-2.0 license rows could theoretically appear twice in the multi-value case (and be double-counted in `total`). The task does not specify multi-licensed packages and the test data uses one license per package, so this does not violate the criterion as written. A `DISTINCT` / `EXISTS` subquery could harden this in the future.
