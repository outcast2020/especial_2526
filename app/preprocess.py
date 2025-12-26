"""Pré-processamento de textos e utilidades de rima."""
import re
import unicodedata

VOWELS = set("aeiou")


def strip_accents(s: str) -> str:
    s = unicodedata.normalize("NFD", s)
    return "".join(ch for ch in s if unicodedata.category(ch) != "Mn")


def normalize_text(s: str) -> str:
    s = str(s).lower().strip()
    s = strip_accents(s)
    s = re.sub(r"[^a-z0-9\\s\\-]", " ", s)
    s = re.sub(r"\\s+", " ", s).strip()
    return s


def last_nonempty_line(poem: str) -> str:
    lines = [ln.strip() for ln in str(poem).splitlines()]
    lines = [ln for ln in lines if ln]
    return lines[-1] if lines else ""


def last_word(line: str) -> str:
    t = normalize_text(line).replace("-", " ")
    parts = t.split()
    return parts[-1] if parts else ""


def rhyme_key(word: str, n=3) -> str:
    w = normalize_text(word).replace(" ", "")
    if not w:
        return ""
    return w[-n:] if len(w) >= n else w


def vowel_tail_key(word: str) -> str:
    w = normalize_text(word).replace(" ", "")
    if not w:
        return ""
    i = len(w) - 1
    while i >= 0 and w[i] not in VOWELS:
        i -= 1
    if i < 0:
        return w[-3:] if len(w) >= 3 else w
    return w[i:]


def last_k_lines(poem: str, k=3) -> str:
    lines = [ln.rstrip() for ln in str(poem).splitlines()]
    lines = [ln for ln in lines if ln.strip()]
    tail = lines[-k:] if len(lines) >= k else lines
    return "\\n".join(tail)


def user_last_line_and_word(user_text: str):
    ll = last_nonempty_line(user_text)
    return ll, last_word(ll)
diff --git a/app/preprocess.py b/app/preprocess.py
new file mode 100644
index 0000000000000000000000000000000000000000..07b75da9459462447b92ad3b6720d6ceee3e22ff
--- /dev/null
+++ b/app/preprocess.py
@@ -0,0 +1,61 @@
+"""Pré-processamento de textos e utilidades de rima."""
+import re
+import unicodedata
+
+VOWELS = set("aeiou")
+
+
+def strip_accents(s: str) -> str:
+    s = unicodedata.normalize("NFD", s)
+    return "".join(ch for ch in s if unicodedata.category(ch) != "Mn")
+
+
+def normalize_text(s: str) -> str:
+    s = str(s).lower().strip()
+    s = strip_accents(s)
+    s = re.sub(r"[^a-z0-9\\s\\-]", " ", s)
+    s = re.sub(r"\\s+", " ", s).strip()
+    return s
+
+
+def last_nonempty_line(poem: str) -> str:
+    lines = [ln.strip() for ln in str(poem).splitlines()]
+    lines = [ln for ln in lines if ln]
+    return lines[-1] if lines else ""
+
+
+def last_word(line: str) -> str:
+    t = normalize_text(line).replace("-", " ")
+    parts = t.split()
+    return parts[-1] if parts else ""
+
+
+def rhyme_key(word: str, n=3) -> str:
+    w = normalize_text(word).replace(" ", "")
+    if not w:
+        return ""
+    return w[-n:] if len(w) >= n else w
+
+
+def vowel_tail_key(word: str) -> str:
+    w = normalize_text(word).replace(" ", "")
+    if not w:
+        return ""
+    i = len(w) - 1
+    while i >= 0 and w[i] not in VOWELS:
+        i -= 1
+    if i < 0:
+        return w[-3:] if len(w) >= 3 else w
+    return w[i:]
+
+
+def last_k_lines(poem: str, k=3) -> str:
+    lines = [ln.rstrip() for ln in str(poem).splitlines()]
+    lines = [ln for ln in lines if ln.strip()]
+    tail = lines[-k:] if len(lines) >= k else lines
+    return "\\n".join(tail)
+
+
+def user_last_line_and_word(user_text: str):
+    ll = last_nonempty_line(user_text)
+    return ll, last_word(ll)
