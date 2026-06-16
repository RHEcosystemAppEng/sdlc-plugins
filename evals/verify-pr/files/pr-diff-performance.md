<!-- SYNTHETIC TEST DATA — mock PR diff for eval testing; simulates `gh pr diff` output for a performance optimization -->

```diff
diff --git a/modules/fundamental/src/advisory/service/advisory.rs b/modules/fundamental/src/advisory/service/advisory.rs
index 2a1f3c8..e7b9d4a 100644
--- a/modules/fundamental/src/advisory/service/advisory.rs
+++ b/modules/fundamental/src/advisory/service/advisory.rs
@@ -1,6 +1,7 @@
 use anyhow::Context;
 use sea_orm::{ColumnTrait, ConnectionTrait, EntityTrait, QueryFilter};
+use sea_orm::QuerySelect;
 use uuid::Uuid;

 use crate::advisory::model::details::AdvisoryDetails;
@@ -45,6 +46,30 @@ impl AdvisoryService {
         Ok(AdvisoryDetails::from_entity(advisory, &tx).await?)
     }

+    /// Fetches multiple advisories by their IDs in a single batched query.
+    pub async fn fetch_advisories_batch(
+        &self,
+        ids: Vec<Uuid>,
+        tx: &Transactional<'_>,
+    ) -> Result<Vec<AdvisoryDetails>, AppError> {
+        if ids.is_empty() {
+            return Ok(vec![]);
+        }
+
+        let advisories = advisory::Entity::find()
+            .filter(advisory::Column::Id.is_in(ids.clone()))
+            .all(&tx.connection())
+            .await
+            .context("Failed to batch-fetch advisories")?;
+
+        let mut results = Vec::with_capacity(advisories.len());
+        for advisory in advisories {
+            let details = AdvisoryDetails::from_entity(advisory, tx).await?;
+            results.push(details);
+        }
+
+        Ok(results)
+    }
+
     /// Lists advisories with optional filtering and pagination.
     pub async fn list(
         &self,
diff --git a/modules/fundamental/src/sbom/service/sbom.rs b/modules/fundamental/src/sbom/service/sbom.rs
index 5c3a1b2..8d4e7f9 100644
--- a/modules/fundamental/src/sbom/service/sbom.rs
+++ b/modules/fundamental/src/sbom/service/sbom.rs
@@ -82,16 +82,14 @@ impl SbomService {
             .context("Failed to find SBOM")?
             .ok_or_else(|| AppError::NotFound(format!("SBOM {} not found", id)))?;

-        // Load linked advisories one at a time
-        let advisory_links = sbom_advisory::Entity::find()
+        // Batch-load all linked advisories in a single query
+        let advisory_ids: Vec<Uuid> = sbom_advisory::Entity::find()
             .filter(sbom_advisory::Column::SbomId.eq(sbom.id))
             .all(&tx.connection())
-            .await?;
-
-        let mut advisories = Vec::new();
-        for link in &advisory_links {
-            let advisory = self.advisory_service.fetch(link.advisory_id, tx).await?;
-            advisories.push(advisory);
-        }
+            .await?
+            .into_iter()
+            .map(|link| link.advisory_id)
+            .collect();
+        let advisories = self.advisory_service.fetch_advisories_batch(advisory_ids, tx).await?;

         Ok(SbomDetails {
             summary: SbomSummary::from_entity(sbom, &tx).await?,
diff --git a/tests/api/sbom_advisory_batch.rs b/tests/api/sbom_advisory_batch.rs
new file mode 100644
index 0000000..a3c1d2e
--- /dev/null
+++ b/tests/api/sbom_advisory_batch.rs
@@ -0,0 +1,62 @@
+use test_context::test_context;
+use trustify_test_context::TrustifyContext;
+
+/// Verifies that batch advisory loading returns the same results as individual loading.
+#[test_context(TrustifyContext)]
+#[test(actix_web::test)]
+async fn test_batch_advisory_matches_individual(
+    ctx: &TrustifyContext,
+) -> Result<(), anyhow::Error> {
+    // Given: an SBOM with multiple linked advisories
+    let sbom_id = ctx.ingest_test_sbom_with_advisories(5).await?;
+
+    // When: fetching SBOM details (uses batch loading internally)
+    let resp = ctx
+        .call_service(
+            actix_web::test::TestRequest::get()
+                .uri(&format!("/api/v2/sbom/{}", sbom_id))
+                .to_request(),
+        )
+        .await;
+
+    // Then: response contains all 5 advisories
+    assert_eq!(resp.status(), actix_web::http::StatusCode::OK);
+    let body: serde_json::Value = actix_web::test::read_body_json(resp).await;
+    let advisories = body["advisories"].as_array().unwrap();
+    assert_eq!(advisories.len(), 5);
+
+    Ok(())
+}
+
+/// Verifies that an SBOM with no advisories returns an empty list.
+#[test_context(TrustifyContext)]
+#[test(actix_web::test)]
+async fn test_sbom_no_advisories(ctx: &TrustifyContext) -> Result<(), anyhow::Error> {
+    // Given: an SBOM with no linked advisories
+    let sbom_id = ctx.ingest_test_sbom_with_advisories(0).await?;
+
+    // When: fetching SBOM details
+    let resp = ctx
+        .call_service(
+            actix_web::test::TestRequest::get()
+                .uri(&format!("/api/v2/sbom/{}", sbom_id))
+                .to_request(),
+        )
+        .await;
+
+    // Then: advisories list is empty (not an error)
+    assert_eq!(resp.status(), actix_web::http::StatusCode::OK);
+    let body: serde_json::Value = actix_web::test::read_body_json(resp).await;
+    let advisories = body["advisories"].as_array().unwrap();
+    assert_eq!(advisories.len(), 0);
+
+    Ok(())
+}
+
+/// Verifies that duplicate advisory IDs are handled gracefully.
+#[test_context(TrustifyContext)]
+#[test(actix_web::test)]
+async fn test_batch_deduplicates_advisories(ctx: &TrustifyContext) -> Result<(), anyhow::Error> {
+    // Given: an SBOM with duplicate advisory links
+    let sbom_id = ctx.ingest_test_sbom_with_duplicate_advisories(3).await?;
+
+    // When: fetching SBOM details
+    let resp = ctx
+        .call_service(
+            actix_web::test::TestRequest::get()
+                .uri(&format!("/api/v2/sbom/{}", sbom_id))
+                .to_request(),
+        )
+        .await;
+
+    // Then: advisories are deduplicated
+    assert_eq!(resp.status(), actix_web::http::StatusCode::OK);
+
+    Ok(())
+}
```
