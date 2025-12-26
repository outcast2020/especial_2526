diff --git a/app/search_theme.py b/app/search_theme.py
new file mode 100644
index 0000000000000000000000000000000000000000..22f5c4754d794beab3fd511d00dadcc3800dc412
--- /dev/null
+++ b/app/search_theme.py
@@ -0,0 +1,49 @@
+"""Busca temática usando TF-IDF e similaridade por cosseno."""
+import numpy as np
+import pandas as pd
+from sklearn.feature_extraction.text import TfidfVectorizer
+from sklearn.metrics.pairwise import cosine_similarity
+
+from .preprocess import normalize_text
+
+
+def build_tfidf(df: pd.DataFrame):
+    corpus = df["_poem"].tolist()
+    vectorizer = TfidfVectorizer(lowercase=True, max_features=200_000, ngram_range=(1, 2), min_df=2)
+    X = vectorizer.fit_transform(corpus)
+    return vectorizer, X
+
+
+def search_theme(df: pd.DataFrame, vectorizer, X, user_text: str, topk=60, exclude_exact=True, prefer_views=True):
+    qv = vectorizer.transform([user_text])
+    sims = cosine_similarity(qv, X).ravel()
+
+    k = min(len(sims), topk * 20)
+    idx = np.argpartition(-sims, k - 1)[:k]
+    idx = idx[np.argsort(-sims[idx])]
+
+    norm_user = normalize_text(user_text)
+    rows = []
+    seen_norm = set()
+    for i in idx:
+        row = df.iloc[int(i)]
+        if exclude_exact and row["_norm_poem"] == norm_user:
+            continue
+        if row["_norm_poem"] in seen_norm:
+            continue
+        seen_norm.add(row["_norm_poem"])
+        rows.append(
+            {
+                "preview": row["_tail3"],
+                "citation": f"{row['Author']} — {row['Title']}".strip(" —"),
+                "views": int(row["Views"]),
+                "score": float(sims[i]),
+            }
+        )
+        if len(rows) >= topk:
+            break
+
+    out = pd.DataFrame(rows)
+    if prefer_views and len(out) > 0:
+        out = out.sort_values(["score", "views"], ascending=[False, False])
+    return out
