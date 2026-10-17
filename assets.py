"""Ficheiros do site (CSS, JavaScript e HTML) dentro do próprio código.

Assim o site não depende de nenhuma pasta no GitHub: basta o app.py e este ficheiro."""

ASSETS = {
    "chat.css": (
        "text/css; charset=utf-8",
        r''':root{--bg:#dde4ef;--paper:#f2f5fa;--card:#fff;--ink:#0c1a2e;--mut:#55647f;--out:#14396b;--outT:#fff;--hum:#fff3d6;--humL:#d79b14;--acc:#9a7220;--accT:#0b1b33;--gold:#d4ac52;--line:#d5dce9;--nav:#0b1b33;--tint:rgba(154,114,32,.11);--sh:0 1px 2px rgba(11,27,51,.08),0 10px 30px rgba(11,27,51,.12)}
@media(prefers-color-scheme:dark){:root{--bg:#03070d;--paper:#0a1424;--card:#101e34;--ink:#e8eef8;--mut:#93a3bf;--out:#1d4f94;--outT:#fff;--hum:#3a3015;--humL:#e0b85c;--acc:#e0b85c;--accT:#0b1b33;--gold:#e0b85c;--line:#1f3354;--nav:#060f20;--tint:rgba(224,184,92,.12);--sh:0 10px 30px rgba(0,0,0,.5)}}
*{box-sizing:border-box}html,body{height:100%;margin:0}
html{background:var(--bg)}
body{background:var(--paper);color:var(--ink);font:16px/1.5 "Segoe UI",system-ui,-apple-system,Roboto,"Helvetica Neue",sans-serif;display:flex;flex-direction:column;padding-top:env(safe-area-inset-top);-webkit-font-smoothing:antialiased}
header{background:var(--nav);color:#fff;padding:12px 18px;display:flex;gap:13px;align-items:center;box-shadow:inset 0 -3px 0 var(--gold)}
header b{display:block;font-size:17px;font-weight:700;letter-spacing:-.01em;line-height:1.2}
header small{display:block;opacity:.82;font-size:12.5px;margin-top:2px}
header small::before{content:"";display:inline-block;width:7px;height:7px;border-radius:50%;background:#4ade80;margin-right:7px;box-shadow:0 0 0 3px rgba(74,222,128,.22)}
.logo{flex:none;width:48px;height:48px;border-radius:50%;box-shadow:0 0 0 2px rgba(212,172,82,.6)}
.logo.emp{border-radius:12px;background:#fff;object-fit:contain;padding:2px}
.dot.emp{background:#fff;object-fit:contain;padding:3px}
.logo-mini{width:16px;height:16px;border-radius:50%;vertical-align:-3px;margin-right:6px}
.dot{flex:none;width:44px;height:44px;border-radius:12px;background:var(--nav);border:1px solid rgba(212,172,82,.55);color:var(--gold);display:grid;place-items:center;font-weight:700;font-size:20px}
.tag{margin-left:auto;flex:none;font-size:12px;font-weight:700;letter-spacing:.02em;border:1px solid rgba(212,172,82,.6);border-radius:8px;padding:3px 9px;color:#e6c877}
.faixa{display:flex;flex-wrap:wrap;gap:4px 18px;padding:8px 18px;background:var(--card);border-bottom:1px solid var(--line);font-size:12.5px;color:var(--mut)}
.faixa span::before{content:"\2713";color:var(--acc);font-weight:700;margin-right:6px}
#log{flex:1;overflow-y:auto;padding:18px 16px;display:flex;flex-direction:column;gap:10px;scroll-behavior:smooth}
.apresenta{align-self:stretch;display:grid;grid-template-columns:46px 1fr;gap:4px 14px;background:var(--card);border:1px solid var(--line);border-radius:14px;padding:16px;margin-bottom:4px;animation:entra .5s ease both}
.apresenta .dot{width:46px;height:46px;grid-row:span 2}
.apresenta h2{margin:0;font-size:17px;font-weight:700;letter-spacing:-.01em;line-height:1.3;align-self:end}
.apresenta p{margin:0;font-size:14.5px;line-height:1.55;color:var(--mut);max-width:62ch}
@keyframes entra{from{opacity:0;transform:translateY(6px)}to{opacity:1;transform:none}}
.m{max-width:min(84%,560px);padding:10px 14px;border-radius:12px;white-space:pre-wrap;font-size:15.5px;line-height:1.5;overflow-wrap:anywhere}
.m.assistant{background:var(--card);border:1px solid var(--line);align-self:flex-start;border-bottom-left-radius:4px}
.m.me{background:var(--out);color:var(--outT);align-self:flex-end;border-bottom-right-radius:4px}
.m.human{background:var(--hum);border:1px solid var(--line);border-left:4px solid var(--humL);align-self:flex-start;border-bottom-left-radius:4px}
.m small{display:block;color:var(--mut);font-size:11.5px;font-weight:700;margin-bottom:2px}
.m.typing{position:relative;width:70px;min-height:42px;color:transparent;user-select:none}
.m.typing::after{content:"";position:absolute;left:18px;top:50%;width:7px;height:7px;margin-top:-3.5px;border-radius:50%;background:var(--acc);box-shadow:13px 0 var(--acc),26px 0 var(--acc);animation:pisca 1.1s ease-in-out infinite}
@keyframes pisca{0%,100%{opacity:.25}50%{opacity:1}}
.sug{display:grid;grid-template-columns:1fr 1fr;gap:8px;align-self:stretch;margin-top:2px}
.sug-t{grid-column:1/-1;margin:6px 2px 0;font-size:13px;color:var(--mut)}
.tema,.chip{font-family:inherit;color:var(--ink);cursor:pointer}
.tema{display:grid;grid-template-columns:34px 1fr;gap:1px 11px;align-items:center;text-align:left;background:var(--card);border:1px solid var(--line);border-radius:12px;padding:12px;transition:border-color .15s,background-color .15s}
.tema:hover{border-color:var(--acc);background:var(--tint)}
.tema .ti{grid-row:span 2;width:34px;height:34px;border-radius:9px;background:var(--tint);color:var(--acc);display:grid;place-items:center}
.tema svg{width:19px;height:19px;stroke:currentColor;fill:none;stroke-width:1.8;stroke-linecap:round;stroke-linejoin:round}
.tema b{font-size:14.5px;font-weight:700;line-height:1.3}
.tema small{font-size:12.5px;color:var(--mut);line-height:1.35}
.chip{background:transparent;border:1px solid var(--acc);border-radius:999px;padding:6px 12px;font:600 13px system-ui,sans-serif}
form{display:flex;gap:10px;padding:12px 16px;background:var(--card);border-top:1px solid var(--line)}
input{flex:1;min-width:0;border:1px solid var(--line);border-radius:12px;padding:12px 14px;font:16px "Segoe UI",system-ui,sans-serif;background:var(--paper);color:var(--ink)}
input::placeholder{color:var(--mut)}
input:focus{border-color:var(--acc)}
button{font-family:inherit}
form button{background:var(--gold);color:#0b1b33;border:0;border-radius:12px;padding:0 22px;font:700 15px "Segoe UI",system-ui,sans-serif;cursor:pointer}
form button:hover{filter:brightness(1.07)}
button:focus-visible,input:focus-visible{outline:3px solid var(--acc);outline-offset:2px}
footer{text-align:center;font-size:11.5px;line-height:1.4;color:var(--mut);padding:7px 16px calc(8px + env(safe-area-inset-bottom));background:var(--card);border-top:1px solid var(--line)}
@media(max-width:440px){.sug{grid-template-columns:1fr}.tema{padding:10px 12px}.m{max-width:90%}.faixa{gap:2px 14px;padding:6px 16px}.apresenta{padding:14px}header{padding:10px 16px}.logo{width:44px;height:44px}}
@media(min-width:900px){body{max-width:860px;margin:0 auto;box-shadow:var(--sh);border-left:1px solid var(--line);border-right:1px solid var(--line)}}
@media(prefers-reduced-motion:reduce){*{transition:none!important;animation:none!important;scroll-behavior:auto!important}}
''',
    ),
    "chat.js": (
        "application/javascript; charset=utf-8",
        r'''var C = JSON.parse(document.getElementById('cfg').textContent), log = document.getElementById('log'), inp = document.getElementById('t');
var vistas = 0, hum = false, ocupado = false, timer = null, base = '/chat/' + C.slug, sug = null;

function novoId() {
  try {
    if (window.crypto && crypto.randomUUID) return crypto.randomUUID();
    var b = new Uint8Array(16); crypto.getRandomValues(b);
    return Array.prototype.map.call(b, function (x) { return ('0' + x.toString(16)).slice(-2); }).join('');
  } catch (e) { return (String(Math.random()).slice(2) + String(Date.now()) + '0000000000000000').replace(/[^0-9]/g, '').slice(0, 32); }
}
function sid() {
  try {
    var k = 'mt_' + C.slug, s = localStorage.getItem(k);
    if (!s) {
      s = novoId();
      localStorage.setItem(k, s);
    }
    return s;
  } catch (e) { return window.__s || (window.__s = String(Math.random()).slice(2) + String(Date.now())); }
}
var S = sid();

function add(txt, cls) {
  var d = document.createElement('div'); d.className = 'm ' + cls;
  if (cls === 'human') { var s = document.createElement('small'); s.textContent = 'equipa'; d.appendChild(s); }
  d.appendChild(document.createTextNode(txt)); log.appendChild(d); log.scrollTop = log.scrollHeight; return d;
}
function mostrar(ms) {
  ms.forEach(function (m) {
    if (m.id > vistas) vistas = m.id;
    add(m.conteudo, m.remetente === 'user' ? 'me' : m.remetente === 'human' ? 'human' : 'assistant');
  });
}
function parar() { if (timer) { clearInterval(timer); timer = null; } }
function poll() {
  fetch(base + '/mensagens?sessao=' + S + '&desde=' + vistas).then(function (r) { return r.json(); })
    .then(function (j) { mostrar(j.mensagens || []); hum = !!j.humano; if (!hum) parar(); }).catch(function () {});
}
function iniciar() { if (!timer) timer = setInterval(poll, 4000); }

// Perguntas sugeridas para o cliente começar a conversa (temas com descrição)
var TEMAS = [
  { t: 'Produtos e serviços', d: 'Descrições, características e disponibilidade', q: 'Que produtos ou serviços têm?',
    i: '<svg viewBox="0 0 24 24"><path d="M21 8l-9-5-9 5 9 5 9-5z"/><path d="M3 8v8l9 5 9-5V8"/><path d="M12 13v8"/></svg>' },
  { t: 'Preços e pagamento', d: 'Valores, formas de pagamento e entrega', q: 'Quais são os preços e as formas de pagamento?',
    i: '<svg viewBox="0 0 24 24"><path d="M20.6 13.4l-7.2 7.2a2 2 0 0 1-2.8 0L3 13V3h10l7.6 7.6a2 2 0 0 1 0 2.8z"/><circle cx="7.5" cy="7.5" r="1.2"/></svg>' },
  { t: 'Horário e localização', d: 'Quando abrimos e como nos contactar', q: 'Qual é o horário?',
    i: '<svg viewBox="0 0 24 24"><circle cx="12" cy="12" r="9"/><path d="M12 7v5l3 2"/></svg>' },
  { t: 'Falar com uma pessoa', d: 'Passamos a conversa à nossa equipa', q: 'Quero falar com uma pessoa',
    i: '<svg viewBox="0 0 24 24"><circle cx="12" cy="8" r="4"/><path d="M4 21c0-4.4 3.6-7 8-7s8 2.6 8 7"/></svg>' }
];
function sugestoes() {
  sug = document.createElement('div'); sug.className = 'sug';
  var t = document.createElement('p'); t.className = 'sug-t'; t.textContent = 'Escolhe um assunto ou escreve a tua pergunta'; sug.appendChild(t);
  TEMAS.forEach(function (x) {
    var b = document.createElement('button'); b.type = 'button'; b.className = 'tema';
    var ic = document.createElement('span'); ic.className = 'ti'; ic.innerHTML = x.i;
    var n = document.createElement('b'); n.textContent = x.t;
    var d = document.createElement('small'); d.textContent = x.d;
    b.appendChild(ic); b.appendChild(n); b.appendChild(d);
    b.onclick = function () { enviar(x.q); }; sug.appendChild(b);
  });
  log.appendChild(sug);
}
function apresentacao() {
  var c = document.createElement('div'); c.className = 'apresenta';
  var av;
  if (C.logo) { av = document.createElement('img'); av.className = 'dot emp'; av.src = '/logo/' + encodeURIComponent(C.slug) + '?v=' + encodeURIComponent(C.logo); av.alt = ''; }
  else { av = document.createElement('div'); av.className = 'dot'; av.textContent = (C.nome || '').slice(0, 1); }
  var h = document.createElement('h2'); h.textContent = 'Atendimento ' + C.nome;
  var p = document.createElement('p');
  p.textContent = 'Tiro dúvidas sobre produtos, serviços, preços e horários. Sou uma inteligência artificial: se precisares de uma pessoa, passo a conversa à equipa.';
  c.appendChild(av); c.appendChild(h); c.appendChild(p); log.appendChild(c);
}
function saudacao() { apresentacao(); add('Olá! Sou o assistente da ' + C.nome + '. Como posso ajudar?', 'assistant'); sugestoes(); }

function falha(w, msg) { if (w) w.remove(); add(msg, 'assistant'); }

// Resposta normal (sem tempo real): usada se o navegador não suportar streaming ou se este falhar
function enviarNormal(t, w) {
  return fetch(base + '/mensagem', { method: 'POST', headers: { 'Content-Type': 'application/json' }, body: JSON.stringify({ sessao: S, texto: t }) })
    .then(function (r) { return r.json().catch(function () { return {}; }).then(function (j) { return { ok: r.ok, j: j }; }); })
    .then(function (x) {
      if (w) w.remove();
      if (!x.ok) add(x.j.erro || 'Não foi possível enviar. Tenta de novo.', 'assistant');
      else { mostrar(x.j.mensagens || []); hum = !!x.j.humano; if (hum) iniciar(); }
    });
}

function enviar(t) {
  t = t.trim(); if (!t || ocupado) return;
  if (sug) { sug.remove(); sug = null; }
  add(t, 'me'); ocupado = true; inp.focus();
  var w = hum ? null : add('…', 'assistant'); if (w) w.classList.add('typing');
  var fim = function () { ocupado = false; };
  if (!(window.fetch && window.ReadableStream && window.TextDecoder)) {
    return enviarNormal(t, w).catch(function () { falha(w, 'Sem ligação. Tenta de novo.'); }).then(fim);
  }
  fetch(base + '/stream', { method: 'POST', headers: { 'Content-Type': 'application/json' }, body: JSON.stringify({ sessao: S, texto: t }) })
    .then(function (r) {
      var tipo = r.headers.get('content-type') || '';
      if (tipo.indexOf('text/event-stream') < 0) {   // resposta fixa, erro ou pessoa assumiu: vem em JSON
        return r.json().catch(function () { return {}; }).then(function (j) {
          if (w) w.remove();
          if (!r.ok) add(j.erro || 'Não foi possível enviar. Tenta de novo.', 'assistant');
          else { mostrar(j.mensagens || []); hum = !!j.humano; if (hum) iniciar(); }
        });
      }
      var rd = r.body.getReader(), dec = new TextDecoder(), buf = '', bolha = w, texto = '';
      function linha(l) {
        if (l.indexOf('data:') !== 0) return;
        var ev; try { ev = JSON.parse(l.slice(5)); } catch (e) { return; }
        if (ev.t) { texto += ev.t; if (bolha) { bolha.classList.remove('typing'); bolha.textContent = texto; } log.scrollTop = log.scrollHeight; }
        if (ev.substituir && bolha) { texto = ev.substituir; bolha.classList.remove('typing'); bolha.textContent = texto; }
        if (ev.fim && ev.id > vistas) vistas = ev.id;
      }
      function ler() {
        return rd.read().then(function (x) {
          if (x.done) { if (buf) linha(buf.trim()); if (!texto && bolha) { bolha.remove(); add('Não consegui responder. Tenta de novo.', 'assistant'); } return; }
          buf += dec.decode(x.value, { stream: true });
          var partes = buf.split('\n\n'); buf = partes.pop();
          partes.forEach(function (p) { linha(p.trim()); });
          return ler();
        });
      }
      return ler();
    })
    .catch(function () { falha(w, 'Sem ligação. Tenta de novo.'); })
    .then(fim);
}

fetch(base + '/mensagens?sessao=' + S + '&desde=0&tudo=1').then(function (r) { return r.json(); }).then(function (j) {
  var ms = j.mensagens || [];
  if (ms.length) { mostrar(ms); hum = !!j.humano; if (hum) iniciar(); } else saudacao();
}).catch(saudacao);

document.getElementById('f').onsubmit = function (e) { e.preventDefault(); var t = inp.value; inp.value = ''; enviar(t); };
''',
    ),
    "logo.svg": (
        "image/svg+xml; charset=utf-8",
        r'''<svg xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" viewBox="0 0 320 320"><defs><clipPath id="c"><circle cx="160" cy="160" r="160"/></clipPath></defs><image width="320" height="320" clip-path="url(#c)" xlink:href="data:image/jpeg;base64,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"/></svg>''',
    ),
    "logo.js": (
        "application/javascript; charset=utf-8",
        r'''window.MTLogo = {
  ler: function (file) {
    return new Promise(function (ok, no) {
      if (!file) { no(new Error('Escolhe uma imagem.')); return; }
      if (!/^image\/(png|jpeg|webp)$/.test(file.type)) { no(new Error('Usa uma imagem PNG, JPG ou WebP.')); return; }
      if (file.size > 10 * 1048576) { no(new Error('Imagem demasiado grande.')); return; }
      function fim(origem, w, h) {
        var k = Math.min(1, 256 / Math.max(w, h)), c = document.createElement('canvas');
        c.width = Math.max(1, Math.round(w * k)); c.height = Math.max(1, Math.round(h * k));
        c.getContext('2d').drawImage(origem, 0, 0, c.width, c.height);
        var u = c.toDataURL('image/png');
        if (u.length > 300000) {
          var c2 = document.createElement('canvas'); c2.width = c.width; c2.height = c.height;
          var x = c2.getContext('2d'); x.fillStyle = '#fff'; x.fillRect(0, 0, c2.width, c2.height); x.drawImage(c, 0, 0);
          u = c2.toDataURL('image/jpeg', 0.85); c = c2;
        }
        if (u.length > 420000) { no(new Error('Imagem demasiado pesada. Use uma mais simples.')); return; }
        ok({ url: u, canvas: c });
      }
      if (window.createImageBitmap) {
        createImageBitmap(file).then(function (b) { fim(b, b.width, b.height); }, function () { no(new Error('Não foi possível ler a imagem.')); });
      } else {
        var im = new Image(), url = URL.createObjectURL(file);
        im.onload = function () { fim(im, im.width, im.height); URL.revokeObjectURL(url); };
        im.onerror = function () { no(new Error('Não foi possível ler a imagem.')); };
        im.src = url;
      }
    });
  },
  desenhar: function (canvas, origem) {
    var x = canvas.getContext('2d'); x.clearRect(0, 0, canvas.width, canvas.height);
    if (!origem) return;
    var k = Math.min(canvas.width / origem.width, canvas.height / origem.height), w = origem.width * k, h = origem.height * k;
    x.drawImage(origem, (canvas.width - w) / 2, (canvas.height - h) / 2, w, h);
  }
};
''',
    ),
    "painel.css": (
        "text/css; charset=utf-8",
        r''':root{--bg:#e4e9f2;--card:#fff;--ink:#0c1a2e;--mut:#55647f;--acc:#14396b;--accT:#fff;--line:#d5dce9;--off:#ffd9d4;--nav:#0b1b33;--gold:#d4ac52;--goldd:#9a7220;--tint:rgba(154,114,32,.11);--sh:0 1px 2px rgba(11,27,51,.06),0 8px 24px rgba(11,27,51,.07)}
@media(prefers-color-scheme:dark){:root{--bg:#03070d;--card:#101e34;--ink:#e8eef8;--mut:#93a3bf;--acc:#e0b85c;--accT:#0b1b33;--line:#1f3354;--off:#5a2a25;--gold:#e0b85c;--goldd:#e0b85c;--tint:rgba(224,184,92,.12);--sh:none}}
*{box-sizing:border-box}[hidden]{display:none!important}
html{scroll-behavior:smooth}
body{margin:0;background:var(--bg);color:var(--ink);font:16px/1.5 "Segoe UI",system-ui,-apple-system,Roboto,sans-serif;-webkit-font-smoothing:antialiased}
header{position:sticky;top:0;z-index:5;background:var(--nav);color:#fff;padding:11px 16px;margin-bottom:16px;font-size:19px;display:flex;gap:10px;align-items:center;box-shadow:inset 0 -3px 0 var(--gold)}
header span{color:var(--gold)}header .msg{color:rgba(255,255,255,.75);margin:0}header button{margin-left:auto}header .btn.alt{color:#fff;border-color:rgba(255,255,255,.45)}
.logo{width:36px;height:36px;border-radius:50%;flex:none;box-shadow:0 0 0 2px rgba(212,172,82,.6)}
main{max-width:760px;margin:0 auto;padding:0 14px 40px}
.titulo{margin:2px 0 12px}.titulo h1{font-size:26px;line-height:1.2;letter-spacing:-.02em;margin:0 0 2px}.titulo p{margin:0;color:var(--mut)}
.atalhos{display:flex;gap:8px;overflow-x:auto;margin:0 -14px 12px;padding:2px 14px;scrollbar-width:none}.atalhos::-webkit-scrollbar{display:none}
.atalhos a{flex:none;text-decoration:none;font-size:13.5px;font-weight:600;color:var(--ink);background:var(--card);border:1px solid var(--line);border-radius:999px;padding:6px 14px}
.atalhos a:hover{border-color:var(--goldd)}
.card{background:var(--card);border:1px solid var(--line);border-radius:16px;padding:16px;margin-bottom:14px;box-shadow:var(--sh);scroll-margin-top:72px}
.sh{display:flex;gap:12px;align-items:flex-start;margin-bottom:10px}
.sh .ic{flex:none;width:38px;height:38px;border-radius:11px;background:var(--nav);color:var(--gold);display:grid;place-items:center}
.sh svg{width:20px;height:20px;fill:none;stroke:currentColor;stroke-width:1.8;stroke-linecap:round;stroke-linejoin:round}
.sh h2{margin:0;font-size:18px;line-height:1.3}
.desc{margin:2px 0 0;font-size:14px;color:var(--mut)}
h2{margin:0 0 8px;font-size:19px}
label{display:block;font-size:13.5px;font-weight:600;color:var(--mut);margin:12px 0 4px}
.chk{display:flex;gap:8px;align-items:center;color:var(--ink);font-size:15px;font-weight:400}
input,textarea,select{width:100%;border:1px solid var(--line);border-radius:12px;padding:10px 12px;font:16px "Segoe UI",system-ui,sans-serif;background:var(--bg);color:var(--ink)}
input:focus,textarea:focus,select:focus{border-color:var(--goldd);outline:0;box-shadow:0 0 0 3px var(--tint)}
input[type=checkbox]{width:auto}
.row{display:flex;gap:8px;margin-top:8px;flex-wrap:wrap}.row input{flex:1;min-width:0}
.btn{background:var(--acc);color:var(--accT);border:0;border-radius:10px;padding:9px 16px;font:700 14px "Segoe UI",system-ui,sans-serif;cursor:pointer}
.btn:hover{filter:brightness(1.08)}
.btn.alt{background:transparent;color:var(--ink);border:1px solid var(--line)}.btn.alt:hover{border-color:var(--goldd);filter:none}
.btn:focus-visible,input:focus-visible,textarea:focus-visible,select:focus-visible,a:focus-visible{outline:3px solid var(--goldd);outline-offset:2px}
.msg{color:var(--mut);font-size:14px;margin:6px 0;word-break:break-word}
.abre>summary{cursor:pointer;font-weight:700;color:var(--acc);padding:6px 0}
.item{border-top:1px solid var(--line);padding:12px 0}
.item:first-child{border-top:0}
.cab{display:flex;gap:12px;align-items:center;margin-bottom:2px}.cab-t b{font-size:17px}
.av{width:46px;height:46px;border-radius:12px;background:var(--nav);color:var(--gold);display:grid;place-items:center;font-weight:700;font-size:20px;overflow:hidden;flex:none;border:1px solid var(--line)}
.av img{width:100%;height:100%;object-fit:contain;background:#fff;display:block}.av canvas{max-width:100%;max-height:100%;background:#fff}
.lgf{display:flex;align-items:center;gap:14px;margin-top:6px}.lgf canvas{width:64px;height:64px;border-radius:14px;border:1px dashed var(--line);background:var(--bg);flex:none}
.lgf .av{width:64px;height:64px;border-radius:14px;font-size:26px}.lgf input{padding:8px}
.badge{display:inline-block;border-radius:999px;padding:1px 10px;font-size:12px;font-weight:700;background:var(--acc);color:var(--accT)}
.badge.off{background:var(--off);color:var(--ink)}
a{color:var(--acc)}
@media(prefers-reduced-motion:reduce){html{scroll-behavior:auto}.btn{transition:none}}
''',
    ),
    "painel.html": (
        "text/html; charset=utf-8",
        r'''<!DOCTYPE html>
<html lang="pt"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>MacTech · Painel</title>
<link rel="icon" href="/static/logo.svg"><link rel="stylesheet" href="/static/painel.css">
</head><body>
<header><img class="logo" src="/static/logo.svg" alt="" width="36" height="36"><b>Mac<span>Tech</span></b> · Painel <button id="sair" class="btn alt" type="button" hidden>Sair</button></header>
<main>
<section id="entrar" class="card">
<h2>Entrar</h2>
<p class="msg">Escreve a chave de administração (a tua ADMIN_API_KEY).</p>
<form id="fl" class="row"><input id="k" type="password" autocomplete="current-password" aria-label="Chave de administração" required><button class="btn" type="submit">Entrar</button></form>
<p id="ml" class="msg"></p>
</section>
<div id="painel" hidden>
<div class="titulo"><h1>Painel do dono</h1><p>Gira empresas, pagamentos e conversas num só lugar.</p></div>
<nav class="atalhos" aria-label="Secções"><a href="#sec-registar">Registar</a><a href="#sec-empresas">Empresas</a><a href="#sec-humanos">À espera de pessoa</a><a href="#sec-tickets">Tickets</a><a href="#sec-conversas">Conversas</a><a href="#sec-exportar">Exportar</a></nav>
<section class="card" id="sec-registar"><div class="sh"><span class="ic"><svg viewBox="0 0 24 24"><path d="M12 5v14M5 12h14"/></svg></span><div><h2>Registar empresa</h2><p class="desc">Crie uma empresa nova, defina o que o assistente sabe e, se quiser, envie o logótipo.</p></div></div>
<details class="abre"><summary>Abrir formulário de registo</summary>
<form id="fe">
<div class="row"><button class="btn alt" id="ex" type="button">Preencher com um exemplo</button></div>
<label for="en">Nome da empresa</label><input id="en" required>
<label for="elg">Logótipo (opcional)</label><div class="lgf"><canvas id="elgp" width="64" height="64" aria-label="Pré-visualização do logótipo"></canvas><input id="elg" type="file" accept="image/png,image/jpeg,image/webp"></div>
<label for="es">Sector (ex.: loja de tecnologia, clínica)</label><input id="es">
<label for="ed">O que a empresa faz</label><textarea id="ed" rows="2"></textarea>
<label for="epd">Produtos ou serviços (um por linha, com detalhes)</label><textarea id="epd" rows="4" required></textarea>
<label for="eho">Horário</label><input id="eho">
<label for="elo">Contactos e localização</label><input id="elo">
<label for="epo">Garantia, entrega e pagamento</label><textarea id="epo" rows="2"></textarea>
<label for="eex">Regras extra para o bot</label><textarea id="eex" rows="2"></textarea>
<label class="chk"><input type="checkbox" id="eh" checked> A empresa tem equipa para atender pessoas</label>
<div class="row"><button class="btn" type="submit">Registar empresa</button></div>
<p id="me" class="msg"></p>
</form></details>
</section>
<section class="card" id="sec-sistema"><div class="sh"><span class="ic"><svg viewBox="0 0 24 24"><path d="M3 12h4l3-8 4 16 3-8h4"/></svg></span><div><h2>Estado do sistema</h2><p class="desc">Verifica se a base de dados, a IA e o WhatsApp estão a funcionar.</p></div></div>
<div class="row"><button class="btn" id="dg" type="button">Testar sistema</button></div><div id="dgr"></div></section>
<section class="card" id="sec-n4"><div class="sh"><span class="ic"><svg viewBox="0 0 24 24"><path d="M12 3l9 5-9 5-9-5 9-5zM3 13l9 5 9-5"/></svg></span><div><h2>Nível 4: departamentos, atendentes e ligações</h2><p class="desc">Departamentos, atendentes e as ferramentas que a IA pode usar (stock, encomendas, faturas).</p></div></div>
<label for="n4e">Empresa</label><select id="n4e"></select>
<label for="n4d">Novo departamento (ex.: Vendas, Suporte, Financeiro)</label>
<div class="row"><input id="n4d"><button class="btn" id="n4db" type="button">Adicionar</button></div>
<label for="n4an">Novo atendente (nome) e departamento (opcional)</label>
<div class="row"><input id="n4an" placeholder="Nome"><input id="n4ad" placeholder="Departamento"><button class="btn" id="n4ab" type="button">Criar</button></div>
<label>Ferramentas da IA</label>
<div class="row"><label class="chk"><input type="checkbox" class="n4f" value="stock"> Stock</label>
<label class="chk"><input type="checkbox" class="n4f" value="encomendas"> Encomendas</label>
<label class="chk"><input type="checkbox" class="n4f" value="fatura"> Pedir fatura</label>
<label class="chk"><input type="checkbox" class="n4f" value="departamentos" checked> Departamentos</label></div>
<label for="n4u">Endereço do CRM/ERP da empresa (https, opcional)</label><input id="n4u" placeholder="https://erp.empresa.ao/mactech">
<label for="n4s">Segredo para assinar os pedidos (só se usares o endereço)</label><input id="n4s" type="password" autocomplete="off">
<div class="row"><button class="btn" id="n4ib" type="button">Guardar ferramentas</button></div>
<label for="n4p">Produtos (uma linha cada: referência;nome;preço;stock)</label><textarea id="n4p" rows="3"></textarea>
<div class="row"><button class="btn alt" id="n4pb" type="button">Importar produtos</button></div>
<label for="n4o">Encomendas (uma linha cada: código;telefone ou email;estado;itens;total)</label><textarea id="n4o" rows="3"></textarea>
<div class="row"><button class="btn alt" id="n4ob" type="button">Importar encomendas</button></div>
<p id="n4m" class="msg"></p></section>
<section class="card" id="sec-tickets"><div class="sh"><span class="ic"><svg viewBox="0 0 24 24"><path d="M4 7h16v4a2 2 0 0 0 0 4v4H4v-4a2 2 0 0 0 0-4V7z"/></svg></span><div><h2>Tickets abertos</h2><p class="desc">Pedidos dos clientes que ainda precisam de uma ação da equipa.</p></div></div><div id="tkadm"></div></section>
<section class="card" id="sec-empresas"><div class="sh"><span class="ic"><svg viewBox="0 0 24 24"><path d="M4 21V5l8-2v18M12 9h8v12M7 9h2M7 13h2M7 17h2M15 13h2M15 17h2"/></svg></span><div><h2>Empresas</h2><p class="desc">Estado, validade, link do chat e logótipo de cada empresa.</p></div></div><div id="lista"></div></section>
<section class="card" id="sec-humanos"><div class="sh"><span class="ic"><svg viewBox="0 0 24 24"><circle cx="12" cy="8" r="4"/><path d="M4 21c0-4.4 3.6-7 8-7s8 2.6 8 7"/></svg></span><div><h2>Conversas à espera de uma pessoa</h2><p class="desc">Clientes que pediram para falar com alguém. Responda daqui.</p></div></div><div id="humanos"></div></section>
<section class="card" id="sec-conversas"><div class="sh"><span class="ic"><svg viewBox="0 0 24 24"><path d="M21 12a8 8 0 0 1-11.6 7.1L4 20l1-4.6A8 8 0 1 1 21 12z"/></svg></span><div><h2>Conversas recentes</h2><p class="desc">As últimas conversas de todas as empresas.</p></div></div><div id="conversas"></div><div id="transc"></div></section>
<section class="card" id="sec-semresp"><div class="sh"><span class="ic"><svg viewBox="0 0 24 24"><circle cx="12" cy="12" r="9"/><path d="M9.5 9.5a2.5 2.5 0 1 1 3.5 2.3c-.7.4-1 .9-1 1.7M12 17h.01"/></svg></span><div><h2>Perguntas que o bot não soube responder</h2><p class="desc">Acrescente estas respostas ao catálogo da empresa para o bot melhorar.</p></div></div>
<div id="semresp"></div></section>
<section class="card" id="sec-exportar"><div class="sh"><span class="ic"><svg viewBox="0 0 24 24"><path d="M12 4v11M7 11l5 5 5-5M5 20h14"/></svg></span><div><h2>Exportar</h2><p class="desc">Descarregue contactos, conversas e uma cópia de segurança.</p></div></div>
<div class="row"><button class="btn alt" id="csv" type="button">Descarregar contactos e conversas (CSV)</button></div>
<div class="row"><button class="btn alt" id="backup" type="button">Descarregar cópia de segurança (empresas e catálogo)</button></div></section>
</div>
</main>
<script src="/static/logo.js"></script>
<script src="/static/painel.js"></script>
</body></html>
''',
    ),
    "painel.js": (
        "application/javascript; charset=utf-8",
        r'''(function () {
  var K = sessionStorage.getItem('mt_admin') || '', tm = null;
  function $(i) { return document.getElementById(i); }
  function h(t, c, x) { var e = document.createElement(t); if (c) e.className = c; if (x != null) e.textContent = x; return e; }
  function erro(x) { alert(x.message); }
  var LG = {}, LOGO_NOVO = null;
  function avatar(e) {
    var a = h('div', 'av'), slug = e.chat_url ? e.chat_url.split('/').pop() : '';
    if (slug && LG[e.id]) { var im = h('img'); im.src = '/logo/' + encodeURIComponent(slug) + '?v=' + LG[e.id]; im.alt = ''; a.appendChild(im); }
    else a.textContent = (e.nome || '?').slice(0, 1).toUpperCase();
    return a;
  }

  // Pedido à API com a chave de administração
  function api(m, u, b) {
    return fetch(u, { method: m, headers: { 'X-API-Key': K, 'Content-Type': 'application/json' }, body: b ? JSON.stringify(b) : undefined })
      .then(function (r) {
        return r.json().catch(function () { return {}; }).then(function (j) {
          if (r.status === 401) { sair(); throw new Error('Chave errada'); }
          if (!r.ok) throw new Error(j.erro || ('Erro ' + r.status));
          return j;
        });
      });
  }
  function mostrar(logado) { $('entrar').hidden = logado; $('painel').hidden = !logado; $('sair').hidden = !logado; }
  function sair() { sessionStorage.removeItem('mt_admin'); K = ''; clearInterval(tm); mostrar(false); }
  // ---- Nível 4 ----
  function n4id() { return $('n4e').value; }
  function n4msg(x) { $('n4m').textContent = x; }
  function preencherN4(emps) {
    var s = $('n4e'), at = s.value; s.textContent = '';
    emps.forEach(function (e) { var o = h('option', null, e.nome); o.value = e.id; s.appendChild(o); });
    if (at) s.value = at;
  }
  function linhas(id) { return $(id).value.split('\n').map(function (l) { return l.trim(); }).filter(Boolean).map(function (l) { return l.split(';').map(function (x) { return x.trim(); }); }); }
  function n4pedir(m, u, b, ok) { if (!n4id()) { n4msg('Escolhe uma empresa.'); return; } api(m, u, b).then(function (j) { n4msg(ok(j)); }).catch(function (x) { n4msg(x.message); }); }
  $('n4db').onclick = function () { n4pedir('POST', '/api/empresas/' + n4id() + '/departamentos', { nome: $('n4d').value }, function (j) { $('n4d').value = ''; return 'Departamentos: ' + j.departamentos.map(function (d) { return d.nome; }).join(', '); }); };
  $('n4ab').onclick = function () { n4pedir('POST', '/api/empresas/' + n4id() + '/agentes', { nome: $('n4an').value, departamento: $('n4ad').value }, function (j) { $('n4an').value = ''; $('n4ad').value = ''; return 'Atendente criado. CHAVE (copia agora, não volta a aparecer): ' + j.chave; }); };
  $('n4ib').onclick = function () {
    var f = Array.prototype.filter.call(document.querySelectorAll('.n4f'), function (c) { return c.checked; }).map(function (c) { return c.value; });
    var b = { ferramentas: f }; if ($('n4u').value.trim()) b.url = $('n4u').value.trim(); if ($('n4s').value) b.segredo = $('n4s').value;
    n4pedir('POST', '/api/empresas/' + n4id() + '/integracao', b, function (j) { $('n4s').value = ''; return 'Ferramentas ativas: ' + (j.ferramentas.join(', ') || 'nenhuma') + (j.url ? ' · ligado a ' + j.url : ''); });
  };
  $('n4pb').onclick = function () {
    var p = linhas('n4p').map(function (c) { return { sku: c[0], nome: c[1], preco: c[2], stock: c[3] }; });
    n4pedir('POST', '/api/empresas/' + n4id() + '/produtos', { produtos: p }, function (j) { return j.importados + ' produtos importados.'; });
  };
  $('n4ob').onclick = function () {
    var o = linhas('n4o').map(function (c) { return { codigo: c[0], contacto: c[1], estado: c[2], itens: c[3], total: c[4] }; });
    n4pedir('POST', '/api/empresas/' + n4id() + '/encomendas', { encomendas: o }, function (j) { return j.importadas + ' encomendas importadas.'; });
  };
  function carregarTickets() {
    api('GET', '/api/tickets').then(function (j) {
      var L = $('tkadm'); L.textContent = '';
      if (!j.tickets.length) { L.appendChild(h('p', 'msg', 'Nenhum ticket aberto.')); return; }
      j.tickets.forEach(function (t) {
        var d = h('div', 'item'); d.appendChild(h('b', null, (t.departamento || 'Geral') + ' · ' + t.tipo)); d.appendChild(h('p', 'msg', t.assunto));
        var b = h('button', 'btn alt', 'Fechar'); b.type = 'button';
        b.onclick = function () { api('POST', '/api/tickets/' + t.id + '/fechar').then(carregarTickets).catch(erro); };
        d.appendChild(b); L.appendChild(d);
      });
    }).catch(function () {});
  }

  function iniciar() { mostrar(true); carregarTickets(); carregarEmpresas(); carregarHumanos(); carregarConversas(); carregarSemResposta(); clearInterval(tm); tm = setInterval(function () { carregarHumanos(); carregarTickets(); }, 15000); }

  $('fl').onsubmit = function (e) {
    e.preventDefault(); K = $('k').value.trim();
    api('GET', '/api/empresas').then(function () {
      sessionStorage.setItem('mt_admin', K); $('k').value = ''; $('ml').textContent = ''; iniciar();
    }).catch(function (x) { $('ml').textContent = x.message; });
  };
  $('sair').onclick = sair;

  function carregarEmpresas() {
    Promise.all([api('GET', '/api/empresas'), api('GET', '/api/estatisticas?dias=7'), api('GET', '/api/pedidos'), api('GET', '/api/logos').catch(function () { return { logos: {} }; })]).then(function (r) {
      LG = r[3].logos || {}; preencherN4(r[0].empresas); var st = {}; r[1].empresas.forEach(function (s) { st[s.empresa] = s; });
      var L = $('lista'); L.textContent = '';
      if (!r[0].empresas.length) { L.appendChild(h('p', 'msg', 'Ainda não há empresas. Regista a primeira acima.')); return; }
      r[0].empresas.forEach(function (e) {
        var c = h('div', 'item'), cab = h('div', 'cab'), tt = h('div', 'cab-t');
        cab.appendChild(avatar(e)); cab.appendChild(tt); c.appendChild(cab);
        tt.appendChild(h('b', null, e.nome + ' '));
        var vd = e.estado === 'ativo' ? e.plano_ate : e.teste_ate, fim = (e.estado === 'teste' || e.estado === 'ativo') && vd ? ' até ' + new Date(vd).toLocaleString('pt-PT') : '';
        tt.appendChild(h('span', 'badge' + (e.ativa ? '' : ' off'), e.estado + fim));
        var ped = r[2].pedidos[e.id];
        if (ped) c.appendChild(h('p', 'msg', 'Contacto: ' + ped.contacto + ' · Ref. pagamento: ' + ped.ref_pagamento));
        var s = st[e.nome];
        if (s) c.appendChild(h('p', 'msg', 'Últimos 7 dias: ' + s.pessoas + ' pessoas · ' + s.mensagens_clientes + ' mensagens · ' + s.contactos_recolhidos + ' contactos · ' + s.perguntas_sem_resposta + ' sem resposta'));
        var b = h('div', 'row');
        if (e.chat_url) {
          var url = location.origin + e.chat_url, p = h('p', 'msg'), a = h('a', null, url);
          a.href = url; a.target = '_blank'; a.rel = 'noopener'; p.appendChild(a); c.appendChild(p);
          var cp = h('button', 'btn', 'Abrir chat'); cp.type = 'button';
          cp.onclick = function () { window.open(url, '_blank'); }; b.appendChild(cp);
          var cc = h('button', 'btn alt', 'Copiar link'); cc.type = 'button';
          cc.onclick = function () { try { navigator.clipboard.writeText(url); cc.textContent = 'Copiado'; } catch (x) { prompt('Copia o link:', url); } };
          b.appendChild(cc);
        }
        [['Pagou: ativar/renovar +1 mês', 'ativo'], ['Suspender', 'suspenso'], ['+1 dia de teste', 'teste']].forEach(function (x) {
          var bt = h('button', 'btn alt', x[0]); bt.type = 'button';
          bt.onclick = function () { api('POST', '/api/empresas/' + e.id + '/estado', { estado: x[1], dias: 1, meses: 1 }).then(carregarEmpresas).catch(erro); };
          b.appendChild(bt);
        });
        var kb = h('button', 'btn alt', e.tem_chave ? 'Nova chave da empresa' : 'Gerar chave da empresa'); kb.type = 'button';
        kb.onclick = function () { api('POST', '/api/empresas/' + e.id + '/chave').then(function (j) { prompt('Copia e envia à empresa (só aparece agora):', j.chave); carregarEmpresas(); }).catch(erro); };
        b.appendChild(kb);
        var lb = h('button', 'btn alt', LG[e.id] ? 'Mudar logótipo' : 'Adicionar logótipo'); lb.type = 'button';
        var lf = h('input'); lf.type = 'file'; lf.accept = 'image/png,image/jpeg,image/webp'; lf.hidden = true;
        lb.onclick = function () { lf.click(); };
        lf.onchange = function () { MTLogo.ler(lf.files[0]).then(function (x) { return api('PUT', '/api/empresas/' + e.id + '/logo', { logo: x.url }); }).then(carregarEmpresas).catch(erro); };
        b.appendChild(lb); b.appendChild(lf);
        if (LG[e.id]) { var lr = h('button', 'btn alt', 'Remover logótipo'); lr.type = 'button'; lr.onclick = function () { api('DELETE', '/api/empresas/' + e.id + '/logo').then(carregarEmpresas).catch(erro); }; b.appendChild(lr); }
        c.appendChild(b); L.appendChild(c);
      });
    }).catch(function (x) { $('lista').textContent = x.message; });
  }

  function carregarHumanos() {
    api('GET', '/api/conversas-humano').then(function (j) {
      var L = $('humanos');
      if (L.contains(document.activeElement) && document.activeElement.tagName === 'INPUT') return; // não interromper quem está a escrever
      L.textContent = '';
      if (!j.conversas.length) { L.appendChild(h('p', 'msg', 'Nenhuma conversa à espera.')); return; }
      j.conversas.forEach(function (c) {
        var d = h('div', 'item'), num = c.cliente_numero.length > 14 ? c.cliente_numero.slice(0, 8) + '…' : c.cliente_numero;
        d.appendChild(h('b', null, (c.empresa || '?') + ' · ' + num + ' · ' + (c.phone_number_id === 'web' ? 'chat web' : 'WhatsApp')));
        d.appendChild(h('p', 'msg', 'Última mensagem (' + c.ultimo_remetente + '): ' + (c.ultima_mensagem || '')));
        var f = h('form', 'row'), i = h('input'), s = h('button', 'btn', 'Enviar');
        i.placeholder = 'Resposta para o cliente'; i.setAttribute('aria-label', 'Resposta'); s.type = 'submit';
        f.appendChild(i); f.appendChild(s);
        f.onsubmit = function (ev) {
          ev.preventDefault(); var t = i.value.trim(); if (!t) return;
          api('POST', '/api/responder-humano', { phone_number_id: c.phone_number_id, cliente_numero: c.cliente_numero, texto: t })
            .then(function () { i.value = ''; alert('Enviado.'); }).catch(erro);
        };
        var dv = h('button', 'btn alt', 'Devolver à IA'); dv.type = 'button';
        dv.onclick = function () { api('POST', '/api/devolver-ia', { phone_number_id: c.phone_number_id, cliente_numero: c.cliente_numero }).then(carregarHumanos).catch(erro); };
        d.appendChild(f); d.appendChild(dv); L.appendChild(d);
      });
    }).catch(function () {});
  }

  // Formulário: monta o texto que a IA vai usar e regista a empresa
  function v(i) { return $(i).value.trim(); }
  $('ex').onclick = function () {
    $('en').value = 'Loja Demo'; $('es').value = 'loja de tecnologia';
    $('ed').value = 'Vende telemóveis, portáteis e acessórios.';
    $('epd').value = 'Portátil Pro 14: 16 GB de RAM, SSD de 512 GB, bateria até 12 h\nTelemóvel Lite 5G: 128 GB, câmara de 50 MP, dual SIM\nAuscultadores Air: Bluetooth, cancelamento de ruído, 30 h de autonomia';
    $('eho').value = 'Segunda a sábado, 8h às 18h'; $('elo').value = 'Luanda';
    $('epo').value = 'Garantia de 1 ano nos equipamentos.'; $('eex').value = '';
  };
  $('elg').onchange = function () {
    MTLogo.ler(this.files[0]).then(function (x) { LOGO_NOVO = x.url; MTLogo.desenhar($('elgp'), x.canvas); })
      .catch(function (x) { LOGO_NOVO = null; $('me').textContent = x.message; });
  };
  $('fe').onsubmit = function (ev) {
    ev.preventDefault();
    var pr = v('en') + (v('es') ? ' (' + v('es') + ')' : '') + '. ' + v('ed') + '\nProdutos e serviços:\n' +
      v('epd').split('\n').filter(Boolean).map(function (l) { return '- ' + l; }).join('\n') +
      (v('eho') ? '\nHorário: ' + v('eho') : '') + (v('elo') ? '\nContactos e localização: ' + v('elo') : '') +
      (v('epo') ? '\nGarantia, entrega e pagamento: ' + v('epo') : '') + (v('eex') ? '\nRegras extra: ' + v('eex') : '');
    api('POST', '/api/empresas', { nome: v('en'), system_prompt: pr, humano_ativo: $('eh').checked }).then(function (j) {
      var p = LOGO_NOVO ? api('PUT', '/api/empresas/' + j.id + '/logo', { logo: LOGO_NOVO }).catch(function () {}) : Promise.resolve();
      return p.then(function () { return j; });
    }).then(function (j) {
      $('me').textContent = 'Empresa registada. Chat: ' + location.origin + j.chat_url + ' (tem 1 dia de teste).';
      $('fe').reset(); $('eh').checked = true; LOGO_NOVO = null; MTLogo.desenhar($('elgp'), null); carregarEmpresas();
    }).catch(function (x) { $('me').textContent = x.message; });
  };

  // Testar o sistema (base de dados, chave e crédito da IA, modelo)
  $('dg').onclick = function () {
    var R = $('dgr'); R.textContent = 'A testar…';
    api('POST', '/api/diagnostico').then(function (j) {
      R.textContent = '';
      [['Base de dados', j.base_de_dados ? 'OK' : 'PROBLEMA'],
       ['IA (' + j.modelo + ')', (j.ia.ok ? 'OK. ' : 'PROBLEMA: ') + j.ia.mensagem],
       ['WhatsApp', j.whatsapp_configurado ? 'configurado' : 'não configurado (normal se só usas o chat web)']
      ].forEach(function (l) { R.appendChild(h('p', 'msg', l[0] + ': ' + l[1])); });
    }).catch(function (x) { R.textContent = x.message; });
  };

  // Conversas recentes e leitura de uma conversa
  function carregarConversas() {
    api('GET', '/api/conversas?limite=20').then(function (j) {
      var L = $('conversas'); L.textContent = '';
      if (!j.conversas.length) { L.appendChild(h('p', 'msg', 'Ainda não há conversas.')); return; }
      j.conversas.forEach(function (c) {
        var d = h('div', 'item');
        d.appendChild(h('b', null, (c.empresa || '?') + ' · ' + c.canal + ' · ' + c.mensagens + ' mensagens' + (c.humano_assumiu ? ' · à espera de pessoa' : '')));
        if (c.contacto) d.appendChild(h('p', 'msg', 'Contacto: ' + c.contacto));
        d.appendChild(h('p', 'msg', c.ultima_mensagem || ''));
        var b = h('button', 'btn alt', 'Ver conversa'); b.type = 'button'; b.onclick = function () { verConversa(c.id); };
        d.appendChild(b); L.appendChild(d);
      });
    }).catch(function () {});
  }
  function verConversa(id) {
    api('GET', '/api/conversas/' + id).then(function (j) {
      var T = $('transc'); T.textContent = ''; T.appendChild(h('h2', null, 'Conversa'));
      j.mensagens.forEach(function (m) {
        var quem = m.remetente === 'user' ? 'Cliente' : m.remetente === 'human' ? 'Equipa' : 'Bot';
        T.appendChild(h('p', 'msg', quem + ': ' + m.conteudo + (m.sem_resposta ? '  (o bot não soube responder)' : '')));
      });
      T.scrollIntoView();
    }).catch(erro);
  }
  function carregarSemResposta() {
    api('GET', '/api/sem-resposta?dias=30').then(function (j) {
      var L = $('semresp'); L.textContent = '';
      if (!j.perguntas.length) { L.appendChild(h('p', 'msg', 'Nenhuma pergunta sem resposta. Bom sinal.')); return; }
      j.perguntas.forEach(function (p) { L.appendChild(h('p', 'msg', (p.empresa || '?') + ': ' + p.pergunta)); });
    }).catch(function () {});
  }
  $('csv').onclick = function () {
    fetch('/api/exportar.csv', { headers: { 'X-API-Key': K } })
      .then(function (r) { if (!r.ok) throw new Error('Erro ' + r.status); return r.blob(); })
      .then(function (b) {
        var a = document.createElement('a'); a.href = URL.createObjectURL(b); a.download = 'mactech_conversas.csv';
        document.body.appendChild(a); a.click(); a.remove();
      }).catch(erro);
  };

  $('backup').onclick = function () {
    fetch('/api/backup', { headers: { 'X-API-Key': K } })
      .then(function (r) { if (!r.ok) throw new Error('Erro ' + r.status); return r.blob(); })
      .then(function (b) {
        var a = document.createElement('a'); a.href = URL.createObjectURL(b); a.download = 'mactech_backup.json';
        document.body.appendChild(a); a.click(); a.remove();
      }).catch(erro);
  };

  if (K) { api('GET', '/api/empresas').then(iniciar).catch(function () { mostrar(false); }); } else { mostrar(false); }
})();
''',
    ),
    "style.css": (
        "text/css; charset=utf-8",
        r'''body{margin:0;min-height:100vh;display:grid;place-items:center;background:#e4e9f2;color:#0c1a2e;font:16px/1.5 system-ui,sans-serif;text-align:center;padding:20px}
h1{font-size:44px;margin:0 0 8px}h1 span{color:#9a7220}p{margin:6px 0;color:#55647f}
.logo{display:block;margin:0 auto 12px;width:96px;height:96px;border-radius:50%}
.btn{display:inline-block;margin-top:10px;background:#14396b;color:#fff;border-radius:999px;padding:10px 20px;font-weight:600;text-decoration:none}
@media(prefers-color-scheme:dark){body{background:#03070d;color:#e8eef8}h1 span{color:#e0b85c}p{color:#93a3bf}.btn{background:#e0b85c;color:#0b1b33}}
''',
    ),
    "agente.html": (
        "text/html; charset=utf-8",
        r'''<!DOCTYPE html>
<html lang="pt"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>MacTech · Atendimento</title>
<link rel="icon" href="/static/logo.svg"><link rel="stylesheet" href="/static/painel.css">
</head><body>
<header><img class="logo" src="/static/logo.svg" alt="" width="36" height="36"><b>Mac<span>Tech</span></b> · Atendimento <span id="quem" class="msg"></span> <button id="sair" class="btn alt" type="button" hidden>Sair</button></header>
<main>
<section id="entrar" class="card">
<h2>Entrar</h2>
<p class="msg">Escreve a tua chave de atendente (dada pelo administrador).</p>
<form id="fl" class="row"><input id="k" type="password" autocomplete="current-password" aria-label="Chave de atendente" required><button class="btn" type="submit">Entrar</button></form>
<p id="ml" class="msg"></p>
</section>
<div id="app" hidden>
<section class="card" id="a-fila"><div class="sh"><span class="ic"><svg viewBox="0 0 24 24"><circle cx="12" cy="8" r="4"/><path d="M4 21c0-4.4 3.6-7 8-7s8 2.6 8 7"/></svg></span><div><h2>Conversas à espera de uma pessoa</h2><p class="desc">Clientes que pediram para falar com alguém. Escolha uma conversa e responda.</p></div></div><div id="fila"></div></section>
<section class="card" id="cv" hidden><h2 id="cvt">Conversa</h2><div id="msgs"></div>
<form id="fr" class="row"><input id="tx" maxlength="2000" placeholder="Escreve a resposta" aria-label="Resposta"><button class="btn" type="submit">Enviar</button></form>
<div class="row"><button class="btn alt" id="dev" type="button">Devolver à IA</button></div></section>
<section class="card" id="a-tk"><div class="sh"><span class="ic"><svg viewBox="0 0 24 24"><path d="M4 7h16v4a2 2 0 0 0 0 4v4H4v-4a2 2 0 0 0 0-4V7z"/></svg></span><div><h2>Tickets abertos</h2><p class="desc">Pedidos dos clientes que ainda precisam de uma ação.</p></div></div><div id="tk"></div></section>
</div>
</main>
<script src="/static/agente.js"></script>
</body></html>
''',
    ),
    "agente.js": (
        "application/javascript; charset=utf-8",
        r'''(function () {
  var K = sessionStorage.getItem('mt_agente') || '', tm = null, atual = null;
  function $(i) { return document.getElementById(i); }
  function h(t, c, x) { var e = document.createElement(t); if (c) e.className = c; if (x != null) e.textContent = x; return e; }
  function api(m, u, b) {
    return fetch(u, { method: m, headers: { 'X-Agent-Key': K, 'Content-Type': 'application/json' }, body: b ? JSON.stringify(b) : undefined })
      .then(function (r) {
        return r.json().catch(function () { return {}; }).then(function (j) {
          if (r.status === 401) { sair(); throw new Error('Chave errada'); }
          if (!r.ok) throw new Error(j.erro || ('Erro ' + r.status));
          return j;
        });
      });
  }
  function erro(x) { alert(x.message); }
  function mostrar(on) { $('entrar').hidden = on; $('app').hidden = !on; $('sair').hidden = !on; }
  function sair() { sessionStorage.removeItem('mt_agente'); K = ''; clearInterval(tm); atual = null; $('cv').hidden = true; mostrar(false); }
  function iniciar() {
    mostrar(true);
    api('GET', '/api/agente/eu').then(function (j) { $('quem').textContent = j.nome + ' · ' + j.empresa + ' · ' + j.departamento; });
    carregar(); clearInterval(tm); tm = setInterval(carregar, 8000);
  }
  function carregar() { fila(); tickets(); if (atual) conversa(atual, true); }

  function fila() {
    api('GET', '/api/agente/fila').then(function (j) {
      var L = $('fila'); L.textContent = '';
      if (!j.conversas.length) { L.appendChild(h('p', 'msg', 'Nenhuma conversa à espera.')); return; }
      j.conversas.forEach(function (c) {
        var d = h('div', 'item');
        d.appendChild(h('b', null, (c.departamento || 'Geral') + ' · ' + c.canal + ' · ' + c.cliente + (c.minha ? ' · tua' : '')));
        if (c.contacto) d.appendChild(h('p', 'msg', 'Contacto: ' + c.contacto));
        d.appendChild(h('p', 'msg', (c.ultimo_remetente === 'user' ? 'Cliente: ' : '') + (c.ultima_mensagem || '')));
        var b = h('button', 'btn', c.livre ? 'Assumir' : 'Abrir'); b.type = 'button';
        b.onclick = function () {
          if (!c.livre) { abrir(c.id); return; }
          api('POST', '/api/agente/assumir', { conversa_id: c.id }).then(function () { abrir(c.id); fila(); }).catch(erro);
        };
        d.appendChild(b); L.appendChild(d);
      });
    }).catch(function () {});
  }
  function abrir(id) { atual = id; $('cv').hidden = false; conversa(id, false); }
  function conversa(id, silencio) {
    api('GET', '/api/agente/conversa/' + id).then(function (j) {
      var T = $('msgs'); T.textContent = ''; $('cvt').textContent = 'Conversa' + (j.contacto ? ' · ' + j.contacto : '');
      j.mensagens.forEach(function (m) {
        var q = m.remetente === 'user' ? 'Cliente' : m.remetente === 'human' ? 'Equipa' : 'Bot';
        T.appendChild(h('p', 'msg', q + ': ' + m.conteudo));
      });
      $('fr').hidden = !j.minha;
      if (!silencio) $('cv').scrollIntoView();
    }).catch(function (x) { if (silencio) { atual = null; $('cv').hidden = true; } else erro(x); });
  }
  $('fr').onsubmit = function (e) {
    e.preventDefault(); var t = $('tx').value.trim(); if (!t || !atual) return;
    api('POST', '/api/agente/responder', { conversa_id: atual, texto: t }).then(function () { $('tx').value = ''; conversa(atual, true); }).catch(erro);
  };
  $('dev').onclick = function () {
    if (!atual) return;
    api('POST', '/api/agente/devolver', { conversa_id: atual }).then(function () { atual = null; $('cv').hidden = true; fila(); }).catch(erro);
  };
  function tickets() {
    api('GET', '/api/agente/tickets').then(function (j) {
      var L = $('tk'); L.textContent = '';
      if (!j.tickets.length) { L.appendChild(h('p', 'msg', 'Nenhum ticket aberto.')); return; }
      j.tickets.forEach(function (t) {
        var d = h('div', 'item');
        d.appendChild(h('b', null, (t.departamento || 'Geral') + ' · ' + t.tipo));
        d.appendChild(h('p', 'msg', t.assunto));
        var b = h('button', 'btn alt', 'Fechar'); b.type = 'button';
        b.onclick = function () { api('POST', '/api/agente/tickets/' + t.id + '/fechar').then(tickets).catch(erro); };
        d.appendChild(b); L.appendChild(d);
      });
    }).catch(function () {});
  }
  $('fl').onsubmit = function (e) {
    e.preventDefault(); K = $('k').value.trim();
    api('GET', '/api/agente/eu').then(function () { sessionStorage.setItem('mt_agente', K); $('k').value = ''; $('ml').textContent = ''; iniciar(); })
      .catch(function (x) { $('ml').textContent = x.message; });
  };
  $('sair').onclick = sair;
  if (K) { api('GET', '/api/agente/eu').then(iniciar).catch(function () { mostrar(false); }); } else { mostrar(false); }
})();
''',
    ),
}


# ---------- Portal da empresa (/minha-empresa): cada empresa gere só os seus dados ----------
ASSETS["minha.html"] = ("text/html; charset=utf-8", r'''<!DOCTYPE html>
<html lang="pt"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>MacTech · Minha empresa</title><link rel="icon" href="/static/logo.svg"><link rel="stylesheet" href="/static/painel.css"></head><body>
<header><img class="logo" src="/static/logo.svg" alt="" width="36" height="36"><b>Mac<span>Tech</span></b> · Minha empresa <button id="sair" class="btn alt" type="button" hidden>Sair</button></header>
<main>
<section id="entrar" class="card"><h2>Entrar</h2><p class="msg">Escreva a chave que recebeu ao registar a empresa.</p>
<form id="fl" class="row"><input id="k" type="password" autocomplete="current-password" aria-label="Chave da empresa" required><button class="btn" type="submit">Entrar</button></form>
<p id="ml" class="msg"></p></section>
<div id="portal" hidden>
<section class="card"><h2 id="nm"></h2><div id="st"></div><p id="vd" class="msg"></p><p id="lk" class="msg"></p><div id="sm" class="msg"></div></section>
<section class="card" id="m-logo"><div class="sh"><span class="ic"><svg viewBox="0 0 24 24"><rect x="3" y="4" width="18" height="16" rx="2"/><circle cx="9" cy="10" r="1.8"/><path d="M21 17l-5-5-9 8"/></svg></span><div><h2>Logótipo</h2><p class="desc">A imagem da sua marca aparece no topo do chat e na lista de empresas, ao lado do nome.</p></div></div>
<div class="lgf"><div class="av" id="lgv"></div><input id="lgi" type="file" accept="image/png,image/jpeg,image/webp" aria-label="Escolher logótipo"></div>
<div class="row"><button class="btn" id="lgs" type="button" disabled>Guardar logótipo</button><button class="btn alt" id="lgr" type="button" hidden>Remover</button></div><p id="lgm" class="msg"></p></section>
<section class="card" id="m-info"><div class="sh"><span class="ic"><svg viewBox="0 0 24 24"><circle cx="12" cy="12" r="9"/><path d="M12 8h.01M11 12h1v5h1"/></svg></span><div><h2>Informação do assistente</h2><p class="desc">Tudo o que o assistente sabe: produtos, preços, horário, contactos, regras. Atualize aqui sempre que algo mudar.</p></div></div>
<label for="enm">Nome da empresa</label><input id="enm" maxlength="120">
<label for="epr">Informação e regras do assistente</label><textarea id="epr" rows="10" maxlength="20000"></textarea>
<label class="chk"><input type="checkbox" id="ehu"> Tenho equipa para atender pessoas</label>
<div class="row"><button class="btn" id="gv" type="button">Guardar</button></div><p id="mg" class="msg"></p></section>
<section class="card" id="m-conversas"><div class="sh"><span class="ic"><svg viewBox="0 0 24 24"><path d="M21 12a8 8 0 0 1-11.6 7.1L4 20l1-4.6A8 8 0 1 1 21 12z"/></svg></span><div><h2>Conversas recentes</h2><p class="desc">As últimas conversas dos seus clientes. Toque numa para ler.</p></div></div><div id="cv"></div><div id="tr"></div></section>
<section class="card" id="m-sem"><div class="sh"><span class="ic"><svg viewBox="0 0 24 24"><circle cx="12" cy="12" r="9"/><path d="M9.5 9.5a2.5 2.5 0 1 1 3.5 2.3c-.7.4-1 .9-1 1.7M12 17h.01"/></svg></span><div><h2>Perguntas que o assistente não soube responder</h2><p class="desc">Acrescente estas respostas à informação acima.</p></div></div><div id="sr"></div></section>
</div></main><script src="/static/logo.js"></script><script src="/static/minha.js"></script></body></html>''')

ASSETS["minha.js"] = ("application/javascript; charset=utf-8", r'''(function () {
  var K = sessionStorage.getItem('mt_empresa') || '', preenchido = false;
  function $(i) { return document.getElementById(i); }
  function h(t, c, x) { var e = document.createElement(t); if (c) e.className = c; if (x != null) e.textContent = x; return e; }
  function api(m, u, b) {
    return fetch(u, { method: m, headers: { 'X-Empresa-Key': K, 'Content-Type': 'application/json' }, body: b ? JSON.stringify(b) : undefined })
      .then(function (r) { return r.json().catch(function () { return {}; }).then(function (j) {
        if (r.status === 401) { sair(); throw new Error('Chave errada'); }
        if (!r.ok) throw new Error(j.erro || ('Erro ' + r.status));
        return j; }); });
  }
  function mostrar(on) { $('entrar').hidden = on; $('portal').hidden = !on; $('sair').hidden = !on; }
  function sair() { sessionStorage.removeItem('mt_empresa'); K = ''; preenchido = false; mostrar(false); }
  var ROT = { pendente: 'À espera da confirmação do pagamento', teste: 'Em teste', ativo: 'Ativa', suspenso: 'Suspensa' };
  function carregar() {
    return api('GET', '/api/minha/resumo').then(function (r) {
      mostrar(true);
      $('nm').textContent = r.nome; mostrarLogo(r);
      var st = $('st'); st.textContent = ''; st.appendChild(h('span', 'badge' + (r.ativa ? '' : ' off'), ROT[r.estado] || r.estado));
      $('vd').textContent = r.valido_ate ? 'Válida até ' + new Date(r.valido_ate).toLocaleDateString('pt-PT') : '';
      var lk = $('lk'); lk.textContent = '';
      if (r.chat_url) { var u = location.origin + r.chat_url, a = h('a', null, u); a.href = u; a.target = '_blank'; a.rel = 'noopener'; lk.appendChild(document.createTextNode('Link do seu chat: ')); lk.appendChild(a); }
      $('sm').textContent = 'Últimos 7 dias: ' + r.semana.pessoas + ' pessoas · ' + r.semana.mensagens + ' mensagens · ' + r.semana.respostas_ia + ' respostas da IA · ' + r.semana.sem_resposta + ' sem resposta';
      if (!preenchido) { preenchido = true; $('enm').value = r.nome; $('epr').value = r.system_prompt; $('ehu').checked = r.humano_ativo; }
      var C = $('cv'); C.textContent = '';
      if (!r.conversas.length) C.appendChild(h('p', 'msg', 'Ainda sem conversas.'));
      r.conversas.forEach(function (c) {
        var d = h('div', 'item'); d.style.cursor = 'pointer';
        d.appendChild(h('b', null, c.canal + (c.contacto ? ' · ' + c.contacto : '') + (c.humano ? ' · à espera de pessoa' : '')));
        d.appendChild(h('p', 'msg', c.ultima || ''));
        d.onclick = function () { api('GET', '/api/minha/conversa/' + c.id).then(function (j) {
          var T = $('tr'); T.textContent = '';
          j.mensagens.forEach(function (m) { T.appendChild(h('p', 'msg', (m.remetente === 'user' ? 'Cliente: ' : m.remetente === 'human' ? 'Equipa: ' : 'IA: ') + m.conteudo)); });
          T.scrollIntoView(); }).catch(function (x) { alert(x.message); }); };
        C.appendChild(d);
      });
      var S = $('sr'); S.textContent = '';
      if (!r.sem_resposta.length) S.appendChild(h('p', 'msg', 'Nada por agora. Bom sinal.'));
      r.sem_resposta.forEach(function (p) { S.appendChild(h('div', 'item', p.pergunta)); });
    });
  }
  var novo = null;
  function mostrarLogo(r) {
    if (novo) return;
    var v = $('lgv'); v.textContent = '';
    var slug = r.chat_url ? r.chat_url.split('/').pop() : '';
    if (r.logo && slug) { var im = h('img'); im.src = '/logo/' + encodeURIComponent(slug) + '?v=' + r.logo; im.alt = 'Logótipo'; v.appendChild(im); }
    else v.textContent = (r.nome || '?').slice(0, 1).toUpperCase();
    $('lgr').hidden = !r.logo;
  }
  $('lgi').onchange = function () {
    MTLogo.ler(this.files[0]).then(function (x) { novo = x.url; var v = $('lgv'); v.textContent = ''; v.appendChild(x.canvas); $('lgs').disabled = false; $('lgm').textContent = ''; })
      .catch(function (x) { $('lgm').textContent = x.message; });
  };
  $('lgs').onclick = function () {
    api('PUT', '/api/minha/logo', { logo: novo }).then(function () { novo = null; $('lgs').disabled = true; $('lgi').value = ''; $('lgm').textContent = 'Logótipo guardado.'; return carregar(); })
      .catch(function (x) { $('lgm').textContent = x.message; });
  };
  $('lgr').onclick = function () {
    api('DELETE', '/api/minha/logo').then(function () { novo = null; $('lgm').textContent = 'Logótipo removido.'; return carregar(); })
      .catch(function (x) { $('lgm').textContent = x.message; });
  };
  $('gv').onclick = function () {
    api('PUT', '/api/minha/info', { nome: $('enm').value, system_prompt: $('epr').value, humano_ativo: $('ehu').checked })
      .then(function () { $('mg').textContent = 'Guardado. O assistente já usa a informação nova.'; preenchido = false; return carregar(); })
      .catch(function (x) { $('mg').textContent = x.message; });
  };
  $('fl').onsubmit = function (ev) {
    ev.preventDefault(); K = $('k').value.trim();
    carregar().then(function () { sessionStorage.setItem('mt_empresa', K); $('k').value = ''; $('ml').textContent = ''; })
      .catch(function (x) { $('ml').textContent = x.message; });
  };
  $('sair').onclick = sair;
  if (K) carregar().catch(function () {}); else mostrar(false);
  setInterval(function () { if (K && !$('portal').hidden) carregar().catch(function () {}); }, 30000);
})();''')
