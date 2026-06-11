<!-- SYNTHETIC TEST DATA — RPM system package Vulnerability issue for triage-security eval testing -->

# Mock Jira Vulnerability Issue

**Key**: TC-8005
**Summary**: CVE-2026-40215 openssl-libs - Buffer over-read in X.509 certificate verification [rhtpa-2.2]
**Issue Type**: Vulnerability
**Status**: New
**Labels**: CVE-2026-40215, pscomponent:org/rhtpa-server
**Affects Versions**: RHTPA 2.0.0
**Due Date**: 2026-08-15
**Assignee**: Unassigned

## Remote Links

- [CVE-2026-40215](https://www.cve.org/CVERecord?id=CVE-2026-40215) — CVE Record
- [RHSA-2026:4021](https://access.redhat.com/errata/RHSA-2026:4021) — Red Hat Security Advisory

## Comments

_(no comments)_

---

## Description

A vulnerability was found in openssl-libs. Versions of openssl before 3.0.7-28.el9_4 are vulnerable to a buffer over-read during X.509 certificate chain verification. A remote attacker can craft a certificate with a malformed extension that triggers an out-of-bounds read, potentially leaking sensitive memory contents or causing a crash.

**Affected package**: openssl-libs
**Affected versions**: versions before 3.0.7-28.el9_4
**Fixed version**: 3.0.7-28.el9_4
**CVSS**: 7.1 (High)

The vulnerability exists in the `X509_verify_cert()` code path where the extension parser does not properly validate the length field of a Subject Alternative Name extension. The fix adds bounds checking before reading extension data.

### References

- https://www.cve.org/CVERecord?id=CVE-2026-40215
- https://access.redhat.com/errata/RHSA-2026:4021
