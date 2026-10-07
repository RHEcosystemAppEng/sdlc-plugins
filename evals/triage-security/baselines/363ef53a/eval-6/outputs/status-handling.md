# Status-Aware Handling Decisions

Handling decisions for each discovered issue, based on the status-aware rules
defined in the triage-security skill (SKILL.md, Discovery Mode, "Status-aware
handling" section).

---

## Untriaged Issues

### TC-9001 -- CVE-2026-40112 h2 (Status: New)

**Handling**: Proceed with full triage (default path).

New status indicates this issue has not been triaged or worked on. Standard
8-step triage applies: data extraction, version impact analysis, Affects
Versions correction, duplicate/sibling check, lifecycle check, already-fixed
check, concurrent triage detection, release Jira orchestration, and
remediation task creation or close recommendation.

### TC-9002 -- CVE-2026-40297 serde_json (Status: New)

**Handling**: Proceed with full triage (default path).

New status indicates this issue has not been triaged or worked on. Standard
8-step triage applies.

### TC-9003 -- CVE-2026-40455 tokio (Status: In Progress)

**Handling**: Warn before proceeding.

This issue is already in In Progress status. It may be actively worked on by
another engineer. Present the following warning:

> "This issue is already in `In Progress`. It may be actively worked on."
>
> Options:
> 1. Proceed with triage anyway (e.g., to verify version impact or update
>    Affects Versions)
> 2. Skip this issue

If the engineer chooses to skip, return to the discovery list or end the
session. If they choose to proceed, continue with the standard triage flow
but be aware that remediation may already be underway.

### TC-9004 -- CVE-2026-40518 ring (Status: New)

**Handling**: Proceed with full triage (default path).

New status indicates this issue has not been triaged or worked on. Standard
8-step triage applies.

---

## Triaged but still New

### TC-9010 -- CVE-2026-39874 quinn-proto (Status: New, label: ai-cve-triaged)

**Handling**: Proceed with full triage (default path), with additional context.

Although the `ai-cve-triaged` label indicates a prior triage was performed,
the issue remains in New status. This means triage completed but no
remediation actions moved the issue forward. Possible reasons:

- Remediation tasks were created but the CVE issue itself was never
  transitioned
- The prior triage recommended closure but the engineer did not confirm
- The prior triage encountered an issue and stopped early

The engineer should review whether re-triage is needed (e.g., to verify
prior findings are still current) or whether the issue simply needs its
status updated to reflect completed triage work. Since the status is New,
the standard triage path applies -- no warning gate is triggered.

---

## Ready for QA Candidates

### TC-9020 -- CVE-2026-38901 hyper (Status: Modified)

**Handling**: Candidate for ON_QA transition.

This issue is triaged (`ai-cve-triaged` label) and in Modified status. All
linked remediation Tasks are completed:
- TC-9021: Done
- TC-9022: Closed

Since all remediation work is finished, this CVE is ready for QA
verification. Recommend transitioning to ON_QA status.

If the engineer selects this issue for triage, the In Progress/Code
Review/QA warning gate applies (Modified is a post-New status). Present:

> "This issue is already in `Modified`. It may be actively worked on."
>
> Options:
> 1. Proceed with triage anyway (e.g., to verify version impact or update
>    Affects Versions)
> 2. Skip this issue

### TC-9023 -- CVE-2026-39102 rustls (Status: In Progress)

**Handling**: Not ready for QA -- excluded.

Remediation is still in progress (TC-9025 is In Progress). This issue
cannot transition to ON_QA until all remediation Tasks are completed.

If the engineer selects this issue for triage, the In Progress warning gate
applies:

> "This issue is already in `In Progress`. It may be actively worked on."
>
> Options:
> 1. Proceed with triage anyway
> 2. Skip this issue

### TC-9026 -- CVE-2026-39330 openssl (Status: Modified)

**Handling**: Not ready for QA -- excluded.

No linked remediation Tasks found (no Depend links). This issue cannot
qualify for Ready for QA without remediation tasks to verify. It may need
re-triage to create remediation tasks, or it may have been triaged with a
close recommendation that was not executed.

If the engineer selects this issue for triage, the Modified status warning
gate applies (same as TC-9020 above).
