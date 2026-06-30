## TC-9004: Add license compliance report endpoint — Implementation Plan

### Tasks

| # | Task | Repository | Summary | Digest |
|---|---|---|---|---|
| 1 | License policy model | trustify-backend | Define LicensePolicy struct and JSON config loading | [sdlc-workflow] Description digest: sha256-md:9297ab151d975fd7123994f702f87043885863bbb60a932bfaf0f251b580b7f1 |
| 2 | License report model | trustify-backend | Define LicenseReport, LicenseGroup, and ComplianceSummary response structs | [sdlc-workflow] Description digest: sha256-md:a20eae0fe18fac66b8e13c8c0b712d6b3c5ece1ceaa0e2394d72285b63713d7d |
| 3 | License report service | trustify-backend | Implement LicenseReportService with policy evaluation and package grouping | [sdlc-workflow] Description digest: sha256-md:490f24b6f2a6ce324f987f3485076b280bf0a22a85346e643e2a36d1044d8d36 |
| 4 | License report endpoint | trustify-backend | Add GET /api/v2/sbom/{id}/license-report handler and route registration | [sdlc-workflow] Description digest: sha256-md:a3c704b1bb15fe6c589534f8a65e882b40efad37f10ec72c5a26b1fd8a3a114b |
| 5 | Integration tests | trustify-backend | Full-stack integration tests for license report endpoint | [sdlc-workflow] Description digest: sha256-md:2a014133af63132a4cc77105968a0c0a3e1bcd47a10b43728eb648bf49dfc94c |

### Repositories

| Repository | Role |
|---|---|
| trustify-backend | Rust backend service — all tasks target this repository |

### Architecture Summary

The feature adds a new `license` domain module under `modules/fundamental/src/license/` following the existing model/service/endpoints pattern. A configurable license policy (JSON file) defines allowed and denied licenses. The `LicenseReportService` queries existing `sbom_package` and `package_license` entities to aggregate packages by license, evaluates each group against the policy, and returns a structured `LicenseReport`. The endpoint is mounted as a sub-resource of SBOM at `GET /api/v2/sbom/{id}/license-report`. No new database tables are required.

Task dependency chain: 1 -> 2 -> 3 -> 4 -> 5 (linear, each builds on the previous).

### Inherited Fields

Inherited fields propagated to tasks: priority=Major, fixVersion=RHTPA 1.5.0
