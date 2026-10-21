# Step 3 — Affects Versions Correction: TC-8005

## Current vs Corrected Affects Versions

| | Affects Versions |
|---|---|
| PSIRT-assigned (current) | RHTPA 2.0.0 |
| Lock-file evidence (corrected) | RHTPA 2.2.0, RHTPA 2.2.1, RHTPA 2.2.2 |

## Rationale

The PSIRT-assigned Affects Version "RHTPA 2.0.0" is incorrect for two reasons:

1. **Wrong stream**: RHTPA 2.0.0 does not correspond to any version in the
   configured 2.2.x or 2.1.x version streams. No 2.0.x stream is configured
   in Security Configuration. The issue's stream suffix `[rhtpa-2.2]` scopes
   it to the 2.2.x stream.

2. **Lock-file evidence**: Analysis of `rpms.lock.yaml` at each pinned build
   tag shows that within the 2.2.x stream:
   - **2.2.0** (v0.4.5): openssl-libs 3.0.7-25.el9_3 — AFFECTED (< 3.0.7-28.el9_4)
   - **2.2.1** (v0.4.8): openssl-libs 3.0.7-27.el9_4 — AFFECTED (< 3.0.7-28.el9_4)
   - **2.2.2** (v0.4.9): retag of 2.2.1 — AFFECTED (same as 2.2.1)
   - **2.2.3** (v0.4.11): openssl-libs 3.0.7-28.el9_4 — NOT AFFECTED (= fixed version)
   - **2.2.4** (v0.4.12): openssl-libs 3.0.7-28.el9_4 — NOT AFFECTED (= fixed version)

## Proposed Jira Update

- **Remove**: RHTPA 2.0.0
- **Add**: RHTPA 2.2.0, RHTPA 2.2.1, RHTPA 2.2.2

These version names use the configured Jira version prefix "RHTPA" and
correspond to the product versions that actually ship vulnerable openssl-libs
per rpms.lock.yaml evidence. The versions would be discovered dynamically
via `getJiraIssueTypeMetaWithFields` for the Vulnerability issue type before
applying the correction.
