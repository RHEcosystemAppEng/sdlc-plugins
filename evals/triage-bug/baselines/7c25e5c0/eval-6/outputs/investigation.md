# Steps 2-3 -- Codebase Investigation

## Component Identification

The bug is in the **sdlc-workflow** component, specifically the **plan-feature** skill's convention conformance analysis.

## Relevant Code Paths

### 1. Convention Heading Extraction

**File**: `plugins/sdlc-workflow/skills/plan-feature/SKILL.md`

The plan-feature skill reads `CONVENTIONS.md` headings using this logic:

```python
for line in conventions_content.split('\n'):
    if line.startswith('## '):
        section_name = line[3:]  # Extracts heading text after "## "
        conventions[section_name] = current_section_content
```

**Finding**: The heading extraction at `line[3:]` does NOT strip trailing whitespace.
If the heading line is `## Migration Patterns  \n`, the extracted section name becomes
`"Migration Patterns  "` (with trailing spaces), which fails exact-match comparison
against the expected `"Migration Patterns"`.

### 2. Convention-Aware Task Enrichment

**File**: `plugins/sdlc-workflow/skills/plan-feature/SKILL.md`

The task enrichment step matches conventions by section name:

```python
if convention_name in discovered_conventions:
    notes.append(f"Per CONVENTIONS.md {convention_name}: {action}")
```

**Finding**: This match fails when `convention_name` has trailing whitespace from the extraction step. The lookup key `"Migration Patterns"` does not equal the stored key `"Migration Patterns  "`, so the convention is silently skipped.

### 3. Test Coverage Gap

**File**: `evals/plan-feature/files/conventions-mock.md`

The existing eval fixture for plan-feature conventions does NOT include trailing whitespace on headings, so this edge case is not covered by current evals.

### 4. CONVENTIONS.md

The repository does not have a `CONVENTIONS.md` at its root -- the bug manifests in downstream repos that do have one with trailing whitespace on headings.

## Summary of Findings

The root cause is localized to the heading extraction code in the plan-feature skill. The `line[3:]` slice captures everything after `## ` including trailing whitespace. The downstream exact-match lookup then fails silently because the key includes trailing spaces. No warning or error is emitted when a convention heading match fails, making the bug silent.
