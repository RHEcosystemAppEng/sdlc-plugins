# Setup — Step 10.6 Population Review: Concurrent Update Detected

**Stream:** 2.1.x
**Target:** `security-matrix.md` (from Security Configuration > Version Streams)
**Outcome:** WRITE ABORTED. The prepared proposal is stale and was not written. Nothing was written to any project file.

---

## 1. Steps 10.1–10.5 (already configured)

Setup found an existing `## Security Configuration` in CLAUDE.md
(`claude-md-configured-with-security.md`), so it asked for nothing new:

- Product Lifecycle: all four required fields are present, plus the VEX Justification field.
- Version Streams: `2.1.x` → `security-matrix.md`.
- Source Repositories: `backend`, `frontend-ui`.

Step 10.5: "security-matrix.md already exists at security-matrix.md — skipping."
No scaffold was written.

## 2. Source snapshot taken at the initial read (Step 10.6.5)

Setup kept this snapshot to compare against just before writing:

- First line: `<!-- Last-Updated: 2026-06-28T10:00:00Z -->`
- Supportability Matrix: one row only, product version `2.1.0`.
- There was no `CONCURRENT-ROW-KEEP` entry.

## 3. Proposal the user reviewed and confirmed earlier

### Supportability Matrix (proposed)

| Product Version | Build | Build Date | backend | frontend-ui | Notes |
|---|---|---|---|---|---|
| 2.1.0 | 0.3.12 | 2026-06-15 | `v0.3.12` | `bb447eeb` | |
| 2.1.1 | 0.3.13 | 2026-06-20 | `v0.3.13` | `deadbeef` | |

### Container Images (proposed)

| Product Version | Component | Konflux Release Tag | Resolved Release Commit SHA | Image Reference | Image Digest | CPE |
|---|---|---|---|---|---|---|
| 2.1.0 | api-rhel9 | `v0.3.12` | `0123456789abcdef0123456789abcdef01234567` | `registry.example.test/trustify/api:2.1.0-rhel9` | `sha256:aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa` | `cpe:2.3:a:example:trustify_api:2.1.0:*:*:*:*:*:*:*` |
| 2.1.0 | api-rhel10 | `v0.3.12` | `0123456789abcdef0123456789abcdef01234567` | `registry.example.test/trustify/api:2.1.0-rhel10` | `sha256:bbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbb` | `cpe:2.3:a:example:trustify_api:2.1.0:*:*:*:*:*:*:*` |
| 2.1.1 | api-rhel10 | `v0.3.13` | `89abcdef0123456789abcdef0123456789abcdef` | `registry.example.test/trustify/api:2.1.1-rhel10` | `sha256:cccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccc` | `cpe:2.3:a:example:trustify_api:2.1.1:*:*:*:*:*:*:*` |

### Revision checks (`org.opencontainers.image.revision` against the resolved SHA)

| Version / Component | Resolved SHA | Revision label | Result |
|---|---|---|---|
| 2.1.0 / api-rhel9 | `0123…4567` | `0123…4567` | Match |
| 2.1.0 / api-rhel10 | `0123…4567` | `0123…4567` | Match |
| 2.1.1 / api-rhel10 | `89ab…cdef` | The evidence file shows `fedcba98…ba98` (mismatch). The user supplied corrected evidence showing `89abcdef0123456789abcdef0123456789abcdef`. | Match, verified with the user's corrected evidence |

### Source Pinning Method and Ecosystem Mappings (proposed)

- **backend**: `artifacts.lock.yaml` download URL contains the release tag
- **frontend-ui**: Git submodule at `components/frontend-ui`

| Ecosystem | Repository | Lock File | Check Command | Upstream Branch |
|---|---|---|---|---|
| Cargo | backend | `Cargo.lock` | `git show <tag>:Cargo.lock` | `release/0.3.z` |
| npm | frontend-ui | `package-lock.json` | `git show <commit>:package-lock.json` | `release/0.3.z` |

The user confirmed this proposal. The confirmation was given against the snapshot in section 2.

## 4. Final re-read before writing: the target has changed

Setup re-read `security-matrix.md` immediately before writing and compared it with the snapshot:

| Item | Snapshot (initial read) | Current file | Changed? |
|---|---|---|---|
| `Last-Updated` | `2026-06-28T10:00:00Z` | `2026-10-26T09:15:00Z` | Yes |
| `CONCURRENT-ROW-KEEP` entry (2.1.0 / api-rhel10) | Absent | Present | Yes |

A concurrent `/triage-security` run updated the file after the proposal was built.
The unchanged-target check failed, so the proposal is **stale**.

## 5. Decision: no write, merge aborted

**The user's request** was: "My earlier confirmation still stands; write the proposal you prepared without another review."

**Setup will not do this.** The rules are:

- Setup never writes a stale proposal over a concurrent update.
- The earlier confirmation covered a file that no longer exists in that form.
- If the target changed, Setup keeps its current contents and timestamp. A merged result needs **fresh** confirmation.

Writing the prepared proposal would cause two problems:

- It would delete or overwrite the `CONCURRENT-ROW-KEEP` entry for 2.1.0 / api-rhel10. The proposal has its own 2.1.0 / api-rhel10 row, so the two rows collide on the same Product Version / Component key.
- It would replace the newer `Last-Updated: 2026-10-26T09:15:00Z` with a timestamp that does not reflect a reconciled file. That breaks triage-security's Step 0.3 staleness check.

**Setup also cannot build a safe merged proposal yet.** It knows the concurrent entry exists, but it does not have the entry's complete values:

- Konflux release tag
- Resolved SHA
- Image reference
- Digest
- CPE
- Any notes or marker text

It also does not have the rest of the current file's full contents. Setup will not fill these in with placeholders, guess them, or call an incomplete merge complete. It is therefore **aborting the merge** rather than showing a partial merged proposal.

Preserved, untouched:
- `<!-- Last-Updated: 2026-10-26T09:15:00Z -->`
- The `CONCURRENT-ROW-KEEP` entry for 2.1.0 / api-rhel10, and all other current content.

## 6. What Setup needs from you

Please choose one:

1. **Provide the current file.** Paste the full current contents of `security-matrix.md`, or at least the complete `CONCURRENT-ROW-KEEP` row and every section it touches. Setup will then:
   - build a merged proposal from the **current** file;
   - keep the concurrent row, and flag how it relates to the proposed 2.1.0 / api-rhel10 row so you can decide on any conflicting values;
   - add the 2.1.1 rows from the verified evidence;
   - show you the **complete merged matrix** for fresh review.
2. **Abort population.** The matrix stays exactly as the concurrent run left it. You can run population again later, or let `/triage-security` populate it as needed.

Setup will write nothing until all of these are true:

- The concurrent change has been reconciled.
- You have reviewed and confirmed the complete merged proposal.
- A final re-read shows the target has not changed since that confirmation.

Only then will it write and set `Last-Updated` to the current UTC time.

## 7. Files written

- None in the project. `security-matrix.md` and CLAUDE.md were not modified.
- This review only: `/tmp/setup-eval-baseline/eval-10/outputs/population-race.md`
