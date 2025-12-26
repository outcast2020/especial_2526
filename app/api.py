diff --git a/app/api.py b/app/api.py
new file mode 100644
index 0000000000000000000000000000000000000000..c80c232789d150e86564b979edb10ff0906234d2
--- /dev/null
+++ b/app/api.py
@@ -0,0 +1,60 @@
+"""API FastAPI para busca de rimas e temas em poemas."""
+from typing import Any, Dict, Literal
+
+from fastapi import FastAPI
+from pydantic import BaseModel
+
+from .config import CANDIDATES_RHYME, CANDIDATES_THEME, N_EACH, Q_BOTTOM, Q_TOP
+from .search_rhyme import search_rhymes
+from .search_theme import build_tfidf, search_theme
+from .tiers import add_views_tier, pick_balanced_with_fallback
+from scripts.build_index import build
+
+app = FastAPI(title="Poesia Buscador API")
+
+df = build()
+vectorizer, X = build_tfidf(df)
+
+
+class SearchReq(BaseModel):
+    text: str
+    mode: Literal["rima", "tema", "ambos"] = "ambos"
+    ranking: Literal["popular", "relevancia", "balanceado"] = "balanceado"
+    top_each: int = N_EACH
+    total: int = 12
+
+
+@app.get("/health")
+def health():
+    return {"ok": True, "rows": len(df)}
+
+
+def finalize(frame, ranking: str, top_each: int, total: int):
+    frame = add_views_tier(frame, q_top=Q_TOP, q_bottom=Q_BOTTOM)
+    if ranking == "balanceado":
+        return pick_balanced_with_fallback(frame, n_each=top_each, total=total)
+    # popular / relevancia: só ordena diferente
+    if ranking == "popular":
+        return frame.sort_values(["views", "score"], ascending=[False, False]).head(total)
+    return frame.sort_values(["score", "views"], ascending=[False, False]).head(total)
+
+
+@app.post("/search")
+def search(req: SearchReq) -> Dict[str, Any]:
+    text = req.text.strip()
+
+    out: Dict[str, Any] = {}
+
+    if req.mode in ("rima", "ambos"):
+        rh = search_rhymes(df, text, topk=CANDIDATES_RHYME, prefer_views=True)
+        if rh is not None and len(rh) > 0:
+            rh = finalize(rh, req.ranking, req.top_each, req.total)
+        out["rima"] = [] if rh is None else rh.to_dict(orient="records")
+
+    if req.mode in ("tema", "ambos"):
+        th = search_theme(df, vectorizer, X, text, topk=CANDIDATES_THEME, prefer_views=True)
+        if th is not None and len(th) > 0:
+            th = finalize(th, req.ranking, req.top_each, req.total)
+        out["tema"] = [] if th is None else th.to_dict(orient="records")
+
+    return out
