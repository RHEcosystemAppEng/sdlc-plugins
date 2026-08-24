# External API Claim Verification

## Detected Claim

In the Requirements section (Section 4), the following claim was detected:

> **Claim**: "PR reviews cannot be updated after initial submission so always create a new review"
> **Supporting statement**: "The GitHub API does not support modifying a submitted review"

This claim asserts that the GitHub REST API has no capability to update or modify a PR review once it has been submitted, and therefore the implementation must always create a new review.

## Verification Finding

This claim is **incorrect**. The GitHub REST API does support updating a submitted pull request review via the following endpoint:

```
PUT /repos/{owner}/{repo}/pulls/{pull_number}/reviews/{review_id}
```

This endpoint allows modifying the body of a previously submitted review. It accepts a `body` parameter with the updated review text and returns the updated review object. This means the implementation can update an existing review in place rather than creating a new one each time.

Reference: [GitHub REST API — Update a pull request review](https://docs.github.com/en/rest/pulls/reviews#update-a-pull-request-review)

## Suggested Corrected Language

**Original requirement**:
| PR reviews cannot be updated after initial submission so always create a new review | The GitHub API does not support modifying a submitted review | Yes |

**Corrected requirement**:
| Update the existing PR review when re-running evals, or create a new review if none exists | Use `PUT /repos/{owner}/{repo}/pulls/{pull_number}/reviews/{review_id}` to update an existing review | Yes |

The corrected language reflects the actual API capability: reviews can be updated after submission using the PUT endpoint, so the implementation should update an existing review rather than always creating a new one.
