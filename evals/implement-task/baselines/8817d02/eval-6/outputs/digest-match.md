# Step 1.5 -- Description Integrity Verification (Digest Match Scenario)

## 1. Locating the Digest Comment

After fetching the task TC-9201 via `jira.get_issue("TC-9201")` in Step 1, retrieve all comments on the issue:

```
jira.get_issue_comments("TC-9201")
```

Search the returned comments for any whose body starts with the marker string `[sdlc-workflow] Description digest:` as defined in `shared/description-digest-protocol.md`. In this case, one comment is found with the body:

```
[sdlc-workflow] Description digest: sha256-md:a1b2c3d4e5f67890a1b2c3d4e5f67890a1b2c3d4e5f67890a1b2c3d4e5f67890
```

Since there is only one matching comment, it is selected directly. If multiple comments matched, the most recent one by `created` timestamp would be selected.

## 2. Comment Edit Detection

Before comparing digests, check whether the digest comment was edited after posting by comparing its `created` and `updated` timestamps. In this scenario, the comment's `created` and `updated` timestamps are identical, which means the comment has not been modified since it was posted. No warning is needed -- proceed to digest comparison.

## 3. Computing and Comparing the Digest

Extract the stored tagged digest from the comment body: `sha256-md:a1b2c3d4e5f67890a1b2c3d4e5f67890a1b2c3d4e5f67890a1b2c3d4e5f67890`. Parse the format tag (`md`) and the hex digest (`a1b2c3d4e5f67890a1b2c3d4e5f67890a1b2c3d4e5f67890a1b2c3d4e5f67890`).

Compute the current digest by extracting the description field from the issue response, writing it to a temp file, and running:

```bash
python3 scripts/sha256-digest.py /tmp/desc-TC-9201.txt
```

The script auto-detects the input format (markdown in this case) and outputs a tagged digest. The computed digest is:

```
sha256-md:a1b2c3d4e5f67890a1b2c3d4e5f67890a1b2c3d4e5f67890a1b2c3d4e5f67890
```

Compare format tags first: both are `sha256-md`, so the tags match. Then compare the hex digests: both are `a1b2c3d4e5f67890a1b2c3d4e5f67890a1b2c3d4e5f67890a1b2c3d4e5f67890`, so the digests match.

## 4. Proceeding Silently

Since the format tags match and the hex digests match, the description has not been modified since plan-feature created it. Per the protocol:

> **Match**: proceed silently -- no additional user prompt, no added latency.

The skill proceeds directly to Step 2 (Verify Dependencies) without alerting the user, without pausing, and without any additional prompts. The integrity verification is complete and confirms the description is authentic and unmodified.
