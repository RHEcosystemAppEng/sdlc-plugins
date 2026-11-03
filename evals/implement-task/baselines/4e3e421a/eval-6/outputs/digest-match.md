# Step 1.5 – Description Integrity Verification (TC-9201)

## Result: digests MATCH, so I continue without prompting

## How I would run it

1. **Get the comments**: call `jira.get_issue_comments(TC-9201)`. This uses MCP first. If MCP fails, the REST fallback is `python3 scripts/jira-client.py get_comments TC-9201`, following Step 0.5.

2. **Find the digest comment**: look for comments whose body starts with the marker `[sdlc-workflow] Description digest:`, as defined in `shared/description-digest-protocol.md`.
   - Exactly one comment matches. It was posted by the earlier plan-feature run:
     `[sdlc-workflow] Description digest: sha256-md:a1b2c3d4e5f67890a1b2c3d4e5f67890a1b2c3d4e5f67890a1b2c3d4e5f67890`
   - With only one match, I don't need the "pick the most recent by `created`" rule.
   - A digest comment exists, so the backward-compatibility branch ("No description digest found") does not apply.

3. **Check whether the comment was edited (4a)**: the comment's `created` and `updated` timestamps are the same.
   - The comment was not edited after it was posted, so I issue no "Digest comment was edited after initial posting" warning.

4. **Read the stored digest (4b)**:
   - Format tag: `sha256-md`. This is a tagged format, so the legacy `sha256:<hex>` warning does not apply.
   - Hex digest: `a1b2c3d4e5f67890a1b2c3d4e5f67890a1b2c3d4e5f67890a1b2c3d4e5f67890`. This is 64 lowercase hex characters.

5. **Compute the current digest (4c)**: write the description field returned by `jira.get_issue(TC-9201)` to `/tmp/desc-TC-9201.txt`, then run:
   ```bash
   python3 scripts/sha256-digest.py /tmp/desc-TC-9201.txt
   ```
   - I check the exit code first. Exit 0 means I use the output. A non-zero exit would mean I warn and skip the check without blocking.
   - The script recognizes plain markdown (the MCP path) and outputs:
     `sha256-md:a1b2c3d4e5f67890a1b2c3d4e5f67890a1b2c3d4e5f67890a1b2c3d4e5f67890`. The scenario says to assume this matches.

6. **Compare format tags (4d)**: the stored tag is `sha256-md` and the computed tag is `sha256-md`.
   - The tags match, so there is no "Digest format mismatch" warning and I go on to compare the hashes.

7. **Compare the hex digests (4e)**: the stored hash and the computed hash are identical, so they **MATCH**.
   - **I continue silently.** I show the user no prompt, ask no proceed/stop question, and add no delay.
   - The description has not changed since plan-feature created the task. Execution goes straight to Step 2 (Verify Dependencies).

## Warnings issued
None. I issue no missing-digest, legacy-format, edited-comment, format-mismatch or digest-mismatch warning.

## What happens next
- Step 2: the task's Dependencies section says "Depends on: None", so I check nothing.
- Step 3: assign TC-9201 to the current user and move it to In Progress.
- Steps 4–11: carry out the work as described in `plan.md`.
