# External API Claim Verification

## Detected Claim

While processing **Section 4 -- Requirements**, the following claim about an external API was detected:

> **"PR reviews cannot be updated after initial submission so always create a new review"**
> Notes: "The GitHub API does not support modifying a submitted review"

This is a claim asserting that the GitHub REST API lacks the capability to modify/update a submitted PR review.

## Verification Attempt

**Status: COULD NOT VERIFY -- web tools unavailable**

WebSearch and WebFetch are unavailable in this session. The claim cannot be verified against the official GitHub REST API documentation.

## Fallback Action

Per the define-feature skill's External API Claim Verification fallback path, the following message was presented to the user:

> I detected a claim about an external API but cannot verify it right now
> (web tools unavailable). The claim is: **"The GitHub API does not support
> modifying a submitted review -- PR reviews cannot be updated after initial
> submission."** Would you like to proceed as-is, or verify it manually before
> continuing?

**User response:** Proceed as-is.

## Outcome

The original claim wording has been **retained unchanged** in the Feature description since it could not be verified. The requirement reads:

| Requirement | Notes | Is MVP? |
|---|---|---|
| PR reviews cannot be updated after initial submission so always create a new review | The GitHub API does not support modifying a submitted review | Yes |

**Note:** This claim should be manually verified against the [GitHub REST API documentation for Pull Request Reviews](https://docs.github.com/en/rest/pulls/reviews) before implementation begins. The GitHub API may support `PUT /repos/{owner}/{repo}/pulls/{pull_number}/reviews/{review_id}` to update a review, which would contradict this requirement.
