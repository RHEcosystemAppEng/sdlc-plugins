# External API Claim Verification

## Detected Claim

**Section:** Requirements (Section 4)

**Claim text:** "PR reviews cannot be updated after initial submission" / "The GitHub API does not support modifying a submitted review"

**Context:** Requirement row states: "PR reviews cannot be updated after initial submission so always create a new review" with note "The GitHub API does not support modifying a submitted review"

## Verification Finding

**Result: INCORRECT**

The GitHub REST API does support updating a submitted pull request review. The endpoint is:

```
PUT /repos/{owner}/{repo}/pulls/{pull_number}/reviews/{review_id}
```

This endpoint allows modifying the body of an already-submitted review. It accepts the `owner`, `repo`, `pull_number`, and `review_id` path parameters along with a `body` field to update the review content.

This means the premise of the requirement -- that reviews are immutable after submission and therefore a new review must always be created -- is factually incorrect.

## Suggested Corrected Language

**Original requirement:** "PR reviews cannot be updated after initial submission so always create a new review"

**Corrected requirement:** "Update an existing eval review if one was previously posted; create a new review only on the first run"

**Original notes:** "The GitHub API does not support modifying a submitted review"

**Corrected notes:** "Use PUT /repos/{owner}/{repo}/pulls/{pull_number}/reviews/{review_id} to update an existing review"
