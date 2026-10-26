# Step 1.5 -- Description Integrity Verification for TC-9201

## Inputs

- **Stored digest comment body:** `[sdlc-workflow] Description digest: sha256-md:a1b2c3d4e5f67890a1b2c3d4e5f67890a1b2c3d4e5f67890a1b2c3d4e5f67890`
- **Comment timestamps:** `created` equals `updated` (comment was not edited after posting)
- **Computed digest** (from `scripts/sha256-digest.py` on the current description): assumed to produce `sha256-md:a1b2c3d4e5f67890a1b2c3d4e5f67890a1b2c3d4e5f67890a1b2c3d4e5f67890`

## Verification Procedure

1. **Retrieve issue comments:** Call `jira.get_issue_comments(TC-9201)` to fetch all comments on the issue.

2. **Locate the digest comment:** Search all comment bodies for the marker prefix `[sdlc-workflow] Description digest:`. One comment matches. Since there is only one matching comment, it is selected (no need to compare `created` timestamps among multiple candidates).

3. **Comment edit detection:** Compare the comment's `created` and `updated` timestamps. They are identical, so the comment has not been edited after initial posting. No warning is needed. Proceed with digest comparison.

4. **Extract the stored digest:** Parse the tagged digest value from the comment body:
   - Format tag: `sha256-md`
   - Hex digest: `a1b2c3d4e5f67890a1b2c3d4e5f67890a1b2c3d4e5f67890a1b2c3d4e5f67890`
   - Not a legacy untagged format (`sha256:<hex>`), so no legacy warning applies.

5. **Compute the current digest:** Extract the description field from the issue response, write it to `/tmp/desc-TC-9201.txt`, and run:
   ```
   python3 scripts/sha256-digest.py /tmp/desc-TC-9201.txt
   ```
   The script outputs: `sha256-md:a1b2c3d4e5f67890a1b2c3d4e5f67890a1b2c3d4e5f67890a1b2c3d4e5f67890`

6. **Compare format tags:** Both stored and computed tags are `sha256-md` -- tags match. Proceed to hex digest comparison.

7. **Compare hex digests:** Stored hex `a1b2c3d4e5f67890...` equals computed hex `a1b2c3d4e5f67890...` -- **match**.

## Outcome

**Match -- proceed silently.** Per the protocol, when the hex digests match, implementation proceeds without any additional user prompt, warning, or added latency. The description has not been modified since plan-feature created it. No output is displayed to the user for this step.
