## Review Comment 30004 -- Classification: Question

**Comment by:** reviewer-a
**File:** modules/fundamental/src/sbom/endpoints/get.rs, line 1
**Comment text:** Have you considered what happens when someone queries `/api/v2/sbom/{id}` for a soft-deleted SBOM without `include_deleted=true`? Looking at `get.rs`, it doesn't filter by `deleted_at` -- so direct GET still returns deleted SBOMs. Is that intentional?

### Classification Reasoning

This comment is classified as a **question** because:

1. **Interrogative framing:** The comment consists entirely of questions -- "Have you considered..." and "Is that intentional?" The reviewer is asking for clarification about a design decision, not requesting a code change.

2. **Seeks clarification, not action:** The reviewer observes that `get.rs` does not filter by `deleted_at` and asks whether this is intentional behavior. They are not stating that the code is wrong or requesting a fix -- they want to understand the design intent before drawing a conclusion.

3. **No directive language:** The comment contains no imperative statements like "you should", "please fix", "this needs to", or "add filtering here". It is purely exploratory, asking the PR author to explain the current behavior.

4. **Contextual observation:** The reviewer is noting a potential gap between the task description (which mentions `include_deleted=true` parameter on GET) and the implementation (which doesn't modify `get.rs`). This is a valid observation that may lead to a follow-up code change request, but as stated, it is a question seeking the author's perspective.

### Action

No sub-task created. This is a question asking for clarification about design intent. The PR author should respond to explain whether the current GET behavior (returning deleted SBOMs without requiring `include_deleted=true`) is intentional. Note: this question relates to the Scope Containment finding -- `get.rs` is listed in the task's Files to Modify but was not changed in the PR.
