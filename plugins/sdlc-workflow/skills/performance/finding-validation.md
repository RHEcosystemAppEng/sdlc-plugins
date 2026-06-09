# Finding Validation Reference

Used by: performance-analyze-module (write + validate), performance-plan-optimization (read + validate).

## Validation Artifact Schema

Path: `{analysis_dir}/findings-validation.json`

```json
{
  "schema_version": "1.0",
  "generated_at": "ISO-8601",
  "workflow": "workflow-name",
  "validation_run": true,
  "statistics": {
    "submitted": 12, "confirmed": 5, "confirmed_low_confidence": 2,
    "downgraded": 1, "discarded": 4
  },
  "findings": [{
    "id": "F1",
    "anti_pattern": "N+1 Queries",
    "step": "7.3",
    "file": "src/handlers/packages.rs",
    "line": 142,
    "detection_method": "Serena",
    "evidence_excerpt": "for pkg in ids { db.query(...).await }",
    "checks": { "9.1-B": "PASS", "9.1-B2": "PASS" },
    "disposition": "Confirmed",
    "confidence": "High",
    "severity": "High",
    "timeline": "1-3 days",
    "reason": "Loop-bound query verified; no batch alternative"
  }]
}
```

## Field Rules

| Field | Rule |
|---|---|
| `validation_run` | Must be `true`. Do not write file if Step 9.1 was not executed |
| `findings[].id` | Unique F1, F2, ... matching Step 9.1-A inventory |
| `findings[].checks` | Both `9.1-B` and `9.1-B2` required for every row |
| `findings[].disposition` | Confirmed, Confirmed (Low Confidence), Downgraded, or Discarded |
| `findings[].reason` | Required for all dispositions |

## Disposition ↔ Checks Consistency

| Disposition | Required outcomes |
|---|---|
| Confirmed / Downgraded | `9.1-B: PASS` and `9.1-B2: PASS` |
| Confirmed (Low Confidence) | Both PASS + `confidence` = Low |
| Discarded | At least one starts with `FAILED:` |

## Validation Checklist

Read `findings-validation.json`. All rules must PASS before writing report or creating optimization plan.

### Artifact Rules (A1–A6)

| Rule | Check | FAIL when |
|---|---|---|
| A1 | Artifact exists and parses as JSON | Missing, invalid, or unknown schema_version |
| A2 | `validation_run` is `true` | false or absent |
| A3 | Every row complete | Missing id, disposition, checks, or reason |
| A4 | Dispositions valid | Not in allowed enum |
| A5 | Disposition ↔ checks consistent | Violates consistency table above |
| A6 | Statistics consistent | submitted ≠ len(findings) or counts don't sum |

### Report Crosswalk Rules (R1–R5)

Extract Finding IDs from scannable report regions (Anti-Pattern Analysis through Dynamic Performance Testing, excluding code fences, Finding Validation Summary, and Executive Summary).

| Rule | Check | FAIL when |
|---|---|---|
| R1 | Scannable IDs are Confirmed/Downgraded | ID has other disposition |
| R2 | Low Confidence in correct section | Low Confidence ID in scannable regions instead of Candidates for Manual Review |
| R3 | Discarded absent from body | Discarded ID in scannable regions |
| R4 | No orphans | Report ID not in artifact |
| R5 | No ghosts | Confirmed/Downgraded artifact row not in report |

**Blocking:** If any rule is FAIL, fix and re-run.
