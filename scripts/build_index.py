"""Script de preparação de índices de rima e TF-IDF."""
from app.data_loader import load_df
from app.preprocess import last_k_lines, last_nonempty_line, last_word, normalize_text, rhyme_key, vowel_tail_key


def build():
    df = load_df()
    df["_poem"] = df["Content"].astype(str)
    df["_norm_poem"] = df["_poem"].map(normalize_text)

    df["_last_line"] = df["_poem"].map(last_nonempty_line)
    df["_last_word"] = df["_last_line"].map(last_word)

    df["_rk2"] = df["_last_word"].map(lambda w: rhyme_key(w, 2))
    df["_rk3"] = df["_last_word"].map(lambda w: rhyme_key(w, 3))
    df["_rk4"] = df["_last_word"].map(lambda w: rhyme_key(w, 4))
    df["_vtail"] = df["_last_word"].map(vowel_tail_key)

    df["_tail3"] = df["_poem"].map(lambda p: last_k_lines(p, k=3))
    return df


def main() -> None:
    df = build()
    print(df[["Author", "Title", "Views", "_last_word", "_rk3", "_vtail"]].head(5))
    print("OK. Rows:", len(df))


if __name__ == "__main__":
    main()
