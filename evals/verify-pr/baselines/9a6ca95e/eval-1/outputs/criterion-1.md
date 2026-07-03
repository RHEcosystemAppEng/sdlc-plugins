## Criterion 1

**Text:** `GET /api/v2/package?license=MIT` returns only packages with MIT license

### Analysis

The diff introduces a complete pipeline for single-license filtering:

1. **Parameter extraction** (`list.rs`): The `PackageListParams` struct gains `pub license: Option<String>`, which Axum's `Query` extractor automatically binds from the `?license=MIT` query string.

2. **Validation** (`list.rs`): The `validate_license_param` function parses the parameter, splitting on commas and validating each identifier via `spdx::Expression::parse(id)`. For a single value like `MIT`, this produces a `Vec<String>` containing one element `["MIT"]`.

3. **Filter application** (`service/mod.rs`): The `PackageService::list` method now accepts `license_filter: Option<&[String]>`. When `Some`, it applies:
   ```rust
   query = query.filter(
       Condition::any()
           .add(package_license::Column::License.is_in(licenses.iter().cloned()))
   );
   query = query.join(JoinType::InnerJoin, package::Relation::PackageLicense.def());
   ```
   The `is_in` with a single element effectively becomes `WHERE license = 'MIT'`, and the `InnerJoin` ensures only packages that have a matching license row are returned.

4. **Handler wiring** (`list.rs`): The `list_packages` handler maps `params.license` through `validate_license_param` and passes the result to `PackageService::list`:
   ```rust
   let license_filter = match &params.license {
       Some(license) => Some(validate_license_param(license)?),
       None => None,
   };
   ```

5. **Test coverage** (`tests/api/package.rs`): `test_list_packages_single_license_filter` seeds three packages (two MIT, one Apache-2.0), queries `?license=MIT`, and asserts:
   - Response status is 200 OK
   - Exactly 2 items returned
   - All returned items have `license == "MIT"`

### Verdict: PASS

The implementation correctly extracts, validates, and applies a single-license filter, and the test verifies the exact scenario described in the criterion.
