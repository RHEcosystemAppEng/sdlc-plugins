# Status-Aware Handling Decisions

For each issue surfaced by discovery mode, the following status-aware handling
decisions apply per the triage-security skill's status-aware handling protocol.

---

## Query 1: Untriaged Issues

### TC-9001 — Status: New

**Handling**: Proceed with full triage (default path).

TC-9001 is in New status with no `ai-cve-triaged` label. This issue is ready
for standard triage beginning at Step 0.7 (Assign and Transition to Assigned).

CVE: CVE-2026-40112 | Library: h2 | Stream: rhtpa-2.2

---

### TC-9002 — Status: New

**Handling**: Proceed with full triage (default path).

TC-9002 is in New status with no `ai-cve-triaged` label. This issue is ready
for standard triage beginning at Step 0.7 (Assign and Transition to Assigned).

CVE: CVE-2026-40297 | Library: serde_json | Stream: rhtpa-2.1

---

### TC-9003 — Status: In Progress

**Handling**: Warning — active work detected.

> This issue is already in `In Progress`. It may be actively worked on.

TC-9003 is in In Progress status, which indicates that another engineer may
already be triaging or remediating this issue. Before proceeding, the engineer
should choose:

1. **Proceed with triage anyway** — e.g., to verify version impact or update
   Affects Versions
2. **Skip this issue** — defer to the engineer currently working on it

CVE: CVE-2026-40455 | Library: tokio | Stream: rhtpa-2.2

---

### TC-9004 — Status: New

**Handling**: Proceed with full triage (default path).

TC-9004 is in New status with no `ai-cve-triaged` label. This issue is ready
for standard triage beginning at Step 0.7 (Assign and Transition to Assigned).

CVE: CVE-2026-40518 | Library: ring | Stream: rhtpa-2.2

---

## Query 2: Triaged but still New

### TC-9010 — Status: New (triaged)

**Handling**: Flagged for follow-up.

TC-9010 has the `ai-cve-triaged` label but remains in New status. This means
the issue was previously triaged but was never moved forward (not transitioned
to In Progress, no remediation tasks actioned, etc.). This issue may need:

- Re-triage to verify the original analysis is still current
- Manual follow-up to determine why it stalled after triage
- Verification that remediation tasks were actually created

CVE: CVE-2026-39874 | Library: quinn-proto | Stream: rhtpa-2.2

---

## Query 3: Ready for QA — Filtering Decisions

### TC-9020 — Status: Modified

**Handling**: Ready for QA. Consider transitioning to ON_QA.

All linked remediation Tasks are completed:
- TC-9021: Done
- TC-9022: Closed

Both Tasks linked via "Depend" have reached a terminal status. Remediation is
complete and this CVE is a candidate for QA verification. Suggest transitioning
TC-9020 to ON_QA.

CVE: CVE-2026-38901 | Library: hyper | Stream: rhtpa-2.2

---

### TC-9023 — Status: In Progress

**Handling**: Excluded from Ready for QA — remediation still in progress.

Linked remediation Tasks:
- TC-9024: Done
- TC-9025: In Progress

TC-9025 is still In Progress. Not all remediation tasks are complete, so this
issue cannot be moved to QA. It will be re-evaluated when TC-9025 reaches
Done or Closed status.

CVE: CVE-2026-39102 | Library: rustls | Stream: rhtpa-2.1

---

### TC-9026 — Status: Modified

**Handling**: Excluded from Ready for QA — no remediation tasks linked.

TC-9026 has no linked Tasks with link type "Depend". Without linked
remediation tasks, there is no remediation to verify. This issue may need
investigation to determine whether remediation tasks were created but not
linked, or whether the triage concluded with a different outcome (e.g.,
close as not affected).

CVE: CVE-2026-39330 | Library: openssl | Stream: rhtpa-2.2
