-- SYNTHETIC TEST DATA — Migration with planted anti-patterns for eval
-- PLANTED ANTI-PATTERN: Step 7.8.3 — Uniform Processing of Partitionable Data
--
-- This migration normalizes license text by expanding LicenseRef- references.
-- The expand_license_expression_with_mappings function is applied to ALL rows,
-- but its early-exit guard shows that rows without 'LicenseRef-' are returned
-- unchanged. The expensive LEFT JOIN + function call could be limited to the
-- minority of rows that actually contain LicenseRef-.

-- PLANTED: Uniform processing — function applied to all rows via UPDATE,
-- but expand_license_expression_with_mappings has an early-exit guard:
--   IF POSITION('LicenseRef-' IN license_text) = 0 THEN RETURN license_text;
-- This means most rows (those without LicenseRef-) pass through unchanged.
-- The expensive LEFT JOIN with licensing_infos is also applied to all rows,
-- even though it is only consumed by the function for LicenseRef- rows.

UPDATE normalized_license nl
SET expanded_text = expand_license_expression_with_mappings(
    nl.original_text,
    COALESCE(lim.license_mapping, ARRAY[]::license_mapping[])
)
FROM (
    SELECT nl2.id, nl2.original_text, nl2.sbom_id
    FROM normalized_license nl2
    WHERE nl2.expanded_text IS NULL
) src
LEFT JOIN (
    SELECT array_agg(ROW(license_id, name)::license_mapping) AS license_mapping, sbom_id
    FROM licensing_infos
    GROUP BY sbom_id
) lim ON lim.sbom_id = src.sbom_id
WHERE nl.id = src.id;
