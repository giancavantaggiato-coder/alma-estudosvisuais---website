(function () {
  var C = window.ALMA_CONFIG || {};

  document.documentElement.classList.add('js');

  // Menu em tela cheia (celular)
  var gav = document.getElementById('gaveta'), abrir = document.querySelector('.nav .abrir');
  function menu(on, pelaTecla) {
    if (!gav) return;
    gav.classList.toggle('aberta', on); gav.setAttribute('aria-hidden', on ? 'false' : 'true');
    abrir && abrir.setAttribute('aria-expanded', on ? 'true' : 'false');
    document.body.style.overflow = on ? 'hidden' : '';
    if (on) { var f = gav.querySelector('.fechar'); f && f.focus({ preventScroll: true }); }
    else if (pelaTecla && abrir) abrir.focus({ preventScroll: true });
    else if (document.activeElement && gav.contains(document.activeElement)) document.activeElement.blur();
  }
  abrir && abrir.addEventListener('click', function () { menu(true); });
  document.querySelectorAll('[data-fechar]').forEach(function (b) { b.addEventListener('click', function () { menu(false); }); });
  gav && gav.querySelectorAll('a').forEach(function (a) { a.addEventListener('click', function () { menu(false); }); });
  document.addEventListener('keydown', function (e) { if (e.key === 'Escape' && gav && gav.classList.contains('aberta')) menu(false, true); });

  // Revelar ao rolar
  var rev = document.querySelectorAll('.rev');
  if ('IntersectionObserver' in window) {
    var io = new IntersectionObserver(function (es) {
      es.forEach(function (e) { if (e.isIntersecting) { e.target.classList.add('on'); io.unobserve(e.target); } });
    }, { rootMargin: '0px 0px -6% 0px' });
    rev.forEach(function (el) { io.observe(el); });
  } else rev.forEach(function (el) { el.classList.add('on'); });

  // Cabeçalho da home: transparente sobre a foto, sólido depois dela
  var cab = document.querySelector('.nav');
  // Some ao descer e volta ao subir (como na loja)
  var ultimo = window.scrollY;
  function rolou() {
    if (!cab) return;
    var y = Math.max(window.scrollY, 0), h = cab.offsetHeight;
    if (cab.classList.contains('sobre-foto')) {
      var foto = document.querySelector('main:not([hidden]) .hero');
      cab.classList.toggle('rolou', y > (foto ? foto.offsetHeight - h : 0) - 1);
    }
    if (document.body.style.overflow === 'hidden') { ultimo = y; return; }
    if (y <= h) cab.classList.remove('escondido');
    else if (y > ultimo + 4) cab.classList.add('escondido');
    else if (y < ultimo - 4) cab.classList.remove('escondido');
    ultimo = y;
  }
  cab && cab.addEventListener('focusin', function () { cab.classList.remove('escondido'); });
  window.addEventListener('scroll', rolou, { passive: true });
  window.addEventListener('resize', rolou);
  rolou();

  // Carrosséis: só rolagem, com pontos indicando a posição.
  // Trabalhos de alunos no celular: carrossel contínuo (depois da última volta para a primeira).
  document.querySelectorAll('[data-carr]').forEach(function (c) {
    var t = c.querySelector('.carr__trilho'), orig = Array.prototype.slice.call(t.querySelectorAll('.carr__item')), pts = c.querySelectorAll('.carr-ponto');
    var n = orig.length, loop = c.classList.contains('carr--trab') && n > 1 && matchMedia('(max-width: 749px)').matches;
    if (loop) {
      orig.forEach(function (it) { var a = it.cloneNode(true); a.setAttribute('aria-hidden', 'true'); t.appendChild(a); });
      orig.slice().reverse().forEach(function (it) { var a = it.cloneNode(true); a.setAttribute('aria-hidden', 'true'); t.insertBefore(a, t.firstChild); });
      c.classList.add('carr--loop');
    }
    var itens = t.querySelectorAll('.carr__item');
    function alvo(it) { return loop ? it.offsetLeft - t.offsetLeft - (t.clientWidth - it.offsetWidth) / 2 : it.offsetLeft - t.offsetLeft; }
    function atual() {
      var i = 0, melhor = Infinity;
      itens.forEach(function (it, k) { var d = Math.abs(alvo(it) - t.scrollLeft); if (d < melhor) { melhor = d; i = k; } });
      return i;
    }
    function marcar() {
      var i = atual();
      if (!loop && t.scrollLeft > 0 && t.scrollLeft + t.clientWidth >= t.scrollWidth - 2) i = n - 1;
      var k0 = ((i % n) + n) % n;
      pts.forEach(function (p, k) { if (k === k0) p.setAttribute('aria-current', 'true'); else p.removeAttribute('aria-current'); });
    }
    var volta = 0;
    function reposicionar() {
      if (!loop) return;
      var i = atual();
      if (i < n || i >= 2 * n) {
        var j = i < n ? i + n : i - n;
        t.style.scrollSnapType = 'none';
        t.scrollLeft = alvo(itens[j]);
        t.offsetHeight; t.style.scrollSnapType = '';
      }
    }
    pts.forEach(function (p, k) { p.addEventListener('click', function () { t.scrollTo({ left: alvo(itens[loop ? n + k : k]), behavior: 'smooth' }); }); });
    t.addEventListener('scroll', function () {
      window.requestAnimationFrame(marcar);
      clearTimeout(volta); volta = setTimeout(reposicionar, 140);
    }, { passive: true });
    if ('onscrollend' in window) t.addEventListener('scrollend', function () { clearTimeout(volta); reposicionar(); });
    function inicio() { if (loop) { t.style.scrollSnapType = 'none'; t.scrollLeft = alvo(itens[n]); t.offsetHeight; t.style.scrollSnapType = ''; } marcar(); }
    window.addEventListener('resize', inicio);
    if (document.readyState === 'complete') inicio(); else window.addEventListener('load', inicio);
    inicio();
  });

  // Visitas: página, origem e aparelho. Sem cookies e sem dados pessoais. Não conta a prévia.
  (function () {
    if (!C.url || /\/previa\//.test(location.pathname) || location.protocol === 'file:' || !/almaestudosvisuais\.com\.br$/.test(location.hostname)) return;
    var ref = ''; try { ref = document.referrer ? new URL(document.referrer).hostname : ''; } catch (e) {}
    if (ref === location.hostname) ref = 'interno';
    var camp = new URLSearchParams(location.search).get('utm_source') || null;
    fetch(C.url + '/rest/v1/site_visitas', { method: 'POST', keepalive: true,
      headers: { apikey: C.key, Authorization: 'Bearer ' + C.key, 'Content-Type': 'application/json', Prefer: 'return=minimal' },
      body: JSON.stringify({ pagina: location.pathname.slice(0, 200) || '/', origem: ref ? ref.slice(0, 200) : null, aparelho: matchMedia('(max-width: 749px)').matches ? 'celular' : 'computador', campanha: camp }) })
      .catch(function () {});
  })();

  // Formulários → Supabase (tabela site_contatos, só inserção)
  function enviar(dados) {
    return fetch(C.url + '/rest/v1/site_contatos', {
      method: 'POST',
      headers: { apikey: C.key, Authorization: 'Bearer ' + C.key, 'Content-Type': 'application/json', Prefer: 'return=minimal' },
      body: JSON.stringify(dados)
    }).then(function (r) { if (!r.ok) throw new Error(r.status); });
  }
  var OK = {
    whatsapp: 'Recebemos seu número. Vamos chamar você no WhatsApp para combinar a aula experimental.',
    novidades: 'Inscrição feita. Você vai receber as novidades do Alma neste e-mail.',
    candidatura: 'Recebemos seu pedido. Vamos chamar você no WhatsApp para combinar o dia da aula experimental.',
    aviso: 'Combinado. Avisamos você quando as inscrições abrirem.'
  };
  document.querySelectorAll('form[data-form]').forEach(function (f) {
    f.addEventListener('submit', function (e) {
      e.preventDefault();
      var tipo = f.dataset.form, aviso = f.querySelector('.aviso') || f.parentNode.querySelector('.aviso');
      var d = { tipo: tipo, pagina: location.pathname };
      new FormData(f).forEach(function (v, k) { d[k] = String(v).trim(); });
      if (d.whatsapp !== undefined && d.whatsapp.replace(/\D/g, '').length < 10) return dizer(aviso, 'Confira o número com DDD.');
      if ((tipo === 'novidades' || tipo === 'aviso' || d.email) && !/^[^@\s]+@[^@\s]+\.[^@\s]+$/.test(d.email || '')) return dizer(aviso, 'Confira o e-mail.');
      if (tipo === 'candidatura' && !d.nome) return dizer(aviso, 'Preencha seu nome.');
      if (d.email === '') delete d.email;
      if (d.interesse !== undefined) { d.mensagem = 'Interesse: ' + d.interesse + (d.mensagem ? '\n' + d.mensagem : ''); delete d.interesse; }
      var b = f.querySelector('button[type=submit]'); b.disabled = true;
      enviar(d).then(function () { f.reset(); dizer(aviso, OK[tipo]); })
        .catch(function () { dizer(aviso, 'Não foi possível enviar agora. Escreva para contato@almaestudosvisuais.com.br.'); })
        .finally(function () { b.disabled = false; });
    });
  });
  function dizer(el, t) { if (el) el.textContent = t; }

  // Blog: filtro por tema e busca
  var posts = document.querySelectorAll('.post'), q = document.getElementById('q'), cont = document.querySelector('.contagem'), vazio = document.querySelector('.vazio');
  if (posts.length) {
    var tag = null;
    function sem(t) { return t.normalize('NFD').replace(/[̀-ͯ]/g, '').toLowerCase(); }
    function filtrar() {
      var termo = sem(q ? q.value.trim() : ''), n = 0;
      posts.forEach(function (p) {
        var ok = (!tag || p.dataset.tag === tag) && (!termo || sem(p.textContent).indexOf(termo) >= 0);
        p.hidden = !ok; if (ok) { n++; p.classList.add('on'); }
      });
      var filtrando = tag || termo;
      cont.textContent = filtrando ? n + (n === 1 ? ' texto encontrado' : ' textos encontrados') : cont.dataset.total + ' textos publicados';
      vazio.hidden = n > 0;
    }
    document.querySelectorAll('.tags button').forEach(function (b) {
      b.addEventListener('click', function () {
        var ja = b.getAttribute('aria-pressed') === 'true';
        var alvo = (ja || !b.dataset.tag) ? document.querySelector('.tags button[data-tag=""]') : b;
        document.querySelectorAll('.tags button').forEach(function (x) { x.setAttribute('aria-pressed', x === alvo ? 'true' : 'false'); });
        tag = alvo.dataset.tag || null; var sl = document.getElementById('tema'); if (sl) sl.value = alvo.dataset.tag || ''; filtrar();
      });
    });
    q && q.addEventListener('input', filtrar);
    var sel = document.getElementById('tema');
    sel && sel.addEventListener('change', function () {
      tag = sel.value || null;
      document.querySelectorAll('.tags button').forEach(function (x) { x.setAttribute('aria-pressed', (x.dataset.tag || '') === sel.value ? 'true' : 'false'); });
      filtrar();
    });
  }
})();
