#!/usr/bin/env python3
"""Gera o site estático do Alma a partir de modelos simples (sem dependências).
Saída em ./site — é essa pasta que vai para a hospedagem."""
import os, re, shutil, html, json, hashlib

RAIZ = os.path.dirname(os.path.abspath(__file__))
SAIDA = os.path.join(RAIZ, "site")
DOMINIO = "https://almaestudosvisuais.com.br"
LOJA = "https://almamateriaisartisticos.com.br"
APP = "https://app.almaestudosvisuais.com.br"
INSTAGRAM = "https://www.instagram.com/alma.estudosvisuais/"
ENDERECO = "Rua São Paulo, 864, São Caetano do Sul, SP"
MAPA = "https://www.google.com/maps/search/?api=1&query=" + "Rua+S%C3%A3o+Paulo%2C+864%2C+S%C3%A3o+Caetano+do+Sul+-+SP"
EMAIL = "contato@almaestudosvisuais.com.br"
NOME = "Alma Centro de Estudos Visuais"
ANO = 2026
LOGO = open(os.path.join(RAIZ, "img", "logo.svg")).read().strip()
LOGO = LOGO.replace('class="marca"', 'class="logo"').replace('aria-label="Alma"', 'aria-hidden="true"')

# WhatsApp do atelier: lido de src/config.js (só dígitos, com DDI). Vazio = o site não mostra WhatsApp.
_cfg = open(os.path.join(RAIZ, "src", "config.js")).read()
WHATSAPP = (re.search(r'whatsapp:\s*"(\d*)"', _cfg) or [None, ""])[1]

def _v(f):
    """Versão do arquivo (hash do conteúdo): o navegador baixa de novo sempre que o arquivo muda."""
    return hashlib.md5(open(os.path.join(RAIZ, "src", f), "rb").read()).hexdigest()[:8]
V_CSS, V_JS, V_CFG = _v("style.css"), _v("site.js"), _v("config.js")

def fone(n):
    n = n[2:] if n.startswith("55") else n
    return f"({n[:2]}) {n[2:-4]}-{n[-4:]}" if len(n) >= 10 else n

def e(t): return html.escape(t, quote=False)
def a(t): return html.escape(t)

EXTERNO = 'target="_blank" rel="noopener"'
SETA = '<svg class="seta-ext" viewBox="0 0 12 12" fill="none" stroke="currentColor" stroke-width="1.1" aria-hidden="true"><path d="M3 9 9 3M4 3h5v5"/></svg>'
EXT_SR = '<span class="sr"> (abre em outro site)</span>'
MENU = [("sobre.html", "Sobre"), ("nossas-aulas.html", "Nossas aulas"), ("blog.html", "Blog"), ("contato.html", "Contato")]
X = '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.25" aria-hidden="true"><path d="M6 6l12 12M18 6 6 18"/></svg>'
HAMBURGUER = '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.25" aria-hidden="true"><path d="M3 9h18M3 15h18"/></svg>'

# ------------------------------------------------------------------ Moldura
def nav(atual, sobre_foto):
    def item(h, t, cls=""):
        c = f' class="{cls}"' if cls else ""
        cur = ' aria-current="page"' if h == atual else ""
        return f'<a{c} href="{h}"{cur}>{t}</a>'
    itens = "".join(item(h, t) for h, t in MENU) + f'<a class="ext" href="{LOJA}" {EXTERNO}>Loja{SETA}{EXT_SR}</a>'
    tela = "".join(f'<li>{item(h, t, "wrap")}</li>' for h, t in [("index.html", "Início")] + MENU) + f'<li><a class="wrap ext" href="{LOJA}" {EXTERNO}>Loja{SETA}{EXT_SR}</a></li>'
    return f'''<header class="nav wrap{' sobre-foto' if sobre_foto else ''}">
  <a class="marca" href="index.html" aria-label="Alma, página inicial">{LOGO}</a>
  <nav class="menu" aria-label="Principal">{itens}</nav>
  <div class="acoes">
    <a class="link-aluno" href="{APP}" {EXTERNO}>Área do aluno</a>
    <a class="btn btn-nav" href="faca-parte.html">Aula experimental</a>
  </div>
  <button class="abrir" type="button" aria-label="Abrir menu" aria-expanded="false" aria-controls="gaveta"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.25" aria-hidden="true"><path d="M3 6.5h18M3 12h18M3 17.5h18"/></svg></button>
</header>
<div class="menu-tela" id="gaveta" role="dialog" aria-modal="true" aria-label="Menu" aria-hidden="true">
  <div class="menu-tela__topo"><span class="menu-tela__rot wrap"></span>
    <button class="fechar" type="button" data-fechar aria-label="Fechar menu">{X}</button></div>
  <nav aria-label="Menu"><ul class="menu-tela__itens">{tela}</ul></nav>
  <div class="menu-tela__pe wrap">
    <a class="btn btn-claro btn-largo" href="faca-parte.html">Agendar aula experimental</a>
    <div class="menu-tela__links"><a href="{APP}" {EXTERNO}>Área do aluno</a><a href="{INSTAGRAM}" {EXTERNO}>Instagram</a><a href="{MAPA}" {EXTERNO}>Como chegar</a></div>
    <p class="menu-tela__end">Rua São Paulo, 864<br>São Caetano do Sul, SP</p>
  </div>
</div>'''

def fecho(segundo=("Nossas aulas", "nossas-aulas.html")):
    """Chamada final, separada do conteúdo da página: faixa em contraste, sem filete e sem a grade de duas colunas."""
    rot, href = segundo
    return f'''<section class="cta" id="aula-experimental" aria-labelledby="cta-tit">
  <div class="cta__in wrap rev">
    <p class="cta__rot">Aula experimental</p>
    <h2 class="cta__tit" id="cta-tit">*Tudo começa por uma aula.</h2>
    <p class="cta__txt">Desenvolva sua percepção, sua técnica e sua produção artística em um percurso acompanhado de forma individual. *Na aula experimental, você conhece o atelier, a turma e o modo de trabalho antes de decidir.</p>
    <div class="botoes"><a class="btn cta__btn" href="faca-parte.html">Agendar</a><a class="btn btn-linha cta__linha" href="{href}">{rot}</a></div>
  </div>
</section>'''

ZAP_RODAPE = f'<a href="https://wa.me/{WHATSAPP}" {EXTERNO}>WhatsApp {fone(WHATSAPP)}</a>' if WHATSAPP else ''

RODAPE = f'''<footer class="rodape wrap">
  <div class="novidades">
    <h2 class="t3">Novidades do Alma</h2>
    <p class="pequeno">*Workshops, textos novos e a agenda do atelier, direto no seu e-mail.</p>
    <form class="form-linha" data-form="novidades" novalidate>
      <label class="sr" for="mail-n">Seu e-mail</label>
      <input class="campo" id="mail-n" name="email" type="email" autocomplete="email" placeholder="Seu e-mail" required>
      <button class="btn btn-claro" type="submit">Assinar</button>
      <p class="aviso" role="status"></p>
    </form>
  </div>
  <div class="rod-colunas">
    <div>
      <h2 class="rotulo">Atelier</h2>
      <p>Rua São Paulo, 864<br>São Caetano do Sul, SP</p>
      <a href="{MAPA}" {EXTERNO}>Como chegar</a>
    </div>
    <nav aria-label="Site">
      <h2 class="rotulo">Site</h2>
      <a href="index.html">Início</a><a href="sobre.html">Sobre</a><a href="nossas-aulas.html">Nossas aulas</a><a href="blog.html">Blog</a><a href="contato.html">Contato</a><a href="faca-parte.html">Aula experimental</a>
    </nav>
    <nav aria-label="Alunos e loja">
      <h2 class="rotulo">Alunos</h2>
      <a href="{APP}" {EXTERNO}>Área do aluno</a>
      <h2 class="rotulo">Loja</h2>
      <a class="ext" href="{LOJA}" {EXTERNO}>Materiais Artísticos{SETA}{EXT_SR}</a>
      <a href="{LOJA}/policies/shipping-policy" {EXTERNO}>Envio e entrega</a>
      <a href="{LOJA}/policies/terms-of-service" {EXTERNO}>Termos e condições</a>
    </nav>
    <div>
      <h2 class="rotulo">Contato</h2>
      {ZAP_RODAPE}
      <a href="mailto:{EMAIL}">{EMAIL}</a>
      <a href="{INSTAGRAM}" {EXTERNO}>Instagram</a>
    </div>
  </div>
  <div class="rod-base">
    <p>© {ANO} {NOME}</p>
    <p>CNPJ 66.843.784/0001-28</p>
    <a href="privacidade.html">Privacidade</a>
  </div>
</footer>'''

ORG = {
    "@context": "https://schema.org", "@type": "EducationalOrganization", "name": NOME,
    "url": DOMINIO, "email": EMAIL, **({"telephone": "+" + WHATSAPP} if WHATSAPP else {}), "logo": DOMINIO + "/img/apple-touch-icon.png", "sameAs": [INSTAGRAM],
    "address": {"@type": "PostalAddress", "streetAddress": "Rua São Paulo, 864", "addressLocality": "São Caetano do Sul",
                "addressRegion": "SP", "addressCountry": "BR"},
}

PAGINAS_PUBLICAS = []

def pagina(arquivo, titulo, descricao, corpo, fecho_html=None, sobre_foto=False, base=None):
    titulo_doc = f"{NOME} | Atelier de artes em São Caetano do Sul" if arquivo == "index.html" else f"{titulo} | {NOME}"
    ld = f'<script type="application/ld+json">{json.dumps(ORG, ensure_ascii=False)}</script>\n' if arquivo == "index.html" else ""
    url = DOMINIO + "/" + ("" if arquivo == "index.html" else arquivo)
    if base is None: PAGINAS_PUBLICAS.append(url)
    doc = f'''<!doctype html>
<html lang="pt-BR">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
{f'<base href="{base}">' if base else ''}<title>{e(titulo_doc)}</title>
<meta name="description" content="{a(descricao)}">
{'' if base else f'<link rel="canonical" href="{url}">'}
<meta property="og:type" content="website">
<meta property="og:locale" content="pt_BR">
<meta property="og:site_name" content="{NOME}">
<meta property="og:title" content="{a(titulo_doc)}">
<meta property="og:description" content="{a(descricao)}">
<meta property="og:url" content="{url}">
<meta property="og:image" content="{DOMINIO}/img/compartilhar.jpg">
<meta property="og:image:width" content="1200">
<meta property="og:image:height" content="630">
<meta name="twitter:card" content="summary_large_image">
<meta name="theme-color" content="#000000">
<meta name="color-scheme" content="light dark">
<link rel="icon" type="image/png" href="img/favicon-32.png">
<link rel="apple-touch-icon" href="img/apple-touch-icon.png">
<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Host+Grotesk:wght@400;500&display=swap" rel="stylesheet">
<link rel="stylesheet" href="style.css?v={V_CSS}">
{ld}</head>
<body>
<a class="pular" href="#conteudo">Pular para o conteúdo</a>
{nav(arquivo, sobre_foto)}
<main id="conteudo" tabindex="-1">
{corpo}
{fecho() if fecho_html is None else fecho_html}
</main>
{RODAPE}
<script src="config.js?v={V_CFG}"></script>
<script src="site.js?v={V_JS}" defer></script>
</body>
</html>
'''
    open(os.path.join(SAIDA, arquivo), "w").write(doc)

# ------------------------------------------------------------------ Peças
def duas(rotulo, lead, extra="", tag="h2", id_=""):
    """Cabeçalho de bloco: rótulo pequeno sob o filete; frase grande (lead) ao lado; texto e ações em `extra`."""
    return f'''<div class="duas cab rev"><{tag} class="cab__rot"{f' id="{id_}"' if id_ else ''}>{rotulo}</{tag}><div class="lado"><p class="lead">{lead}</p>{extra}</div></div>'''

def corpo(t): return f'<div class="corpo"><p>{t}</p></div>'
def botoes(*bs): return '<div class="botoes">' + "".join(bs) + '</div>'

def abertura(titulo, texto, escura=False):
    return f'''<section class="abertura wrap{' escura' if escura else ''}">
  <div class="duas"><h1 class="t1">{titulo}</h1><div class="lado"><p class="corpo">{texto}</p></div></div>
</section>'''

JOVENS = ("frente-jovens.jpg", "Jovens Artistas", "*Introdução à prática artística e desenvolvimento da percepção visual para crianças e adolescentes, no tempo de aprendizagem de cada idade, estimulando a observação, a criatividade e a construção de repertório.")
WORKSHOPS = ("frente-extensao.jpg", "Extensão", "Leva a prática artística para além do espaço interno do Alma, com atividades abertas e sazonais que ampliam o contato com as Artes Visuais e com a criação.")

FRENTES = [
    ("frente-atelier.jpg", "Atelier", "Formação em estrutura de atelier: o percurso de cada aluno parte de um currículo básico e abre, aos poucos, a percepção para a sua própria Forma.", "nossas-aulas.html", None),
    (JOVENS[0], JOVENS[1], JOVENS[2], "nossas-aulas.html#em-breve", "Em breve"),
    (WORKSHOPS[0], WORKSHOPS[1], WORKSHOPS[2], "nossas-aulas.html#em-breve", "Em breve"),
]

def frentes():
    out, breve = [], []
    for img, t, d, href, selo in FRENTES:
        if selo:
            breve.append(f'''<a class="frente frente--breve rev" href="{href}"><div class="foto"><img src="img/{img}" alt="" loading="lazy"></div>
<div class="frente__corpo"><span class="frente__selo">{selo}</span><h3 class="frente__tit">{t}</h3><p class="frente__txt">{d}</p></div></a>''')
        else:
            out.append(f'''<a class="frente frente--principal rev" href="{href}"><div class="foto"><img src="img/{img}" alt="" loading="lazy"></div>
<div class="frente__corpo"><h3 class="frente__tit">{t}</h3><p class="frente__txt">{d}</p></div></a>''')
    # Jovens Artistas e Extensão ficam só no bloco "Em breve" de Nossas aulas (com o Avise-me)
    return '<div class="frentes frentes--uma">' + "".join(out) + '</div>'

FATOS = [("4 a 9", "pessoas por aula, com acompanhamento individual de cada trabalho"),
         ("6 linhas", "de aprofundamento: aquarela, guache, acrílica, óleo, escultura e gravura"),
         ("2 bases", "Desenho e Plástica: todos começam pelo mesmo currículo básico"),
         ("Sem prazo", "de conclusão: cada aluno permanece o tempo do próprio percurso")]

def fatos():
    return '<dl class="fatos">' + "".join(f'<div class="rev"><dt>{n}</dt><dd>{t}</dd></div>' for n, t in FATOS) + '</dl>'

SETA_E = '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.25" aria-hidden="true"><path d="M15 5l-7 7 7 7"/></svg>'
SETA_D = '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.25" aria-hidden="true"><path d="M9 5l7 7-7 7"/></svg>'
def controles(n, rotulo):
    return f'''<div class="carr-pontos" role="group" aria-label="{rotulo}">''' + "".join(f'<button type="button" class="carr-ponto" aria-label="{i+1} de {n}"{" aria-current=\"true\"" if i == 0 else ""}></button>' for i in range(n)) + '</div>'

TRAB = [("trabalho-1.jpg", 1252, 1600), ("trabalho-2.jpg", 939, 1200), ("trabalho-3.jpg", 1080, 1600)]
TRABALHOS = (f'<div class="carr carr--trab" data-carr><div class="carr__trilho trabalhos">'
    + "".join(f'<figure class="carr__item"><img src="img/{i}" width="{w}" height="{h}" alt="Trabalho de aluno do Alma" decoding="async"></figure>' for i, w, h in TRAB)
    + '</div>' + controles(len(TRAB), "Trabalhos de alunos") + '</div>')

NOTAS = [("nota-valor-tonal.jpg", "Percepção", "2026-08-04", "4 ago 2026", "A construção do valor tonal na pintura a óleo"),
         ("nota-velatura.jpg", "Técnica", "2026-07-28", "28 jul 2026", "Velatura e opacidade: dois modos de construir a cor"),
         ("nota-desenho.jpg", "Processo", "2026-07-15", "15 jul 2026", "O que o Desenho ensina antes da tinta"),
         ("blog-6.jpg", "Materiais", "2026-07-02", "2 jul 2026", "História dos pigmentos e do meio que os carrega"),
         ("blog-4.jpg", "História da arte", "2026-06-18", "18 jun 2026", "<i>Chiaroscuro</i> e o peso construtivo da sombra"),
         ("blog-7.jpg", "Cor", "2026-06-04", "4 jun 2026", "Albers e a interação entre cores vizinhas"),
         ("blog-2.jpg", "Percepção", "2026-05-21", "21 mai 2026", "Movimento e ritmo na percepção da forma"),
         ("blog-3.jpg", "Teoria", "2026-05-07", "7 mai 2026", "Grisaille e a construção do valor tonal"),
         ("blog-8.jpg", "Fotografia", "2026-04-23", "23 abr 2026", "Frontalidade e obliquidade no enquadramento"),
         ("blog-9.jpg", "Cinema", "2026-04-09", "9 abr 2026", "Kepes e a composição em movimento")]

def cartoes_notas():
    cart = lambda img, cat, dt, data, t: f'''<a class="cartao" href="blog.html"><div class="foto"><img src="img/{img}" alt="" loading="lazy"></div>
<p class="meta"><span>{cat}</span><time datetime="{dt}">{data}</time></p><h3 class="t3">*{t}</h3></a>'''
    paginas = [NOTAS[k:k+2] for k in range(0, min(len(NOTAS), 10), 2)]  # celular: 2 textos por página, até 5 páginas
    return ('<div class="carr carr--notas" data-carr><div class="carr__trilho notas">'
        + "".join('<div class="carr__item notas__pag lista-m">' + "".join(cart(*n) for n in pg) + '</div>' for pg in paginas)
        + '</div>' + controles(len(paginas), "Notas e Ensaios") + '</div>')

DIRECAO = duas("Direção pedagógica", "Giancarlo Avantaggiato",
    '<p class="cargo">Artista Plástico e Diretor</p>' + corpo("*Formado em Design de Produto e em Arquitetura e Urbanismo, fez estudos avançados no Atelier José Paulo de Latorre "
          "e integra o coletivo de artistas Matizes."))

def acordeao(itens):
    return '<div class="acordeao">' + "".join(
        f'<details class="rev"><summary>{q}</summary><div class="resp corpo">{r}</div></details>' for q, r in itens) + '</div>'

FAQ = [("Preciso saber desenhar para começar?", "<p>*Não. Todos começam pelo currículo básico de Desenho e Plástica, com ou sem experiência anterior.</p>"),
       ("Para quem são as aulas?", "<p>*As aulas regulares são para adultos, de qualquer idade e em qualquer momento da vida. O programa para crianças e adolescentes, Jovens Artistas, abre em breve.</p>"),
       ("Quanto tempo dura o curso?", "<p>*Não há prazo de conclusão. Depois do currículo básico, cada aluno permanece o tempo que fizer sentido para o próprio percurso. Há alunos com poucos meses de atelier e outros com mais de cinco anos.</p>"),
       ("Quanto custa?", "<p>*As mensalidades começam em R$ 420, conforme a frequência semanal. Os valores completos são apresentados na aula experimental.</p>"),
       ("Como escolho os dias de aula?", "<p>*Você escolhe dias fixos na semana, conforme a frequência do seu plano. O dia da aula experimental é combinado pelo WhatsApp.</p>"),
       ("O que acontece além das aulas?", "<p>*Sessões de modelo vivo, encontros de história da arte, projetos especiais e visitas a exposições.</p>"),
       ("E se eu precisar faltar?", "<p>*Basta desmarcar pelo app com pelo menos 4 horas de antecedência. A falta vira uma reposição, que pode ser usada em qualquer dia com vaga.</p>")]

REFERENCIAS = [("Josef Albers", "A interação da cor e o ensino pela experiência."),
               ("Rudolf Arnheim", "A percepção visual como forma de pensamento."),
               ("James J. Gibson", "A percepção direta e as invariantes do ambiente."),
               ("György Kepes", "A linguagem da visão e o movimento."),
               ("László Moholy-Nagy", "Materiais, sentidos e o curso preliminar da Bauhaus.")]

LOREM1 = "<p>*Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat.</p><p>Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat cupidatat non proident.</p>"

def em_breve():
    def item(img, t, d, chave):
        return f'''<article class="breve__item rev">
      <div class="breve__img"><img src="img/{img}" alt="" loading="lazy"><span class="selo">Em breve</span></div>
      <h3 class="breve__tit">{t}</h3>
      <p class="corpo">{d}</p>
      <form class="form-linha breve__form" data-form="aviso" novalidate>
        <input type="hidden" name="interesse" value="{t}">
        <label class="sr" for="aviso-{chave}">Seu e-mail para saber quando {t} abrir</label>
        <input class="campo" id="aviso-{chave}" name="email" type="email" autocomplete="email" placeholder="Seu e-mail" required>
        <button class="btn" type="submit">Avise-me</button>
        <p class="aviso" role="status"></p>
      </form>
    </article>'''
    return f'''<section class="bloco wrap" id="em-breve">
  {duas("Em breve", "*Jovens Artistas e Extensão estão em preparação.", corpo("*Deixe seu e-mail e avisamos quando as inscrições abrirem."))}
  <div class="breve apos">
    {item(*JOVENS, "jovens")}
    {item(*WORKSHOPS, "workshops")}
  </div>
</section>'''

# ------------------------------------------------------------------ Páginas
def build():
    if os.path.exists(SAIDA): shutil.rmtree(SAIDA)
    os.makedirs(SAIDA)
    PAGINAS_PUBLICAS.clear()
    shutil.copytree(os.path.join(RAIZ, "img"), os.path.join(SAIDA, "img"))
    for f in ("style.css", "site.js", "config.js", "CNAME"):
        p = os.path.join(RAIZ, "src", f)
        if os.path.exists(p): shutil.copy(p, SAIDA)

    # Início
    pagina("index.html", "Início",
      "Centro de Estudos Visuais em São Caetano do Sul. Atelier de Desenho, Plástica, pintura, escultura e gravura para adultos.",
      f'''<section class="hero wrap">
  <img src="img/hero-inicio.jpg" alt="Estudantes trabalhando em esculturas num atelier" fetchpriority="high">
  <div class="chamada">
    <div class="chamada__txt"><h1 class="t1">Da Ideia à Forma.<br>No seu Ritmo.</h1></div>
    <div class="botoes"><a class="btn btn-claro" href="faca-parte.html">Aula experimental</a><a class="btn btn-linha" href="nossas-aulas.html">Nossas aulas</a></div>
  </div>
</section>
<section class="bloco escuro wrap">
  {duas("Quem somos", "*Três frentes, um pensamento.",
        corpo("Somos um Centro de Estudos Visuais dedicado à formação, à pesquisa e à experimentação em Artes Visuais. Tratamos a percepção como forma ativa de compreensão do mundo e trabalhamos em três frentes: o Atelier, espaço de trabalho e formação do pensamento artístico; Jovens Artistas, iniciação da percepção visual para crianças e adolescentes; e a Extensão, que leva a prática visual para além do Atelier.")
        + botoes('<a class="btn btn-claro" href="sobre.html">Sobre o Alma</a>'))}
  <div class="apos">{frentes()}</div>
</section>
<section class="bloco tom wrap">
  {duas("Trabalhos de alunos", "*Estudos e trabalhos feitos no atelier, em diferentes técnicas e momentos do percurso.")}
  <div class="apos">{TRABALHOS}</div>
</section>
<section class="bloco wrap">
  {duas("Notas e Ensaios", "*Notas e ensaios sobre ver, fazer e pensar a imagem.", corpo("Reunimos reflexões que atravessam a prática do atelier e ampliam o olhar sobre a Arte.") + botoes('<a class="btn" href="blog.html">Todos os textos</a>'))}
  <div class="apos">{cartoes_notas()}</div>
</section>
<section class="bloco tom wrap">
  {duas("Materiais Artísticos", "Curadoria de materiais artísticos feita a partir da prática de atelier.",
        corpo("O Alma Materiais Artísticos reúne uma seleção de meios abrasivos e fluidos, papéis, pincéis e instrumentos escolhidos criteriosamente por sua qualidade técnica, consistência de uso e adequação ao trabalho de artistas, estudantes e processos manuais.")
        + botoes(f'<a class="btn btn-ext" href="{LOJA}" {EXTERNO}>Visitar a loja{SETA}{EXT_SR}</a>'))}
  <a class="larga apos rev" href="{LOJA}" {EXTERNO} aria-label="Visitar a loja de materiais"><picture><source media="(max-width: 749px)" srcset="img/loja-m.jpg"><img src="img/loja.jpg" alt="Parede de pincéis, trinchas e utensílios de pintura em uma loja de materiais artísticos" loading="lazy"></picture></a>
</section>''', sobre_foto=True)

    # Sobre
    pagina("sobre.html", "Sobre",
      "O ver tem gramática, e essa gramática se ensina. O manifesto e a história do Alma.",
      f'''<section class="video-sec" aria-label="Vídeo institucional">
  <figure class="video">
    <!-- Quando o vídeo estiver pronto, trocar o quadro por <video controls playsinline poster="(foto de capa)"><source src="..."></video> ou pelo player do Vimeo/YouTube -->
    <div class="video__quadro" role="img" aria-label="Espaço do vídeo institucional do Alma, em produção">
    </div>
    <h1 class="t1 video__tit wrap">Sobre o Alma</h1>
  </figure>
</section>
<section class="abertura escura wrap sobre-intro"><p class="lead">Toda forma que vemos é resultado de uma operação: distribuição de luz, organização de valores, articulação de espaços positivos e negativos no campo. O olho constrói a imagem que recebe. O Alma forma o domínio dessa construção em três frentes, que partem da mesma convicção: a percepção visual como forma de compreensão do mundo.</p></section>
<section class="bloco wrap" id="manifesto">
  <div class="duas cab rev"><h2 class="cab__rot">Manifesto</h2><div class="lado"><div class="corpo">{LOREM1}</div></div></div>
</section>
<section class="bloco tom wrap" id="historia">
  <div class="duas cab rev"><h2 class="cab__rot">Nossa história</h2><div class="lado"><div class="corpo">{LOREM1}</div></div></div>
</section>
<section class="bloco wrap" id="direcao">{DIRECAO}</section>''')

    # Nossas aulas
    BASES = [("blog-8.jpg", "Desenho", "Grafite, carvão, sanguínea e nanquim. Estudo de proporção, valor tonal, construção do espaço e articulação de cheios e vazios no campo."),
             ("hero-inicio.jpg", "Plástica", "Gesso, madeira, plastilina e argila. Estudo do volume, do peso e da relação entre matéria e forma no espaço tridimensional.")]
    MEIOS = ["Aquarela", "Guache", "Acrílica", "Óleo", "Escultura", "Gravura"]
    PERCURSO = [("Aula experimental", "Você conhece o atelier e a turma numa primeira aula orientada."),
                ("Currículo básico", "Desenho e Plástica. O mesmo começo para todos, com ou sem experiência."),
                ("Seu meio", "Concluído o currículo básico, você escolhe o meio em que quer se aprofundar."),
                ("Própria luz", "Sem prazo de conclusão. O trabalho segue até encontrar a sua linguagem.")]
    PRINCIPIOS = [("Percepção", "*Percepção é a operação pela qual a mente organiza o mundo sensível em estruturas reconhecíveis: direções, formas, relações, tensões. Ela realiza no nível dos sentidos o que o raciocínio realiza no nível do pensamento, e já é, em si, uma forma de inteligência."),
                  ("Formação do pensamento", "Ver é compreender. O pensamento se forma dentro da atividade perceptiva: ao organizar o que se vê, constrói repertório e passa a orientar como a pessoa relaciona parte e todo, reconhece padrão em meio à complexidade e julga tensão e equilíbrio em qualquer experiência, visual ou não."),
                  ("Técnica e processo", "A técnica se desenvolve de acordo com cada material e é o meio que conduz o artista da ideia à forma. Ela se ensina como caminho de descoberta, que ganha sentido quando se funde à criação de cada aluno."),
                  ("Composição", "*Composição é a organização das partes de uma obra em relação ao todo, como um sistema de tensões, proporções e direções: a construção de uma unidade que dá corpo visível a um sentido.")]
    NO_ATELIER = [("Turma", "Até 8 pessoas por aula, cada uma no seu projeto"), ("Acompanhamento", "Individual, em cada trabalho"),
                  ("Horários", "Noites durante a semana e tardes de sábado")]
    pagina("nossas-aulas.html", "Nossas aulas",
      "Como funcionam as aulas do Alma: o percurso a partir do Desenho, as técnicas do atelier e o dia a dia das turmas.",
      f'''<section class="ab-foto wrap">
  <img src="img/frente-atelier.jpg" alt="Alunos trabalhando lado a lado num atelier" fetchpriority="high">
  <div class="ab-foto__txt">
    <h1 class="t1 ab-foto__tit">Nossas aulas</h1>
    <p class="ab-foto__sub">*Um atelier de formação para adultos, com turmas pequenas e acompanhamento individual.</p>
  </div>
</section>
<section class="frase wrap">
  <p class="frase__txt rev">*Todo aluno começa pelo Desenho e pela Plástica. A partir deles, cada um encontra o seu meio e, com o tempo, a <em>própria luz</em>.</p>
</section>
<section class="bloco tom wrap" id="percurso">
  {duas("O percurso", "*Quatro etapas, da primeira aula à linguagem própria.", corpo("O percurso começa por uma base comum, em que os alunos abordam os fundamentos, e é a partir dela que cada um é conduzido ao aprofundamento da própria prática."))}
  <ol class="percurso apos">{"".join(f'<li class="rev"><span class="percurso__n" aria-hidden="true">{i+1}</span><div><h3 class="t3">{t}</h3><p class="texto-cartao">*{d}</p></div></li>' for i, (t, d) in enumerate(PERCURSO))}</ol>
</section>
<section class="bloco escuro wrap" id="formacao">
  {duas("Formação", "*Duas disciplinas de base e, a partir delas, linguagens de aprofundamento.", corpo("*A formação básica segue quatro princípios, nesta ordem: a percepção visual, base de todo o trabalho; o Desenho, que estrutura o espaço; a luz, que dá plasticidade à forma; e a composição, que dá unidade ao trabalho."))}
  <div class="bases apos">{"".join(f'<article class="base rev"><div class="base__img"><img src="img/{img}" alt="" loading="lazy"></div><h3 class="base__tit">{t}</h3><p class="texto-cartao">*{d}</p></article>' for img, t, d in BASES)}</div>
  <div class="duas cab continua">
    <div class="rev"><h3 class="base__tit continua__tit">Formação contínua</h3><p class="texto-cartao continua__txt">*A abordagem de materiais é extensa e voltada à expressão de cada aluno, respeitando as características próprias de cada meio. Concluído o ciclo básico, o aluno segue pelo material que mais deseja explorar.</p></div>
    <ul class="meios meios--lista lado">{"".join(f'<li class="rev">{m}</li>' for m in MEIOS)}</ul>
  </div>
</section>
<section class="bloco wrap" id="no-atelier">
  {duas("No atelier", "*Um grupo único, com pessoas em momentos diferentes do percurso. Boa parte do aprendizado nasce dessa convivência.", corpo("Composto por diferentes artistas, o Alma promove um ambiente de aprendizado horizontal: a mesma turma reúne alunos em materiais, meios e estágios diferentes, e cada percurso segue a sua própria lógica de desenvolvimento. Nesse espaço, a singularidade de cada um se nutre da comunidade."))}
  <div class="dividido apos">
    <div class="dividido__img rev"><img src="img/nota-desenho.jpg" alt="Estudo feito no atelier" loading="lazy"></div>
    <dl class="ficha dividido__txt">{"".join(f'<div class="rev"><dt>{n}</dt><dd>*{t}</dd></div>' for n, t in NO_ATELIER)}</dl>
  </div>
</section>
<section class="bloco tom wrap" id="trabalhos">
  {duas("Trabalhos de alunos", "*Estudos e trabalhos feitos no atelier.")}
  <div class="apos">{TRABALHOS}</div>
</section>
<section class="bloco wrap" id="principios">
  {duas("Sobre o ensino", "*Quatro ideias que guiam o trabalho em sala.")}
  <ul class="principios principios--4 apos">{"".join(f'<li class="rev"><p class="principios__t">{t}</p><p class="corpo">{d}</p></li>' for t, d in PRINCIPIOS)}</ul>
</section>
<section class="bloco tom wrap" id="faq">
  {duas("Perguntas frequentes", "*O que mais nos perguntam antes da primeira aula.", (f'<p class="pequeno">Outras dúvidas: <a href="https://wa.me/{WHATSAPP}" {EXTERNO}>WhatsApp {fone(WHATSAPP)}</a> ou <a href="mailto:{EMAIL}">{EMAIL}</a></p>' if WHATSAPP else f'<p class="pequeno">Outras dúvidas: <a href="mailto:{EMAIL}">{EMAIL}</a></p>'))}
  <div class="apos">{acordeao(FAQ)}</div>
</section>
{em_breve()}''', fecho_html=fecho(("Contato", "contato.html")))

    # Blog
    POSTS = [("blog-1.jpg", "Materiais", "História dos pigmentos e do meio que os carrega", "Pigmento é matéria seca e inerte. O meio que o carrega decide o brilho, a secagem e a permanência da cor."),
             ("blog-2.jpg", "Percepção", "Movimento e ritmo na percepção da forma", "A mesa permanece retangular enquanto você caminha ao redor dela. A forma resiste à mudança de aparência."),
             ("blog-3.jpg", "Teoria", "Grisaille e a construção do valor tonal", "A chave tonal se estabelece antes da primeira mistura: o valor decide de onde vem a luz e o que fica na sombra."),
             ("blog-4.jpg", "História da arte", "<i>Chiaroscuro</i> e o peso construtivo da sombra", "Em Caravaggio, a sombra ganha peso construtivo e passa a sustentar a figura com a mesma força do claro."),
             ("blog-5.jpg", "Prática", "Velatura e a cor que nasce da luz refletida", "Camada transparente sobre camada seca. A cor nasce da luz que atravessa a película e volta refletida."),
             ("blog-6.jpg", "Pensamento", "<i>Pentimento</i> e a memória do próprio processo", "O traço que a decisão anterior deixa visível na superfície. A obra guarda a memória do próprio processo."),
             ("blog-7.jpg", "Cor", "Albers e a interação entre cores vizinhas", "Nenhuma cor é vista isolada. O tom muda conforme a vizinhança, e é essa comparação que a prática exercita."),
             ("blog-8.jpg", "Fotografia", "Frontalidade e obliquidade no enquadramento", "A posição da câmera diante do plano decide antes da luz: a frontalidade organiza, a obliquidade abre profundidade."),
             ("blog-9.jpg", "Cinema", "Kepes e a composição em movimento", "O movimento como condição da vida moderna, e a disciplina formal diante da novidade.")]
    TAGS = [t for t in dict.fromkeys(p[1] for p in POSTS)]
    pagina("blog.html", "Notas e Ensaios",
      "Notas e Ensaios do Alma: textos sobre percepção visual, processos de criação, técnica e história da arte.",
      abertura("Notas e Ensaios", "Notas e ensaios sobre percepção visual, processos de criação, técnica, história da arte e pensamento artístico. Reunimos reflexões que atravessam a prática do atelier e ampliam o olhar sobre a Arte.") + f'''
<section class="bloco wrap" id="ultimas">
  <div class="duas cab rev"><h2 class="cab__rot">Últimas publicações</h2><div class="lado"></div></div>
  <div class="destaques apos">
    {"".join(f'''<a class="destaque{" destaque--1" if k == 0 else ""} rev" href="#todos"><div class="foto"><img src="img/{img}" alt="" loading="lazy"></div><div class="destaque__txt"><p class="meta"><span>{cat}</span><time datetime="{dt}">{data}</time></p><h3 class="{"destaque__tit" if k == 0 else "t3"}">*{t}</h3></div></a>''' for k, (img, cat, dt, data, t) in enumerate(NOTAS[:3]))}
  </div>
</section>
<section class="bloco tom wrap" id="todos">
  <div class="duas cab rev"><h2 class="cab__rot">Todos os textos</h2><div class="lado"></div></div>
  <div class="filtros rev apos">
    <label class="busca" for="q"><span class="sr">Buscar textos</span><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5" aria-hidden="true"><circle cx="10.5" cy="10.5" r="6.5"/><path d="m15.5 15.5 5 5"/></svg>
      <input id="q" type="search" placeholder="Buscar textos" autocomplete="off"></label>
    <label class="tema-m"><span class="sr">Tema</span><select id="tema">{"".join(f'<option value="{v}">{t}</option>' for v, t in [("", "Todos os temas")] + [(t, t) for t in TAGS])}</select></label>
    <div class="tags" role="group" aria-label="Filtrar por tema"><button type="button" aria-pressed="true" data-tag="">Todos</button>{"".join(f'<button type="button" aria-pressed="false" data-tag="{t}">{t}</button>' for t in TAGS)}</div>
  </div>
  <p class="contagem pequeno" data-total="{len(POSTS)}" aria-live="polite">{len(POSTS)} textos publicados</p>
  <div class="posts">''' + "".join(
        f'''<article class="post rev" data-tag="{tag}"><div class="foto"><img src="img/{img}" alt="" loading="lazy"></div>
<p class="meta"><span>{tag}</span></p><h3 class="t3">*{t}</h3><p class="texto-cartao">*{d}</p></article>''' for img, tag, t, d in POSTS) + '''</div>
  <p class="vazio corpo" hidden>Nenhum texto encontrado. Tente outro termo ou outro tema.</p>
</section>''')

    # Aula experimental
    INTERESSES = ["Ainda não sei", "Desenho", "Pintura (aquarela, guache, acrílica, óleo)", "Escultura", "Gravura", "Outra"]
    pagina("faca-parte.html", "Aula experimental",
      "Agende uma aula experimental no Alma Centro de Estudos Visuais, em São Caetano do Sul.",
      abertura("Aula experimental", "*A entrada no Alma começa por uma aula experimental. Deixe seu contato e combinamos pelo WhatsApp o dia da sua visita ao atelier.") + f'''
<section class="bloco wrap">
  <div class="duas">
    <div class="rev">
      <h2 class="cab__rot">Como funciona</h2>
      <ol class="passos-curtos">
        <li><span class="passos-curtos__n" aria-hidden="true">1</span><div><h3 class="t3">Combinamos o dia</h3><p class="texto-cartao">*Respondemos pelo WhatsApp com os dias disponíveis.</p></div></li>
        <li><span class="passos-curtos__n" aria-hidden="true">2</span><div><h3 class="t3">Você vem ao atelier</h3><p class="texto-cartao">*Faz uma aula com a turma, com orientação individual.</p></div></li>
        <li><span class="passos-curtos__n" aria-hidden="true">3</span><div><h3 class="t3">Você decide</h3><p class="texto-cartao">*Se quiser continuar, combinamos seus dias fixos e a matrícula.</p></div></li>
      </ol>
    </div>
    <form class="formulario lado rev" data-form="candidatura" novalidate>
      <label>Nome<input name="nome" autocomplete="name" required></label>
      <label>WhatsApp<input name="whatsapp" type="tel" inputmode="tel" autocomplete="tel" placeholder="(11) 90000-0000" required></label>
      <label><span>E-mail <span class="opcional">opcional</span></span><input name="email" type="email" autocomplete="email"></label>
      <label>Técnica de interesse<select name="interesse">{"".join(f'<option>{t}</option>' for t in INTERESSES)}</select></label>
      <label><span>Conte um pouco sobre você <span class="opcional">opcional</span></span><textarea name="mensagem" rows="4" placeholder="Sua experiência com arte, o que procura, período de preferência"></textarea></label>
      <p class="pequeno">Usamos seus dados apenas para combinar a aula experimental. <a href="privacidade.html">Privacidade</a></p>
      <button class="btn btn-largo" type="submit">Enviar pedido</button>
      <p class="aviso" role="status"></p>
      {f'<p class="pequeno form-alt">Prefere conversar direto? <a href="https://wa.me/{WHATSAPP}" {EXTERNO}>Chame no WhatsApp</a></p>' if WHATSAPP else ''}
    </form>
  </div>
</section>''', fecho_html="")

    # Contato
    zap = (f'''<div><dt class="t3">WhatsApp</dt><dd class="corpo">{fone(WHATSAPP)}, *para aula experimental e dúvidas sobre o atelier.</dd>
        <dd><a class="btn" href="https://wa.me/{WHATSAPP}" {EXTERNO}>Conversar no WhatsApp</a></dd></div>''' if WHATSAPP else "")
    pagina("contato.html", "Contato",
      "Endereço, e-mail e redes do Alma Centro de Estudos Visuais, em São Caetano do Sul.",
      abertura("Contato", "*O Alma fica em São Caetano do Sul, no ABC Paulista. Visitas ao atelier são agendadas previamente.") + f'''
<section class="bloco wrap">
  <div class="duas">
    <dl class="contatos rev">
      {zap}
      <div><dt class="t3">E-mail</dt><dd class="corpo"><a href="mailto:{EMAIL}">{EMAIL}</a></dd></div>
      <div><dt class="t3">Instagram</dt><dd class="corpo"><a href="{INSTAGRAM}" {EXTERNO}>@alma.estudosvisuais</a></dd></div>
    </dl>
    <div class="endereco lado rev">
      <p class="endereco__rot">Atelier</p>
      <p class="endereco__txt">Rua São Paulo, 864<br>São Caetano do Sul, SP</p>
      <div class="endereco__apps">
        <a class="ext" href="{MAPA}" {EXTERNO}>Google Maps{SETA}{EXT_SR}</a>
        <a class="ext" href="https://maps.apple.com/?q=Alma%20Centro%20de%20Estudos%20Visuais&address=Rua%20S%C3%A3o%20Paulo%2C%20864%2C%20S%C3%A3o%20Caetano%20do%20Sul%20-%20SP" {EXTERNO}>Apple Maps{SETA}{EXT_SR}</a>
        <a class="ext" href="https://waze.com/ul?q=Rua%20S%C3%A3o%20Paulo%20864%20S%C3%A3o%20Caetano%20do%20Sul&navigate=yes" {EXTERNO}>Waze{SETA}{EXT_SR}</a>
      </div>
    </div>
  </div>
</section>
<section class="bloco tom wrap">
  {duas("Parcerias", "*Formação visual com escolas, instituições e coletivos.",
        corpo("*Residências, oficinas fechadas, curadoria de material para turmas e projetos de extensão.")
        + botoes(f'<a class="btn" href="mailto:{EMAIL}?subject=Parcerias">Propor parceria</a>'))}
</section>''')

    # 404 (servida em qualquer endereço: caminhos a partir da raiz)
    TELA = '''<svg class="tela404" viewBox="0 0 600 420" fill="none" stroke="currentColor" aria-hidden="true">
  <g stroke-width="1" opacity=".35"><path d="M0 250H600"/><path d="M300 250 40 420M300 250 560 420M300 250 150 420M300 250 450 420"/></g>
  <rect class="tela404__quadro" x="170" y="40" width="260" height="300" stroke-width="1.5"/>
  <g class="tela404__linhas" stroke-width="1" opacity=".6"><path d="M170 40 430 340M430 40 170 340M300 40V340M170 190H430"/></g>
  <circle cx="300" cy="250" r="3" fill="currentColor" stroke="none"/>
</svg>'''
    pagina("404.html", "Página não encontrada", "Página não encontrada.",
      f'''<section class="nao-achei wrap">
  <div class="nao-achei__arte">{TELA}<span class="nao-achei__num">404</span></div>
  <div class="nao-achei__txt">
    <h1 class="t1">Fora do enquadramento.</h1>
    <p class="corpo">*Esta página não existe ou mudou de lugar. O ponto de fuga continua o mesmo: volte ao início ou conheça as aulas do atelier.</p>
    <div class="botoes"><a class="btn btn-claro" href="index.html">Início</a><a class="btn btn-linha" href="nossas-aulas.html">Nossas aulas</a></div>
  </div>
</section>''', fecho_html="", base="/")

    # Privacidade
    pagina("privacidade.html", "Privacidade",
      "Como o Alma Centro de Estudos Visuais trata os dados enviados pelo site.",
      abertura("Privacidade", "*Como tratamos os dados que você envia pelo site. Última atualização: outubro de 2026.") + f'''
<section class="bloco wrap">
  <div class="duas cab">
    <h2 class="cab__rot">Política de privacidade</h2>
    <div class="lado"><div class="corpo texto-longo">
      <h3>Quem trata os dados</h3>
      <p>{NOME}, CNPJ 66.843.784/0001-28, Rua São Paulo, 864, São Caetano do Sul, SP. Contato: <a href="mailto:{EMAIL}">{EMAIL}</a>.</p>
      <h3>O que coletamos</h3>
      <p>Apenas o que você escreve nos formulários: nome, WhatsApp, e-mail, a linguagem de interesse e a mensagem opcional, no pedido de aula experimental; e o e-mail, na inscrição de novidades e nos avisos de novas turmas.</p>
      <p>Também registramos visitas de forma anônima: a página vista, o site de origem e se o acesso foi por celular ou computador. Não usamos cookies, não identificamos quem visita e não compartilhamos esses dados com plataformas de publicidade.</p>
      <h3>Para que usamos</h3>
      <p>Para responder ao seu pedido, combinar a aula experimental, enviar as novidades que você pediu e entender quais páginas do site são mais úteis. Não vendemos nem cedemos seus dados.</p>
      <h3>Onde ficam e por quanto tempo</h3>
      <p>Os dados ficam em um banco de dados com acesso restrito à equipe do Alma. Pedidos de contato são guardados enquanto forem necessários para o atendimento, e o e-mail de novidades, até você pedir a remoção.</p>
      <h3>Seus direitos</h3>
      <p>Pela Lei Geral de Proteção de Dados (Lei 13.709/2018), você pode pedir acesso, correção ou exclusão dos seus dados e cancelar o envio de novidades a qualquer momento. Basta escrever para <a href="mailto:{EMAIL}">{EMAIL}</a>.</p>
    </div></div>
  </div>
</section>''', fecho_html="")

    # Mapa do site
    open(os.path.join(SAIDA, "sitemap.xml"), "w").write(
        '<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
        + "".join(f"  <url><loc>{u}</loc></url>\n" for u in PAGINAS_PUBLICAS) + "</urlset>\n")

    print("ok:", sorted(os.listdir(SAIDA)))

if __name__ == "__main__":
    build()
