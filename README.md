# Presente de Natal — Itapagipe (Cordel 2.0)

Este repositório é um mini-game em HTML (GitHub Pages) para dedicar poesias como presente.

## Estrutura
- `index.html` — o jogo
- `data/poems.json` — dataset (API estática). Substitua por um JSON maior quando quiser.

## Como publicar no GitHub Pages
1. Crie um repositório no GitHub (ex.: `especial-2526`).
2. Envie estes arquivos para a raiz do repo.
3. Vá em **Settings → Pages**:
   - Source: **Deploy from a branch**
   - Branch: `main` / folder: `/ (root)`
4. Aguarde e acesse:
   - `https://SEU_USUARIO.github.io/SEU_REPO/`

## Como embutir no seu site (iframe)
```html
<iframe
  src="https://SEU_USUARIO.github.io/SEU_REPO/"
  style="width:100%;height:880px;border:0;border-radius:24px;background:#fff;overflow:hidden;"
  loading="lazy"
  allow="clipboard-write"
  title="Presente de Natal na Península de Itapagipe">
</iframe>
```

## Trocar o dataset (API)
Basta substituir `data/poems.json` no repo e fazer commit. O jogo carrega automaticamente.

Formato aceito:
- `{"items":[{...},{...}]}` ou diretamente `[{...},{...}]`

Campos aceitos por poema:
- `texto` / `text` / `poem`
- `titulo` / `title`
- `autor` / `author`
- `tags` (opcional)
