<!-- SYNTHETIC TEST DATA — Vulnerability issue for a dev-only dependency (criterion) for triage-security eval testing -->

# Mock Jira Vulnerability Issue

**Key**: TC-8050
**Summary**: CVE-2026-99001 criterion - Path traversal in benchmark output [rhtpa-2.2]
**Issue Type**: Vulnerability
**Status**: New
**Labels**: CVE-2026-99001, pscomponent:org/rhtpa-server
**Affects Versions**: RHTPA 2.2.0
**Due Date**: 2026-08-01
**Assignee**: Unassigned

## Remote Links

- [CVE-2026-99001](https://www.cve.org/CVERecord?id=CVE-2026-99001) — CVE Record

## Comments

_(no comments)_

---

## Description

A vulnerability was found in criterion. The criterion crate before version 0.5.2 allows an attacker to write benchmark output files to arbitrary paths via crafted benchmark names containing path separators.

**Affected package**: criterion
**Affected versions**: versions before 0.5.2
**Fixed version**: 0.5.2
**CVSS**: 5.3 (Medium)

### References

- https://www.cve.org/CVERecord?id=CVE-2026-99001

---

## Mock Dependency Chain Data

The following data simulates what Step 2.3.5 would discover when inspecting
the Cargo.toml manifest files. In a real triage, the skill reads manifests
via `git show`; in this eval, use this data as the simulated output.

### criterion dependency chain for backend

```
Dependency chain for criterion:
  backend (workspace) → criterion (direct dev-dependency)
  Profile: dev-only ([dev-dependencies] in backend/Cargo.toml)
  NOT present in production builds — used for benchmarks only

First appeared: 2.1.0 (initial project setup)
Present in all versions
```

**Manifest evidence:**
```toml
# backend/Cargo.toml (all versions)
[dev-dependencies]
criterion = "0.5.1"
```
