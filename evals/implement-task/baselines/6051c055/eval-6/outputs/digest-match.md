# Description Integrity Verification — Step 1.5

## Task: TC-9201

## 1. Retrieve Issue Comments

Fetch all comments on the Jira issue TC-9201 using:

```
jira.get_issue_comments(TC-9201)
```

This returns the full list of comments, including their body text, `created`
timestamp, and `updated` timestamp.

## 2. Locate the Digest Comment

Scan the returned comments for any whose body starts with the marker string
defined in `shared/description-digest-protocol.md`:

```
[sdlc-workflow] Description digest:
```

One matching comment is found with body:

```
[sdlc-workflow] Description digest: sha256-md:a1b2c3d4e5f67890a1b2c3d4e5f67890a1b2c3d4e5f67890a1b2c3d4e5f67890
```

Since only one comment matches the marker, it is selected directly. (If multiple
comments matched, the most recent by `created` timestamp would be selected per the
protocol.)

## 3. Comment Edit Detection

The comment's `created` and `updated` timestamps are compared. In this case they
are identical, which confirms the comment has not been edited since it was originally
posted. No warning is emitted. This rules out the tampering scenario where an
attacker modifies both the description and the digest comment to match.

## 4. Extract the Stored Digest

Parse the tagged digest value from the comment body:

- **Format tag:** `sha256-md` (markdown format)
- **Hex digest:** `a1b2c3d4e5f67890a1b2c3d4e5f67890a1b2c3d4e5f67890a1b2c3d4e5f67890`

The format tag is `md`, not the legacy untagged `sha256:` format, so no legacy
warning is needed. Proceed with full integrity verification.

## 5. Compute the Current Digest

Extract the description field from the TC-9201 issue response (fetched in Step 1).
Write it to a temporary file and compute the digest:

```bash
python3 scripts/sha256-digest.py /tmp/desc-TC-9201.txt
```

The script auto-detects the input format (markdown in this case, since the
description was retrieved via MCP which returns markdown) and outputs a tagged
digest. The output is:

```
sha256-md:a1b2c3d4e5f67890a1b2c3d4e5f67890a1b2c3d4e5f67890a1b2c3d4e5f67890
```

The script exits with code 0, confirming successful computation.

## 6. Compare Format Tags

- Stored tag: `sha256-md`
- Computed tag: `sha256-md`

The format tags match. Both the producer (plan-feature) and consumer
(implement-task) used the same Jira access method (MCP, returning markdown).
Proceed to hex digest comparison.

## 7. Compare Hex Digests

- Stored hex: `a1b2c3d4e5f67890a1b2c3d4e5f67890a1b2c3d4e5f67890a1b2c3d4e5f67890`
- Computed hex: `a1b2c3d4e5f67890a1b2c3d4e5f67890a1b2c3d4e5f67890a1b2c3d4e5f67890`

**The digests match.** The task description has not been modified since plan-feature
created it.

## 8. Outcome: Proceed Silently

Per the protocol (SKILL.md Step 1.5, sub-step 4e — "Match: proceed silently — no
additional user prompt, no added latency") and
`shared/description-digest-protocol.md` (Consumer Verification, "Compare hex
digests — Match: proceed normally — description is unmodified since planning"):

- No user alert is emitted.
- No confirmation prompt is shown.
- No additional latency is introduced.
- Execution continues directly to Step 2 (Verify Dependencies).

This is the happy path — the digest check confirms integrity and adds zero
interaction overhead. The user is not notified because the verification succeeded
and there is nothing actionable to report.
