# Codebase Investigation -- ACME-500

## Investigation Summary

Bug ACME-500 reports that the plan-feature skill silently drops conventions from CONVENTIONS.md when heading lines contain trailing whitespace.

## Relevant Code Paths

### 1. Convention Heading Extraction

**File**: `plugins/sdlc-workflow/skills/plan-feature/SKILL.md`

The plan-feature skill reads CONVENTIONS.md headings using the following logic:

```python
for line in conventions_content.split('\n'):
    if line.startswith('## '):
        section_name = line[3:]  # Extracts heading text after "## "
        conventions[section_name] = current_section_content
```

**Finding**: The heading extraction at `line[3:]` does NOT strip trailing whitespace. When the heading line is `## Migration Patterns  \n`, the extracted section name becomes `"Migration Patterns  "` (with two trailing spaces). This is the root of the bug.

### 2. Convention-Aware Task Enrichment

**File**: `plugins/sdlc-workflow/skills/plan-feature/SKILL.md`

The task enrichment step matches conventions by section name using exact string comparison:

```python
if convention_name in discovered_conventions:
    notes.append(f"Per CONVENTIONS.md {convention_name}: {action}")
```

**Finding**: This match fails when `convention_name` is `"Migration Patterns"` (no trailing spaces) but the key in `discovered_conventions` is `"Migration Patterns  "` (with trailing spaces from extraction). The exact-match comparison returns False, so the convention is silently skipped.

### 3. Test Coverage Gap

**File**: `evals/plan-feature/files/conventions-mock.md`

The existing eval fixture for plan-feature conventions does NOT include trailing whitespace on headings. This edge case is not covered by current evals, which is why the bug was not caught earlier.

### 4. No Warning or Error Logging

The code does not log a warning when a convention fails to match. The failure is entirely silent -- no diagnostic output tells the user that a convention was skipped. This makes the bug difficult to detect without careful inspection of the generated task output.

## Affected Component

- **Component**: sdlc-workflow
- **Skill**: plan-feature
- **Scope**: Convention conformance analysis and task enrichment
