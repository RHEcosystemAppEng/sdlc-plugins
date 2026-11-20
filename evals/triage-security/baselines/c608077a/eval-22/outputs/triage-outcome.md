# Triage Outcome: TC-8021 (CVE-2026-31812, quinn-proto < 0.11.14)

**Decision: AFFECTED. Case A (cross-stream impact on 2.1.x) plus Case B (remediation for
the in-scope 2.2.x stream).** The issue is not closed. The Affects Versions field needs
correcting.

All actions below are proposals. In interactive mode each one needs engineer
confirmation. Nothing was sent to Jira.

## Basis

1. **Version impact (Step 2).** The lock-file data shows quinn-proto < 0.11.14 in:
   - 2.2.x (in scope): 2.2.0 (0.11.9), 2.2.1 (0.11.12), and 2.2.2 (retag of 2.2.1).
     2.2.3 and 2.2.4 ship 0.11.14 and are not affected.
   - 2.1.x (out of scope): 2.1.0 and 2.1.1 (both 0.11.9).
2. **Affects Versions (Step 3).** PSIRT set `RHTPA 2.0.0`, which is wrong. Replace it with
   `RHTPA 2.2.0, RHTPA 2.2.1, RHTPA 2.2.2`. Post a correction comment with the impact
   table and the Comment Footnote.
3. **Duplicates and siblings (Step 4).** Not run, because Jira is unavailable in this eval.
   A real triage would search `labels = CVE-2026-31812` for siblings and overlaps, which
   decides whether 2.1.x already has its own CVE issue.
4. **Lifecycle (Step 5).** The product pages were not fetched. All affected versions are
   assumed supported.
5. **Already fixed (Step 6).** Sibling data is not available. No resolved sibling is known.
6. **Concurrent triage (Step 7).** The JQL returned 0 in-progress or in-review triages on
   `quinn-proto`. Triage continues silently with no warning prompt and no
   `concurrent-triage-overlap` label. See `concurrent-triage.md`.

## Step 7.5 – Release Jira (proposed)

- 2.2.x: find or create `RHTPA 2.2.5 Release Tasks` (Epic) and `RHTPA 2.2.5 CVE triage`
  (Task). 2.2.5 is the default next patch after 2.2.4. Each creation needs individual
  confirmation.
- 7.5.3 cross-CVE dedup: look for existing remediation Tasks linked to the release Task
  that already cover `quinn-proto`. None are known, so tasks are not deduplicated.

## Step 8 – Remediation

**Case B: 2.2.x (in scope). Cargo is a source dependency, so 2 tasks.**
- Upstream fix status: `release/0.4.z` already ships quinn-proto 0.11.14. This is inferred
  from tags v0.4.11 and v0.4.12; branch HEAD was not checked. That makes this the
  "fix available" variant.
  1. Dependency bump / verification task for `rhtpa-backend` on `release/0.4.z`
     (quinn-proto >= 0.11.14). The fix is effectively already present, so this task
     mainly confirms and documents it.
  2. Downstream propagation task in `rhtpa-release.0.4.z`, blocked by task 1. It
     confirms the next release pins a backend tag at or after v0.4.11.
- Link both tasks to TC-8021 (Depend), link task 1 to task 2 (Blocks), link both to the
  release Task (Blocks), and link TC-8021 to the release Task (Related).
- **Engineer judgement needed:** the current 2.2.x release (2.2.4, and 2.2.3 before it)
  already ships the fix. The engineer may decide that 2.2.x needs no new code and that
  the fix is "upgrade to 2.2.3 or later". In that case the tasks become verification
  only.

**Case A: cross-stream 2.1.x (outside the issue's `[rhtpa-2.2]` scope).**
- Post a cross-stream impact comment on TC-8021: "quinn-proto < 0.11.14 also affects
  stream 2.1.x (2.1.0, 2.1.1 ship 0.11.9) based on lock file analysis..."
- If Step 4 finds no CVE-2026-31812 issue for 2.1.x, create **preemptive** tasks for
  2.1.x: an upstream backport on `release/0.3.z` (no fix seen there) plus downstream
  propagation in `rhtpa-release.0.3.z`. They carry the label `security-preemptive` and
  link to TC-8021 as **Related**. Then post a comment listing them. If a 2.1.x sibling
  exists, create no 2.1.x tasks.

## Post-triage (proposed)

- Add the `ai-cve-triaged` label to TC-8021.
- Post a summary comment with the impact table, the Affects Versions correction, the
  outcome, task links, release Jira keys, dedup results (none), an @mention of the
  reporter, and the Comment Footnote.

## Caveats

- The matrix is 145 days old (Last-Updated 2026-06-28). Releases after that date are not
  covered. Refreshing it is recommended.
- MITRE and OSV were not queried, so the fix threshold comes from the Jira description
  only.
- The development stream was not evaluated (no unreleased Jira version data).
- The issue key in the file (TC-8001) does not match the task (TC-8021). TC-8021 was used.
