# Criterion 2: Packages with no vulnerabilities show `vulnerability_count: 0`

**Verdict: PASS (vacuous: only true because of a hardcoded stub)**

## Reasoning
- In `modules/fundamental/src/package/service/mod.rs` the field is filled in as `vulnerability_count: 0, // TODO: implement subquery` for **every** package.
- A package with no vulnerabilities will therefore return `0`, so the literal wording of the criterion holds.
- That result does not come from computing anything. The value is a constant, not a count from the `sbom_package -> sbom_advisory -> advisory` join. Packages that *do* have vulnerabilities also return 0. That is wrong, and Criterion 3 and the task Description catch it.
- The test `test_package_without_vulnerabilities_has_zero_count` asserts 0 and would pass, but only because of the stub.

## Evidence
- `+                vulnerability_count: 0, // TODO: implement subquery`
- `tests/api/package_vuln_count.rs`: `assert_eq!(pkg.vulnerability_count, 0);`
