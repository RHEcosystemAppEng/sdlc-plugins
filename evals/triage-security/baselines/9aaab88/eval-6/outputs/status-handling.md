# Status-Aware Handling

Based on the discovery results, each issue's current Jira status determines how the skill proceeds when the engineer selects it for triage.

---

## New Issues -- Full Triage

The following issues are in **New** status and are eligible for full triage (Steps 1-7):

### TC-9001 — CVE-2026-40112 h2 - HTTP/2 rapid reset vulnerability [rhtpa-2.2]
- **Status:** New
- **Action:** Proceed with full triage (default path). Extract CVE data, perform version impact analysis across supported streams, correct Affects Versions, check for duplicates/siblings, verify lifecycle status, check for existing fixes, and create remediation tasks or close as appropriate.

### TC-9002 — CVE-2026-40297 serde_json - Stack overflow on deeply nested input [rhtpa-2.1]
- **Status:** New
- **Action:** Proceed with full triage (default path). Extract CVE data, perform version impact analysis across supported streams, correct Affects Versions, check for duplicates/siblings, verify lifecycle status, check for existing fixes, and create remediation tasks or close as appropriate.

### TC-9004 — CVE-2026-40518 ring - Timing side-channel in RSA verification [rhtpa-2.2]
- **Status:** New
- **Action:** Proceed with full triage (default path). Extract CVE data, perform version impact analysis across supported streams, correct Affects Versions, check for duplicates/siblings, verify lifecycle status, check for existing fixes, and create remediation tasks or close as appropriate.

---

## In Progress Issue -- Active Work Warning

### TC-9003 — CVE-2026-40455 tokio - Race condition in task cancellation [rhtpa-2.2]
- **Status:** In Progress
- **Action:** This issue is already in `In Progress`. It may be actively worked on.

> **Warning:** This issue is already in `In Progress`. It may be actively worked on.

The engineer is presented with two options:
1. **Proceed with triage anyway** -- for example, to verify version impact or update Affects Versions even though work is underway.
2. **Skip this issue** -- return to the discovery list or end the session.

If the engineer chooses to skip, return to the discovery list above.
