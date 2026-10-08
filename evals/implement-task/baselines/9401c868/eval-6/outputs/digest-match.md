# Step 1.5 -- Description Integrity Verification for TC-9201

## 1. Retrieve issue comments

Fetch all comments on TC-9201:

```
jira.get_issue_comments("TC-9201")
```

This returns the list of comments on the issue. In this case, there is one comment.

## 2. Locate the digest comment

Search all returned comments for bodies starting with the marker string `[sdlc-workflow] Description digest:`.

One comment matches:

```
[sdlc-workflow] Description digest: sha256-md:a1b2c3d4e5f67890a1b2c3d4e5f67890a1b2c3d4e5f67890a1b2c3d4e5f67890
```

Since only one comment matches, it is selected directly (no need for most-recent tiebreaking).

## 3. Check for comment editing

Compare the comment's `created` and `updated` timestamps. They are identical, which means the comment has not been edited after initial posting. No warning is needed. Proceed to digest comparison.

## 4. Extract the stored digest

Parse the tagged digest value from the comment body:

- **Format tag**: `sha256-md` (indicates the description was hashed as markdown text)
- **Hex digest**: `a1b2c3d4e5f67890a1b2c3d4e5f67890a1b2c3d4e5f67890a1b2c3d4e5f67890`

This is not a legacy untagged format (`sha256:<hex>`) -- it uses the current format-tagged convention. No legacy warning needed.

## 5. Compute the current digest

Extract the description field from the TC-9201 issue response. Write it to a temp file and compute the digest using the script:

```bash
python3 scripts/sha256-digest.py /tmp/desc-TC-9201.txt
```

The script auto-detects the input format. Since the description is markdown text (fetched via MCP), the script outputs:

```
sha256-md:a1b2c3d4e5f67890a1b2c3d4e5f67890a1b2c3d4e5f67890a1b2c3d4e5f67890
```

The script exits with status 0 (success).

## 6. Compare format tags

- Stored tag: `sha256-md`
- Computed tag: `sha256-md`

Tags match. Proceed to hex digest comparison.

## 7. Compare hex digests

- Stored hex: `a1b2c3d4e5f67890a1b2c3d4e5f67890a1b2c3d4e5f67890a1b2c3d4e5f67890`
- Computed hex: `a1b2c3d4e5f67890a1b2c3d4e5f67890a1b2c3d4e5f67890a1b2c3d4e5f67890`

**Match.** The description has not been modified since plan-feature created it.

## 8. Outcome

Per the SKILL.md specification: when digests match, **proceed silently** -- no additional user prompt, no added latency. The integrity check passes and execution continues to Step 2 (Verify Dependencies) without any user interaction or warning output.
