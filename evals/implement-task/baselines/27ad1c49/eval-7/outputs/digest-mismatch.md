# Step 1.5 -- Description Integrity Verification: Digest Mismatch Handling

## 1. Locating the Digest Comment

After fetching task TC-9201 in Step 1, Step 1.5 begins by retrieving all comments on the issue:

```
jira.get_issue_comments("TC-9201")
```

The returned comments are searched for any whose body starts with the marker string defined in `shared/description-digest-protocol.md`:

```
[sdlc-workflow] Description digest:
```

This is an exact prefix match -- the consumer scans each comment body for this literal marker. If multiple comments match (e.g., from plan-feature re-runs), the most recent one by `created` timestamp is selected to ensure deterministic behavior.

In this scenario, exactly one comment matches, with body:

```
[sdlc-workflow] Description digest: sha256-md:0000000000000000000000000000000000000000000000000000000000000000
```

## 2. Comment Edit Detection

Before proceeding to digest comparison, the comment's `created` and `updated` timestamps are compared. In this scenario, the two timestamps are identical, which means the comment has not been edited after initial posting. No edit-detection warning is emitted. Digest comparison proceeds normally.

## 3. Extracting the Stored Digest

The stored digest value is parsed from the comment body:

- **Format tag:** `sha256-md`
- **Hex digest:** `0000000000000000000000000000000000000000000000000000000000000000`

Since the digest uses the tagged format (`sha256-md:<hex>`), not the legacy untagged format (`sha256:<hex>`), the integrity check proceeds. (A legacy untagged format would trigger a warning and skip the check.)

## 4. Computing the Current Digest

The current description is extracted from the issue response obtained in Step 1. It is written to a temporary file and the digest is computed using the script:

```bash
python3 scripts/sha256-digest.py /tmp/desc-TC-9201.txt
```

The script auto-detects the input format (markdown text in this case) and outputs a format-tagged digest. Suppose the script outputs:

```
sha256-md:e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855
```

(The actual hex value would depend on the current description content.)

## 5. Comparing Format Tags

The stored tag is `sha256-md` and the computed tag is `sha256-md` -- the tags match. This means both the producer (plan-feature) and the consumer (implement-task) used the same Jira access method (both returned markdown). The hex digests can be compared directly.

If the tags had differed (e.g., stored `sha256-adf` vs. computed `sha256-md`), the skill would log a warning about different API access methods and skip the integrity check entirely. That is not the case here.

## 6. Detecting the Hex Digest Mismatch

The hex digests are compared:

- **Expected (from digest comment):** `sha256-md:0000000000000000000000000000000000000000000000000000000000000000`
- **Actual (computed from current description):** `sha256-md:e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855`

The hex values differ. This means the task description was modified after plan-feature created the task and recorded its digest.

## 7. Alerting the User

The following alert is presented to the user:

```
WARNING: Task description integrity check failed.

The description for TC-9201 was modified after plan-feature created it.
The content has changed since planning, which may mean the implementation
plan no longer aligns with the current description.

  Expected digest (recorded by plan-feature):
    sha256-md:0000000000000000000000000000000000000000000000000000000000000000

  Actual digest (computed from current description):
    sha256-md:e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855

How would you like to proceed?

  1. Proceed -- implement using the current (modified) description as-is
  2. Stop -- abort so you can re-run plan-feature to regenerate tasks
     with an updated plan

Choose (1/2):
```

## 8. Stopping Execution

Execution stops immediately at this point. The skill does NOT proceed to Step 2 (Verify Dependencies), Step 3 (Transition to In Progress), or any subsequent step. No branch is created, no code is read, no implementation planning occurs.

The skill waits for the user to respond with their choice:

- **If the user chooses 1 (Proceed):** The skill accepts the current description as the specification and continues to Step 2 (Verify Dependencies) and onward through the normal flow.
- **If the user chooses 2 (Stop):** The skill terminates. The user is expected to re-run plan-feature to regenerate tasks that reflect the updated description, producing a new digest comment that will match on the next implement-task run.
