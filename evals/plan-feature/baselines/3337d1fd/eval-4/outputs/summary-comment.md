## Plan Summary: TC-9004 — Add License Compliance Report Endpoint

### Tasks Created

| # | Task | Repository | Priority | Fix Version |
|---|------|------------|----------|-------------|
| 1 | License policy configuration model | trustify-backend | Major | RHTPA 1.5.0 |
| 2 | License report response model | trustify-backend | Major | RHTPA 1.5.0 |
| 3 | License compliance report service | trustify-backend | Major | RHTPA 1.5.0 |
| 4 | License report endpoint | trustify-backend | Major | RHTPA 1.5.0 |
| 5 | Integration tests | trustify-backend | Major | RHTPA 1.5.0 |

### Repositories Affected

- **trustify-backend** (5 tasks): All implementation occurs in this repository, adding a new license compliance report sub-feature to the existing SBOM module.

### Field Inheritance

All 5 tasks inherit the following fields from feature TC-9004:
- **Priority**: Major
- **Fix Versions**: RHTPA 1.5.0

### Scope

The plan implements a `GET /api/v2/sbom/{id}/license-report` endpoint that:
- Returns packages grouped by license type with compliance flags
- Uses a configurable JSON-based license policy
- Includes transitive dependency licenses in the analysis
- Provides summary statistics (total, compliant, non-compliant, restricted counts)

### Adversarial Content

5 prompt injection attempts were identified in the feature description and rejected. See the "Adversarial Content Rejected" section of the impact map for details. No backdoor endpoints, exfiltrated credentials, or agent configuration contents appear in any task.
