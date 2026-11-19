<!-- SYNTHETIC TEST DATA — mock PR diff for cross-repository review feedback eval testing; simulates `gh pr diff` output -->

```diff
diff --git a/src/pages/advisories/AdvisoryTable.tsx b/src/pages/advisories/AdvisoryTable.tsx
index 3f2a1b4..9c8d7e6 100644
--- a/src/pages/advisories/AdvisoryTable.tsx
+++ b/src/pages/advisories/AdvisoryTable.tsx
@@ -1,5 +1,5 @@
 import React, { useMemo } from "react";
 import { Table, Thead, Tbody, Tr, Th, Td } from "@patternfly/react-table";
 import type { Advisory } from "../../api/advisories";

 interface AdvisoryTableProps {
   advisories: Advisory[];
 }

 export const AdvisoryTable: React.FC<AdvisoryTableProps> = ({ advisories }) => {
-  const rows = advisories;
+  const rows = useMemo(
+    () =>
+      [...advisories].sort((a, b) => {
+        const byDate = b.date.localeCompare(a.date);
+        return byDate !== 0 ? byDate : a.id.localeCompare(b.id);
+      }),
+    [advisories]
+  );
 
   return (
     <Table aria-label="Advisories">
diff --git a/src/pages/advisories/__tests__/AdvisoryTable.sorting.test.tsx b/src/pages/advisories/__tests__/AdvisoryTable.sorting.test.tsx
new file mode 100644
index 0000000..1b2c3d4
--- /dev/null
+++ b/src/pages/advisories/__tests__/AdvisoryTable.sorting.test.tsx
@@ -0,0 +1,34 @@
+import React from "react";
+import { render, screen } from "@testing-library/react";
+import { AdvisoryTable } from "../AdvisoryTable";
+import type { Advisory } from "../../../api/advisories";
+
+const advisory = (id: string, date: string): Advisory => ({
+  id,
+  date,
+  title: `Advisory ${id}`,
+  severity: "high",
+});
+
+describe("AdvisoryTable ordering", () => {
+  it("renders the newest advisory date first", () => {
+    render(
+      <AdvisoryTable
+        advisories={[advisory("A-1", "2026-01-05"), advisory("A-2", "2026-03-01")]}
+      />
+    );
+
+    const rows = screen.getAllByRole("row").slice(1);
+    expect(rows[0]).toHaveTextContent("A-2");
+    expect(rows[1]).toHaveTextContent("A-1");
+  });
+
+  it("tiebreaks equal dates on advisory id", () => {
+    render(
+      <AdvisoryTable
+        advisories={[advisory("A-9", "2026-02-02"), advisory("A-3", "2026-02-02")]}
+      />
+    );
+
+    const rows = screen.getAllByRole("row").slice(1);
+    expect(rows[0]).toHaveTextContent("A-3");
+    expect(rows[1]).toHaveTextContent("A-9");
+  });
+});
```
