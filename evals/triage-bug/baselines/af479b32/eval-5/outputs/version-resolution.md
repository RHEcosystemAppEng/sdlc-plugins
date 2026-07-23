# Step 4.5 -- Affects Version Resolution

## 4.5.1 -- Check Existing Field

The bug's `affectsVersions` field is **not populated** (recorded as "(none)" in Step 1 metadata). No existing versions to keep, replace, or augment. Proceeding to extraction.

## 4.5.2 -- Extract Version from Description

**Environment / Version section content:**

> Not sure which version -- using whatever is deployed on staging.

**Extraction attempt:** Scanned the section content for version identifiers:

- Explicit version numbers (e.g., `0.9.0`, `2.1.1`): **none found**
- Product-prefixed versions (e.g., `RHTPA 2.1.0`): **none found**
- Version keywords followed by numbers (e.g., `version 1.2.3`): **none found**

The section contains only vague text ("Not sure which version", "whatever is deployed on staging"). No version pattern can be extracted.

**Result:** No version identifier found. Skipping to sub-step 4.5.6 (gap flagging).

## 4.5.3 -- Discover Available Jira Versions

Skipped -- version extraction failed in 4.5.2, so matching against available Jira versions is not applicable.

## 4.5.4 -- Match

Skipped -- no version text was extracted in 4.5.2.

## 4.5.5 -- Confirm with User

Skipped -- no match to confirm.

## 4.5.6 -- Flag Gap

**Reason version could not be determined:**

The Environment / Version section of bug ACME-511 does not contain any recognizable version identifier. The reporter stated "Not sure which version -- using whatever is deployed on staging," which is vague text without a specific version number, product-prefixed version, or version keyword followed by a number.

**Action:** Post a comment on the Bug issue:

> Affects Version could not be determined from the bug description -- please set manually.

(Comment would include the sdlc-workflow/triage-bug footnote with plugin version.)

**Affects Version field remains unset on ACME-511.**
