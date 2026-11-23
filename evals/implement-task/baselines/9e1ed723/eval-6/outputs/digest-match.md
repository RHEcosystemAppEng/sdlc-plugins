# Step 1.5 – Description Integrity Verification (TC-9201)

## Inputs

- Task: TC-9201 ("Add advisory severity aggregation service and endpoint")
- Protocol: `plugins/sdlc-workflow/shared/description-digest-protocol.md`
- Description fetched in Step 1 via `jira.get_issue(TC-9201)` (MCP path, so the description is markdown)

## Steps

1. **Get the comments.** Call `jira.get_issue_comments(TC-9201)`. It returns one comment.

2. **Find the digest comment.** Look for comments whose body starts with the fixed marker `[sdlc-workflow] Description digest:`.
   - One comment matches:
     `[sdlc-workflow] Description digest: sha256-md:a1b2c3d4e5f67890a1b2c3d4e5f67890a1b2c3d4e5f67890a1b2c3d4e5f67890`
   - Only one comment matches, so there is nothing to choose between. The "most recent by `created`" rule only applies when several comments match.
   - A digest comment exists, so the "No description digest found" warning does not apply.

3. **Check whether the comment was edited (4a).** The comment's `created` and `updated` timestamps are present and identical.
   - The comment has not been changed since it was posted.
   - No "Digest comment was edited after initial posting" warning is needed.

4. **Read the stored digest (4b).**
   - Format tag: `sha256-md`. This is the tagged format, not the legacy untagged `sha256:<hex>`, so the legacy-format skip does not apply.
   - Hex digest: `a1b2c3d4e5f67890a1b2c3d4e5f67890a1b2c3d4e5f67890a1b2c3d4e5f67890` (64 lowercase hex characters, which is valid).

5. **Compute the current digest (4c).** Write the description from the `get_issue` response to `/tmp/desc-TC-9201.txt`, then run:
   ```bash
   python3 scripts/sha256-digest.py /tmp/desc-TC-9201.txt
   ```
   - Check the exit code first. A non-zero exit would mean: warn, skip the check, keep going.
   - The script detects plain text or markdown and strips leading and trailing whitespace before hashing.
   - Output (per the eval scenario): `sha256-md:a1b2c3d4e5f67890a1b2c3d4e5f67890a1b2c3d4e5f67890a1b2c3d4e5f67890`

6. **Compare the format tags (4d).** Stored is `sha256-md` and computed is `sha256-md`. They match, so the "Digest format mismatch" skip does not apply. Go on to compare the hex values.

7. **Compare the hex digests (4e).** Stored and computed hex are the same, so the digests **match**.

## Result

**The digests match, so the check passes and execution continues silently.**

- The user gets no prompt and nothing is shown to them. There is no Proceed/Stop question, no expected-vs-actual display and no extra delay.
- No warnings are raised: the digest comment exists, it was not edited, it uses the tagged format and the format tags agree.
- The description is unchanged since plan-feature created it, so the task content from Step 1 is used as-is.
- No Jira comment is posted about the check. Nothing is written back to Jira at this stage.
- Execution goes straight on to **Step 2 – Verify Dependencies**. The task lists "Depends on: None", so that step passes immediately. Step 3 (assign and move to In Progress) follows, then the implementation plan in `plan.md`.

If any of the following had happened instead, the flow would be different:

| Condition | Behaviour |
|---|---|
| No digest comment | Warn ("No description digest found — skipping integrity check…") and continue |
| `updated` > `created` | Warn that the comment was edited, but still compare the digests |
| Legacy `sha256:<hex>` | Warn ("Legacy digest format — skipping integrity check") and continue |
| The script exits non-zero | Warn, skip the check, continue |
| Tag mismatch (md vs adf) | Warn ("Digest format mismatch — skipping integrity check") and continue |
| Hex mismatch | Show expected and actual digests, ask whether to Proceed or Stop, and **stop until the user answers** |

None of these apply here.
