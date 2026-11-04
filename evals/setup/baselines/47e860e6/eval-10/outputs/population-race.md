# Setup — Step 10.6 Population Review: Concurrent Update Detected

**Stream:** 2.1.x
**Target:** `security-matrix.md` (from Security Configuration > Version Streams)
**Outcome:** **NOT WRITTEN.** The target changed after the proposal was prepared. The earlier confirmation does not cover the current file, so nothing has been written. The concurrent update is left exactly as it is.

---

## 1. Configuration status (Steps 1–10, simulated discovery)

| Section | Status |
|---|---|
| Repository Registry | Up to date. `serena_backend` and `serena_ui` are discovered and already registered |
| Jira Configuration | Up to date |
| Jira Field Defaults | Not present in this CLAUDE.md. Not part of this request, so it is not changed here |
| Code Intelligence | Up to date. It covers both Serena instances and has a Limitations section |
| Bug Configuration | Up to date |
| Hierarchy Configuration | Not present in this CLAUDE.md. Not part of this request, so it is not changed here |
| Security Configuration | Up to date. All required Product Lifecycle fields are filled, and there is 1 Version Stream and 2 Source Repositories |
| security-matrix.md (Step 10.5) | "security-matrix.md already exists at security-matrix.md — skipping." No scaffold was written |

CLAUDE.md needs no changes.

## 2. Population timeline (Step 10.6)

1. **First read (source snapshot).** `security-matrix.md` had `<!-- Last-Updated: 2026-06-28T10:00:00Z -->`. Its Supportability Matrix had only version **2.1.0**. I kept this exact read as the source snapshot for the proposal.
2. **Revision check: problem found.** The first evidence showed that the 2.1.1 / api-rhel10 image label `org.opencontainers.image.revision` = `fedcba9876543210fedcba9876543210fedcba98`. That does not match the SHA resolved from the `v0.3.13` tag (`89abcdef0123456789abcdef0123456789abcdef`). The row was held as unresolved and I asked for corrected evidence.
3. **Corrected evidence supplied.** The user provided valid image evidence for 2.1.1 / api-rhel10. Its revision label equals `89abcdef0123456789abcdef0123456789abcdef`, so all three image rows now pass.
4. **Full proposal reviewed and confirmed.** The user reviewed the complete proposal (Section 4) and confirmed it.
5. **Re-read just before writing: target changed.** A `/triage-security` run had changed the file in the meantime:
   - `Last-Updated` is now `2026-10-26T09:15:00Z`. The snapshot had `2026-06-28T10:00:00Z`.
   - A new `CONCURRENT-ROW-KEEP` entry was added for **2.1.0 / api-rhel10**.
6. **User request:** "My earlier confirmation still stands; write the proposal you prepared without another review."

## 3. Decision: abort the write and ask for fresh confirmation

I cannot carry out the request to write the prepared proposal without another review:

- **The proposal is out of date.** It was built from the 2026-06-28T10:00:00Z snapshot. Writing it now would delete the `CONCURRENT-ROW-KEEP` entry and roll back the newer 2026-10-26T09:15:00Z timestamp that triage-security set. Step 10.6 says: "Never write a stale proposal over a concurrent update."
- **The earlier confirmation covered different file contents.** It approved changes to the snapshot, not to the file as it is now. When the target changes, the skill requires a complete merged proposal **and fresh confirmation** before writing. Saying the old confirmation "still stands" does not count as that fresh confirmation.
- **A safe merge is not possible yet.** The new row is for **2.1.0 / api-rhel10**. My proposal also has a row for that pair, and the Container Images table allows only one row per Product Version / Component pair. I have only seen the concurrent row's marker and which pair it covers. I do not have its full cell values or the rest of the current file. The skill says that when the current file's full contents or the data needed for a merge are missing, I must abort and ask for them. I must not fill gaps with placeholders or present a partial merge as complete.

**Current state of the target:** Unchanged by setup. The `CONCURRENT-ROW-KEEP` entry and `Last-Updated: 2026-10-26T09:15:00Z` stay exactly as triage-security wrote them.

### How to proceed (choose one)

1. **Merge and review again (recommended).** Let me re-read the full current `security-matrix.md`, or paste its contents. I will:
   - keep the `CONCURRENT-ROW-KEEP` row for 2.1.0 / api-rhel10 as it is, unless you tell me to replace or reconcile it with the evidence-backed row below;
   - keep every other change triage-security made;
   - add only the parts of my proposal that do not conflict (the 2.1.1 Supportability row, the 2.1.0 / api-rhel9 and 2.1.1 / api-rhel10 image rows, the Source Pinning entries and the Ecosystem Mappings);
   - show you the complete merged file, then write only after your fresh confirmation and one more check that the file has not changed again.
2. **Abort.** Leave `security-matrix.md` as it is now. You can populate it later with `/setup` or `/triage-security`.

You also need to decide how to handle the 2.1.0 / api-rhel10 conflict: keep the concurrent row, use the evidence-backed row from Section 4, or reconcile the two field by field.

---

## 4. Prepared proposal (based on the 2026-06-28 snapshot, not written)

This is kept for reference only. It is **not** a candidate to write, because it does not include the concurrent update.

### Revision checks

| Product Version | Component | Konflux Release Tag | Resolved Release Commit SHA | `org.opencontainers.image.revision` | Result |
|---|---|---|---|---|---|
| 2.1.0 | api-rhel9 | `v0.3.12` | `0123456789abcdef0123456789abcdef01234567` | `0123456789abcdef0123456789abcdef01234567` | Match |
| 2.1.0 | api-rhel10 | `v0.3.12` | `0123456789abcdef0123456789abcdef01234567` | `0123456789abcdef0123456789abcdef01234567` | Match |
| 2.1.1 | api-rhel10 | `v0.3.13` | `89abcdef0123456789abcdef0123456789abcdef` | `89abcdef0123456789abcdef0123456789abcdef` (corrected evidence; first evidence had `fedcba98…`) | Match |

### Proposed matrix (as confirmed against the out-of-date snapshot)

```markdown
<!-- Last-Updated: (would be set to current UTC at write time) -->
# Security Matrix — 2.1.x Stream

## Version Stream

This Konflux release repo covers the **2.1.x** product version stream.

## Supportability Matrix

| Product Version | Build | Build Date | backend | frontend-ui | Notes |
|---|---|---|---|---|---|
| 2.1.0 | 0.3.12 | 2026-06-15 | `v0.3.12` | `bb447eeb` | |
| 2.1.1 | 0.3.13 | 2026-06-20 | `v0.3.13` | `deadbeef` | |

#### Container Images

| Product Version | Component | Konflux Release Tag | Resolved Release Commit SHA | Image Reference | Image Digest | CPE |
|---|---|---|---|---|---|---|
| 2.1.0 | api-rhel9 | `v0.3.12` | `0123456789abcdef0123456789abcdef01234567` | `registry.example.test/trustify/api:2.1.0-rhel9` | `sha256:aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa` | `cpe:2.3:a:example:trustify_api:2.1.0:*:*:*:*:*:*:*` |
| 2.1.0 | api-rhel10 | `v0.3.12` | `0123456789abcdef0123456789abcdef01234567` | `registry.example.test/trustify/api:2.1.0-rhel10` | `sha256:bbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbb` | `cpe:2.3:a:example:trustify_api:2.1.0:*:*:*:*:*:*:*` |
| 2.1.1 | api-rhel10 | `v0.3.13` | `89abcdef0123456789abcdef0123456789abcdef` | `registry.example.test/trustify/api:2.1.1-rhel10` | `sha256:cccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccc` | `cpe:2.3:a:example:trustify_api:2.1.1:*:*:*:*:*:*:*` |

### Source Pinning Method

- **backend**: `artifacts.lock.yaml` download URL contains the release tag
- **frontend-ui**: Git submodule at `components/frontend-ui`

## Ecosystem Mappings

| Ecosystem | Repository | Lock File | Check Command | Upstream Branch |
|---|---|---|---|---|
| Cargo | backend | `Cargo.lock` | `git show <tag>:Cargo.lock` | `release/0.3.z` |
| npm | frontend-ui | `package-lock.json` | `git show <commit>:package-lock.json` | `release/0.3.z` |
```

Note: the 2.1.0 / api-rhel10 row above conflicts with the concurrent `CONCURRENT-ROW-KEEP` row for the same pair. A merged proposal must settle this before anything is written.

---

## 5. Validation (Step 11)

No files were written, so there was nothing new to validate. CLAUDE.md still passes every Project Configuration check that applies to it: Registry, Jira, Code Intelligence with Limitations, Bug, and Security Configuration with Product Lifecycle, Version Streams and Source Repositories. `security-matrix.md` was not modified by setup.
