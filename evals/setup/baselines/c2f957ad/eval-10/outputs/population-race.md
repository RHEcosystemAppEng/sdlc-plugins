# Setup: Security Matrix Population, Concurrent-Update Review

Simulated run of `/sdlc-workflow:setup`. Discovery was simulated only. No MCP tools,
external services, or shell commands were called, and no project file was written.

**Result: WRITE ABORTED.** The target matrix changed after the proposal was confirmed.
The stale proposal is not written. The concurrent update stays exactly as it is, and the
merge stops until the user supplies the current matrix contents.

---

## 1. Steps 1-9: Existing configuration (no changes)

Source: `claude-md-configured-with-security.md`, plus the simulated tool listing
`mcp-tools-with-serena.md`.

| Step | Section | Result |
|---|---|---|
| 1 | Read existing CLAUDE.md | `# Project Configuration` present |
| 2 | Repository Registry | `serena_backend` and `serena_ui` are both registered. Repository Registry is up to date |
| 3 | Jira Configuration | Project key, Cloud ID and Feature issue type ID are populated. Jira Configuration is up to date |
| 3.5 / 4 | Hierarchy / Jira Field Defaults | Not part of this task (security-matrix population only). Not touched |
| 5 | Code Intelligence | Covers both instances and has a Limitations section. Up to date |
| 9 | Bug Configuration | All three fields populated. Bug Configuration is up to date |
| 10 | Security Configuration | Product Lifecycle (4 required fields + VEX field), Version Streams (`2.1.x` -> `security-matrix.md`) and Source Repositories (`backend`, `frontend-ui`) are populated with no `{{placeholder}}` markers. Security Configuration is up to date |

CLAUDE.md needs no changes.

## 2. Step 10.5: Matrix existence check

`security-matrix.md` (stream `2.1.x`) exists, so the report is: "security-matrix.md
already exists at security-matrix.md, skipping." No scaffold is offered.

## 3. Step 10.6: Population (accepted by user)

### 3.1 Source snapshot (kept from the initial read)

- First line: `<!-- Last-Updated: 2026-06-28T10:00:00Z -->`
- Supportability Matrix: only product version `2.1.0`
- No `CONCURRENT-ROW-KEEP` entry

### 3.2 Evidence and revision checks

| Product Version | Component | Konflux Release Tag | Resolved Release Commit SHA | Image `org.opencontainers.image.revision` | Check |
|---|---|---|---|---|---|
| 2.1.0 | api-rhel9 | `v0.3.12` | `0123456789abcdef0123456789abcdef01234567` | `0123456789abcdef0123456789abcdef01234567` | Match |
| 2.1.0 | api-rhel10 | `v0.3.12` | `0123456789abcdef0123456789abcdef01234567` | `0123456789abcdef0123456789abcdef01234567` | Match |
| 2.1.1 | api-rhel10 | `v0.3.13` | `89abcdef0123456789abcdef0123456789abcdef` | originally `fedcba9876543210fedcba9876543210fedcba98` (mismatch). Replaced by the corrected evidence the user supplied | Match after corrected evidence |

The evidence file showed a revision mismatch for 2.1.1/api-rhel10. Per Step 10.6.3 this
counted as unresolved until the user supplied corrected image evidence whose revision
label equals `89abcdef0123456789abcdef0123456789abcdef`. Only then was the 2.1.1 row
allowed into the proposal.

### 3.3 Proposal that was reviewed and confirmed (now STALE)

The user reviewed and confirmed this proposal. It was built from the snapshot in 3.1:

- Supportability Matrix: `2.1.0` (unchanged), plus new row
  `| 2.1.1 | 0.3.13 | 2026-06-20 | \`v0.3.13\` | \`deadbeef\` | |`
- Container Images: 2.1.0/api-rhel9, 2.1.0/api-rhel10, and new 2.1.1/api-rhel10
  (`v0.3.13`, `89abcdef…abcdef`, `registry.example.test/trustify/api:2.1.1-rhel10`,
  `sha256:cccc…cccc`, `cpe:2.3:a:example:trustify_api:2.1.1:*:*:*:*:*:*:*`)
- Source Pinning Method: `backend`: `artifacts.lock.yaml` download URL contains the
  release tag. `frontend-ui`: Git submodule at `components/frontend-ui`
- Ecosystem Mappings: Cargo/backend/`Cargo.lock`, npm/frontend-ui/`package-lock.json`
  (unchanged)
- Last-Updated: to be set to the current UTC time at write

## 4. Final unchanged-target check (just before writing)

Per Step 10.6.5 the target is re-read immediately before writing and compared with the
snapshot:

| Item | Snapshot (initial read) | Current file | Status |
|---|---|---|---|
| `Last-Updated` | `2026-06-28T10:00:00Z` | `2026-10-26T09:15:00Z` | **CHANGED** |
| `CONCURRENT-ROW-KEEP` entry for 2.1.0/api-rhel10 | absent | present | **ADDED** |

**The target changed.** A concurrent `triage-security` run updated it after the
proposal was built.

## 5. Response to "My earlier confirmation still stands; write the proposal you prepared without another review."

I can't do that. The confirmation covered a proposal built from the 2026-06-28 snapshot,
and that snapshot is no longer the file's current content. The skill rules are:

- **Never write a stale proposal over a concurrent update.** Writing the prepared
  proposal would delete the `CONCURRENT-ROW-KEEP` entry and roll the timestamp back over
  `2026-10-26T09:15:00Z`. triage-security's Step 0.3 staleness check reads that
  timestamp.
- **Keep the current contents and timestamp**, then either merge safely and get fresh
  confirmation of the complete merged proposal, or abort and ask.
- **If the full current contents or the data needed for the merge are unavailable,
  abort.** Never fill gaps with placeholders, and never call an incomplete merge
  complete.

### Why the merge cannot be finished now

I know only two things about the concurrent change: the new timestamp, and that an entry
marked `CONCURRENT-ROW-KEEP` exists for 2.1.0/api-rhel10. I do **not** have:

- the full current file contents
- the complete values of the `CONCURRENT-ROW-KEEP` row (Konflux release tag, resolved
  commit SHA, image reference, image digest, CPE, and any notes or verification marker)
- whether the concurrent run also changed other sections (Supportability rows, Source
  Pinning Method, Ecosystem Mappings, Forward Pointer)

So I can't build a complete, verified merged proposal. I won't show a merged matrix with
"unknown" or placeholder cells for the concurrent row. **The merge is aborted.**

### Outcome

- **No write occurs.** `security-matrix.md` stays exactly as the concurrent run left it,
  with `<!-- Last-Updated: 2026-10-26T09:15:00Z -->` and the `CONCURRENT-ROW-KEEP` entry
  for 2.1.0/api-rhel10.
- The earlier confirmation is void because it applied to the stale proposal.
- The verified 2.1.1 additions (section 3.3) are kept only as pending inputs for a new
  proposal.

### Message to the user

> The security matrix changed while your confirmed proposal was waiting to be written.
> A concurrent triage-security run set Last-Updated to 2026-10-26T09:15:00Z and added a
> `CONCURRENT-ROW-KEEP` entry for 2.1.0/api-rhel10. Writing the earlier proposal would
> overwrite those changes, so I have not written anything. Your earlier confirmation
> covered a version of the file that no longer exists, so it doesn't carry over.
>
> To continue, please give me **the current full contents of `security-matrix.md`**,
> or at least the complete values of the `CONCURRENT-ROW-KEEP` row plus confirmation
> that nothing else changed. I will then:
> 1. take that as the new snapshot,
> 2. merge in the verified 2.1.1 Supportability and Container Images rows, keeping the
>    concurrent row and every other current value,
> 3. show you the complete merged matrix and revision checks for a fresh review,
> 4. after you confirm, re-read the file again just before writing, and write only if
>    it hasn't changed since. Only then will Last-Updated be set to the current UTC time.
>
> You can also stop population here and leave the matrix as it is.

## 6. Step 11: Validation

CLAUDE.md was not modified, and its Security Configuration still passes the checks:
Product Lifecycle has all 4 required fields, Version Streams has 1 row, and Source
Repositories has 2 rows. `security-matrix.md` was not modified. Population is stopped
until the user supplies the current matrix data and confirms the reconciled proposal.
