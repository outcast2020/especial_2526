"""Interface Streamlit para o buscador de poemas."""
import requests
import streamlit as st

API_URL = st.secrets.get("API_URL", "http://localhost:8000")

st.set_page_config(page_title="Buscador de Poesia", layout="wide")
st.title("Buscador de Rimas & Temáticas (PT)")

text = st.text_area("Cole um verso ou um poema:", height=180)

col1, col2, col3 = st.columns(3)
mode = col1.selectbox("Modo", ["ambos", "rima", "tema"])
ranking = col2.selectbox("Ranking", ["balanceado", "popular", "relevancia"])
top_each = col3.slider("Itens por prateleira (balanceado)", 2, 8, 4)

total = st.slider("Total por bloco", 6, 30, 12)


def render_block(title, items):
    st.subheader(title)
    if not items:
        st.info("Nada encontrado.")
        return

    for it in items:
        tier = it.get("tier", "")
        emoji = {"Tradicionais": "🏛️", "Criativas": "🎨", "Fora da caixa": "🚀"}.get(tier, "")
        st.markdown(f"**{emoji} {tier}** — views={it.get('views')} • score={it.get('score'):.3f}")
        st.code(it.get("preview", ""), language="text")
        st.caption(it.get("citation", ""))
        if it.get("key_used"):
            st.caption(f"rima: {it['key_used']}")
        st.divider()


if st.button("Buscar ideias", type="primary"):
    if not text.strip():
        st.warning("Digite um verso ou poema.")
    else:
        payload = {"text": text, "mode": mode, "ranking": ranking, "top_each": top_each, "total": total}
        res = requests.post(f"{API_URL}/search", json=payload, timeout=60)
        res.raise_for_status()
        data = res.json()

        if "rima" in data:
            render_block("Rimas", data["rima"])
        if "tema" in data:
            render_block("Temáticas", data["tema"])
diff --git a/ui/streamlit_app.py b/ui/streamlit_app.py
new file mode 100644
index 0000000000000000000000000000000000000000..3766a3b995dd39f60ef7ab8fe045d76dc41e1f14
--- /dev/null
+++ b/ui/streamlit_app.py
@@ -0,0 +1,49 @@
+"""Interface Streamlit para o buscador de poemas."""
+import requests
+import streamlit as st
+
+API_URL = st.secrets.get("API_URL", "http://localhost:8000")
+
+st.set_page_config(page_title="Buscador de Poesia", layout="wide")
+st.title("Buscador de Rimas & Temáticas (PT)")
+
+text = st.text_area("Cole um verso ou um poema:", height=180)
+
+col1, col2, col3 = st.columns(3)
+mode = col1.selectbox("Modo", ["ambos", "rima", "tema"])
+ranking = col2.selectbox("Ranking", ["balanceado", "popular", "relevancia"])
+top_each = col3.slider("Itens por prateleira (balanceado)", 2, 8, 4)
+
+total = st.slider("Total por bloco", 6, 30, 12)
+
+
+def render_block(title, items):
+    st.subheader(title)
+    if not items:
+        st.info("Nada encontrado.")
+        return
+
+    for it in items:
+        tier = it.get("tier", "")
+        emoji = {"Tradicionais": "🏛️", "Criativas": "🎨", "Fora da caixa": "🚀"}.get(tier, "")
+        st.markdown(f"**{emoji} {tier}** — views={it.get('views')} • score={it.get('score'):.3f}")
+        st.code(it.get("preview", ""), language="text")
+        st.caption(it.get("citation", ""))
+        if it.get("key_used"):
+            st.caption(f"rima: {it['key_used']}")
+        st.divider()
+
+
+if st.button("Buscar ideias", type="primary"):
+    if not text.strip():
+        st.warning("Digite um verso ou poema.")
+    else:
+        payload = {"text": text, "mode": mode, "ranking": ranking, "top_each": top_each, "total": total}
+        res = requests.post(f"{API_URL}/search", json=payload, timeout=60)
+        res.raise_for_status()
+        data = res.json()
+
+        if "rima" in data:
+            render_block("Rimas", data["rima"])
+        if "tema" in data:
+            render_block("Temáticas", data["tema"])
