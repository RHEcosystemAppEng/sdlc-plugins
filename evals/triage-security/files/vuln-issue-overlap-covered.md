<!-- SYNTHETIC TEST DATA — cross-CVE overlap where existing remediation already covers this CVE's fix threshold -->

# Mock Jira Vulnerability Issue

**Key**: TC-8010
**Summary**: CVE-2026-44492 axios - Server-Side Request Forgery via crafted URL [rhtpa-2.2]
**Issue Type**: Vulnerability
**Status**: New
**Labels**: CVE-2026-44492, pscomponent:org/rhtpa-ui
**Affects Versions**: RHTPA 2.2.0
**Due Date**: 2026-08-01
**Assignee**: Unassigned

## Custom Fields

- **customfield_10632** (Upstream Affected Component): axios
- **customfield_10669** (PS Component): pscomponent:org/rhtpa-ui
- **customfield_10832** (Stream): rhtpa-2.2

## Issue Links

_(no existing links)_

## Remote Links

- [GHSA-2026-ax91-r7pp](https://github.com/advisories/GHSA-2026-ax91-r7pp) — GitHub Advisory
- [CVE-2026-44492](https://www.cve.org/CVERecord?id=CVE-2026-44492) — CVE Record

## Comments

_(no comments)_

---

## Description

A vulnerability was found in axios. The axios package before version 1.8.2 is vulnerable to Server-Side Request Forgery (SSRF) via a crafted URL that bypasses hostname validation. An attacker can exploit this to make requests to internal services.

**Affected package**: axios
**Affected versions**: versions before 1.8.2
**Fixed version**: 1.8.2
**CVSS**: 8.1 (High)

The vulnerability exists because axios does not properly validate the hostname in URLs when following redirects. An attacker can craft a URL that initially resolves to an external host but redirects to an internal service.

### References

- https://github.com/advisories/GHSA-2026-ax91-r7pp

### Related CVE Jiras (provided by JQL search on customfield_10632 = "axios")

The following related CVE Jira was found affecting the same upstream component:

- **TC-8008** — CVE-2026-42035 axios - Prototype Pollution via header parsing [rhtpa-2.2]
  - **Status**: In Progress
  - **Labels**: CVE-2026-42035, pscomponent:org/rhtpa-ui
  - **customfield_10632**: axios
  - **customfield_10669**: pscomponent:org/rhtpa-ui
  - **customfield_10832**: rhtpa-2.2
  - **Issue Links**:
    - **Depend**: TC-8009 (remediation Task)
      - **Summary**: Bump axios to 1.9.0 in rhtpa-ui [rhtpa-2.2]
      - **Status**: In Progress
      - **Description excerpt**: "Bump axios from 1.7.4 to 1.9.0 to resolve CVE-2026-42035. The fix requires axios >= 1.8.0."
