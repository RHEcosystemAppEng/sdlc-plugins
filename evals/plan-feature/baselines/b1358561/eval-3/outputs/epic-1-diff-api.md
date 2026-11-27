# Epic 1 — TC-9003: SBOM comparison diff API

**Issue type:** Epic (level 1) | **Parent:** TC-9003 | **Labels:** ai-generated-jira | **Priority:** Critical | **Fix Versions:** RHTPA 1.5.0

Backend work in trustify-backend for TC-9003: a comparison model and on-the-fly diff service over existing SBOM package, license and advisory data (Task 1), exposed as GET /api/v2/sbom/compare?left={id1}&right={id2} with validation, fail-closed 404 for unknown SBOMs, and integration tests (Task 2).
