# Finding Validation Reference

Used by: performance-analyze-module (write + validate), performance-plan-optimization (read + validate).

## Validation Artifact Schema

Path: `{analysis_dir}/findings-validation.json`

```json
{
  "schema_version": "1.1",
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
  },
  {
    "id": "F13",
    "anti_pattern": "Sequential Scan",
    "step": "9.7.4",
    "file": "src/handlers/sbom.rs",
    "line": 142,
    "detection_method": "EXPLAIN ANALYZE",
    "evidence_excerpt": "Seq Scan on sbom_packages (actual rows=45000)",
    "checks": { "9.1-B": "PASS", "9.1-B2": "PASS" },
    "disposition": "Confirmed",
    "confidence": "High",
    "severity": "High",
    "timeline": "1-4 hours",
    "reason": "Live EXPLAIN ANALYZE confirms sequential scan on 45K rows",
    "explain_data": {
      "execution_time_ms": 234.5,
      "planning_time_ms": 1.2,
      "bottleneck_type": "seq_scan",
      "table": "sbom_packages",
      "estimated_rows": 1000,
      "actual_rows": 45000,
      "row_mismatch_ratio": 45.0
    }
  }]
}
```

**Schema Version:** `"1.1"`. Readers must accept both `"1.0"` (no `explain_data`) and `"1.1"`.

## Field Rules

| Field | Rule |
|---|---|
| `schema_version` | `"1.0"` or `"1.1"` |
| `validation_run` | Must be `true`. Do not write file if Step 9.1 was not executed |
| `findings[].id` | Unique F1, F2, ... matching Step 9.1-A inventory. Live SQL findings use the same F-sequence (no separate namespace) |
| `findings[].checks` | Both `9.1-B` and `9.1-B2` required for every row. For EXPLAIN-backed findings (step 9.7.4), 9.1-B confirms the query exists at the recorded source location; 9.1-B2 verifies the recommended fix is valid for the framework |
| `findings[].disposition` | Confirmed, Confirmed (Low Confidence), Downgraded, or Discarded |
| `findings[].detection_method` | `"Serena"`, `"Grep"`, `"EXPLAIN ANALYZE"`, or `"EXPLAIN"` |
| `findings[].reason` | Required for all dispositions |
| `findings[].explain_data` | Optional. Required when `step` is `"9.7.4"`. Must be absent for non-EXPLAIN findings. Contains: `execution_time_ms`, `planning_time_ms`, `bottleneck_type`, `table`, `estimated_rows`, `actual_rows`, `row_mismatch_ratio` |

## Disposition ↔ Checks Consistency

| Disposition | Required outcomes |
|---|---|
| Confirmed / Downgraded | `9.1-B: PASS` and `9.1-B2: PASS` |
| Confirmed (Low Confidence) | Both PASS + `confidence` = Low |
| Discarded | At least one starts with `FAILED:` |

## Validation Checklist

Read `findings-validation.json`. All rules must PASS before writing report or creating optimization plan.

### Artifact Rules (A1–A7)

| Rule | Check | FAIL when |
|---|---|---|
| A1 | Artifact exists and parses as JSON | Missing, invalid, or schema_version not in `["1.0", "1.1"]` |
| A2 | `validation_run` is `true` | false or absent |
| A3 | Every row complete | Missing id, disposition, checks, or reason |
| A4 | Dispositions valid | Not in allowed enum |
| A5 | Disposition ↔ checks consistent | Violates consistency table above |
| A6 | Statistics consistent | submitted ≠ len(findings) or counts don't sum |
| A7 | EXPLAIN findings have `explain_data` | `step` is `"9.7.4"` but `explain_data` is missing, OR `explain_data` present but `detection_method` not in `["EXPLAIN ANALYZE", "EXPLAIN"]` |

### Report Crosswalk Rules (R1–R5)

Extract Finding IDs from scannable report regions (Anti-Pattern Analysis through Live SQL Analysis, excluding code fences, Finding Validation Summary, and Executive Summary). The scannable region includes: Anti-Pattern Analysis, Backend Source Code Analysis, Cross-Repository Over-Fetching Analysis, Cross-Layer Computation Waste, Dynamic Performance Testing, and Live SQL Analysis (EXPLAIN ANALYZE).

| Rule | Check | FAIL when |
|---|---|---|
| R1 | Scannable IDs are Confirmed/Downgraded | ID has other disposition |
| R2 | Low Confidence in correct section | Low Confidence ID in scannable regions instead of Candidates for Manual Review |
| R3 | Discarded absent from body | Discarded ID in scannable regions |
| R4 | No orphans | Report ID not in artifact |
| R5 | No ghosts | Confirmed/Downgraded artifact row not in report |

**Blocking:** If any rule is FAIL, fix and re-run.
