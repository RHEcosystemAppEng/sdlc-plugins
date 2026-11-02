# Codebase Investigation: ACME-500

## Steps 2-3 -- Investigation Findings

### Identified Bug Location

**File**: `plugins/sdlc-workflow/skills/plan-feature/SKILL.md` (convention conformance analysis)

### Bug Mechanism

The plan-feature skill reads `CONVENTIONS.md` and extracts section headings using the following logic:

```python
for line in conventions_content.split('\n'):
    if line.startswith('## '):
        section_name = line[3:]  # Extracts heading text after "## "
        conventions[section_name] = current_section_content
```

The heading extraction at `line[3:]` slices from character index 3 onward but does **not** strip trailing whitespace. When a heading line contains trailing spaces (e.g., `## Migration Patterns  \n`), the extracted section name becomes `"Migration Patterns  "` (with trailing spaces).

### How the Match Fails

The task enrichment step matches conventions by exact section name:

```python
if convention_name in discovered_conventions:
    notes.append(f"Per CONVENTIONS.md Section {convention_name}: {action}")
```

The lookup uses the canonical name `"Migration Patterns"` (without trailing whitespace), which does not match the extracted key `"Migration Patterns  "` (with trailing whitespace). The convention is silently skipped -- no warning or error is emitted.

### Test Coverage Gap

The existing eval fixture (`evals/plan-feature/files/conventions-mock.md`) does **not** include trailing whitespace on headings. This edge case is not covered by current evals, which is why the bug was not caught before release.

### Persistence Impact Analysis

The convention lookup is a **runtime operation** -- the buggy section names extracted from `CONVENTIONS.md` are used in-memory during plan-feature execution and are not persisted to any data store. This means:

- No corrupted data exists in storage
- The fix is immediate upon deployment -- no migration or data cleanup is needed
- The impact is limited to the quality of generated task descriptions (missing convention references)

### Affected Components

| Component | Impact |
|---|---|
| plan-feature convention lookup | Primary: heading extraction does not strip whitespace |
| plan-feature task enrichment | Secondary: exact-match comparison fails on whitespace-padded keys |
| Generated task descriptions | Symptom: missing convention references in Implementation Notes |
