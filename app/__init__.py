 (cd "$(git rev-parse --show-toplevel)" && git apply --3way <<'EOF' 
diff --git a/app/__init__.py b/app/__init__.py
new file mode 100644
index 0000000000000000000000000000000000000000..b73627d0d6a9dc5129a8677d6a8917046240197f
--- /dev/null
+++ b/app/__init__.py
@@ -0,0 +1 @@
+"""Inicialização do módulo de aplicação do buscador de poemas."""
 
EOF
)
