# Step 1.5 -- Verify Description Integrity (TC-9201)

## 1. Retrieve Issue Comments

After fetching the task description in Step 1, retrieve all comments on TC-9201:

```
jira.get_issue_comments("TC-9201")
```

## 2. Locate the Digest Comment

Search the returned comments for any whose body starts with the marker string `[sdlc-workflow] Description digest:`, as defined in `shared/description-digest-protocol.md`. This is an exact prefix match on the comment body text.

One comment is found with the body:

```
[sdlc-workflow] Description digest: sha256-md:a1b2c3d4e5f67890a1b2c3d4e5f67890a1b2c3d4e5f67890a1b2c3d4e5f67890
```

Since only one comment matches the marker, it is selected directly. If multiple comments had matched, the most recent one by `created` timestamp would be selected, per the protocol's "Multiple Digest Comments" rule.

## 3. Comment Edit Detection

Compare the comment's `created` and `updated` timestamps. In this case, the two timestamps are identical, which means the comment has not been edited since it was posted. No warning is needed -- the comment is trustworthy.

## 4. Extract the Stored Digest

Parse the tagged digest value from the comment body:

- **Format tag**: `sha256-md` (indicates the description was hashed as markdown text)
- **Hex digest**: `a1b2c3d4e5f67890a1b2c3d4e5f67890a1b2c3d4e5f67890a1b2c3d4e5f67890`

The digest uses the format-tagged style (`sha256-md:`), not the legacy untagged format (`sha256:`), so no legacy-format warning is needed.

## 5. Compute the Current Digest

Extract the description field from the TC-9201 issue response (as returned by `jira.get_issue`). Write the description content to a temporary file and compute the digest:

```bash
python3 scripts/sha256-digest.py /tmp/desc-TC-9201.txt
```

The script auto-detects the input format (markdown text in this case) and outputs a tagged digest. The script exits zero, producing:

```
sha256-md:a1b2c3d4e5f67890a1b2c3d4e5f67890a1b2c3d4e5f67890a1b2c3d4e5f67890
```

## 6. Compare Format Tags

The stored tag is `sha256-md` and the computed tag is `sha256-md` -- the tags match. Both the producer (plan-feature) and the consumer (implement-task) used the same Jira access method, so the hex digests are directly comparable.

## 7. Compare Hex Digests

- **Stored digest**: `a1b2c3d4e5f67890a1b2c3d4e5f67890a1b2c3d4e5f67890a1b2c3d4e5f67890`
- **Computed digest**: `a1b2c3d4e5f67890a1b2c3d4e5f67890a1b2c3d4e5f67890a1b2c3d4e5f67890`

The digests **match**. The task description has not been modified since plan-feature created it.

## 8. Outcome

Per the protocol: when digests match, **proceed silently** -- no additional user prompt, no added latency. The integrity check passes without any user-facing output or interruption. Execution continues directly to Step 2 (Verify Dependencies) with zero additional delay for this happy-path scenario.
