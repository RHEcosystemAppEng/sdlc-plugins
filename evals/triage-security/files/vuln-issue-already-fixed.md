<!-- SYNTHETIC TEST DATA — Vulnerability issue where all versions ship patched dependency for triage-security eval testing -->

# Mock Jira Vulnerability Issue

**Key**: TC-8002
**Summary**: CVE-2026-28940 serde_json - Stack overflow on deeply nested input [rhtpa-2.2]
**Issue Type**: Vulnerability
**Status**: New
**Labels**: CVE-2026-28940, pscomponent:org/rhtpa-server
**Affects Versions**: RHTPA 2.2.0
**Due Date**: 2026-07-30
**Assignee**: Unassigned

## Remote Links

- [GHSA-2026-j9r2-m5vk](https://github.com/advisories/GHSA-2026-j9r2-m5vk) — GitHub Advisory
- [CVE-2026-28940](https://www.cve.org/CVERecord?id=CVE-2026-28940) — CVE Record

## Comments

_(no comments)_

---

## Description

A vulnerability was found in serde_json. Versions of serde_json before 1.0.135 are vulnerable to a stack overflow when deserializing deeply nested JSON input. An attacker can craft a JSON payload with thousands of nested arrays or objects that causes unbounded recursion during deserialization, leading to a stack overflow and process crash.

**Affected package**: serde_json
**Affected versions**: versions before 1.0.135
**Fixed version**: 1.0.135
**CVSS**: 5.3 (Medium)

The fix introduces a configurable recursion limit that defaults to 128 levels of nesting.

### References

- https://github.com/advisories/GHSA-2026-j9r2-m5vk
- https://rustsec.org/advisories/RUSTSEC-2026-0019.html
