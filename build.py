#!/usr/bin/env python3
"""Gera o site estático do Alma a partir de modelos simples (sem dependências).
Saída em ./site — é essa pasta que vai para a hospedagem."""
import os, shutil, html, json, hashlib

RAIZ = os.path.dirname(os.path.abspath(__file__))
SAIDA = os.path.join(RAIZ, "site")
LOJA = "https://almamateriaisartisticos.com.br"
APP = "https://app.almaestudosvisuais.com.br"
LOGO = open(os.path.join(RAIZ, "img", "logo.svg")).read().strip()
LOGO = LOGO.replace('class="marca"', 'class="logo"').replace('aria-label="Alma"', 'aria-hidden="true"')

def e(t): return html.escape(t, quote=False)

def _v(f): return hashlib.md5(open(os.path.join(RAIZ, "src", f), "rb").read()).hexdigest()[:8]

MENU = [("sobre.html", "Sobre"), ("nossas-aulas.html", "Nossas Aulas"), ("blog.html", "Blog"),
        ("nossas-aulas.html#faq", "FAQ"), ("contato.html", "Contato")]

def nav(atual, solida=False):
    itens = "".join(
        f'<a href="{h}"{" aria-current=\"page\"" if h == atual else ""}>{t}</a>' for h, t in MENU)
    gav = "".join(f'<a href="{h}">{t}</a>' for h, t in MENU)
    return f'''<header class="nav wrap{' solida' if solida else ''}">
  <div class="esq">
    <a class="marca" href="index.html" aria-label="Alma, página inicial">{LOGO}</a>
    <nav class="menu" aria-label="Principal">{itens}</nav>
  </div>
  <a class="btn loja" href="{LOJA}" target="_blank" rel="noopener">Loja <span class="seta">↗</span></a>
  <button class="abrir" aria-label="Abrir menu" aria-expanded="false" aria-controls="gaveta"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5"><path d="M3 7h18M3 12h18M3 17h18"/></svg></button>
</header>
<div class="veu" data-fechar></div>
<aside class="gaveta" id="gaveta" aria-label="Menu">
  <div class="topo"><a href="index.html" aria-label="Alma, página inicial">{LOGO.replace('class="logo"','class="logo"')}</a>
    <button class="fechar" data-fechar aria-label="Fechar menu"><svg width="17" height="12" viewBox="0 0 17 12" fill="currentColor"><path fill-rule="evenodd" d="M14.85 6.525 10.16 11.21l.75.75L16.87 6 10.91.04l-.75.75 4.69 4.69H0v1.05h14.85z"/></svg></button></div>
  <nav>{gav}</nav>
  <a class="btn btn-claro loja-m" href="{LOJA}" target="_blank" rel="noopener">Loja <span class="seta">↗</span></a>
</aside>'''

COMECAR = '''<section class="comecar wrap" id="comecar">
  <h2 class="t2 rev">Sua formação começa onde você está*</h2>
  <p class="corpo rev">Entre em contato e desenvolva sua percepção, sua técnica e sua produção artística a partir de um percurso acompanhado de forma individual. Na aula experimental, você conhece o atelier, a turma e o modo de trabalho antes de decidir. Deixe seu WhatsApp e combinamos o dia.*</p>
  <form class="form-linha rev" data-form="whatsapp" novalidate>
    <label class="sr" for="wpp">Seu WhatsApp</label>
    <input class="campo" id="wpp" name="whatsapp" type="tel" inputmode="tel" autocomplete="tel" placeholder="00 00000-0000" required>
    <button class="btn" type="submit">Quero agendar</button>
  </form>
  <p class="aviso" role="status"></p>
</section>'''

RODAPE = f'''<footer class="rodape wrap">
  <div class="novidades">
    <h2 class="t2">Acompanhe as novidades</h2>
    <p class="novidades__txt">Workshops, textos novos e a agenda do atelier, direto no seu e-mail.*</p>
    <div>
      <form class="form-linha" data-form="novidades" novalidate>
        <label class="sr" for="mail-n">Seu e-mail</label>
        <input class="campo" id="mail-n" name="email" type="email" autocomplete="email" placeholder="Digite seu e-mail" required>
        <button class="btn btn-claro" type="submit">Se inscrever</button>
      </form>
      <p class="termos">Ao se inscrever você aceita os <a href="{LOJA}/policies/terms-of-service" target="_blank" rel="noopener">Termos de Uso</a>.</p>
      <p class="aviso" role="status"></p>
    </div>
  </div>
  <div class="contatos">
    <div>
      <strong>Alma Centro de Estudos Visuais</strong>
      <p>Rua São Paulo, 864<br>São Caetano do Sul, São Paulo - Brasil</p>
      <p>CNPJ&nbsp; 66.843.784/0001-28</p>
    </div>
    <div>
      <p><strong>Contato</strong><br><a href="mailto:contato@almaestudosvisuais.com.br">contato@almaestudosvisuais.com.br</a></p>
      <p><strong>Loja</strong><br><a href="mailto:loja@almaestudosvisuais.com.br">loja@almaestudosvisuais.com.br</a></p>
    </div>
  </div>
  <nav class="links" aria-label="Rodapé">
    <a href="index.html">Início</a><a href="sobre.html">Sobre nós</a>
    <a href="mailto:loja@almaestudosvisuais.com.br?subject=Atacado">Atacado</a>
    <a href="{LOJA}/policies/terms-of-service" target="_blank" rel="noopener">Termos e Condições</a>
    <a href="{LOJA}/policies/shipping-policy" target="_blank" rel="noopener">Envio e Entrega</a>
    <a href="{APP}" target="_blank" rel="noopener">App do aluno</a>
  </nav>
</footer>'''

def pagina(arquivo, titulo, descricao, corpo, atual=None, solida=False, comecar=True):
    doc = f'''<!doctype html>
<html lang="pt-BR">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
<title>{e(titulo)}</title>
<meta name="description" content="{html.escape(descricao)}">
<meta property="og:title" content="{html.escape(titulo)}">
<meta property="og:description" content="{html.escape(descricao)}">
<meta property="og:image" content="img/hero-inicio.jpg">
<meta name="theme-color" content="#000000">
<link rel="icon" type="image/png" href="img/favicon-32.png">
<link rel="apple-touch-icon" href="img/apple-touch-icon.png">
<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Host+Grotesk:wght@400;500&display=swap" rel="stylesheet">
<link rel="stylesheet" href="style.css?v={_v("style.css")}">
</head>
<body>
{nav(atual or arquivo, solida)}
<main>
{corpo}
{COMECAR if comecar else ''}
</main>
{RODAPE}
<script src="config.js?v={_v("config.js")}"></script>
<script src="site.js?v={_v("site.js")}" defer></script>
</body>
</html>
'''
    open(os.path.join(SAIDA, arquivo), "w").write(doc)

def intro(titulo, texto_html, extra="", tag="h2"):
    return f'''<div class="duas intro rev"><{tag} class="t2">{titulo}</{tag}><div class="direita"><div class="corpo">{texto_html}</div>{extra}</div></div>'''

FRENTES_TXT = {
  "inicio": [
    ("frente-atelier.jpg", "Nosso atelier", "Formação em estrutura de atelier, onde o percurso do aluno é construído a partir de um currículo básico, com desenvolvimento gradual de sua percepção para explorar sua própria Forma."),
    ("frente-jovens.jpg", "Jovens Artistas", "Introdução da prática artística e desenvolvimento da percepção visual para crianças e adolescentes, respeitando o tempo de aprendizagem de cada idade e estimulando a observação, a criatividade e a construção do repertório."),
    ("frente-extensao.jpg", "Extensão", "Extensão leva a prática artística para além do espaço interno do Alma, desenvolvendo atividades abertas sazonais que ampliam o contato com as Artes Visuais e com a criação."),
  ],
  "aulas": [
    ("frente-atelier.jpg", "Nosso atelier", "Formação em estrutura de atelier, onde o percurso do aluno é construído a partir de um currículo básico, com desenvolvimento gradual de sua percepção para explorar sua própria Forma."),
    ("frente-jovens.jpg", "Jovens Artistas", "Introdução da prática artística e desenvolvimento da percepção visual para crianças e adolescentes, respeitando o tempo de aprendizagem de cada idade e estimulando a observação, a criatividade e a construção do repertório."),
    ("frente-extensao.jpg", "Extensão", "Extensão leva a prática artística para além do espaço interno do Alma, desenvolvendo atividades abertas sazonais que ampliam o contato com as Artes Visuais e com a criação."),
  ],
}
FRENTE_LINK = {"Nosso atelier": "nossas-aulas.html#frentes", "Jovens Artistas": "nossas-aulas.html#frentes", "Extensão": "nossas-aulas.html#frentes"}

def passos(itens, classe="quatro"):
    return f'<ol class="{classe} passos apos-cab">' + "".join(
        f'<li class="passo rev"><span class="n" aria-hidden="true">{i+1}</span><h3 class="t3">{t}</h3><p class="corpo">{d}</p></li>' for i, (t, d) in enumerate(itens)) + '</ol>'

PERCURSO = [("Aula experimental", "Você conhece o atelier e a turma numa primeira aula orientada.*"),
            ("Currículo básico", "Desenho e Plástica. O mesmo começo para todos, com ou sem experiência.*"),
            ("Seu meio", "Concluído o currículo básico, você escolhe o meio em que quer se aprofundar: aquarela, guache, acrílica, óleo, escultura ou gravura.*"),
            ("Própria luz", "Sem prazo de conclusão. O trabalho segue até encontrar a sua linguagem.*")]
INGRESSO = [("Agendamento", "Respondemos pelo WhatsApp com os horários que têm vaga e combinamos a data da sua aula.*"),
            ("Aula no atelier", "Você participa de uma aula regular, junto à turma e com orientação individual. Conversamos sobre seu repertório e sobre o que pretende estudar.*"),
            ("Matrícula", "Se decidir continuar, definimos a frequência semanal, os dias fixos e o início do currículo básico de Desenho e Plástica.*")]

def frentes(qual):
    return '<div class="tres">' + "".join(
        f'''<a class="frente rev" href="{FRENTE_LINK[t]}"><div class="foto"><img src="img/{img}" alt="" loading="lazy"></div>
<div class="txt">{'<span class="selo">Em breve*</span>' if t != "Nosso atelier" else ''}<h3 class="t3">{t}</h3><p class="corpo">{d}</p></div></a>''' for img, t, d in FRENTES_TXT[qual]) + '</div>'

EDUCACAO = f'''<section class="secao wrap" id="educacao">
  {intro("Educação", "<p>A formação no Alma acontece em três segmentos: nosso Atelier, espaço de trabalho e formação do pensamento artístico; Jovens Artistas, segmento de iniciação da percepção visual para crianças e adolescentes; e Extensão, que leva a prática visual para além do espaço interno do Atelier.</p>")}
  <div class="apos-cab">{frentes("inicio")}</div>
  <hr class="filete">
</section>'''

LOJA_SEC = f'''<section class="secao wrap" id="loja">
  {intro("Loja", "<p>Curadoria de materiais artísticos feita a partir da prática de atelier. O Alma Materiais Artísticos reúne uma seleção de meios abrasivos e fluidos, papéis, pincéis e instrumentos escolhidos criteriosamente por sua qualidade técnica, consistência de uso e adequação ao trabalho de artistas, estudantes e processos manuais.</p>",
         f'<a class="btn btn-preto" href="{LOJA}" target="_blank" rel="noopener">Loja <span class="seta">↗</span></a>')}
  <a class="larga rev apos-cab" href="{LOJA}" target="_blank" rel="noopener" style="display:block" aria-label="Ir para a loja"><img src="img/loja-armarios.jpg" alt="Armários de madeira com pigmentos, tintas e pincéis numa loja tradicional de materiais artísticos" loading="lazy"></a>
  <hr class="filete">
</section>'''

NOTAS = [("nota-valor-tonal.jpg", "Percepção", "2026-08-04", "04 ago 2026", "A construção do valor tonal na pintura a óleo"),
         ("nota-velatura.jpg", "Técnica", "2026-07-28", "28 jul 2026", "Velatura e opacidade: dois modos de construir a cor"),
         ("nota-desenho.jpg", "Processo", "2026-07-15", "15 jul 2026", "O que o Desenho ensina antes da tinta")]
NOTAS_SEC = f'''<section class="secao wrap" id="notas">
  {intro("Notas e Ensaios", "<p>Notas e ensaios sobre percepção visual, processos de criação, técnica, história da arte e pensamento artístico. Aqui, reunimos reflexões que atravessam a prática do atelier e ampliam o olhar sobre a Arte.</p>",
         '<a class="btn btn-preto" href="blog.html">Ver todos</a>')}
  <div class="tres apos-cab">''' + "".join(
    f'''<a class="cartao rev" href="blog.html"><div class="foto"><img src="img/{img}" alt="" loading="lazy"></div>
<div class="meta"><span class="cat">{cat}</span><time datetime="{dt}">{data}</time></div><h3 class="t3">{t}*</h3></a>''' for img, cat, dt, data, t in NOTAS) + '''</div>
</section>'''

def build():
    if os.path.exists(SAIDA): shutil.rmtree(SAIDA)
    os.makedirs(SAIDA)
    shutil.copytree(os.path.join(RAIZ, "img"), os.path.join(SAIDA, "img"))
    for f in ("style.css", "site.js", "config.js", "CNAME", "404.html"):
        p = os.path.join(RAIZ, "src", f)
        if os.path.exists(p): shutil.copy(p, SAIDA)

    # ---------------- Início ----------------
    pagina("index.html", "Alma · Centro de Estudos Visuais",
      "Centro de Estudos Visuais em São Caetano do Sul: atelier de Desenho, pintura e escultura, Jovens Artistas e Extensão.",
      f'''<section class="hero wrap">
  <img src="img/hero-inicio.jpg" alt="Estudantes trabalhando em esculturas num atelier" fetchpriority="high">
  <div class="chamada">
    <h1 class="t1">Da Ideia à Forma.<br>No seu Ritmo.*</h1>
    <div class="botoes"><a class="btn" href="nossas-aulas.html">Nossas aulas</a><a class="btn" href="{LOJA}" target="_blank" rel="noopener">Loja <span class="seta">↗</span></a></div>
  </div>
</section>
<section class="faixa wrap">
  <div class="lin">
    <div class="txt rev"><h2 class="t2">Três frentes, um pensamento.*</h2>
      <p class="corpo">Somos um Centro de Estudos Visuais dedicado à formação, pesquisa e experimentação em Artes Visuais. Tratamos a percepção como forma ativa de compreensão do mundo e operamos em três frentes: o <em>Atelier</em>, espaço de trabalho e formação do pensamento artístico; Jovens Artistas, segmento de iniciação da percepção visual para crianças e adolescentes; e Extensão, que leva a prática visual para além do espaço interno do Atelier.</p></div>
    <div class="botoes rev"><a class="btn btn-claro" href="sobre.html">Saiba mais</a><a class="btn btn-linha" href="faca-parte.html">Quero começar</a></div>
  </div>
</section>
{EDUCACAO}
{LOJA_SEC}
{NOTAS_SEC}''', atual="index.html")

    # ---------------- Sobre ----------------
    LOREM1 = "<p>Acreditamos que ver se aprende. Antes da técnica, antes do estilo, existe o olhar: a capacidade de perceber relações de luz, valor, espaço e proporção, e de organizá-las numa forma que tenha sentido.*</p><p>Por isso o Alma ensina a partir da percepção e respeita o tempo de cada um. Não formamos em série nem prometemos atalhos: acompanhamos cada percurso até que a pessoa encontre a sua própria Forma.*</p>"
    LOREM2 = "<p>O Alma nasceu em São Caetano do Sul a partir da prática de atelier de Giancarlo Avantaggiato, artista plástico, com a ideia de reunir formação, pesquisa e experimentação em Artes Visuais num mesmo espaço.*</p><p>A pedagogia do Alma se apoia na tradição da Bauhaus e no estudo da percepção visual. Hoje o Alma reúne o atelier para adultos, a loja de materiais artísticos e os programas Jovens Artistas e Extensão, em preparação.*</p>"
    pagina("sobre.html", "Sobre · Alma", "A percepção visual como forma de compreensão do mundo. Conheça o manifesto e a história do Alma.",
      f'''<section class="abertura escura wrap"><h1 class="t1">Sobre o Alma</h1>
  <p>Toda forma que vemos é resultado de uma operação: distribuição de luz, organização de valores, articulação de espaços positivos e negativos no campo. O olho não recebe uma imagem pronta — ele a constrói. O Alma forma o domínio dessa construção e o faz por <em>três</em> frentes que partem da mesma convicção: <em>a percepção visual como forma de compreensão do mundo.</em></p></section>
<section class="wrap sobre-topo">
  <div class="larga sobre-foto rev"><img src="img/sobre-bauhaus.jpg" alt="Fotografia do edifício da Bauhaus em Dessau, com anotações manuscritas" loading="lazy"></div>
  <div class="secao">{intro("Manifesto", LOREM1, '<a class="btn btn-preto" href="#historia">Saiba mais</a>')}</div>
</section>
<section class="historia wrap" id="historia"><img src="img/sobre-historia-fundo.jpg" alt="">
  {intro("Nossa história", LOREM2, '<a class="btn btn-claro" href="nossas-aulas.html">Saiba mais</a>').replace('class="t2"','class="t2 claro"')}
</section>
<section class="secao wrap" id="direcao">
  {intro("Direção pedagógica", "<p><strong>Giancarlo Avantaggiato</strong><br>Artista Plástico e Diretor</p><p>Formado em Design de Produto e em Arquitetura e Urbanismo, fez estudos avançados no Atelier José Paulo de Latorre e integra o coletivo de artistas Matizes.*</p>")}
  <hr class="filete">
</section>
{EDUCACAO}
{LOJA_SEC}
{NOTAS_SEC}''')

    # ---------------- Nossas aulas ----------------
    ENSINO = [("Formação Básica e Contínua", "A formação segue princípios básicos como percepção visual, composição do espaço pictórico, e a luz à Forma."),
              ("Percepção", "Percepção é a operação pela qual a mente organiza o mundo sensível em estruturas reconhecíveis — direções, formas, relações, tensões. A percepção, nesse sentido, opera ao nível dos sentidos o que o raciocínio realiza no nível do pensamento — ela já é, em si, uma forma de inteligência."),
              ("Formação do Pensamento", "O ver é compreender. O pensamento se forma dentro da atividade perceptiva, desde o primeiro instante em que se organiza o que se vê, constrói repertório, e passa a orientar como a pessoa relaciona parte e todo, reconhece padrão em meio à complexidade, julga tensão e equilíbrio em qualquer experiência, visual ou não."),
              ("Técnica e Processo", "A técnica se desenvolve de acordo com cada tipo de material, e é o meio que conduz o artista da ideia à forma."),
              ("Composição", "Composição é a organização das partes de uma obra em relação ao todo, como um sistema de tensões, proporções e direções — a construção de uma unidade que dá corpo visível a um sentido."),
              ("Diferentes Materiais", "A abordagem de materiais é extensa e direcionada à autoexpressão de cada aluno, ao mesmo tempo que respeita as características intrínsecas do meio. Após um ciclo teórico básico, o aluno é conduzido ao seu trabalho pelo material que mais deseja explorar."),
              ("Diferentes Artistas", "Composto por diferentes artistas, o Alma promove um ambiente de aprendizado horizontal, no qual a mesma turma reúne alunos em materiais, meios e estágios diferentes — cada percurso seguindo sua própria lógica de desenvolvimento. Nesse espaço, a singularidade de cada um não é apagada pela comunidade — pelo contrário, se nutre dela.")]
    FAQ = [("Preciso saber desenhar para começar?", "Não. Todos começam pelo currículo básico de Desenho e Plástica, com ou sem experiência anterior.*"),
           ("Para quem são as aulas?", "As aulas regulares são para adultos, de qualquer idade e em qualquer momento da vida. O programa para crianças e adolescentes, Jovens Artistas, abre em breve.*"),
           ("Quanto tempo dura o curso?", "Não há prazo de conclusão. Depois do currículo básico, cada aluno permanece o tempo que fizer sentido para o próprio percurso.*"),
           ("Quanto custa?", "As mensalidades começam em R$ 420, conforme a frequência semanal. Os valores completos são apresentados na aula experimental.*"),
           ("Como escolho os dias de aula?", "Você escolhe dias fixos na semana, conforme a frequência do seu plano. O dia da aula experimental é combinado pelo WhatsApp.*"),
           ("O que acontece além das aulas?", "Sessões de modelo vivo, encontros de história da arte, projetos especiais e visitas a exposições.*"),
           ("E se eu precisar faltar?", "Basta desmarcar pelo app com pelo menos 4 horas de antecedência. A falta vira uma reposição, que pode ser usada em qualquer dia com vaga.*")]
    def acordeao(itens, abrir_primeiro=True):
        return '<div class="acordeao">' + "".join(
            f'<details class="rev"{" open" if (i == 0 and abrir_primeiro) else ""}><summary>{q}</summary><p class="resp">{r}</p></details>' for i, (q, r) in enumerate(itens)) + '</div>'
    pagina("nossas-aulas.html", "Nossas aulas · Alma", "Atelier, Jovens Artistas e Extensão: como funcionam as aulas do Alma.",
      f'''<section class="abertura escura wrap"><h1 class="t1">Nossas aulas</h1>
  <p>O atelier é, ao mesmo tempo, espaço de trabalho, de estudo e de convivência. O desenvolvimento de cada aluno acontece de forma individualizada, em aulas coletivas: as atividades partem do repertório do aluno, constroem o currículo básico a partir dele e, progressivamente, abrem espaço para a investigação visual própria, através de diferentes meios e técnicas.</p></section>
<section class="secao wrap" id="frentes">{frentes("aulas")}<hr class="filete"></section>
<section class="secao wrap" id="percurso">
  {intro("O percurso", "<p>Todo aluno começa pelo Desenho e pela Plástica. A partir deles, cada um encontra o seu meio e, com o tempo, a própria luz.*</p>")}
  {passos(PERCURSO)}
  <hr class="filete">
</section>
<section class="secao wrap" id="ensino">
  {intro("Sobre o ensino", "<p>O percurso começa por uma base comum, onde os artistas abordam os fundamentos básicos — e é a partir disso que cada artista é conduzido ao aprofundamento de sua prática.</p>")}
  {acordeao(ENSINO)}
</section>
<section class="secao" id="trabalhos">
  <h2 class="t2 wrap rev">Trabalhos de Alunos</h2>
  <div class="tres trabalhos wrap">
    <figure><img src="img/trabalho-1.jpg" alt="Trabalho de aluno" loading="lazy"></figure>
    <figure><img src="img/trabalho-2.jpg" alt="Trabalho de aluno" loading="lazy"></figure>
    <figure><img src="img/trabalho-3.jpg" alt="Trabalho de aluno" loading="lazy"></figure>
  </div>
  <div class="wrap"><hr class="filete"></div>
</section>
<section class="secao wrap" id="faq">
  {intro("FAQ", "<p>O que mais nos perguntam antes da primeira aula. Outras dúvidas podem ser enviadas pelo WhatsApp ou por e-mail.*</p>")}
  {acordeao(FAQ)}
</section>''')

    # ---------------- Blog ----------------
    POSTS = [("blog-1.jpg", "Materiais", "História dos pigmentos e do meio que os carrega", "Pigmento é matéria seca e inerte. O meio que o carrega decide o brilho, a secagem e a permanência da cor."),
             ("blog-2.jpg", "Percepção Visual", "Movimento e ritmo na percepção da forma", "A mesa permanece retangular enquanto você caminha ao redor dela. A forma resiste à mudança de aparência."),
             ("blog-3.jpg", "Teoria", "Grisaille e a construção do valor tonal", "A chave tonal se estabelece antes da primeira mistura: o valor decide de onde vem a luz e o que fica na sombra."),
             ("blog-4.jpg", "História da Arte", "Chiaroscuro e o peso construtivo da sombra", "Em Caravaggio a sombra ganha peso construtivo e passa a sustentar a figura com a força do claro."),
             ("blog-5.jpg", "Prática", "Velatura e a cor que nasce da luz refletida", "Camada transparente sobre camada seca. A cor não nasce da mistura: nasce da luz que atravessa e volta refletida."),
             ("blog-6.jpg", "Pensamento", "Pentimento e a memória do próprio processo", "O traço que a decisão anterior deixa visível na superfície. A obra guarda a memória do próprio processo."),
             ("blog-7.jpg", "Estética", "Albers e a interação entre cores vizinhas", "Nenhuma cor é vista isolada. O tom muda conforme a vizinhança, e é essa comparação que a prática exercita."),
             ("blog-8.jpg", "Fotografia", "Frontalidade e obliquidade no enquadramento", "A posição da câmera diante do plano decide antes da luz: frontalidade organiza, obliquidade abre profundidade."),
             ("blog-9.jpg", "Cinema", "Kepes e a composição em movimento", "Movimento como condição da vida moderna, e a disciplina formal — ritmo, sequência, unidade — acima da novidade.")]
    TAGS = ["Materiais", "Percepção Visual", "Teoria", "História da Arte", "Prática", "Pensamento", "Estética", "Fotografia", "Cinema"]
    pagina("blog.html", "Blog · Alma", "Notas e Ensaios: textos sobre percepção visual, processos de criação, técnica e história da arte.",
      f'''<section class="abertura curta wrap"><h1 class="t1">Blog</h1>
  <p>Notas e ensaios sobre percepção visual, processos de criação, técnica, história da arte e pensamento artístico. Aqui, reunimos reflexões que atravessam a prática do atelier e ampliam o olhar sobre a Arte.</p>
  <div class="busca">
    <label for="q">O que você procura?</label>
    <div class="barra"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.6"><circle cx="10.5" cy="10.5" r="6.5"/><path d="m15.5 15.5 5 5"/></svg>
      <input id="q" type="search" placeholder="Cores complementares" autocomplete="off"></div>
  </div>
  <div class="tags" role="group" aria-label="Filtrar por tema">{"".join(f'<button type="button" aria-pressed="false" data-tag="{t}">{t}</button>' for t in TAGS)}</div>
</section>
<section class="secao wrap">
  <h2 class="t2 contagem" data-total="9">9 textos publicados</h2>
  <div class="posts">''' + "".join(
        f'''<a class="post rev" href="#" data-tag="{tag}"><div class="foto"><img src="img/{img}" alt="" loading="lazy"></div>
<div class="cab"><h3 class="t3">{t}*</h3><span class="pill">{tag}</span></div><p class="corpo">{d}*</p><span class="ler">Ler texto</span></a>''' for img, tag, t, d in POSTS) + f'''</div>
  <p class="vazio" hidden>Nenhum texto encontrado com esses termos.</p>
  <hr class="filete">
</section>
{LOJA_SEC}''', solida=True)

    # ---------------- Faça Parte ----------------
    pagina("faca-parte.html", "Faça Parte · Alma", "Candidate-se para estudar no Alma: conte quem você é e o que procura.",
      '''<section class="abertura curta wrap"><h1 class="t1">Faça Parte</h1>
  <p>O ingresso no Alma começa por uma aula experimental: um primeiro contato com o atelier, a turma e o método de trabalho. Deixe seus dados e combinamos o dia pelo WhatsApp.*</p></section>
<section class="secao wrap" id="ingresso">
  ''' + intro("Como ingressar", "<p>Três passos, da primeira conversa à matrícula.*</p>") + passos(INGRESSO, "tres") + '''
  <hr class="filete">
</section>
<section class="wrap">
  <form class="formulario" data-form="candidatura" novalidate>
    <div class="grade">
      <div class="col">
        <label>Nome<input name="nome" autocomplete="name" required></label>
        <label>E-mail<input name="email" type="email" autocomplete="email" required></label>
      </div>
      <div class="col">
        <label>Whatsapp<input name="whatsapp" type="tel" inputmode="tel" autocomplete="tel" required></label>
        <label>Conte um pouco sobre você<textarea name="mensagem" required placeholder="Sua experiência com arte, o que procura, período de preferência"></textarea></label>
      </div>
    </div>
    <div class="enviar"><button class="btn btn-preto" type="submit">Enviar</button></div>
    <p class="aviso" role="status" style="text-align:right"></p>
  </form>
</section>''', solida=True)

    # ---------------- Contato ----------------
    pagina("contato.html", "Contato · Alma", "Endereço, WhatsApp e e-mail do Alma Centro de Estudos Visuais, em São Caetano do Sul.",
      '''<section class="abertura curta wrap"><h1 class="t1">Contato</h1>
  <p>O Alma fica em São Caetano do Sul, no ABC Paulista. O atendimento acontece de segunda a sábado, e a visita ao atelier pode ser agendada previamente por WhatsApp ou e-mail.*</p></section>
<section class="contatos-sec wrap">
  <div class="duas">
    <div class="lista rev">
      <div><h2 class="t3">Endereço</h2><p class="corpo">Rua São Paulo, 864 — São Caetano do Sul, São Paulo. Entrada pelo portão lateral, sem campainha: bata na porta de vidro.*</p></div>
      <div><h2 class="t3">Whatsapp</h2><p class="corpo"><a href="https://wa.me/5511993196228" target="_blank" rel="noopener">(11) 99319-6228</a>. Canal usado para agendamento de aula experimental, dúvidas sobre turmas e informações sobre materiais.*</p></div>
      <div><h2 class="t3">E-mail</h2><p class="corpo"><a href="mailto:contato@almaestudosvisuais.com.br">contato@almaestudosvisuais.com.br</a> para o atelier. <a href="mailto:loja@almaestudosvisuais.com.br">loja@almaestudosvisuais.com.br</a> para pedidos e materiais.*</p></div>
    </div>
    <iframe class="mapa rev" title="Mapa: Rua São Paulo, 864, São Caetano do Sul" loading="lazy" referrerpolicy="no-referrer-when-downgrade"
      src="https://www.google.com/maps?q=Rua%20S%C3%A3o%20Paulo%2C%20864%2C%20S%C3%A3o%20Caetano%20do%20Sul%20-%20SP&output=embed"></iframe>
  </div>
  <hr class="filete">
</section>
<section class="secao wrap">
  ''' + intro("Parcerias", "<p>Trabalhamos com escolas, instituições culturais e coletivos interessados em formação visual continuada. Propostas de residência, oficina fechada, curadoria de material para turmas e projetos de extensão podem ser apresentadas por e-mail ou WhatsApp.*</p>",
      '<div class="botoes"><a class="btn btn-preto" href="mailto:contato@almaestudosvisuais.com.br?subject=Parcerias">E-mail</a><a class="btn btn-preto" href="#" data-whatsapp>Whatsapp</a></div>') + '''
</section>''', solida=True)

    print("ok:", sorted(os.listdir(SAIDA)))

if __name__ == "__main__":
    build()
