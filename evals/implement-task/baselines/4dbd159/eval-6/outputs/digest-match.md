# Description Integrity Verification (Step 1.5)

## Procedure

1. **Retrieve issue comments**: Call `jira.get_issue_comments(TC-9201)` to fetch all comments on the Jira issue.

2. **Locate the digest comment**: Search through all returned comments for those whose body starts with the marker string `[sdlc-workflow] Description digest:`. In this case, one comment is found with body:
   ```
   [sdlc-workflow] Description digest: sha256:a1b2c3d4e5f67890a1b2c3d4e5f67890a1b2c3d4e5f67890a1b2c3d4e5f67890
   ```
   If multiple comments matched the marker, the most recent one by `created` timestamp would be selected to handle plan-feature re-run scenarios deterministically.

3. **Check for comment editing**: Compare the comment's `created` and `updated` timestamps. In this case, the `created` and `updated` timestamps are identical, which means the comment has not been edited since it was originally posted. No warning is needed. (If `updated` were later than `created`, a warning would be surfaced: "Digest comment was edited after initial posting -- integrity cannot be fully guaranteed." If timestamps were absent from the API response, this check would be skipped silently.)

4. **Extract the stored digest**: Parse the `sha256:<hex-digest>` value from the comment body. The stored digest is:
   ```
   a1b2c3d4e5f67890a1b2c3d4e5f67890a1b2c3d4e5f67890a1b2c3d4e5f67890
   ```

5. **Compute the current digest**: Take the current description field text from the Jira issue as returned by the API. Use the `scripts/sha256-digest.py` script (preferred method) to compute the SHA-256 hash. The normalization depends on the format:
   - If ADF JSON (MCP path): parse as JSON and re-serialize with compact separators (`json.dumps(parsed, separators=(',', ':'))`) before hashing.
   - If raw text (REST API path): strip leading and trailing whitespace before hashing.
   The result is a lowercase 64-character hexadecimal digest.

6. **Compare digests**: Compare the stored digest from the comment against the freshly computed digest of the current description.

## Outcome

The computed digest **matches** the stored digest `sha256:a1b2c3d4e5f67890a1b2c3d4e5f67890a1b2c3d4e5f67890a1b2c3d4e5f67890`. This confirms that the task description has not been modified since plan-feature originally created it.

**Action**: Proceed silently to the next step. No user prompt is required. No additional latency is added. The integrity check passes and execution continues without interruption.

If the digests had mismatched, the skill would have:
- Alerted the user that the task description was modified after plan-feature created it
- Displayed both the expected digest (from the comment) and the actual digest (computed from the current description)
- Asked the user whether to (1) proceed with the current description as-is, or (2) stop so they can re-run plan-feature to regenerate tasks
- Stopped execution immediately until the user responded
