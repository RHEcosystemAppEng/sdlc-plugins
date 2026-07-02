## TC-9003: SBOM Comparison View — Implementation Plan Summary

### Tasks Created

8 tasks created for feature TC-9003:

| Task | Repository | Description |
|---|---|---|
| Task 1 | trustify-ui | Create feature branch `TC-9003` (bookend: create-branch) |
| Task 2 | trustify-backend | Comparison response model and diff service |
| Task 3 | trustify-backend | Comparison REST endpoint and integration tests |
| Task 4 | trustify-ui | Comparison API types, client function, and React Query hook |
| Task 5 | trustify-ui | Comparison page UI with diff sections |
| Task 6 | trustify-ui | Route registration, SBOM list compare action, and E2E tests |
| Task 7 | trustify-backend | Documentation for SBOM comparison feature |
| Task 8 | trustify-ui | Merge feature branch `TC-9003` to `main` (bookend: merge-branch) |

### Repositories Affected

- **trustify-backend** — 3 tasks (model/service, endpoint/tests, documentation)
- **trustify-ui** — 5 tasks (2 bookends + API layer, comparison page, routing/E2E)

### Architecture Summary

**Workflow mode**: Feature-branch (`TC-9003`) — cross-repo atomicity required because the frontend comparison page depends on the backend comparison endpoint; neither functions independently.

**Backend**: New `GET /api/v2/sbom/compare?left={id1}&right={id2}` endpoint computes a structured diff on the fly from existing SBOM, package, advisory, and license data (no new database tables). The diff includes six categories: added packages, removed packages, version changes, new vulnerabilities, resolved vulnerabilities, and license changes.

**Frontend**: New comparison page at `/sbom/compare` with PatternFly components following Figma design specs — header toolbar with typeahead SBOM selectors, Compare/Export actions, and six collapsible diff sections with color-coded count badges and sortable data tables. URL-encoded SBOM IDs support bookmarking and sharing. The SBOM list page gains checkbox selection and a "Compare selected" navigation action.

### Propagated Fields

```
additional_fields: { "labels": ["ai-generated-jira"], "priority": {"name": "Critical"}, "fixVersions": [{"name": "RHTPA 1.5.0"}] }
```

Priority **Critical** and Fix Version **RHTPA 1.5.0** propagated from parent feature TC-9003 to all tasks.
