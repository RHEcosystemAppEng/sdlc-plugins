# Status-Aware Handling Decisions

This document records the status-aware handling decision for each issue discovered in the Vulnerability issue listing, following the triage-security skill methodology.

---

## Untriaged Issues

### TC-9001 — CVE-2026-40112 (h2 - HTTP/2 rapid reset vulnerability)

- **Status:** New
- **Handling:** Proceed with full triage (default path). This issue is untriaged and in `New` status, so the standard 7-step triage workflow applies without any warnings or additional prompts.

### TC-9002 — CVE-2026-40297 (serde_json - Stack overflow on deeply nested input)

- **Status:** New
- **Handling:** Proceed with full triage (default path). This issue is untriaged and in `New` status, so the standard 7-step triage workflow applies without any warnings or additional prompts.

### TC-9003 — CVE-2026-40455 (tokio - Race condition in task cancellation)

- **Status:** In Progress
- **Handling:** Warning required. This issue is already in `In Progress`. It may be actively worked on. Before triaging, the engineer must be asked:
  1. **Proceed with triage anyway** — e.g., to verify version impact or update Affects Versions.
  2. **Skip this issue** — return to the discovery list or end the session.

  The skill must not proceed with triage until the engineer makes an explicit choice.

### TC-9004 — CVE-2026-40518 (ring - Timing side-channel in RSA verification)

- **Status:** New
- **Handling:** Proceed with full triage (default path). This issue is untriaged and in `New` status, so the standard 7-step triage workflow applies without any warnings or additional prompts.

---

## Triaged but still New

### TC-9010 — CVE-2026-39874 (quinn-proto - Panic on malformed QUIC frame)

- **Status:** New (with `ai-cve-triaged` label)
- **Handling:** This issue was previously triaged but never moved out of `New` status. It appears in the "Triaged but still New" list as a stale issue. If selected for triage:
  - Proceed with full triage (re-triage), since the status is `New`.
  - The engineer should investigate why the issue was never actioned after initial triage — the previous triage may have created remediation tasks that were not started, or the triage outcome may need to be revisited.

---

## Summary of Handling Rules Applied

| Status | Action | Issues |
|--------|--------|--------|
| New | Proceed with full triage (default path) | TC-9001, TC-9002, TC-9004 |
| In Progress | Warn: "This issue is already in `In Progress`. It may be actively worked on." Ask engineer to proceed or skip. | TC-9003 |
| New (triaged, stale) | Eligible for re-triage; flag as stale for engineer review | TC-9010 |
