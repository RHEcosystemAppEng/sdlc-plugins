# Step 1.5 -- Description Integrity Verification for TC-9201

## 1. Retrieve Issue Comments

Fetch all comments on TC-9201 using:

```
jira.get_issue_comments("TC-9201")
```

## 2. Locate the Digest Comment

Search all returned comments for those whose body starts with the marker string defined in `shared/description-digest-protocol.md`:

```
[sdlc-workflow] Description digest:
```

One comment is found with the body:

```
[sdlc-workflow] Description digest: sha256-md:a1b2c3d4e5f67890a1b2c3d4e5f67890a1b2c3d4e5f67890a1b2c3d4e5f67890
```

Since only one comment matches the marker, it is selected directly. (If multiple comments had matched, the most recent one by `created` timestamp would be selected, per the protocol's Multiple Digest Comments rule.)

## 3. Comment Edit Detection

The comment's `created` and `updated` timestamps are compared. They are identical, meaning the comment has not been edited after initial posting. No warning is necessary -- the digest comment is unmodified and trustworthy.

## 4. Extract the Stored Digest

From the comment body, parse the tagged digest value:

- **Format tag:** `sha256-md` (indicates the description was hashed as markdown text)
- **Hex digest:** `a1b2c3d4e5f67890a1b2c3d4e5f67890a1b2c3d4e5f67890a1b2c3d4e5f67890`

The digest uses the current format-tagged format (`sha256-md:`), not the legacy untagged format (`sha256:`), so no legacy-format warning is needed.

## 5. Compute the Current Digest

Extract the description field from the TC-9201 issue response. Write it to a temporary file and compute the digest using the script:

```bash
python3 scripts/sha256-digest.py /tmp/desc-TC-9201.txt
```

The script auto-detects the input format (markdown text in this case) and outputs a format-tagged digest. The output is:

```
sha256-md:a1b2c3d4e5f67890a1b2c3d4e5f67890a1b2c3d4e5f67890a1b2c3d4e5f67890
```

The script exits with status 0, so the digest is valid.

## 6. Compare Format Tags

The stored tag is `sha256-md` and the computed tag is `sha256-md`. The tags match, so the digests are directly comparable. No format mismatch warning is needed.

## 7. Compare Hex Digests

- **Stored digest:** `a1b2c3d4e5f67890a1b2c3d4e5f67890a1b2c3d4e5f67890a1b2c3d4e5f67890`
- **Computed digest:** `a1b2c3d4e5f67890a1b2c3d4e5f67890a1b2c3d4e5f67890a1b2c3d4e5f67890`

The hex digests **match**. The task description has not been modified since plan-feature created it.

## 8. Outcome

**Proceed silently.** Per the protocol, when digests match there is no additional user prompt and no added latency. The integrity check passes on the happy path -- execution continues directly to Step 2 (Verify Dependencies) without alerting the user or pausing.
