# Description Integrity Verification -- Step 1.5

## 1. Locating the Digest Comment

After fetching the Jira issue TC-9201 and parsing its structured description in Step 1, Step 1.5 begins by retrieving all comments on the issue:

```
jira.get_issue_comments("TC-9201")
```

The returned comments are searched for any whose body starts with the marker string defined in `shared/description-digest-protocol.md`:

```
[sdlc-workflow] Description digest:
```

In this case, one comment matches:

```
[sdlc-workflow] Description digest: sha256-md:a1b2c3d4e5f67890a1b2c3d4e5f67890a1b2c3d4e5f67890a1b2c3d4e5f67890
```

Since only one comment matches the marker, it is selected directly. If multiple had matched, the most recent by `created` timestamp would be selected per the protocol.

## 2. Comment Edit Detection

The comment's `created` and `updated` timestamps are compared. In this case, they are identical -- the comment has not been edited since initial posting. No warning is needed; proceed with digest comparison.

## 3. Extracting the Stored Digest

The tagged digest value is parsed from the comment body:

- **Format tag**: `sha256-md` (indicates the description was hashed as markdown text)
- **Hex digest**: `a1b2c3d4e5f67890a1b2c3d4e5f67890a1b2c3d4e5f67890a1b2c3d4e5f67890`

The digest uses the current format-tagged convention (not the legacy untagged `sha256:<hex>` format), so no legacy-format warning is needed.

## 4. Computing the Current Digest

The current description field from the Jira issue response is written to a temporary file and the digest is computed using the canonical script:

```bash
python3 scripts/sha256-digest.py /tmp/desc-TC-9201.txt
```

The script auto-detects that the input is plain markdown text (not ADF JSON) and outputs:

```
sha256-md:a1b2c3d4e5f67890a1b2c3d4e5f67890a1b2c3d4e5f67890a1b2c3d4e5f67890
```

## 5. Comparing Format Tags

The stored tag (`sha256-md`) and the computed tag (`sha256-md`) match. Both the producer (plan-feature) and the consumer (implement-task) used the same API access method, so the digests are directly comparable. No format-mismatch warning is needed.

## 6. Comparing Hex Digests

The stored hex digest and the computed hex digest are compared:

- **Stored**: `a1b2c3d4e5f67890a1b2c3d4e5f67890a1b2c3d4e5f67890a1b2c3d4e5f67890`
- **Computed**: `a1b2c3d4e5f67890a1b2c3d4e5f67890a1b2c3d4e5f67890a1b2c3d4e5f67890`

**Result: MATCH.**

## 7. Outcome

The digests match, confirming that the task description has not been modified since plan-feature created it. Per the protocol and Step 1.5 specification:

- **Proceed silently** -- no user prompt, no alert, no additional latency.
- The integrity check is complete. Execution continues to Step 2 (Verify Dependencies) without any user interaction or output related to the digest verification.

This is the happy path: the digest comment exists, is unedited, uses the current format-tagged convention, and the hex digests match. No warnings, no alerts, no pauses.
