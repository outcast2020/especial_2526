diff --git a/app/data_loader.py b/app/data_loader.py
new file mode 100644
index 0000000000000000000000000000000000000000..095d16f09e7ba449efb7e14061c70eb1e04c56c5
--- /dev/null
+++ b/app/data_loader.py
@@ -0,0 +1,14 @@
+"""Funções de carregamento e validação do dataset de poemas."""
+import pandas as pd
+
+from .config import DATA_PATH
+
+
+def load_df() -> pd.DataFrame:
+    df = pd.read_csv(DATA_PATH)
+    df["Content"] = df["Content"].astype(str)
+    df["Author"] = df["Author"].astype(str)
+    df["Title"] = df["Title"].astype(str)
+    df["Views"] = pd.to_numeric(df["Views"], errors="coerce").fillna(0)
+    df = df.dropna(subset=["Content"]).reset_index(drop=True)
+    return df
