"""Busca de rimas baseada em heurísticas de sufixo."""
import pandas as pd

from .preprocess import normalize_text, rhyme_key, user_last_line_and_word, vowel_tail_key


def citation(author: str, title: str) -> str:
    a = (author or "").strip()
    t = (title or "").strip()
    if a and t:
        return f"{a} — {t}"
    return a or t or "(sem autor/título)"


def search_rhymes(df: pd.DataFrame, user_text: str, topk=60, prefer_views=True, exclude_exact=True) -> pd.DataFrame:
    _, lw = user_last_line_and_word(user_text)
    if not lw:
        return pd.DataFrame(columns=["preview", "citation", "views", "score", "key_used"])

    keys = [
        ("rk3", rhyme_key(lw, 3)),
        ("vtail", vowel_tail_key(lw)),
        ("rk4", rhyme_key(lw, 4)),
        ("rk2", rhyme_key(lw, 2)),
    ]

    results = []
    seen_idx = set()
    seen_norm = set()
    norm_user = normalize_text(user_text)

    for keyname, keyval in keys:
        if not keyval:
            continue
        col = f"_{keyname}" if keyname != "vtail" else "_vtail"
        cand = df[df[col] == keyval].copy()

        if exclude_exact:
            cand = cand[cand["_norm_poem"] != norm_user]

        base = {"rk4": 1.00, "rk3": 0.90, "vtail": 0.75, "rk2": 0.60}.get(keyname, 0.50)

        if prefer_views and len(cand) > 0:
            v = cand["Views"].to_numpy(dtype=float)
            v_norm = (v - v.min()) / (v.max() - v.min() + 1e-9)
            cand["_vnorm"] = v_norm
            cand = cand.sort_values(["_vnorm"], ascending=False)
        else:
            cand["_vnorm"] = 0.0

        for idx, row in cand.head(500).iterrows():
            norm_poem = row["_norm_poem"]
            if idx in seen_idx or norm_poem in seen_norm:
                continue
            seen_idx.add(idx)
            seen_norm.add(norm_poem)

            score = base + 0.15 * float(row["_vnorm"])
            results.append(
                {
                    "preview": row["_tail3"],  # últimos 3 versos
                    "citation": citation(row["Author"], row["Title"]),
                    "views": int(row["Views"]),
                    "score": float(score),
                    "key_used": f"{keyname}:{keyval}",
                }
            )

        if len(results) >= topk:
            break

    out = pd.DataFrame(results).sort_values(["score", "views"], ascending=False).head(topk)
    return out
