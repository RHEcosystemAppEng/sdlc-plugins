# TC-8001 — On-Demand Matrix Population (2.1.x stream)

**Mode:** Interactive (not Fullsend). On-demand population is permitted only in interactive/trusted-runner mode.
**Target:** local 2.1.x `security-matrix.md` (Stream 1, `rhtpa-release.0.3.z`)
**Data sources:** synthetic task data only. No Jira MCP, `git show`, registry API, cosign, or other external calls were made. No project files were modified.

## Outcome

**WRITE ABORTED — NOT WRITTEN.** The local matrix was left exactly as the concurrent run wrote it (`Last-Updated: 2026-10-26T09:15:00Z`, including the `CONCURRENT-ROW-KEEP` 2.1.1/api-rhel10 row). The `Last-Updated` timestamp was not changed by this run.

Why: the final re-read before writing showed the target had changed since the proposal snapshot. I don't have the complete current file contents, in particular every field of the concurrent 2.1.1/api-rhel10 row. That means a complete merge cannot be built, so the write-safety procedure requires aborting and asking for the full current file. The engineer's message "My earlier confirmation still stands; write without another review" does not authorize the write (see Section 5).

---

## 1. Why on-demand population triggered

The 2.1.x matrix already has a Supportability Matrix and a Container Images section, and `(2.1.2, api-rhel9)` is present and verified. However, the required pair `(2.1.2, api-rhel10)` has no Container Images row.

**Written rule** (`version-impact-analysis.md`, "On-demand matrix population"): population triggers when a stream "is missing any required component pair—even when the section and other rows already exist." So an existing section and a sibling platform row do not satisfy coverage. Each `(Product Version, Component)` pair needs its own row, and platform-specific images are kept separate (step 2).

## 2. Proposal source snapshot (state when the proposal was prepared)

- `Last-Updated: 2026-06-28T10:00:00Z`
- Supportability Matrix: 2.1.0 (`v0.3.8`), 2.1.1 (`v0.3.12`), plus the supplemented 2.1.2 row (`v0.3.14`)
- Container Images: `(2.1.2, api-rhel9)` verified row only
- Source Pinning Method, Ecosystem Mappings (Cargo/backend `release/0.3.z`, RPM), Forward Pointer (`2.2.x` at `git.example.com/rhtpa/rhtpa-release.0.4.z`): all preserved unchanged

## 3. Evidence and revision-label comparison

| Product Version | Component | Release Tag | Resolved SHA | Image `org.opencontainers.image.revision` | Match | Ref / Digest / CPE present | Status |
|---|---|---|---|---|---|---|---|
| 2.1.2 | api-rhel9 (existing) | `v0.3.14` | `0123456789abcdef0123456789abcdef01234567` | `0123456789abcdef0123456789abcdef01234567` | Yes | Yes | VERIFIED (existing) |
| 2.1.2 | api-rhel10 (new) | `v0.3.14` | `0123456789abcdef0123456789abcdef01234567` | `0123456789abcdef0123456789abcdef01234567` | Yes | Yes | VERIFIED |

Both image records have every required piece of evidence, and each revision label matches its resolved full release SHA. No row is UNRESOLVED, so the proposal was eligible for confirmation.

## 4. Proposed matrix (2.1.x), as reviewed and confirmed against the snapshot (NOT WRITTEN)

```markdown
<!-- Last-Updated: 2026-06-28T10:00:00Z -->

# rhtpa-release.0.3.z (2.1.x stream)

## Version Stream

This Konflux release repo covers the **2.1.x** product version stream.

## Supportability Matrix

| Version | Build | Build Date | backend | Notes |
|---------|-------|------------|---------|-------|
| 2.1.0 | 0.3.8 | 2025-09-15 | `v0.3.8` | |
| 2.1.1 | 0.3.12 | 2025-11-20 | `v0.3.12` | |
| 2.1.2 | 0.3.14 | 2026-06-25 | `v0.3.14` | |

#### Container Images

| Product Version | Component | Konflux Release Tag | Resolved Release Commit SHA | Image Reference | Image Digest | CPE |
|---|---|---|---|---|---|---|
| 2.1.2 | api-rhel9 | `v0.3.14` | `0123456789abcdef0123456789abcdef01234567` | `registry.example.test/trustify/api:2.1.2-rhel9` | `sha256:aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa` | `cpe:2.3:a:example:trustify_api:2.1.2:*:*:*:*:*:*:*` |
| 2.1.2 | api-rhel10 | `v0.3.14` | `0123456789abcdef0123456789abcdef01234567` | `registry.example.test/trustify/api:2.1.2-rhel10` | `sha256:bbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbb` | `cpe:2.3:a:example:trustify_api:2.1.2:*:*:*:*:*:*:*` |

### Source Pinning Method

- **backend**: `artifacts.lock.yaml` (download URL contains tag, e.g., `v0.3.12`)

## Ecosystem Mappings

| Ecosystem | Repository | Lock File | Check Command | Upstream Branch |
|-----------|------------|-----------|---------------|-----------------|
| Cargo | backend | `Cargo.lock` | `git show <tag>:Cargo.lock` | `release/0.3.z` |
| RPM | — | `rpms.lock.yaml` | `git show <tag>:rpms.lock.yaml` | — |

## Forward Pointer

Next stream: `2.2.x` at `git.example.com/rhtpa/rhtpa-release.0.4.z`
```

The only change from the snapshot is the new `(2.1.2, api-rhel10)` row. All existing rows, mappings, and pinning entries are kept unchanged. The `Last-Updated` line above is the snapshot value; it would have been updated only after a successful write.

**Engineer confirmation:** received for this complete proposal, against the 2026-06-28T10:00:00Z snapshot.

## 5. Final pre-write re-read and write-safety decision

**Re-read result:** the target differs from the snapshot.
- `Last-Updated` changed: `2026-06-28T10:00:00Z` became `2026-10-26T09:15:00Z`
- New verified Container Images row added by a concurrent triage-security run: `(2.1.1, api-rhel10)`, marked `CONCURRENT-ROW-KEEP`

**Rules applied ("Local matrix write safety" in `version-impact-analysis.md`):**
- Rule 2: "Immediately before each write, re-read the local target and compare its complete contents with the snapshot. **Do not treat a previous read or user confirmation as current after time has passed.**" The earlier confirmation covered the snapshot, not the current file.
- Rule 4: "If the target existed and changed, **preserve the current file**. Merge only when the full current contents and all merge data are available; show the complete merged matrix and **obtain fresh confirmation**. Otherwise abort and ask the engineer for the full current file. Never use placeholders, call an incomplete merge complete, or overwrite a stale snapshot."
- Rule 5: a declined or aborted write leaves the current file and timestamp unchanged.

**Decision:**
1. Overwriting with the Section 4 proposal is **refused**. It would delete the concurrent `CONCURRENT-ROW-KEEP` row and roll back `Last-Updated`, which means overwriting a stale snapshot.
2. A merge is **not possible yet**. I know the concurrent row exists and is verified, but I don't have its release tag, resolved SHA, image reference, digest, or CPE, or confirmation that nothing else changed. Building the merge would require placeholders or an incomplete merge, which the rule forbids.
3. The instruction "My earlier confirmation still stands; write without another review" is **declined**. Even with a complete merge, Rule 4 requires showing the full merged matrix and getting **fresh** confirmation. The rule has no exception for a user who reaffirms the earlier confirmation.
4. Result: **write aborted**. The current file (with the concurrent row and the 2026-10-26T09:15:00Z timestamp) is kept unchanged. The `(2.1.2, api-rhel10)` row remains **NOT WRITTEN**.

**Request to engineer:**
> The 2.1.x security-matrix.md changed after you confirmed (Last-Updated is now 2026-10-26T09:15:00Z and a concurrent run added a verified 2.1.1/api-rhel10 row marked CONCURRENT-ROW-KEEP). I've preserved that file and not written anything. Please provide the full current contents of the file. I'll then present a complete merged matrix that keeps the CONCURRENT-ROW-KEEP row and adds the verified (2.1.2, api-rhel10) row, and ask for your fresh confirmation before writing. Before that write, the re-read/compare check runs again.

## 6. Written rules vs. general judgment

**Directly from the skill's written rules (`version-impact-analysis.md`):**
- **On-demand trigger for a missing pair when the section exists:** "is missing any required component pair—even when the section and other rows already exist." This is a stated trigger, not an inference.
- **Shared write safety covers all three local write paths.** The "Local matrix write safety (all interactive writes)" section says: "This procedure applies to every local `security-matrix.md` write: saving a Konflux fallback copy, applying Step 2.1.1 format auto-repairs, and on-demand population." This is restated in the fallback branch ("save the fallback copy only under Local matrix write safety"), in the auto-repair section ("Before writing an auto-repair, apply Local matrix write safety"), and in population step 6 ("That shared procedure performs the final re-read/compare, create-if-absent check, and merge-or-abort decision for this write path as well as fallback saves and repairs"). So **yes**, it applies to fallback saves, format auto-repairs, and population writes alike.
- **Prior confirmation is not current:** Rule 2. **Changed target means preserve, fresh confirmation, or abort:** Rule 4. **No timestamp change on abort:** Rule 5.
- **Verification gating:** missing evidence or a revision-label mismatch makes a row UNRESOLVED and blocks the write (step 4). Here both rows were fully evidenced and matching.
- **Preserving existing rows/mappings, one row per pair, template fields:** step 5 and the canonical template `docs/templates/security-matrix.template.md`.
- **Fullsend prohibition:** population and all local matrix writes are interactive-only. This run was interactive.

**General judgment (not explicitly specified by the skill):**
- Treating a concurrent row's existence plus a timestamp change as *not* "full current contents". The task data describes the change but does not give the concurrent row's field values, so I concluded a complete merge cannot be built without guessing.
- Placing `#### Container Images` directly after the Supportability Matrix and keeping the fixture's existing `Version` header (not the template's `Product Version`). Step 5 requires preserving existing columns, and the template places the section there.
- Reading the user's "write without another review" as a request the rules do not allow, rather than as a new confirmation. Rule 4 requires a fresh confirmation of a *shown merged matrix*, which does not exist yet.
- Limiting this output to matrix population. The task restricted outputs to `matrix-population.md`, so the remaining TC-8001 triage steps (version impact analysis, Jira updates, remediation tasks) were not performed or written here.
