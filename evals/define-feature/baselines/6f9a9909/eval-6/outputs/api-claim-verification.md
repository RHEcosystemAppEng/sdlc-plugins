# External API Claim Verification

## Detected Claim

**Section:** Requirements (Section 4)

**Claim:** "PR reviews cannot be updated after initial submission so always create a new review" with the note "The GitHub API does not support modifying a submitted review."

## Verification Attempt

**Method:** WebSearch / WebFetch
**Result:** UNAVAILABLE -- web tools are not accessible in this environment.

## Fallback Triggered

Per the define-feature skill's External API Claim Verification fallback procedure:

> I detected a claim about an external API but cannot verify it right now
> (web tools unavailable). The claim is: **"The GitHub API does not support
> modifying a submitted review -- PR reviews cannot be updated after initial
> submission."** Would you like to proceed as-is, or verify it manually before
> continuing?

## Status

**UNVERIFIED** -- This claim has not been confirmed or refuted against official
GitHub REST API documentation. It is flagged for manual verification before
implementation begins.

## Recommendation

Before proceeding with implementation, verify this claim against the official
GitHub REST API documentation. Specifically, check whether the endpoint
`PUT /repos/{owner}/{repo}/pulls/{pull_number}/reviews/{review_id}` exists,
as it would allow updating a submitted PR review.
