 (cd "$(git rev-parse --show-toplevel)" && git apply --3way <<'EOF' 
diff --git a/README.md b/README.md
new file mode 100644
index 0000000000000000000000000000000000000000..44054d78d0184d24b3580a3291e0fab2b73a0e61
--- /dev/null
+++ b/README.md
@@ -0,0 +1,76 @@
+# Buscador de Rimas & Temáticas (Poemas PT)
+
+Aplicação FastAPI + Streamlit para sugerir rimas e temas a partir de poemas em português. Usa TF-IDF para similaridade temática e heurísticas de sufixo/vogais para rimas, com prateleiras de popularidade balanceadas por quantis de views.
+
+## Dataset
+CSV com colunas:
+- `Author`
+- `Title`
+- `Content` (poema completo, com quebras de linha)
+- `Views` (numérico)
+
+Configure o caminho via variável de ambiente `POEMS_CSV_PATH` (default: `data/poems.csv`). Para datasets grandes, baixe no deploy ou use Git LFS e evite carregar tudo no repo.
+
+## Execução da API
+Requisitos: Python 3.11.
+
+```bash
+pip install -r requirements.txt
+export POEMS_CSV_PATH=/caminho/para/poems.csv
+uvicorn app.api:app --host 0.0.0.0 --port 8000 --reload
+```
+
+### Endpoints
+- `GET /health`
+- `POST /search`
+
+Payload de exemplo:
+
+```bash
+curl -X POST http://localhost:8000/search \
+  -H "Content-Type: application/json" \
+  -d '{"text":"No fundo do peito mora um clarão","mode":"ambos","ranking":"balanceado","top_each":4,"total":12}'
+```
+
+Campos:
+- `text`: verso ou poema do usuário (usamos a última linha útil para rima).
+- `mode`: `"rima" | "tema" | "ambos"`.
+- `ranking`: `"popular"` (views), `"relevancia"` (score), `"balanceado"` (prateleiras 80/20).
+- `top_each`: itens por prateleira no modo balanceado (default: 4).
+- `total`: limite final por bloco.
+
+## Execução da UI (Streamlit)
+```bash
+export API_URL=http://localhost:8000
+streamlit run ui/streamlit_app.py
+```
+
+## Notas de implementação e performance
+- O índice é montado em memória em `scripts/build_index.py` usando as chaves `_rk2/_rk3/_rk4/_vtail`, `_tail3` (últimos 3 versos) e normalizações `_norm_poem`.
+- Para datasets grandes, cacheie o TF-IDF (`build_tfidf`) e, se necessário, persista matrizes/artefatos para não reconstruir a cada boot.
+- A classificação por prateleira usa quantis 0.80/0.20 de views e o modo balanceado tenta 4/4/4 com fallback para completar o total solicitado.
+- Não armazene credenciais ou tokens no repositório. Caso use notebooks externos para baixar modelos ou dados (ex.: via `kagglehub`), autentique por variáveis de ambiente ou arquivos locais ignorados no Git (`.env`, `.kaggle/kaggle.json`) e garanta que tais arquivos estejam listados no `.gitignore`.
+
+## Estrutura
+```
+poesia-buscador/
+  app/
+    config.py        # env e limites de ranking
+    data_loader.py   # leitura e tipagem do CSV
+    preprocess.py    # normalização, chaves de rima, utilitários de versos
+    search_rhyme.py  # busca por rima com deduplicação
+    search_theme.py  # TF-IDF + cosseno
+    tiers.py         # prateleiras e balanceamento
+    api.py           # FastAPI
+  ui/
+    streamlit_app.py
+  scripts/
+    build_index.py
+  tests/
+    test_rhyme.py
+    test_theme.py
+  requirements.txt
+  Dockerfile
+  README.md
+  .gitignore
+```
 
EOF
)
