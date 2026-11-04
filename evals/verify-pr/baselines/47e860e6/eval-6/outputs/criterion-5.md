# Criterion 5: Check 6 produces N/A when no new symbols are introduced in the PR

**Verdict: PASS**

## Evidence
N/A is defined in two places:
- 6a: "If no new symbols are found, skip to the Verdict and record N/A."
- 6c: "**N/A** — no new symbols introduced in the PR"

This uses the same early-exit pattern as Checks 2 and 3 ("If no test files are found, skip to the Verdict and record N/A").

Because 6b skips Markdown files, a PR that changes only Markdown (like this one) will always get N/A. That fits the criterion, but it is exactly the behavior review comment 50001 challenges (see review-50001.md).
