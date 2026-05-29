## Criterion 5: Response includes a `threshold_applied` boolean field indicating whether filtering is active

**Result: FAIL**

### Evidence

The diff modifies the `AdvisorySummary` construction in `modules/fundamental/src/advisory/endpoints/get.rs`:

```rust
AdvisorySummary {
    critical: summary.critical,
    high: if threshold_idx <= 1 { summary.high } else { 0 },
    medium: if threshold_idx <= 2 { summary.medium } else { 0 },
    low: if threshold_idx <= 3 { summary.low } else { 0 },
    total: summary.critical + summary.high + summary.medium + summary.low,
}
```

The constructed `AdvisorySummary` contains only the fields: `critical`, `high`, `medium`, `low`, and `total`. There is no `threshold_applied` boolean field anywhere in the diff.

Additionally, looking at the `None` branch:

```rust
None => summary,
```

The unmodified summary is returned directly, which also would not contain a `threshold_applied` field.

The `AdvisorySummary` struct definition (located in `modules/fundamental/src/advisory/model/summary.rs` per the repository structure) is not modified in this diff to add a `threshold_applied` field. No changes to model files appear in the diff at all.

### Expected Behavior

The `AdvisorySummary` struct should include a `threshold_applied: bool` field. When a valid threshold parameter is provided, this should be set to `true`. When no threshold is provided, it should be set to `false`. This allows API consumers to determine whether the returned counts have been filtered.

### Conclusion

The `threshold_applied` boolean field is completely absent from the implementation. Neither the model struct nor the response construction includes this field. The acceptance criterion is not met.
