#!/usr/bin/env python3
"""Gera o site estático do Alma a partir de modelos simples (sem dependências).
Saída em ./site — é essa pasta que vai para a hospedagem."""
import os, shutil, html, json

RAIZ = os.path.dirname(os.path.abspath(__file__))
SAIDA = os.path.join(RAIZ, "site")
DOMINIO = "https://almaestudosvisuais.com.br"
LOJA = "https://almamateriaisartisticos.com.br"
APP = "https://app.almaestudosvisuais.com.br"
ENDERECO = "Rua São Paulo, 864, São Caetano do Sul, SP"
MAPA = "https://www.google.com/maps/search/?api=1&query=" + "Rua+S%C3%A3o+Paulo%2C+864%2C+S%C3%A3o+Caetano+do+Sul+-+SP"
EMAIL = "contato@almaestudosvisuais.com.br"
NOME = "Alma Centro de Estudos Visuais"
LOGO = open(os.path.join(RAIZ, "img", "logo.svg")).read().strip()
LOGO = LOGO.replace('class="marca"', 'class="logo"').replace('aria-label="Alma"', 'aria-hidden="true"')

def e(t): return html.escape(t, quote=False)
def a(t): return html.escape(t)

EXTERNO = 'target="_blank" rel="noopener"'
MENU = [("sobre.html", "Sobre"), ("nossas-aulas.html", "Nossas aulas"), ("blog.html", "Blog"), ("contato.html", "Contato")]
X = '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5" aria-hidden="true"><path d="M6 6l12 12M18 6 6 18"/></svg>'
HAMBURGUER = '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5" aria-hidden="true"><path d="M3 7h18M3 12h18M3 17h18"/></svg>'

# ------------------------------------------------------------------ Moldura
def nav(atual, sobre_foto):
    def item(h, t):
        return f'<a href="{h}"{" aria-current=\"page\"" if h == atual else ""}>{t}</a>'
    itens = "".join(item(h, t) for h, t in MENU) + f'<a href="{LOJA}" {EXTERNO}>Loja</a>'
    return f'''<header class="nav wrap{' sobre-foto' if sobre_foto else ''}">
  <a class="marca" href="index.html" aria-label="Alma, página inicial">{LOGO}</a>
  <nav class="menu" aria-label="Principal">{itens}</nav>
  <div class="acoes">
    <a class="link-aluno" href="{APP}" {EXTERNO}>Área do aluno</a>
    <a class="btn btn-nav" href="faca-parte.html">Aula experimental</a>
  </div>
  <button class="abrir" type="button" aria-label="Abrir menu" aria-expanded="false" aria-controls="gaveta">{HAMBURGUER}</button>
</header>
<div class="veu" data-fechar hidden></div>
<aside class="gaveta" id="gaveta" aria-label="Menu" aria-hidden="true">
  <div class="topo"><a href="index.html" aria-label="Alma, página inicial">{LOGO}</a>
    <button class="fechar" type="button" data-fechar aria-label="Fechar menu">{X}</button></div>
  <nav aria-label="Menu">{"".join(item(h, t) for h, t in MENU)}<a href="{LOJA}" {EXTERNO}>Loja</a><a href="{APP}" {EXTERNO}>Área do aluno</a></nav>
  <a class="btn btn-claro btn-largo" href="faca-parte.html">Agendar aula experimental</a>
</aside>'''

FECHO = '''<section class="bloco fecho wrap" id="aula-experimental">
  <div class="duas rev">
    <h2 class="t2">Aula experimental</h2>
    <div class="lado">
      <p class="corpo">A entrada no Alma começa por uma aula experimental. Você conhece o atelier, a turma e o modo de trabalho antes de decidir.</p>
      <div class="botoes"><a class="btn" href="faca-parte.html">Agendar</a><a class="btn btn-linha" href="nossas-aulas.html#como-funciona">Como funciona</a></div>
    </div>
  </div>
</section>'''

RODAPE = f'''<footer class="rodape wrap">
  <div class="rod-topo">
    <div class="novidades">
      <h2 class="t3">Novidades do Alma</h2>
      <p class="pequeno">Workshops, textos novos e a agenda do atelier.</p>
      <form class="form-linha" data-form="novidades" novalidate>
        <label class="sr" for="mail-n">Seu e-mail</label>
        <input class="campo" id="mail-n" name="email" type="email" autocomplete="email" placeholder="Seu e-mail" required>
        <button class="btn btn-claro" type="submit">Assinar</button>
      </form>
      <p class="aviso" role="status"></p>
    </div>
  </div>
  <div class="rod-colunas">
    <div>
      <h2 class="rotulo">Alma</h2>
      <p>{NOME}<br>Rua São Paulo, 864<br>São Caetano do Sul, SP</p>
      <p class="pequeno">CNPJ 66.843.784/0001-28</p>
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
      <a href="{MAPA}" {EXTERNO}>Como chegar</a>
    </div>
  </div>
</footer>'''

ORG = {
    "@context": "https://schema.org", "@type": "EducationalOrganization", "name": NOME,
    "url": DOMINIO, "email": EMAIL, "logo": DOMINIO + "/img/apple-touch-icon.png",
    "address": {"@type": "PostalAddress", "streetAddress": "Rua São Paulo, 864", "addressLocality": "São Caetano do Sul",
                "addressRegion": "SP", "addressCountry": "BR"},
}

def pagina(arquivo, titulo, descricao, corpo, fecho=True, sobre_foto=False):
    titulo_doc = NOME if arquivo == "index.html" else f"{titulo} | {NOME}"
    ld = f'<script type="application/ld+json">{json.dumps(ORG, ensure_ascii=False)}</script>\n' if arquivo == "index.html" else ""
    url = DOMINIO + "/" + ("" if arquivo == "index.html" else arquivo)
    doc = f'''<!doctype html>
<html lang="pt-BR">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
<title>{e(titulo_doc)}</title>
<meta name="description" content="{a(descricao)}">
<link rel="canonical" href="{url}">
<meta property="og:type" content="website">
<meta property="og:locale" content="pt_BR">
<meta property="og:site_name" content="{NOME}">
<meta property="og:title" content="{a(titulo_doc)}">
<meta property="og:description" content="{a(descricao)}">
<meta property="og:url" content="{url}">
<meta property="og:image" content="{DOMINIO}/img/hero-inicio.jpg">
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
{FECHO if fecho else ''}
</main>
{RODAPE}
<script src="config.js"></script>
<script src="site.js" defer></script>
</body>
</html>
'''
    open(os.path.join(SAIDA, arquivo), "w").write(doc)

# ------------------------------------------------------------------ Peças
def duas(titulo, texto_html, extra="", tag="h2", classe=""):
    return f'''<div class="duas rev{(' ' + classe) if classe else ''}"><{tag} class="t2">{titulo}</{tag}><div class="lado"><div class="corpo">{texto_html}</div>{extra}</div></div>'''

def abertura(titulo, texto, escura=False, extra=""):
    return f'''<section class="abertura wrap{' escura' if escura else ''}">
  <div class="duas"><h1 class="t1">{titulo}</h1><div class="lado"><p class="corpo">{texto}</p>{extra}</div></div>
</section>'''

FRENTES = [
    ("frente-atelier.jpg", "Atelier", "Formação em atelier para adultos: currículo básico de Desenho e, depois dele, o percurso de cada aluno na técnica que escolher.", "nossas-aulas.html#como-funciona", None),
    ("frente-jovens.jpg", "Jovens Artistas", "Iniciação à prática artística e à percepção visual para crianças e adolescentes, no tempo de cada idade.", None, "Em breve"),
    ("frente-extensao.jpg", "Extensão", "Workshops e atividades abertas ao longo do ano, que levam a prática do atelier para além das turmas regulares.", "nossas-aulas.html#frentes", None),
]

def frentes():
    out = []
    for img, t, d, href, selo in FRENTES:
        tag, attr = ("a", f' href="{href}"') if href else ("div", ' aria-disabled="true"')
        s = f'<span class="selo">{selo}</span>' if selo else ""
        out.append(f'''<{tag} class="frente rev{' inativa' if selo else ''}"{attr}><div class="foto"><img src="img/{img}" alt="" loading="lazy">{s}</div>
<h3 class="t3">{t}</h3><p class="corpo">{d}</p></{tag}>''')
    return '<div class="tres carrossel">' + "".join(out) + '</div>'

FATOS = [("4 a 9", "pessoas por aula, com acompanhamento individual de cada trabalho"),
         ("5 técnicas", "no mesmo atelier: Desenho, pintura a óleo, aquarela, escultura e gravura"),
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

DOCENTE = duas("Direção pedagógica",
    "<p><strong>Giancarlo Avantaggiato</strong> é pintor a óleo e escultor, fundador e diretor do Alma. "
    "Formado em Design de Produto e em Arquitetura e Urbanismo, fez estudos avançados no Atelier José Paulo de Latorre "
    "e desenvolve doutorado em Artes. Integra o coletivo de artistas Matizes.</p>")

def acordeao(itens, abrir_primeiro=False):
    return '<div class="acordeao">' + "".join(
        f'<details class="rev"{" open" if (i == 0 and abrir_primeiro) else ""}><summary>{q}</summary><div class="resp corpo">{r}</div></details>'
        for i, (q, r) in enumerate(itens)) + '</div>'

PASSOS = [("Aula experimental", "Você visita o atelier, conhece a turma e faz uma primeira aula orientada."),
          ("Ciclo básico de Desenho", "Fundamentos da luz, do valor e da composição. É o ponto de partida de todos, com ou sem experiência."),
          ("A técnica de cada um", "Concluído o ciclo básico, o aluno segue na técnica que escolher: óleo, aquarela, Desenho, escultura ou gravura."),
          ("O próprio percurso", "Não há prazo de conclusão. O trabalho avança até a linguagem de cada aluno, o que chamamos de busca da própria luz.")]

ROTINA = [("Dias fixos", "Cada aluno tem seus dias fixos na semana e pode pedir mudança pelo app."),
          ("Reposições", "Faltas avisadas até 4 horas antes viram reposição, usada em qualquer dia com vaga."),
          ("App do aluno", "Agenda, reposições, recados e o diário de trabalhos ficam no app do Alma."),
          ("Mensalidade", "Cobrança mensal, de acordo com a frequência semanal escolhida.")]

ENSINO = [("Desenho como fundamento", "<p>O Desenho é tratado como disciplina de pensamento, não como etapa a ser superada. É nele que se aprende a ver luz, valor e proporção, e é a ele que todas as técnicas voltam.</p>"),
          ("Ver é construir", "<p>A percepção é ativa: o olho organiza o que vê. Por isso o ensino parte de exercícios de observação e de estrutura antes da representação.</p>"),
          ("Técnica e sensibilidade juntas", "<p>Não separamos o domínio técnico da sensibilidade. A técnica é o meio pelo qual a intenção ganha forma, e não um fim em si.</p>"),
          ("Sem mito do talento", "<p>Partimos do princípio de que ver se aprende. O progresso vem do trabalho contínuo e acompanhado, não de um dom anterior à prática.</p>")]

FAQ = [("Preciso saber desenhar para começar?", "<p>Não. Todos começam pelo ciclo básico de Desenho, com ou sem experiência anterior.</p>"),
       ("Como é uma aula?", "<p>As aulas são coletivas, com 4 a 9 pessoas, e o acompanhamento é individual. Na mesma aula cada aluno trabalha no seu projeto e na sua técnica.</p>"),
       ("Quais técnicas posso estudar?", "<p>Desenho, pintura a óleo, aquarela, escultura e gravura. Além das aulas, o atelier promove modelo vivo, encontros de história da arte, projetos especiais e visitas a exposições.</p>"),
       ("Quanto tempo dura o curso?", "<p>Não há prazo de conclusão. Depois do ciclo básico, cada aluno permanece o tempo que fizer sentido; há alunos com poucos meses e outros com mais de cinco anos de atelier.</p>"),
       ("E se eu precisar faltar?", "<p>Basta desmarcar pelo app com pelo menos 4 horas de antecedência. A falta vira uma reposição, que pode ser usada em qualquer dia com vaga.</p>"),
       ("Para quem são as aulas?", "<p>As turmas regulares são para adultos, inclusive quem está começando depois dos 60. O programa para crianças e adolescentes, Jovens Artistas, abre em breve.</p>")]

REFERENCIAS = [("Josef Albers", "a interação da cor e o ensino pela experiência"),
               ("Rudolf Arnheim", "a percepção visual como forma de pensamento"),
               ("James J. Gibson", "a percepção direta e as invariantes do ambiente"),
               ("György Kepes", "a linguagem da visão e o movimento"),
               ("László Moholy-Nagy", "materiais, sentidos e o curso preliminar da Bauhaus")]

LOREM1 = "<p>Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat.</p><p>Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat cupidatat non proident.</p>"

# ------------------------------------------------------------------ Páginas
def build():
    if os.path.exists(SAIDA): shutil.rmtree(SAIDA)
    os.makedirs(SAIDA)
    shutil.copytree(os.path.join(RAIZ, "img"), os.path.join(SAIDA, "img"))
    for f in ("style.css", "site.js", "config.js", "CNAME", "404.html"):
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
  {duas("Três frentes, um pensamento.", "<p>Somos um Centro de Estudos Visuais dedicado à formação, à pesquisa e à experimentação em Artes Visuais. Tratamos a percepção como forma ativa de compreensão do mundo, e é desse princípio que partem as três frentes do Alma.</p>",
        '<div class="botoes"><a class="btn btn-claro" href="sobre.html">Sobre o Alma</a></div>')}
  <div class="apos">{frentes()}</div>
</section>
<section class="bloco wrap">
  {duas("O atelier", "<p>A formação acontece em estrutura de atelier, com turmas pequenas e convivência entre estudantes de diferentes idades, repertórios e níveis de experiência. Cada percurso começa pelo mesmo currículo básico e se abre, aos poucos, para a linguagem de cada um.</p>",
        '<div class="botoes"><a class="btn" href="nossas-aulas.html#como-funciona">Como funciona</a></div>')}
  <div class="apos">{fatos()}</div>
</section>
<section class="bloco tom wrap">
  {duas("Trabalhos de alunos", "<p>Estudos e trabalhos desenvolvidos no atelier, em diferentes técnicas e momentos do percurso.</p>")}
  <div class="apos">{TRABALHOS}</div>
</section>
<section class="bloco wrap">
  {duas("Notas e Ensaios", "<p>Textos sobre percepção visual, processos de criação, técnica e história da arte, escritos a partir da prática do atelier.</p>",
        '<div class="botoes"><a class="btn" href="blog.html">Ver todos</a></div>')}
  <div class="apos">{cartoes_notas()}</div>
</section>
<section class="bloco tom wrap">
  {duas("Materiais Artísticos", "<p>A loja do Alma reúne papéis, pincéis, tintas e instrumentos escolhidos pela prática do atelier, pela qualidade técnica e pela consistência de uso.</p>",
        f'<div class="botoes"><a class="btn" href="{LOJA}" {EXTERNO}>Visitar a loja</a></div>')}
  <a class="larga apos rev" href="{LOJA}" {EXTERNO} aria-label="Visitar a loja de materiais"><img src="img/loja.jpg" alt="Pintura de natureza-morta com frascos e potes de tinta" loading="lazy"></a>
</section>''', sobre_foto=True)

    # Sobre
    pagina("sobre.html", "Sobre",
      "O ver tem gramática, e essa gramática se ensina. A história, o manifesto e as referências do Alma.",
      abertura("Sobre o Alma", "Toda forma que vemos é resultado de uma operação: distribuição de luz, organização de valores, articulação de cheios e vazios. O olho não recebe a imagem pronta, ele a constrói. O Alma ensina o domínio dessa construção, a partir de uma convicção: o ver tem gramática, e essa gramática se ensina.", escura=True) + f'''
<div class="larga wrap-larga"><img src="img/sobre-bauhaus.jpg" alt="Fotografia do edifício da Bauhaus em Dessau, com anotações manuscritas" loading="lazy"></div>
<section class="bloco wrap" id="manifesto">{duas("Manifesto", LOREM1)}</section>
<section class="bloco tom wrap" id="historia">{duas("Nossa história", LOREM1)}</section>
<section class="bloco wrap" id="referencias">
  {duas("Referências", "<p>O ensino do Alma se apoia na tradição da Bauhaus e em autores que estudaram a percepção como forma ativa de conhecimento.</p>")}
  <ul class="lista-ref apos">{"".join(f'<li class="rev"><span class="t3">{n}</span><span class="corpo">{d}</span></li>' for n, d in REFERENCIAS)}</ul>
</section>
<section class="bloco tom wrap" id="direcao">{DOCENTE}</section>''')

    # Nossas aulas
    TECNICAS = [("blog-3.jpg", "Desenho", "A base de tudo: luz, valor, proporção e composição."),
                ("blog-6.jpg", "Pintura a óleo", "Camadas, velaturas e a construção da cor pela luz."),
                ("blog-5.jpg", "Aquarela", "Transparência, água e a decisão de cada mancha."),
                ("hero-inicio.jpg", "Escultura", "A forma no espaço, do volume ao detalhe."),
                ("blog-2.jpg", "Gravura", "Matriz, traço e a lógica da impressão.")]
    PERCURSO = [("Aula experimental", "Você conhece o atelier e a turma numa primeira aula orientada."),
                ("Ciclo básico de Desenho", "Luz, valor e composição. O mesmo começo para todos, com ou sem experiência."),
                ("A sua técnica", "Concluído o ciclo, você segue na técnica que escolher."),
                ("A própria luz", "Sem prazo de conclusão: o trabalho avança até a sua linguagem.")]
    PRINCIPIOS = [("Ver se aprende.", "Não partimos de dom. Partimos de trabalho contínuo e acompanhado."),
                  ("O Desenho é o fundamento.", "É nele que se aprende a ver, e é a ele que todas as técnicas voltam."),
                  ("Técnica e sensibilidade andam juntas.", "A técnica é o meio pelo qual a intenção ganha forma.")]
    NO_ATELIER = [("4 a 9 pessoas", "por aula, cada uma no seu projeto"), ("Acompanhamento individual", "durante toda a aula"),
                  ("Dias fixos na semana", "escolhidos por você"), ("Reposições pelo app", "avisando até 4 horas antes")]
    FAQ_CURTA = FAQ[:4]
    pagina("nossas-aulas.html", "Nossas aulas",
      "Como funcionam as aulas do Alma: o percurso a partir do Desenho, as técnicas do atelier e o dia a dia das turmas.",
      f'''<section class="ab-foto wrap">
  <img src="img/frente-atelier.jpg" alt="Alunos trabalhando lado a lado num atelier" fetchpriority="high">
  <div class="ab-foto__txt">
    <h1 class="t1">Nossas aulas</h1>
    <p class="corpo">Um atelier de formação para adultos, com turmas pequenas e acompanhamento individual.</p>
    <nav class="atalhos" aria-label="Nesta página"><a href="#percurso">O percurso</a><a href="#tecnicas">Técnicas</a><a href="#no-atelier">No atelier</a><a href="#faq">Perguntas</a></nav>
  </div>
</section>
<section class="frase wrap">
  <p class="frase__txt rev">Todo aluno começa pelo Desenho. A partir dele, cada um encontra a sua técnica e, com o tempo, a <em>própria luz</em>.</p>
</section>
<section class="bloco tom wrap" id="percurso">
  {duas("O percurso", "<p>Um começo comum e, depois dele, um caminho individual.</p>")}
  <ol class="percurso apos">{"".join(f'<li class="rev"><span class="percurso__n" aria-hidden="true">{i+1:02d}</span><h3 class="t3">{t}</h3><p class="texto-cartao">{d}</p></li>' for i, (t, d) in enumerate(PERCURSO))}</ol>
</section>
<section class="bloco wrap" id="tecnicas">
  {duas("Técnicas", "<p>Cinco linguagens convivem na mesma sala. Na mesma aula, cada aluno trabalha na sua.</p>")}
  <div class="tecnicas carrossel apos">{"".join(f'<figure class="tecnica rev"><div class="tecnica__img"><img src="img/{img}" alt="" loading="lazy"></div><figcaption><span class="t3">{t}</span><span class="texto-cartao">{d}</span></figcaption></figure>' for img, t, d in TECNICAS)}</div>
</section>
<section class="bloco escuro wrap" id="no-atelier">
  <div class="dividido">
    <div class="dividido__img rev"><img src="img/blog-8.jpg" alt="Estudo de Desenho feito no atelier" loading="lazy"></div>
    <div class="dividido__txt">
      <h2 class="t2 rev">No atelier</h2>
      <p class="corpo rev">O atelier funciona como um grupo único. Em cada aula você encontra pessoas em momentos diferentes do percurso, e é dessa convivência que nasce boa parte do aprendizado.</p>
      <dl class="numeros">{"".join(f'<div class="rev"><dt>{n}</dt><dd>{t}</dd></div>' for n, t in NO_ATELIER)}</dl>
      <p class="pequeno rev">Além das aulas: modelo vivo, encontros de história da arte, projetos especiais e visitas a exposições.</p>
    </div>
  </div>
</section>
<section class="bloco wrap" id="principios">
  {duas("O que buscamos", "<p>Três ideias guiam o trabalho em sala.</p>")}
  <ul class="principios apos">{"".join(f'<li class="rev"><p class="principios__t">{t}</p><p class="texto-cartao">{d}</p></li>' for t, d in PRINCIPIOS)}</ul>
</section>
<section class="bloco tom wrap" id="trabalhos">
  {duas("Do atelier", "<p>Estudos e trabalhos de alunos, em diferentes técnicas e momentos do percurso.</p>")}
  <div class="apos">{TRABALHOS}</div>
</section>
<section class="bloco wrap" id="alem">
  {duas("Além do atelier", "<p>Outras frentes do Alma, para outros públicos e formatos.</p>")}
  <div class="alem apos">
    <div class="alem__item rev"><span class="selo selo--linha">Em breve</span><h3 class="t3">Jovens Artistas</h3><p class="texto-cartao">Iniciação à prática artística e à percepção visual para crianças e adolescentes.</p></div>
    <a class="alem__item rev" href="contato.html"><h3 class="t3">Extensão</h3><p class="texto-cartao">Workshops e atividades abertas ao longo do ano. Assine as novidades para saber das próximas datas.</p></a>
  </div>
</section>
<section class="bloco tom wrap" id="faq">
  {duas("Perguntas frequentes", "<p>Outras dúvidas: <a href=\"mailto:" + EMAIL + "\">" + EMAIL + "</a>.</p>")}
  <div class="apos">{acordeao(FAQ_CURTA)}</div>
</section>''')

    # Blog
    POSTS = [("blog-1.jpg", "Materiais", "História dos pigmentos e do meio que os carrega", "Pigmento é matéria seca e inerte. O meio que o carrega decide o brilho, a secagem e a permanência da cor."),
             ("blog-2.jpg", "Percepção Visual", "Movimento e ritmo na percepção da forma", "A mesa permanece retangular enquanto você caminha ao redor dela. A forma resiste à mudança de aparência."),
             ("blog-3.jpg", "Teoria", "Grisaille e a construção do valor tonal", "A chave tonal se estabelece antes da primeira mistura: o valor decide de onde vem a luz e o que fica na sombra."),
             ("blog-4.jpg", "História da Arte", "Chiaroscuro e o peso construtivo da sombra", "Em Caravaggio a sombra ganha peso construtivo e passa a sustentar a figura com a força do claro."),
             ("blog-5.jpg", "Prática", "Velatura e a cor que nasce da luz refletida", "Camada transparente sobre camada seca. A cor não nasce da mistura: nasce da luz que atravessa e volta refletida."),
             ("blog-6.jpg", "Pensamento", "Pentimento e a memória do próprio processo", "O traço que a decisão anterior deixa visível na superfície. A obra guarda a memória do próprio processo."),
             ("blog-7.jpg", "Estética", "Albers e a interação entre cores vizinhas", "Nenhuma cor é vista isolada. O tom muda conforme a vizinhança, e é essa comparação que a prática exercita."),
             ("blog-8.jpg", "Fotografia", "Frontalidade e obliquidade no enquadramento", "A posição da câmera diante do plano decide antes da luz: frontalidade organiza, obliquidade abre profundidade."),
             ("blog-9.jpg", "Cinema", "Kepes e a composição em movimento", "Movimento como condição da vida moderna, e a disciplina formal acima da novidade.")]
    TAGS = ["Materiais", "Percepção Visual", "Teoria", "História da Arte", "Prática", "Pensamento", "Estética", "Fotografia", "Cinema"]
    pagina("blog.html", "Notas e Ensaios",
      "Notas e Ensaios do Alma: textos sobre percepção visual, processos de criação, técnica e história da arte.",
      abertura("Notas e Ensaios", "Textos sobre percepção visual, processos de criação, técnica e história da arte, escritos a partir da prática do atelier.") + f'''
<section class="bloco wrap">
  <div class="filtros rev">
    <label class="busca" for="q"><span class="sr">Buscar textos</span><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.6" aria-hidden="true"><circle cx="10.5" cy="10.5" r="6.5"/><path d="m15.5 15.5 5 5"/></svg>
      <input id="q" type="search" placeholder="Buscar textos" autocomplete="off"></label>
    <div class="tags" role="group" aria-label="Filtrar por tema">{"".join(f'<button type="button" aria-pressed="false" data-tag="{t}">{t}</button>' for t in TAGS)}</div>
  </div>
  <p class="contagem pequeno" data-total="23" aria-live="polite">23 textos publicados</p>
  <div class="posts">''' + "".join(
        f'''<a class="post rev" href="#" data-tag="{tag}"><div class="foto"><img src="img/{img}" alt="" loading="lazy"></div>
<p class="meta"><span>{tag}</span></p><h3 class="t3">{t}</h3><p class="corpo">{d}</p></a>''' for img, tag, t, d in POSTS) + '''</div>
  <p class="vazio corpo" hidden>Nenhum texto encontrado com esses termos.</p>
</section>''')

    # Faça parte (aula experimental)
    TECNICAS = ["Ainda não sei", "Desenho", "Pintura a óleo", "Aquarela", "Escultura", "Gravura"]
    pagina("faca-parte.html", "Aula experimental",
      "Agende uma aula experimental no Alma Centro de Estudos Visuais, em São Caetano do Sul.",
      abertura("Faça parte", "A entrada no Alma começa por uma aula experimental. Deixe seu contato e combinamos pelo WhatsApp o dia da sua visita ao atelier.") + f'''
<section class="bloco wrap">
  <div class="duas">
    <div class="rev">
      <h2 class="t2">Como é a aula experimental</h2>
      <ol class="passos-curtos">
        <li><span class="t3">Combinamos o dia</span><span class="corpo">Respondemos pelo WhatsApp com os dias disponíveis.</span></li>
        <li><span class="t3">Você vem ao atelier</span><span class="corpo">Faz uma aula com a turma, com orientação individual.</span></li>
        <li><span class="t3">Você decide</span><span class="corpo">Se quiser continuar, combinamos seus dias fixos e a matrícula.</span></li>
      </ol>
    </div>
    <form class="formulario lado rev" data-form="candidatura" novalidate>
      <label>Nome<input name="nome" autocomplete="name" required></label>
      <label>WhatsApp<input name="whatsapp" type="tel" inputmode="tel" autocomplete="tel" placeholder="(11) 90000-0000" required></label>
      <label><span>E-mail <span class="opcional">opcional</span></span><input name="email" type="email" autocomplete="email"></label>
      <label>Técnica de interesse<select name="interesse">{"".join(f'<option>{t}</option>' for t in TECNICAS)}</select></label>
      <label><span>Conte um pouco sobre você <span class="opcional">opcional</span></span><textarea name="mensagem" rows="4"></textarea></label>
      <p class="pequeno">Usamos seus dados apenas para combinar a aula experimental.</p>
      <button class="btn btn-largo" type="submit">Enviar</button>
      <p class="aviso" role="status"></p>
    </form>
  </div>
</section>''', fecho=False)

    # Contato
    pagina("contato.html", "Contato",
      "Endereço, WhatsApp e e-mail do Alma Centro de Estudos Visuais, em São Caetano do Sul.",
      abertura("Contato", "O Alma fica em São Caetano do Sul, no ABC Paulista. Visitas ao atelier são agendadas previamente.") + f'''
<section class="bloco wrap">
  <div class="duas">
    <dl class="contatos rev">
      <div><dt class="t3">Endereço</dt><dd class="corpo">Rua São Paulo, 864<br>São Caetano do Sul, SP<br>Entrada pelo portão lateral.</dd>
        <dd><a class="btn btn-linha-escura" href="{MAPA}" {EXTERNO}>Abrir no mapa</a></dd></div>
      <div><dt class="t3">WhatsApp</dt><dd class="corpo">11 90000-0000, para aula experimental, dúvidas sobre o atelier e materiais.</dd>
        <dd data-so-whatsapp><a class="btn btn-linha-escura" href="#" data-whatsapp>Conversar</a></dd></div>
      <div><dt class="t3">E-mail</dt><dd class="corpo"><a href="mailto:{EMAIL}">{EMAIL}</a></dd></div>
    </dl>
    <iframe class="mapa lado rev" title="Mapa: {ENDERECO}" loading="lazy" referrerpolicy="no-referrer-when-downgrade"
      src="https://www.google.com/maps?q=Rua%20S%C3%A3o%20Paulo%2C%20864%2C%20S%C3%A3o%20Caetano%20do%20Sul%20-%20SP&output=embed"></iframe>
  </div>
</section>
<section class="bloco tom wrap">
  {duas("Parcerias", "<p>Trabalhamos com escolas, instituições culturais e coletivos interessados em formação visual continuada: residências, oficinas fechadas, curadoria de material para turmas e projetos de extensão.</p>",
        f'<div class="botoes"><a class="btn" href="mailto:{EMAIL}?subject=Parcerias">Escrever</a></div>')}
</section>''')

    print("ok:", sorted(os.listdir(SAIDA)))

if __name__ == "__main__":
    build()
