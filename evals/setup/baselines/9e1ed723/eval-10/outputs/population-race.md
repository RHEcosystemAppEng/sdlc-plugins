# Setup — Security Matrix Population: Concurrent-Update Review

Simulation only. No MCP tools, external services, or shell commands were called, and
no project file was modified. This is the only file written.

## Configuration status (Steps 1–10)

| Section | Result |
|---|---|
| Repository Registry | Up to date (`serena_backend`, `serena_ui` already registered) |
| Jira Configuration | Up to date |
| Code Intelligence | Up to date (both instances listed under Limitations) |
| Bug Configuration | Up to date |
| Security Configuration | Present and populated: Product Lifecycle, one Version Stream (`2.1.x` -> `security-matrix.md`), two Source Repositories |
| Step 10.5 scaffold | `security-matrix.md already exists at security-matrix.md — skipping.` |

Nothing changes in CLAUDE.md for this run.

## Step 10.6: population timeline

### 1. Initial read (snapshot S0)

The proposal is based on the exact contents of `security-matrix.md` read at this point:

- First line: `<!-- Last-Updated: 2026-06-28T10:00:00Z -->`
- Supportability Matrix: only product version **2.1.0**
- No `CONCURRENT-ROW-KEEP` entry

### 2. Evidence and revision checks

| Product Version | Component | Konflux Release Tag | Resolved Release Commit SHA | `org.opencontainers.image.revision` | Result |
|---|---|---|---|---|---|
| 2.1.0 | api-rhel9 | `v0.3.12` | `0123456789abcdef0123456789abcdef01234567` | `0123456789abcdef0123456789abcdef01234567` | Match, verified |
| 2.1.0 | api-rhel10 | `v0.3.12` | `0123456789abcdef0123456789abcdef01234567` | `0123456789abcdef0123456789abcdef01234567` | Match, verified |
| 2.1.1 | api-rhel10 | `v0.3.13` | `89abcdef0123456789abcdef0123456789abcdef` | evidence file had `fedcba9876543210fedcba9876543210fedcba98` (mismatch). The user's corrected evidence matches the resolved SHA | Verified only after the user's corrected evidence |

The 2.1.1 row is in the proposal only because the user supplied valid corrected image
evidence. The original evidence file's revision label did not match the resolved SHA.
No 2.1.1 / api-rhel9 row is proposed because there is no release or image evidence for it.

### 3. Proposal reviewed and confirmed by the user (based on S0)

- Supportability Matrix: keep 2.1.0 and add `2.1.1 | 0.3.13 | 2026-06-20 | v0.3.13 | deadbeef`
- Container Images: the three verified rows above, each with its own Konflux tag, resolved SHA, image reference, `sha256:` digest, and CPE
- Source Pinning Method: backend uses the release tag in the `artifacts.lock.yaml` download URL. frontend-ui uses a Git submodule at `components/frontend-ui`
- Ecosystem Mappings: Cargo/backend/`Cargo.lock` and npm/frontend-ui/`package-lock.json`, both on `release/0.3.z`
- Last-Updated would be set to the current UTC time when the file is written

### 4. Final re-read before writing (snapshot S1). The file has changed.

| Item | Snapshot S0 (basis of proposal) | Current file S1 |
|---|---|---|
| Last-Updated | `2026-06-28T10:00:00Z` | `2026-10-26T09:15:00Z` |
| `CONCURRENT-ROW-KEEP` entry for 2.1.0 / api-rhel10 | absent | **present** (written by a concurrent triage-security run) |

**Result: the target changed after the proposal was built. The proposal is stale.**

## Decision: no write. The merge is aborted until the current matrix contents are provided.

You said, "My earlier confirmation still stands; write the proposal you prepared
without another review." I can't do that:

1. **I won't write a stale proposal over a concurrent update.** Your confirmation
   applied to a proposal built from S0. Writing it now would delete the
   `CONCURRENT-ROW-KEEP` entry and roll Last-Updated back from `2026-10-26T09:15:00Z`.
   That would lose triage-security's newer work.
2. **I'm keeping the current file's contents and timestamp.** The `CONCURRENT-ROW-KEEP`
   entry and `Last-Updated: 2026-10-26T09:15:00Z` stay as they are.
3. **I can't build a complete merged proposal.** I only know that a
   `CONCURRENT-ROW-KEEP` entry exists for 2.1.0 / api-rhel10. I don't have its
   Konflux tag, resolved SHA, image reference, digest, CPE, notes, or its exact
   position in the file. I also don't know whether the concurrent run changed
   anything else. I won't fill those gaps with placeholders or guesses, and I won't
   present an incomplete merge as complete. It is also unclear how the concurrent
   2.1.0 / api-rhel10 entry relates to my proposed row for the same pair. The table
   must have exactly one row per Product Version / Component pair, and I won't decide
   which one wins without the data.
4. **Your earlier confirmation doesn't cover a merge.** Any merged result is a new
   proposal and needs a fresh review and confirmation.

## What I need from you

Choose one:

- **A. Provide the current contents.** Paste the full current `security-matrix.md`.
  At minimum, include the complete `CONCURRENT-ROW-KEEP` row with every column and
  anything else the concurrent run changed. I will then build a merged proposal:
  - keep the concurrent row and its values
  - add only the verified 2.1.1 additions that don't conflict
  - flag any conflict on the 2.1.0 / api-rhel10 pair for you to decide

  I will show the complete merged matrix with its revision checks. Before writing, I
  will check once more that the file hasn't changed again. Only after that check
  passes, and after you confirm the merged proposal, will I write it and set
  Last-Updated to the current UTC time.
- **B. Stop here.** `security-matrix.md` stays exactly as triage-security left it.
  You can re-run population later, or let `/triage-security` populate on demand.

**Nothing will be written** until the concurrent change is reconciled, the final
merged proposal is confirmed, and the target is unchanged at write time. So far,
`security-matrix.md` is untouched.

## Step 11: Validate

No files were written, so there is nothing to validate. CLAUDE.md is unchanged and still
passes the existing Security Configuration checks: Product Lifecycle has four required
fields, one Version Streams row, and two Source Repositories rows.
