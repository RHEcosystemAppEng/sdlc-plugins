# Criterion 2: Packages with no vulnerabilities show `vulnerability_count: 0`

**Verdict: FAIL**

## Reasoning
- `modules/fundamental/src/package/service/mod.rs` (hunk `@@ -30,6 +30,14 @@`) sets the value to a literal:
  ```rust
  vulnerability_count: 0, // TODO: implement subquery
  ```
- A package with no vulnerabilities does report `0`, but only because **every** package reports `0`. The value is never computed from the `sbom_package` -> `sbom_advisory` -> `advisory` data.
- The criterion assumes a real count, where zero is the computed result for a package with no linked advisories. A hardcoded stub meets it by accident, not by implementing it. The matching test, `test_package_without_vulnerabilities_has_zero_count`, passes trivially and proves nothing about the behaviour.
- The TODO comment shows the author knew the work was incomplete.

## Required fix
Implement the correlated subquery from the Implementation Notes, so that `0` comes out of a real `COUNT(DISTINCT a.id)` for packages with no linked advisories.
