#!/usr/bin/env python3
"""Gera o site estático do Alma a partir de modelos simples (sem dependências).
Saída em ./site — é essa pasta que vai para a hospedagem."""
import os, re, shutil, html, json

RAIZ = os.path.dirname(os.path.abspath(__file__))
SAIDA = os.path.join(RAIZ, "site")
DOMINIO = "https://almaestudosvisuais.com.br"
LOJA = "https://almamateriaisartisticos.com.br"
APP = "https://app.almaestudosvisuais.com.br"
INSTAGRAM = "https://www.instagram.com/almaestudosvisuais/"
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

def fone(n):
    n = n[2:] if n.startswith("55") else n
    return f"({n[:2]}) {n[2:-4]}-{n[-4:]}" if len(n) >= 10 else n

def e(t): return html.escape(t, quote=False)
def a(t): return html.escape(t)

EXTERNO = 'target="_blank" rel="noopener"'
MENU = [("sobre.html", "Sobre"), ("nossas-aulas.html", "Nossas aulas"), ("blog.html", "Blog"), ("contato.html", "Contato")]
X = '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.25" aria-hidden="true"><path d="M6 6l12 12M18 6 6 18"/></svg>'
HAMBURGUER = '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.25" aria-hidden="true"><path d="M3 9h18M3 15h18"/></svg>'

# ------------------------------------------------------------------ Moldura
def nav(atual, sobre_foto):
    def item(h, t, cls=""):
        c = f' class="{cls}"' if cls else ""
        cur = ' aria-current="page"' if h == atual else ""
        return f'<a{c} href="{h}"{cur}>{t}</a>'
    itens = "".join(item(h, t) for h, t in MENU) + f'<a href="{LOJA}" {EXTERNO}>Loja</a>'
    tela = "".join(f'<li>{item(h, t, "wrap")}</li>' for h, t in MENU) + f'<li><a class="wrap" href="{LOJA}" {EXTERNO}>Loja</a></li>'
    return f'''<header class="nav wrap{' sobre-foto' if sobre_foto else ''}">
  <a class="marca" href="index.html" aria-label="Alma, página inicial">{LOGO}</a>
  <nav class="menu" aria-label="Principal">{itens}</nav>
  <div class="acoes">
    <a class="link-aluno" href="{APP}" {EXTERNO}>Área do aluno</a>
    <a class="btn btn-nav" href="faca-parte.html">Aula experimental</a>
  </div>
  <button class="abrir" type="button" aria-label="Abrir menu" aria-expanded="false" aria-controls="gaveta">{HAMBURGUER}</button>
</header>
<div class="menu-tela" id="gaveta" role="dialog" aria-modal="true" aria-label="Menu" aria-hidden="true">
  <div class="menu-tela__topo"><span class="menu-tela__rot wrap">Menu</span>
    <button class="fechar" type="button" data-fechar aria-label="Fechar menu">{X}</button></div>
  <nav aria-label="Menu"><ul class="menu-tela__itens">{tela}</ul></nav>
  <div class="menu-tela__pe wrap">
    <a class="btn btn-claro btn-largo" href="faca-parte.html">Agendar aula experimental</a>
    <div class="menu-tela__links"><a href="{APP}" {EXTERNO}>Área do aluno</a><a href="{INSTAGRAM}" {EXTERNO}>Instagram</a><a href="{MAPA}" {EXTERNO}>Como chegar</a></div>
    <p class="menu-tela__end">Rua São Paulo, 864<br>São Caetano do Sul, SP</p>
  </div>
</div>'''

def fecho(segundo=("Nossas aulas", "nossas-aulas.html")):
    rot, href = segundo
    return f'''<section class="bloco fecho wrap" id="aula-experimental">
  <div class="duas cab rev">
    <h2 class="cab__rot">Aula experimental</h2>
    <div class="lado">
      <p class="lead">Tudo começa por uma aula.</p>
      <p class="corpo">Você conhece o atelier, a turma e o modo de trabalho antes de decidir.</p>
      <div class="botoes"><a class="btn" href="faca-parte.html">Agendar</a><a class="btn btn-linha" href="{href}">{rot}</a></div>
    </div>
  </div>
</section>'''

RODAPE = f'''<footer class="rodape wrap">
  <div class="novidades">
    <h2 class="t3">Novidades do Alma</h2>
    <p class="pequeno">Workshops, textos novos e a agenda do atelier, direto no seu e-mail.</p>
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
      <a href="sobre.html">Sobre</a><a href="nossas-aulas.html">Nossas aulas</a><a href="blog.html">Blog</a><a href="contato.html">Contato</a><a href="faca-parte.html">Aula experimental</a>
    </nav>
    <nav aria-label="Alunos e loja">
      <h2 class="rotulo">Alunos</h2>
      <a href="{APP}" {EXTERNO}>Área do aluno</a>
      <h2 class="rotulo">Loja</h2>
      <a href="{LOJA}" {EXTERNO}>Materiais Artísticos</a>
      <a href="{LOJA}/policies/shipping-policy" {EXTERNO}>Envio e entrega</a>
      <a href="{LOJA}/policies/terms-of-service" {EXTERNO}>Termos e condições</a>
    </nav>
    <div>
      <h2 class="rotulo">Contato</h2>
      <a href="mailto:{EMAIL}">{EMAIL}</a>
      <a href="{INSTAGRAM}" {EXTERNO}>Instagram</a>
    </div>
  </div>
  <div class="rod-base">
    <p>© {ANO} {NOME}</p>
    <p>CNPJ 66.843.784/0001-28</p>
  </div>
</footer>'''

ORG = {
    "@context": "https://schema.org", "@type": "EducationalOrganization", "name": NOME,
    "url": DOMINIO, "email": EMAIL, "logo": DOMINIO + "/img/apple-touch-icon.png", "sameAs": [INSTAGRAM],
    "address": {"@type": "PostalAddress", "streetAddress": "Rua São Paulo, 864", "addressLocality": "São Caetano do Sul",
                "addressRegion": "SP", "addressCountry": "BR"},
}

PAGINAS_PUBLICAS = []

def pagina(arquivo, titulo, descricao, corpo, fecho_html=None, sobre_foto=False, base=None):
    titulo_doc = NOME if arquivo == "index.html" else f"{titulo} | {NOME}"
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
<meta property="og:image" content="{DOMINIO}/img/hero-inicio.jpg">
<meta name="twitter:card" content="summary_large_image">
<meta name="theme-color" content="#000000">
<link rel="icon" type="image/png" href="img/favicon-32.png">
<link rel="apple-touch-icon" href="img/apple-touch-icon.png">
<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Host+Grotesk:wght@400;500&display=swap" rel="stylesheet">
<link rel="stylesheet" href="style.css">
{ld}</head>
<body>
{nav(arquivo, sobre_foto)}
<main>
{corpo}
{fecho() if fecho_html is None else fecho_html}
</main>
{RODAPE}
<script src="config.js"></script>
<script src="site.js" defer></script>
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

JOVENS = ("frente-jovens.jpg", "Jovens Artistas", "Iniciação à prática artística e à percepção visual para crianças e adolescentes, no tempo de cada idade.")
WORKSHOPS = ("frente-extensao.jpg", "Workshops", "Encontros abertos e de curta duração, com inscrição avulsa, para estudar uma técnica ou um tema sem matrícula.")

FRENTES = [
    ("frente-atelier.jpg", "Atelier", "Formação para adultos: o ciclo básico de Desenho e, depois dele, o percurso de cada aluno na técnica que escolher.", "nossas-aulas.html", None),
    (JOVENS[0], JOVENS[1], JOVENS[2], "nossas-aulas.html#em-breve", "Em breve"),
    (WORKSHOPS[0], WORKSHOPS[1], WORKSHOPS[2], "nossas-aulas.html#em-breve", "Em breve"),
]

def frentes():
    out = []
    for img, t, d, href, selo in FRENTES:
        s = f'<span class="selo">{selo}</span>' if selo else ""
        out.append(f'''<a class="frente rev" href="{href}"><div class="foto"><img src="img/{img}" alt="" loading="lazy">{s}</div>
<h3 class="t3">{t}</h3><p class="texto-cartao">{d}</p></a>''')
    return '<div class="tres carrossel">' + "".join(out) + '</div>'

FATOS = [("4 a 9", "pessoas por aula, com acompanhamento individual de cada trabalho"),
         ("5 técnicas", "na mesma sala: Desenho, pintura a óleo, aquarela, escultura e gravura"),
         ("Desenho", "como base: todos começam pelo ciclo básico de luz, valor e composição"),
         ("Sem prazo", "de conclusão: cada aluno permanece o tempo do próprio percurso")]

def fatos():
    return '<dl class="fatos">' + "".join(f'<div class="rev"><dt>{n}</dt><dd>{t}</dd></div>' for n, t in FATOS) + '</dl>'

TRABALHOS = '''<div class="tres trabalhos carrossel">
    <figure class="rev"><img src="img/trabalho-1.jpg" alt="Trabalho de aluno do Alma" loading="lazy"></figure>
    <figure class="rev"><img src="img/trabalho-2.jpg" alt="Trabalho de aluno do Alma" loading="lazy"></figure>
    <figure class="rev"><img src="img/trabalho-3.jpg" alt="Trabalho de aluno do Alma" loading="lazy"></figure>
  </div>'''

NOTAS = [("nota-valor-tonal.jpg", "Percepção", "2026-08-04", "4 ago 2026", "A construção do valor tonal na pintura a óleo"),
         ("nota-velatura.jpg", "Técnica", "2026-07-28", "28 jul 2026", "Velatura e opacidade: dois modos de construir a cor"),
         ("nota-desenho.jpg", "Processo", "2026-07-15", "15 jul 2026", "O que o Desenho ensina antes da tinta")]

def cartoes_notas():
    return '<div class="tres carrossel">' + "".join(
        f'''<a class="cartao rev" href="blog.html"><div class="foto"><img src="img/{img}" alt="" loading="lazy"></div>
<p class="meta"><span>{cat}</span><time datetime="{dt}">{data}</time></p><h3 class="t3">{t}</h3></a>''' for img, cat, dt, data, t in NOTAS) + '</div>'

DIRECAO = duas("Direção pedagógica", "Giancarlo Avantaggiato, pintor a óleo e escultor, fundador do Alma.",
    corpo("Formado em Design de Produto e em Arquitetura e Urbanismo, fez estudos avançados no Atelier José Paulo de Latorre "
          "e integra o coletivo de artistas Matizes."))

def acordeao(itens):
    return '<div class="acordeao">' + "".join(
        f'<details class="rev"><summary>{q}</summary><div class="resp corpo">{r}</div></details>' for q, r in itens) + '</div>'

FAQ = [("Preciso saber desenhar para começar?", "<p>Não. Todos começam pelo ciclo básico de Desenho, com ou sem experiência anterior.</p>"),
       ("Para quem são as aulas?", "<p>As aulas regulares são para adultos, de qualquer idade e em qualquer momento da vida. O programa para crianças e adolescentes, Jovens Artistas, abre em breve.</p>"),
       ("Quanto tempo dura o curso?", "<p>Não há prazo de conclusão. Depois do ciclo básico, cada aluno permanece o tempo que fizer sentido para o próprio percurso. Há alunos com poucos meses de atelier e outros com mais de cinco anos.</p>"),
       ("E se eu precisar faltar?", "<p>Basta desmarcar pelo app com pelo menos 4 horas de antecedência. A falta vira uma reposição, que pode ser usada em qualquer dia com vaga.</p>")]

REFERENCIAS = [("Josef Albers", "A interação da cor e o ensino pela experiência."),
               ("Rudolf Arnheim", "A percepção visual como forma de pensamento."),
               ("James J. Gibson", "A percepção direta e as invariantes do ambiente."),
               ("György Kepes", "A linguagem da visão e o movimento."),
               ("László Moholy-Nagy", "Materiais, sentidos e o curso preliminar da Bauhaus.")]

LOREM1 = "<p>Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat.</p><p>Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat cupidatat non proident.</p>"

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
  {duas("Em breve", "Duas novas frentes estão em preparação.", corpo("Deixe seu e-mail e avisamos quando as inscrições abrirem."))}
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
      "Centro de Estudos Visuais em São Caetano do Sul. Atelier de Desenho, pintura a óleo, aquarela, escultura e gravura para adultos.",
      f'''<section class="hero wrap">
  <img src="img/hero-inicio.jpg" alt="Estudantes trabalhando em esculturas num atelier" fetchpriority="high">
  <div class="chamada">
    <h1 class="t1">Da Ideia à Forma.<br>No seu Ritmo.</h1>
    <div class="botoes"><a class="btn btn-claro" href="nossas-aulas.html">Nossas aulas</a><a class="btn btn-linha" href="faca-parte.html">Aula experimental</a></div>
  </div>
</section>
<section class="bloco escuro wrap">
  {duas("O Alma", "Três frentes, um pensamento.",
        corpo("Somos um Centro de Estudos Visuais dedicado à formação, à pesquisa e à experimentação em Artes Visuais. Tratamos a percepção como forma ativa de compreensão do mundo, e é desse princípio que partem as três frentes do Alma.")
        + botoes('<a class="btn btn-claro" href="sobre.html">Sobre o Alma</a>'))}
  <div class="apos">{frentes()}</div>
</section>
<section class="bloco wrap">
  {duas("O atelier", "Turmas pequenas, um começo comum e o tempo de cada um.",
        corpo("A formação acontece em estrutura de atelier, na convivência entre estudantes de diferentes idades, repertórios e níveis de experiência. Cada percurso começa pelo mesmo currículo básico e se abre, aos poucos, para a linguagem de cada um.")
        + botoes('<a class="btn" href="nossas-aulas.html#percurso">Como funciona</a>'))}
  <div class="apos">{fatos()}</div>
</section>
<section class="bloco tom wrap">
  {duas("Trabalhos de alunos", "Estudos e trabalhos feitos no atelier, em diferentes técnicas e momentos do percurso.")}
  <div class="apos">{TRABALHOS}</div>
</section>
<section class="bloco wrap">
  {duas("Notas e Ensaios", "Textos sobre ver, fazer e pensar a imagem.", botoes('<a class="btn" href="blog.html">Ver todos</a>'))}
  <div class="apos">{cartoes_notas()}</div>
</section>
<section class="bloco tom wrap">
  {duas("Materiais Artísticos", "Os materiais que usamos no atelier, escolhidos pela prática.",
        corpo("Papéis, pincéis, tintas e instrumentos selecionados pela qualidade técnica e pela consistência de uso.")
        + botoes(f'<a class="btn" href="{LOJA}" {EXTERNO}>Visitar a loja</a>'))}
  <a class="larga apos rev" href="{LOJA}" {EXTERNO} aria-label="Visitar a loja de materiais"><img src="img/loja.jpg" alt="Pintura de natureza-morta com frascos e potes de tinta" loading="lazy"></a>
</section>''', sobre_foto=True)

    # Sobre
    pagina("sobre.html", "Sobre",
      "O ver tem gramática, e essa gramática se ensina. O manifesto, a história e as referências do Alma.",
      abertura("Sobre o Alma", "Toda forma que vemos é resultado de uma operação: distribuição de luz, organização de valores, articulação de cheios e vazios no campo. O olho constrói a imagem que recebe. O Alma ensina o domínio dessa construção a partir de uma convicção: o ver tem gramática, e essa gramática se ensina.", escura=True) + f'''
<div class="larga"><img src="img/sobre-bauhaus.jpg" alt="Fotografia do edifício da Bauhaus em Dessau, com anotações manuscritas" loading="lazy"></div>
<section class="bloco wrap" id="manifesto">
  <div class="duas cab rev"><h2 class="cab__rot">Manifesto</h2><div class="lado"><div class="corpo">{LOREM1}</div></div></div>
</section>
<section class="bloco tom wrap" id="historia">
  <div class="duas cab rev"><h2 class="cab__rot">Nossa história</h2><div class="lado"><div class="corpo">{LOREM1}</div></div></div>
</section>
<section class="bloco wrap" id="referencias">
  {duas("Referências", "A tradição da Bauhaus e os autores que estudaram a percepção como conhecimento.")}
  <ul class="lista-ref apos">{"".join(f'<li class="rev"><span class="t3">{n}</span><span class="corpo">{d}</span></li>' for n, d in REFERENCIAS)}</ul>
</section>
<section class="bloco tom wrap" id="direcao">{DIRECAO}</section>''')

    # Nossas aulas
    TECNICAS = [("blog-3.jpg", "Desenho", "A base de tudo: luz, valor, proporção e composição."),
                ("blog-6.jpg", "Pintura a óleo", "Camadas, velaturas e a construção da cor pela luz."),
                ("blog-5.jpg", "Aquarela", "Transparência, água e a decisão de cada mancha."),
                ("hero-inicio.jpg", "Escultura", "A forma no espaço, do volume ao detalhe."),
                ("blog-2.jpg", "Gravura", "Matriz, traço e a lógica da impressão.")]
    PERCURSO = [("Aula experimental", "Você conhece o atelier e a turma numa primeira aula orientada."),
                ("Ciclo básico de Desenho", "Luz, valor e composição. O mesmo começo para todos, com ou sem experiência."),
                ("A sua técnica", "Concluído o ciclo, você segue na técnica que escolher."),
                ("A própria luz", "Sem prazo de conclusão. O trabalho segue até encontrar a sua linguagem.")]
    PRINCIPIOS = [("Ver se aprende.", "O progresso vem do trabalho contínuo e acompanhado."),
                  ("O Desenho é o fundamento.", "É nele que se aprende a ver, e é a ele que todas as técnicas voltam."),
                  ("Técnica e sensibilidade andam juntas.", "A técnica é o meio pelo qual a intenção ganha forma.")]
    NO_ATELIER = [("Turma", "4 a 9 pessoas, cada uma no seu projeto"), ("Acompanhamento", "Individual, em cada trabalho"),
                  ("Frequência", "Dias fixos na semana, escolhidos por você"), ("Faltas", "Reposição pelo app, avisando até 4 horas antes"),
                  ("Além das aulas", "Modelo vivo, história da arte, projetos especiais e visitas a exposições")]
    pagina("nossas-aulas.html", "Nossas aulas",
      "Como funcionam as aulas do Alma: o percurso a partir do Desenho, as técnicas do atelier e o dia a dia das turmas.",
      f'''<section class="ab-foto wrap">
  <img src="img/frente-atelier.jpg" alt="Alunos trabalhando lado a lado num atelier" fetchpriority="high">
  <div class="ab-foto__txt">
    <h1 class="t1 ab-foto__tit">Nossas aulas</h1>
    <p class="ab-foto__sub">Um atelier de formação para adultos, com turmas pequenas e acompanhamento individual.</p>
  </div>
  <nav class="indice" aria-label="Nesta página"><a href="#percurso">O percurso</a><a href="#tecnicas">Técnicas</a><a href="#no-atelier">No atelier</a><a href="#faq">Perguntas</a></nav>
</section>
<section class="frase wrap">
  <p class="frase__txt rev">Todo aluno começa pelo Desenho. A partir dele, cada um encontra a sua técnica e, com o tempo, a <em>própria luz</em>.</p>
</section>
<section class="bloco tom wrap" id="percurso">
  {duas("O percurso", "Um começo comum e, depois dele, um caminho individual.")}
  <ol class="percurso apos">{"".join(f'<li class="rev"><span class="percurso__n" aria-hidden="true">{i+1}</span><div><h3 class="t3">{t}</h3><p class="texto-cartao">{d}</p></div></li>' for i, (t, d) in enumerate(PERCURSO))}</ol>
</section>
<section class="bloco wrap" id="tecnicas">
  {duas("Técnicas", "Cinco linguagens dividem a mesma sala, e cada aluno trabalha na sua.")}
  <ul class="tecnicas apos">{"".join(f'<li class="tecnica rev"><div class="tecnica__img"><img src="img/{img}" alt="" loading="lazy"></div><div class="tecnica__txt"><h3 class="tecnica__nome">{t}</h3><p class="texto-cartao">{d}</p></div></li>' for img, t, d in TECNICAS)}</ul>
</section>
<section class="bloco escuro wrap" id="no-atelier">
  {duas("No atelier", "Um grupo único, com pessoas em momentos diferentes do percurso. Boa parte do aprendizado nasce dessa convivência.")}
  <div class="dividido apos">
    <div class="dividido__img rev"><img src="img/blog-8.jpg" alt="Estudo de Desenho feito no atelier" loading="lazy"></div>
    <dl class="ficha dividido__txt">{"".join(f'<div class="rev"><dt>{n}</dt><dd>{t}</dd></div>' for n, t in NO_ATELIER)}</dl>
  </div>
</section>
<section class="bloco wrap" id="principios">
  {duas("O que buscamos", "Três ideias que guiam o trabalho em sala.")}
  <ul class="principios apos">{"".join(f'<li class="rev"><p class="principios__t">{t}</p><p class="texto-cartao">{d}</p></li>' for t, d in PRINCIPIOS)}</ul>
</section>
<section class="bloco tom wrap" id="trabalhos">
  {duas("Trabalhos de alunos", "Estudos e trabalhos feitos no atelier.")}
  <div class="apos">{TRABALHOS}</div>
</section>
{em_breve()}
<section class="bloco tom wrap" id="faq">
  {duas("Perguntas frequentes", "O que mais nos perguntam antes da primeira aula.", f'<p class="pequeno">Outras dúvidas: <a href="mailto:{EMAIL}">{EMAIL}</a></p>')}
  <div class="apos">{acordeao(FAQ)}</div>
</section>''', fecho_html=fecho(("Contato", "contato.html")))

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
      abertura("Notas e Ensaios", "Textos sobre percepção visual, processos de criação, técnica e história da arte, escritos a partir da prática do atelier.") + f'''
<section class="bloco wrap">
  <div class="filtros rev">
    <label class="busca" for="q"><span class="sr">Buscar textos</span><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5" aria-hidden="true"><circle cx="10.5" cy="10.5" r="6.5"/><path d="m15.5 15.5 5 5"/></svg>
      <input id="q" type="search" placeholder="Buscar textos" autocomplete="off"></label>
    <div class="tags" role="group" aria-label="Filtrar por tema"><button type="button" aria-pressed="true" data-tag="">Todos</button>{"".join(f'<button type="button" aria-pressed="false" data-tag="{t}">{t}</button>' for t in TAGS)}</div>
  </div>
  <p class="contagem pequeno" data-total="{len(POSTS)}" aria-live="polite">{len(POSTS)} textos publicados</p>
  <div class="posts">''' + "".join(
        f'''<article class="post rev" data-tag="{tag}"><div class="foto"><img src="img/{img}" alt="" loading="lazy"></div>
<p class="meta"><span>{tag}</span></p><h3 class="t3">{t}</h3><p class="texto-cartao">{d}</p></article>''' for img, tag, t, d in POSTS) + '''</div>
  <p class="vazio corpo" hidden>Nenhum texto encontrado. Tente outro termo ou outro tema.</p>
</section>''')

    # Aula experimental
    INTERESSES = ["Ainda não sei", "Desenho", "Pintura a óleo", "Aquarela", "Escultura", "Gravura"]
    pagina("faca-parte.html", "Aula experimental",
      "Agende uma aula experimental no Alma Centro de Estudos Visuais, em São Caetano do Sul.",
      abertura("Aula experimental", "A entrada no Alma começa por uma aula experimental. Deixe seu contato e combinamos pelo WhatsApp o dia da sua visita ao atelier.") + f'''
<section class="bloco wrap">
  <div class="duas">
    <div class="rev">
      <h2 class="cab__rot">Como funciona</h2>
      <ol class="passos-curtos">
        <li><span class="passos-curtos__n" aria-hidden="true">1</span><div><h3 class="t3">Combinamos o dia</h3><p class="texto-cartao">Respondemos pelo WhatsApp com os dias disponíveis.</p></div></li>
        <li><span class="passos-curtos__n" aria-hidden="true">2</span><div><h3 class="t3">Você vem ao atelier</h3><p class="texto-cartao">Faz uma aula com a turma, com orientação individual.</p></div></li>
        <li><span class="passos-curtos__n" aria-hidden="true">3</span><div><h3 class="t3">Você decide</h3><p class="texto-cartao">Se quiser continuar, combinamos seus dias fixos e a matrícula.</p></div></li>
      </ol>
    </div>
    <form class="formulario lado rev" data-form="candidatura" novalidate>
      <label>Nome<input name="nome" autocomplete="name" required></label>
      <label>WhatsApp<input name="whatsapp" type="tel" inputmode="tel" autocomplete="tel" placeholder="(11) 90000-0000" required></label>
      <label><span>E-mail <span class="opcional">opcional</span></span><input name="email" type="email" autocomplete="email"></label>
      <label>Técnica de interesse<select name="interesse">{"".join(f'<option>{t}</option>' for t in INTERESSES)}</select></label>
      <label><span>Conte um pouco sobre você <span class="opcional">opcional</span></span><textarea name="mensagem" rows="4" placeholder="Sua experiência com arte, o que procura, dias de preferência"></textarea></label>
      <p class="pequeno">Usamos seus dados apenas para combinar a aula experimental.</p>
      <button class="btn btn-largo" type="submit">Enviar pedido</button>
      <p class="aviso" role="status"></p>
    </form>
  </div>
</section>''', fecho_html="")

    # Contato
    zap = (f'''<div><dt class="t3">WhatsApp</dt><dd class="corpo">{fone(WHATSAPP)}, para aula experimental e dúvidas sobre o atelier.</dd>
        <dd><a class="btn btn-linha-escura" href="https://wa.me/{WHATSAPP}" {EXTERNO}>Conversar</a></dd></div>''' if WHATSAPP else "")
    pagina("contato.html", "Contato",
      "Endereço, e-mail e redes do Alma Centro de Estudos Visuais, em São Caetano do Sul.",
      abertura("Contato", "O Alma fica em São Caetano do Sul, no ABC Paulista. Visitas ao atelier são agendadas previamente.") + f'''
<section class="bloco wrap">
  <div class="duas">
    <dl class="contatos rev">
      <div><dt class="t3">Endereço</dt><dd class="corpo">Rua São Paulo, 864<br>São Caetano do Sul, SP<br>Entrada pelo portão lateral.</dd>
        <dd><a class="btn btn-linha-escura" href="{MAPA}" {EXTERNO}>Abrir no mapa</a></dd></div>
      {zap}
      <div><dt class="t3">E-mail</dt><dd class="corpo"><a href="mailto:{EMAIL}">{EMAIL}</a></dd></div>
      <div><dt class="t3">Instagram</dt><dd class="corpo"><a href="{INSTAGRAM}" {EXTERNO}>@almaestudosvisuais</a></dd></div>
    </dl>
    <iframe class="mapa lado rev" title="Mapa: {ENDERECO}" loading="lazy" referrerpolicy="no-referrer-when-downgrade"
      src="https://www.google.com/maps?q=Rua%20S%C3%A3o%20Paulo%2C%20864%2C%20S%C3%A3o%20Caetano%20do%20Sul%20-%20SP&output=embed"></iframe>
  </div>
</section>
<section class="bloco tom wrap">
  {duas("Parcerias", "Formação visual com escolas, instituições e coletivos.",
        corpo("Residências, oficinas fechadas, curadoria de material para turmas e projetos de extensão.")
        + botoes(f'<a class="btn" href="mailto:{EMAIL}?subject=Parcerias">Escrever</a>'))}
</section>''')

    # 404 (servida em qualquer endereço: caminhos a partir da raiz)
    pagina("404.html", "Página não encontrada", "Página não encontrada.",
      '''<section class="abertura wrap nao-achei">
  <div class="duas"><h1 class="t1">Esta página não existe.</h1>
    <div class="lado"><p class="corpo">O endereço pode ter mudado ou estar incompleto. Siga por uma das páginas abaixo.</p>
      <div class="botoes"><a class="btn" href="index.html">Início</a><a class="btn btn-linha" href="nossas-aulas.html">Nossas aulas</a></div></div></div>
</section>''', fecho_html="", base="/")

    # Mapa do site
    open(os.path.join(SAIDA, "sitemap.xml"), "w").write(
        '<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
        + "".join(f"  <url><loc>{u}</loc></url>\n" for u in PAGINAS_PUBLICAS) + "</urlset>\n")

    print("ok:", sorted(os.listdir(SAIDA)))

if __name__ == "__main__":
    build()
