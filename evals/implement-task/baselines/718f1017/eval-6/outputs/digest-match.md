# Step 1.5 -- Description Integrity Verification for TC-9201

## Context

The Jira issue TC-9201 has one comment posted by a previous plan-feature run with the body:

```
[sdlc-workflow] Description digest: sha256-md:a1b2c3d4e5f67890a1b2c3d4e5f67890a1b2c3d4e5f67890a1b2c3d4e5f67890
```

The eval prompt states that this format-tagged digest MATCHES the digest computed from the current task description, and that the comment's `created` and `updated` timestamps are identical.

## How Step 1.5 Would Be Handled

### Sub-step 1: Retrieve issue comments

Fetch all comments on TC-9201 using:

```
jira.get_issue_comments("TC-9201")
```

This returns the list of comments on the issue.

### Sub-step 2: Locate the digest comment

Search all returned comments for bodies starting with the marker string `[sdlc-workflow] Description digest:`. In this case, exactly one comment matches. Since there is only one matching comment, it is selected directly (no need to compare timestamps across multiple candidates).

The matched comment body is:
```
[sdlc-workflow] Description digest: sha256-md:a1b2c3d4e5f67890a1b2c3d4e5f67890a1b2c3d4e5f67890a1b2c3d4e5f67890
```

### Sub-step 3: Digest comment found -- proceed with verification

Since a digest comment was found, we proceed through the verification sub-steps:

#### 4a. Check for comment editing

Compare the comment's `created` and `updated` timestamps. In this scenario, they are identical, meaning the comment has NOT been edited after initial posting. No warning is emitted. Proceed with digest comparison.

#### 4b. Extract the stored digest

Parse the tagged digest value from the comment body:
- **Format tag**: `sha256-md` (indicating the description was hashed as markdown text)
- **Hex digest**: `a1b2c3d4e5f67890a1b2c3d4e5f67890a1b2c3d4e5f67890a1b2c3d4e5f67890`

This is NOT a legacy untagged format (which would be `sha256:<hex>` without the `-md` or `-adf` suffix), so no legacy warning is needed.

#### 4c. Compute the current digest

Extract the description field from the TC-9201 issue response, write it to a temp file, and compute the digest:

```bash
python3 scripts/sha256-digest.py /tmp/desc-TC-9201.txt
```

The script auto-detects the format (in this case, markdown text) and outputs a tagged digest. Per the eval premise, the output would be:

```
sha256-md:a1b2c3d4e5f67890a1b2c3d4e5f67890a1b2c3d4e5f67890a1b2c3d4e5f67890
```

#### 4d. Compare format tags

The stored tag is `sha256-md` and the computed tag is `sha256-md`. The tags MATCH, so we proceed to hex digest comparison. No format mismatch warning is needed.

#### 4e. Compare hex digests

The stored hex digest is `a1b2c3d4e5f67890a1b2c3d4e5f67890a1b2c3d4e5f67890a1b2c3d4e5f67890` and the computed hex digest is the same value. The digests MATCH.

### Outcome

**The description integrity check passes silently.** No user prompt is needed, no warning is emitted, and no additional latency is added. The skill proceeds directly to Step 2 (Verify Dependencies).

This confirms that the task description has not been modified since plan-feature created it, providing confidence that the implementation will be based on the original planned specification.
