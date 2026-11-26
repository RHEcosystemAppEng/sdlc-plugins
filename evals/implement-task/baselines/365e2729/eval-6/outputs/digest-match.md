# Step 1.5 – Verify Description Integrity (TC-9201)

Protocol: `shared/description-digest-protocol.md`. I ran this check after Step 1 (fetch and parse TC-9201) and before Step 2 (verify dependencies).

## 1. Retrieve issue comments

```
jira.get_issue_comments("TC-9201")
```

(If MCP failed, Step 0.5 says to prompt the user before switching to the REST fallback: `python3 scripts/jira-client.py get_comments TC-9201`.)

Result (per the scenario): one comment.

| Field | Value |
|---|---|
| Body | `[sdlc-workflow] Description digest: sha256-md:a1b2c3d4e5f67890a1b2c3d4e5f67890a1b2c3d4e5f67890a1b2c3d4e5f67890` |
| created | T |
| updated | T (identical to created) |

## 2. Locate the digest comment

- I searched for comments whose body starts with the fixed marker `[sdlc-workflow] Description digest:`.
- Exactly one comment matched, so no tie-break was needed. With several matches I would pick the one with the latest `created` timestamp.
- A digest comment exists, so the "no digest found" path does not apply.

## 3. Comment edit detection (4a)

- `created` and `updated` are both present and equal.
- So the comment has not been edited since it was posted, and no "Digest comment was edited after initial posting" warning is issued.

## 4. Extract the stored digest (4b)

- Tagged value: `sha256-md:a1b2c3d4e5f67890a1b2c3d4e5f67890a1b2c3d4e5f67890a1b2c3d4e5f67890`
- Format tag: `sha256-md`. This is the tagged format, not the legacy untagged `sha256:<hex>`, so the legacy-skip path does not apply.
- Hex digest: `a1b2c3d4e5f67890a1b2c3d4e5f67890a1b2c3d4e5f67890a1b2c3d4e5f67890`. It is 64 lowercase hex characters, so it is a well-formed full SHA-256.

## 5. Compute the current digest (4c)

- I took the `description` field from the Step 1 `jira.get_issue("TC-9201")` response. MCP returns it as markdown.
- I wrote it to `/tmp/desc-TC-9201.txt` and ran:

  ```bash
  python3 scripts/sha256-digest.py /tmp/desc-TC-9201.txt
  ```

- I checked the exit code: it was 0. A non-zero exit would mean "warn and skip the integrity check, do not block".
- Output (per the scenario): `sha256-md:a1b2c3d4e5f67890a1b2c3d4e5f67890a1b2c3d4e5f67890a1b2c3d4e5f67890`
- I did not compute the hash by hand. The script is the only computation method allowed.

## 6. Compare format tags (4d)

- Stored tag `sha256-md` equals computed tag `sha256-md`.
- So there is no format mismatch: producer and consumer both used the markdown (MCP) path. I went on to compare the hex digests.

## 7. Compare hex digests (4e)

- Stored: `a1b2c3d4e5f67890a1b2c3d4e5f67890a1b2c3d4e5f67890a1b2c3d4e5f67890`
- Computed: `a1b2c3d4e5f67890a1b2c3d4e5f67890a1b2c3d4e5f67890a1b2c3d4e5f67890`
- The digests match.

## Outcome

- **Match:** the description has not changed since plan-feature created TC-9201.
- **Proceed silently.** Per the skill, a match adds no user prompt, no confirmation question and no extra latency. Neither the "description modified" alert nor the Proceed/Stop choice is shown.
- No warnings are surfaced:
  - no edit warning (timestamps are identical)
  - no legacy-format warning
  - no format-mismatch warning
  - no missing-digest warning
- Execution continues straight to **Step 2 – Verify Dependencies**. TC-9201 lists "Depends on: None", so there is nothing to check there, and the run moves on to Step 3.

The full implementation plan is in `plan.md`.
