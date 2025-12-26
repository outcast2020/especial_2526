"""Classificação por popularidade e balanceamento."""
import pandas as pd


def add_views_tier(frame: pd.DataFrame, q_top=0.80, q_bottom=0.20) -> pd.DataFrame:
    if frame is None or len(frame) == 0:
        return frame
    f = frame.copy()
    f["views"] = pd.to_numeric(f["views"], errors="coerce").fillna(0)

    hi = f["views"].quantile(q_top)
    lo = f["views"].quantile(q_bottom)

    def tier(v):
        if v >= hi:
            return "Tradicionais"
        if v <= lo:
            return "Fora da caixa"
        return "Criativas"

    f["tier"] = f["views"].map(tier)
    return f


def pick_balanced_with_fallback(frame: pd.DataFrame, n_each=4, total=12) -> pd.DataFrame:
    if frame is None or len(frame) == 0:
        return frame

    tiers = ["Tradicionais", "Criativas", "Fora da caixa"]
    f = frame.copy()
    if "score" not in f.columns:
        f["score"] = 0.0
    if "views" not in f.columns:
        f["views"] = 0

    picks = []
    for t in tiers:
        part = f[f["tier"] == t].copy()
        part = part.sort_values(["score", "views"], ascending=[False, False]).head(n_each)
        picks.append(part)

    base = pd.concat(picks, axis=0) if picks else f.head(0)
    have = set(base.index.tolist())
    need = max(0, total - len(base))

    if need > 0:
        rest = f.drop(index=have, errors="ignore").sort_values(["score", "views"], ascending=[False, False]).head(need)
        out = pd.concat([base, rest], axis=0)
    else:
        out = base

    # ordena por prateleira
    order = {"Tradicionais": 0, "Criativas": 1, "Fora da caixa": 2}
    out["_o"] = out["tier"].map(order).fillna(99)
    out = out.sort_values(["_o", "score", "views"], ascending=[True, False, False]).drop(columns=["_o"])
    return out
