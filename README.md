# Site do Alma · almaestudosvisuais.com.br

Site estático gerado por `build.py` (Python puro, sem dependências).

- `src/` estilos (`style.css`), script (`site.js`), `config.js` (Supabase + WhatsApp do atelier) e `CNAME`.
- `img/` imagens extraídas do Figma (Alma_Brandbook_2026 › Website - Autolayout).
- `python3 build.py` gera a pasta `site/`; o GitHub Actions faz isso e publica no GitHub Pages a cada push na `main`.

Formulários (WhatsApp, novidades, Faça Parte) gravam na tabela `site_contatos` do Supabase (só inserção pelo público; só a equipe lê).
