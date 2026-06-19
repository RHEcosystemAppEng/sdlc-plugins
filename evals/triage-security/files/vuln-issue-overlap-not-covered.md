<!-- SYNTHETIC TEST DATA — cross-CVE overlap where existing remediation does NOT cover this CVE's fix threshold -->

# Mock Jira Vulnerability Issue

**Key**: TC-8011
**Summary**: CVE-2026-45678 webpack - Arbitrary Code Execution via loader chain [rhtpa-2.2]
**Issue Type**: Vulnerability
**Status**: New
**Labels**: CVE-2026-45678, pscomponent:org/rhtpa-ui
**Affects Versions**: RHTPA 2.2.0
**Due Date**: 2026-08-15
**Assignee**: Unassigned

## Custom Fields

- **customfield_10632** (Upstream Affected Component): webpack
- **customfield_10669** (PS Component): pscomponent:org/rhtpa-ui
- **customfield_10832** (Stream): rhtpa-2.2

## Issue Links

_(no existing links)_

## Remote Links

- [GHSA-2026-wk55-m3rr](https://github.com/advisories/GHSA-2026-wk55-m3rr) — GitHub Advisory
- [CVE-2026-45678](https://www.cve.org/CVERecord?id=CVE-2026-45678) — CVE Record

## Comments

_(no comments)_

---

## Description

A vulnerability was found in webpack. The webpack package before version 5.98.0 allows arbitrary code execution through a specially crafted loader chain configuration. An attacker with control over a project's webpack configuration can execute arbitrary code during the build process.

**Affected package**: webpack
**Affected versions**: versions before 5.98.0
**Fixed version**: 5.98.0
**CVSS**: 7.8 (High)

The vulnerability exists because webpack does not properly sanitize loader paths when resolving the loader chain, allowing path traversal to execute arbitrary modules.

### References

- https://github.com/advisories/GHSA-2026-wk55-m3rr

### Related CVE Jiras (provided by JQL search on customfield_10632 = "webpack")

The following related CVE Jira was found affecting the same upstream component:

- **TC-8012** — CVE-2026-43210 webpack - ReDoS in chunk name validation [rhtpa-2.2]
  - **Status**: Closed (Done)
  - **Labels**: CVE-2026-43210, pscomponent:org/rhtpa-ui
  - **customfield_10632**: webpack
  - **customfield_10669**: pscomponent:org/rhtpa-ui
  - **customfield_10832**: rhtpa-2.2
  - **Issue Links**:
    - **Depend**: TC-8013 (remediation Task)
      - **Summary**: Bump webpack to 5.96.1 in rhtpa-ui [rhtpa-2.2]
      - **Status**: Closed (Done)
      - **Description excerpt**: "Bump webpack from 5.95.0 to 5.96.1 to resolve CVE-2026-43210. The fix requires webpack >= 5.96.0."
