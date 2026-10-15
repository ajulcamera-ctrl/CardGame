const SYM = {C:'♣',D:'♦',H:'♥',S:'♠',NT:'NT'};
const SEATS = ['N','E','S','W'], NAMES = ['North','East','South','West'];
const RANKS = '23456789TJQKA';
const app = document.getElementById('app');
let sess = JSON.parse(localStorage.getItem('bridge') || 'null');
let state = null, msg = '', timer = null;

async function api(path, body) {
  const opts = body ? {method:'POST', headers:{'Content-Type':'application/json'}, body:JSON.stringify(body)} : {};
  const r = await fetch(path, opts);
  const j = await r.json();
  if (!r.ok) throw new Error(j.error || 'Error');
  return j;
}
function save(s) { sess = s; if (s) localStorage.setItem('bridge', JSON.stringify(s)); else localStorage.removeItem('bridge'); }
const esc = s => String(s).replace(/[&<>"]/g, c => ({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;'}[c]));
function nameVal() { return (document.getElementById('nm')?.value || localStorage.getItem('bname') || 'Player'); }

async function act(fn) {
  try { msg = ''; const r = await fn(); if (r && r.token) save({table:r.table, token:r.token}); if (r && r.started !== undefined) state = r; }
  catch (e) { msg = e.message; }
  if (sess) await poll(); else render();
}
function create(solo) { localStorage.setItem('bname', nameVal()); act(() => api('/api/create', {name:nameVal(), solo})); }
function join() {
  localStorage.setItem('bname', nameVal());
  act(() => api('/api/join', {name:nameVal(), table:document.getElementById('code').value.trim().toUpperCase()}));
}
function leave() { save(null); state = null; render(); }
const post = (p, extra) => act(() => api(p, Object.assign({table:sess.table, token:sess.token}, extra||{})));

async function poll() {
  if (!sess) return;
  try { state = await api(`/api/state?table=${sess.table}&token=${sess.token}`); }
  catch (e) { if (/not found/i.test(e.message)) { save(null); state = null; msg = 'Table expired'; } }
  render();
}

function cardHtml(c, opts={}) {
  const red = c[1]==='H'||c[1]==='D';
  const label = (c[0]==='T'?'10':c[0]) + SYM[c[1]];
  if (opts.click) return `<button class="card legal ${red?'red':''}" onclick="playCard('${c}')">${label}</button>`;
  return `<span class="card ${red?'red':''}">${label}</span>`;
}
function playCard(c) { post('/api/play', {card:c}); }
function bid(c) { post('/api/bid', {call:c}); }
function callHtml(c) {
  if (c==='P') return 'Pass';
  if (c==='X'||c==='XX') return c;
  const s = c.slice(1); return c[0] + (s==='NT'?'NT':`<span class="${s==='H'||s==='D'?'red':''}">${SYM[s]}</span>`);
}

function handHtml(seat, d, clickable) {
  const cards = d.hands[seat];
  if (!cards) return `<div class="hand">${'<span class="card back">&nbsp;</span>'.repeat(d.counts[seat])}</div>`;
  let h = '';
  for (const s of 'SHDC') {
    const cs = cards.filter(c => c[1]===s);
    if (!cs.length) continue;
    h += `<div class="suitrow">${cs.map(c => clickable && d.legal && d.legal.includes(c) ? cardHtml(c,{click:1}) : cardHtml(c)).join('')}</div>`;
  }
  return `<div class="hand" style="flex-direction:column;align-items:center">${h}</div>`;
}

function seatHtml(seat, cls, d) {
  const sd = state.seats[seat];
  const isDummy = d.contract && d.contract.dummy === seat;
  const label = `${NAMES[seat]}${isDummy?' (dummy)':''}${d.contract&&d.contract.declarer===seat?' (declarer)':''} — ${esc(sd.name||'empty')}${seat===state.me?' (you)':''}`;
  const canClick = d.phase==='playing' && d.actor===state.me && d.legal &&
     (seat===d.turn);
  return `<div class="seat ${cls} ${d.turn===seat||(d.phase==='bidding'&&d.actor===seat)?'turn':''}"><div class="name">${label}</div>${handHtml(seat,d,canClick)}</div>`;
}

function auctionHtml(d) {
  let rows = '<tr>' + SEATS.map((s,i)=>`<th>${s}${d.vul[i%2]?'*':''}</th>`).join('') + '</tr><tr>';
  let col = 0;
  for (let i=0;i<d.dealer;i++) { rows += '<td></td>'; col++; }
  d.calls.forEach(c => { if (col%4===0 && col>0) rows += '</tr><tr>'; rows += `<td>${callHtml(c.call)}</td>`; col++; });
  return `<table class="auction">${rows}</tr></table>`;
}
function bidBox(d) {
  if (d.actor !== state.me) return `<div class="info">Waiting for ${NAMES[d.actor]}…</div>`;
  const ok = new Set(d.legal);
  let h = `<div class="bidbox"><button ${ok.has('P')?'':'disabled'} onclick="bid('P')">Pass</button>` +
    `<button ${ok.has('X')?'':'disabled'} onclick="bid('X')">X</button><button ${ok.has('XX')?'':'disabled'} onclick="bid('XX')">XX</button><span></span><span></span>`;
  for (let l=1;l<=7;l++) for (const s of ['C','D','H','S','NT']) {
    const c = l+s; h += `<button ${ok.has(c)?'':'disabled'} onclick="bid('${c}')">${callHtml(c)}</button>`;
  }
  return h + '</div>';
}

function lobbyHtml() {
  return `<div class="panel lobby"><h1>♠ Bridge ♥</h1>
  <div><input id="nm" placeholder="Your name" maxlength="16" value="${esc(localStorage.getItem('bname')||'')}"></div>
  <div><button onclick="create(true)">Play solo vs computer</button></div>
  <div><button onclick="create(false)">Create multiplayer table</button></div>
  <div><button onclick="openHelp('tutorial')">Tutorial</button> <button onclick="openHelp('basics')">Rules</button></div>
  <div><input id="code" placeholder="Table code" maxlength="4" size="6" style="text-transform:uppercase"> <button onclick="join()">Join</button></div>
  <div class="msg">${esc(msg)}</div></div>`;
}
function waitingHtml() {
  const rows = state.seats.map((s,i)=>`<div>${NAMES[i]}: ${s.name?esc(s.name):'<i>empty (CPU will fill in)</i>'}</div>`).join('');
  const host = state.me === state.host;
  return `<div class="panel lobby"><h2>Table ${state.code}</h2><p>Share this code with friends: they open this page, enter <b>${state.code}</b> and click Join.</p>${rows}
  <div>${host?'<button onclick="post(\'/api/start\')">Start game</button>':'Waiting for host to start…'}</div>
  <div><button onclick="leave()">Leave</button></div><div class="msg">${esc(msg)}</div></div>`;
}

const openBoards = new Set();
function toggleBoard(el) { const b = el.dataset.board; if (el.open) openBoards.add(b); else openBoards.delete(b); }
function render() { renderMain(); app.innerHTML += helpHtml(); }
function renderMain() {
  if (!sess || !state) { app.innerHTML = lobbyHtml(); return; }
  if (!state.started) { app.innerHTML = waitingHtml(); return; }
  const d = state.deal, me = state.me ?? 2;
  const pos = i => (me + i) % 4;
  let center = '';
  if (d.phase === 'bidding') center = auctionHtml(d) + bidBox(d);
  else {
    const rel = s => (s - me + 4) % 4;
    const tr = d.trick.length ? d.trick : [];
    center = `<div class="trick">${tr.map(t=>`<span class="t${(rel(t.seat))===0?2:(rel(t.seat))===1?3:(rel(t.seat))===2?0:1}">${cardHtml(t.card)}</span>`).join('')}</div>`;
  }
  const vulTxt = `You (NS) ${d.vul[0]?'vulnerable':'not vulnerable'} · Opponents (EW) ${d.vul[1]?'vulnerable':'not vulnerable'}`;
  let status = '';
  if (d.phase==='playing') status = `Contract ${d.contract.text} · Tricks NS ${d.tricks[0]} – EW ${d.tricks[1]}` +
     (d.actor===state.me ? ` · <b>Your turn${d.turn!==state.me?' (play for dummy)':''}</b>` : d.actor!=null ? ` · Waiting for ${NAMES[d.actor]}` : '');
  if (d.phase==='bidding') status = `Dealer ${NAMES[d.dealer]} · Auction`;
  if (d.phase==='done') {
    const r = d.result, fmt = n => (n>=0?'+':'') + n;
    status = `<div class="summary"><b>Hand summary</b>
      <div>Contract: ${d.contract ? d.contract.text + ' by ' + NAMES[d.contract.declarer] : 'Passed out'}</div>
      <div>Result: ${esc(r.text)}</div>
      <div>Score this hand: NS <b>${fmt(r.ns)}</b> / EW <b>${fmt(r.ew)}</b></div>
      <div>Running total: NS <b>${state.score.ns}</b> / EW <b>${state.score.ew}</b></div>
      <button onclick="post('/api/next')">Next deal</button></div>`;
  }
  const hist = state.history.slice().reverse().map(h => {
    const winner = h.ns > h.ew ? 'North/South' : h.ew > h.ns ? 'East/West' : 'Tie';
    const tricks = (h.tricks || []).map((t, i) =>
      `<li>Trick ${i + 1}: ${t.plays.map(p => `${NAMES[p.seat]} ${cardHtml(p.card)}`).join(' · ')} — won by ${NAMES[t.winner]} (${t.winner % 2 === 0 ? 'North/South' : 'East/West'})</li>`
    ).join('');
    return `<details class="deal-summary" data-board="${h.board}"${openBoards.has(String(h.board))?' open':''} ontoggle="toggleBoard(this)"><summary>Board ${h.board}: ${esc(h.text)} · NS ${h.ns} / EW ${h.ew} · Winner: ${winner}</summary><ol>${tricks || '<li>No cards played (passed out)</li>'}</ol></details>`;
  }).join('');
  app.innerHTML = `<div class="panel"><div>Board ${d.board} · ${vulTxt} · Table ${state.code} · Total: NS <b>${state.score.ns}</b> / EW <b>${state.score.ew}</b>
    <span style="float:right"><button onclick="openHelp('basics')">Help</button> <button onclick="toggleHints()">Hints: ${hintsOn?'on':'off'}</button> <button onclick="leave()">Leave</button></span></div><div class="info">${status}</div>${tipHtml(d)}<div class="msg">${esc(msg)}</div></div>
    <div class="board">${seatHtml(pos(2),'top',d)}${seatHtml(pos(1),'left',d)}<div class="center panel">${center}</div>${seatHtml(pos(3),'right',d)}${seatHtml(pos(0),'bottom',d)}</div>
    <div class="panel info"><b>Results</b>${hist||'<div>None yet</div>'}</div>`;
}

if (sess) poll(); else render();
setInterval(() => { if (sess && !document.hidden && !document.activeElement?.matches('input')) poll(); }, 1000);
