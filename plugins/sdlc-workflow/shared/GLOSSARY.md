# CVE Dependency Remediation

This glossary defines terms shared by CVE triage and dependency implementation.

## Dependency Remediation

**Dependency update convention**:
A target project's declared policy for how dependencies are updated and how the result is verified.
_Avoid_: inferred package-manager policy

**Batch update**:
An update operation that refreshes all dependencies within the project's declared constraints.
_Avoid_: blanket upgrade

**Targeted update**:
An update operation limited to one affected dependency.
_Avoid_: surgical update

**Resolved dependency graph**:
The complete set of dependency versions and paths that the project will build or ship after resolution.
_Avoid_: lockfile entry alone

**Waiting for fix**:
The state of a CVE remediation task that remains open because no permitted project update path removes every vulnerable dependency path.
_Avoid_: fixed, resolved

**Upstream fix evidence**:
Public advisory/version information and configured upstream branch evidence showing whether the fixed release is available to the project.
_Avoid_: resolver preflight
