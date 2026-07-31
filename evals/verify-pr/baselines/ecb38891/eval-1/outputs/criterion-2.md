## Criterion 2: `GET /api/v2/package?license=MIT,Apache-2.0` returns packages with either license

### Verdict: PASS

### Reasoning

The implementation supports comma-separated license values through the validation and filtering pipeline:

**Parsing and validation** (`modules/fundamental/src/package/endpoints/list.rs`):
- `validate_license_param` splits the input string on commas: `license.split(',').map(|s| s.trim().to_string()).collect()`. For input "MIT,Apache-2.0", this produces `vec!["MIT", "Apache-2.0"]`.
- Each identifier is validated individually via `Expression::parse(id)`. Both "MIT" and "Apache-2.0" are valid SPDX identifiers.
- The validated vector is returned and passed to the service layer.

**Query construction** (`modules/fundamental/src/package/service/mod.rs`):
- The filter uses `Condition::any()` with `is_in(licenses.iter().cloned())`. `Condition::any()` produces an OR-based filter, and `is_in` generates `WHERE license IN ('MIT', 'Apache-2.0')`.
- This correctly returns the union of packages matching either license.

**Test coverage** (`tests/api/package.rs`):
- `test_list_packages_multi_license_filter` seeds 3 packages (MIT, Apache-2.0, GPL-3.0-only), requests `?license=MIT,Apache-2.0`, and asserts:
  - Response status is 200 OK
  - Exactly 2 items returned (MIT and Apache-2.0, excluding GPL-3.0-only)
  - All returned items have license equal to "MIT" or "Apache-2.0"

The comma-separation parsing, OR-based filtering, and union semantics are all verified.
