<!-- SYNTHETIC TEST DATA — fictional Go-module CVE used to evaluate policy-driven task generation. -->

# Mock Jira Vulnerability Issue

**Key**: TC-8350
**Summary**: CVE-2026-77123: parser panic in netparser [rhtpa-2.2]
**Status**: New
**Labels**: CVE-2026-77123, pscomponent:org/rhtpa-server

## Description

The Go module `example.com/acme/netparser` before version 2.4.6 can panic when
parsing a malformed network frame. The affected range is `< 2.4.6`; fixed version
`2.4.6` is available. This is a high-severity denial-of-service vulnerability.

Upstream fix reference: https://example.invalid/netparser/pull/46
