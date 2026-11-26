# External API Claim Verification — Fallback Result

## Claim Detected

- **Section:** Requirements (Step 3d), row 4
- **API:** GitHub REST API (Pull Request Reviews)
- **Claim (requirement):** "PR reviews cannot be updated after initial submission so always create a new review"
- **Claim (notes):** "The GitHub API does not support modifying a submitted review"
- **Pattern matched:** "X cannot be updated / modified after creation" and "The API does not support Y"

## User Notification

> I detected a claim about an external API capability in your Requirements section:
> **"PR reviews cannot be updated after initial submission"** / **"The GitHub API does not support modifying a submitted review"**.
> I will attempt to verify it against the official GitHub REST API documentation.

## Verification Attempt

- **WebSearch:** unavailable — not performed
- **WebFetch:** unavailable — not performed
- **Official documentation consulted:** none (web tools unavailable)

## Result: UNVERIFIED (fallback path)

The claim could not be confirmed or refuted against official documentation. Following the
skill's fallback rule, the claim is flagged to the user rather than silently accepted:

> "I detected a claim about an external API but cannot verify it right now
> (web tools unavailable). The claim is: **PR reviews cannot be updated after initial
> submission — the GitHub API does not support modifying a submitted review**. Would you
> like to proceed as-is, or verify it manually before continuing?"

## Suggested Manual Verification

Before relying on this requirement, check the official GitHub REST API documentation for
Pull Request Reviews (docs.github.com, "REST API endpoints for pull request reviews") and
look specifically for whether an update method (e.g., a `PUT` on
`/repos/{owner}/{repo}/pulls/{pull_number}/reviews/{review_id}`) exists for submitted reviews.
If such an endpoint exists, the requirement should be revised (e.g., to "update the existing
eval-results review on subsequent runs instead of creating a new one"), since this assumption
directly shapes downstream planning and implementation.

## Handling in This Run

- No correction was applied — the skill must not fabricate or alter user content without confirmation.
- The original wording is retained in the Feature description, and the claim is surfaced as
  **unverified** in the preview and in the post-creation Jira comment so it is reviewed during
  planning (`/sdlc-workflow:plan-feature`).
