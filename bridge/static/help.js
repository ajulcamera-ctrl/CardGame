// Rules, tutorial and contextual tips for the Bridge client.
let helpTab = null;      // null = closed, else key of HELP_TABS or 'tutorial'
let tutStep = 0;
let hintsOn = localStorage.getItem('bhints') !== '0';

const HELP_TABS = {
  basics: ['Basics', `<h3>The goal</h3>
<p>Bridge is a trick-taking game for 4 players in 2 partnerships: North–South (NS) and East–West (EW). You sit South; North is your partner.</p>
<p>Each deal has two stages: an <b>auction</b> (bidding) to decide the contract, then <b>play</b> of 13 tricks.</p>
<h3>Cards</h3>
<p>52 cards, 13 each. Ranks high to low: A K Q J 10 9 8 7 6 5 4 3 2. Suits: ♠ spades, ♥ hearts, ♦ diamonds, ♣ clubs. ♠ and ♥ are the <b>major</b> suits, ♦ and ♣ the <b>minor</b> suits.</p>
<h3>Hand strength</h3>
<p>Count <b>high card points (HCP)</b>: Ace 4, King 3, Queen 2, Jack 1. The deck has 40. Roughly 26 combined points between partners are needed for a game contract.</p>`],
  bidding: ['Bidding', `<h3>The auction</h3>
<p>Starting with the dealer and going clockwise, each player makes a call: <b>Pass</b>, a <b>bid</b>, <b>Double (X)</b> or <b>Redouble (XX)</b>.</p>
<h3>Bids</h3>
<p>A bid is a level (1–7) and a denomination (♣ &lt; ♦ &lt; ♥ &lt; ♠ &lt; NT). It promises your side will win at least <b>6 + level</b> tricks with that suit as trump (or no trump). Each bid must be higher than the last: a higher level, or the same level in a higher denomination.</p>
<h3>Ending</h3>
<p>The auction ends after three consecutive passes following a bid. If all four pass, the deal is thrown in.</p>
<h3>Contract and declarer</h3>
<p>The last bid is the <b>contract</b>. The <b>declarer</b> is the player of the winning side who first bid that denomination. Declarer's partner is the <b>dummy</b>.</p>
<h3>Double and redouble</h3>
<p>X doubles the opponents' contract (bigger penalties if it fails, bigger bonus if it makes). XX redoubles it again. Any new bid cancels them.</p>
<h3>Simple opening guide</h3>
<ul><li>12–21 points: open 1 of your longest suit (majors with 5+ cards first).</li>
<li>15–17 balanced: open 1NT.</li><li>Fewer than 12: pass.</li>
<li>Respond with 6+ points; support partner's major with 3+ cards.</li></ul>`],
  play: ['Play', `<h3>Opening lead</h3>
<p>The player left of declarer leads any card. Then the <b>dummy</b> hand is laid face up.</p>
<h3>Tricks</h3>
<p>Each player plays one card clockwise. You <b>must follow suit</b> if you can; if not you may play any card. The trick is won by the highest card of the suit led, or by the highest <b>trump</b> if any trump was played. The winner leads next. Playable cards are highlighted in gold.</p>
<h3>Declarer and dummy</h3>
<p>Declarer plays both their own hand and dummy's. Dummy takes no decisions. When you are declarer, click cards from the dummy when it is dummy's turn.</p>
<h3>Tips</h3>
<ul><li>Count your sure winners before the first card is played.</li>
<li>As declarer, draw the opponents' trumps early.</li>
<li>As defender, lead the top of a sequence (e.g. K from K-Q-J) or fourth-best from a long suit.</li>
<li>"Second hand low, third hand high."</li></ul>`],
  scoring: ['Scoring', `<h3>Making a contract</h3>
<p>Declarer needs <b>6 + level</b> tricks. Tricks bid for count as <b>contract points</b>: ♣/♦ 20 each, ♥/♠ 30 each, NT 40 for the first and 30 for later tricks. Overtricks score the same per trick (doubled values if doubled).</p>
<h3>Bonuses</h3>
<ul><li><b>Part score</b> (contract points under 100): 50.</li>
<li><b>Game</b> (100+ contract points): 300 not vulnerable, 500 vulnerable. Needs 3NT, 4♥/♠ or 5♣/♦.</li>
<li><b>Small slam</b> (6 level): 500 / 750. <b>Grand slam</b> (7): 1000 / 1500.</li>
<li>Making a doubled contract adds 50, redoubled 100 ("insult").</li></ul>
<h3>Going down</h3>
<p>If declarer fails, the defenders score penalty points per undertrick: 50 (not vulnerable) or 100 (vulnerable) undoubled. Doubles increase this sharply.</p>
<h3>Vulnerability</h3>
<p>Shown in the header and an asterisk (*) in the auction. Vulnerable sides get bigger bonuses and bigger penalties.</p>`],
};

const TUTORIAL = [
  ['Welcome', 'This tutorial walks through a hand of Bridge. Use Next and Back to move. You can reopen it any time from the Help button.'],
  ['Partnerships', 'You (South) and North are partners against East and West. Your goal is to win more tricks than needed for your contract.'],
  ['Count your points', 'Before bidding, count HCP: A=4, K=3, Q=2, J=1. With 12+ points you should open the bidding; with fewer, pass.'],
  ['Bidding', 'Choose a bid in the bid box. Grayed buttons are not allowed (they are not higher than the last bid). "1♥" means: we will win 7 tricks with hearts as trumps.'],
  ['Trumps and NT', 'The final suit is trump: a trump beats any card of another suit. In No Trump (NT) the highest card of the led suit always wins.'],
  ['Declarer & dummy', 'After the auction one partner becomes declarer. The other hand (dummy) is shown to everyone and played by declarer.'],
  ['Playing a trick', 'Click a gold-outlined card. You must follow the suit led if you can. Highest card of the suit led (or highest trump) wins the trick.'],
  ['Scoring', 'Make your contract to score points; bid and make game (about 26 points between you) or a slam for big bonuses. See the Scoring tab for details.'],
  ['Ready!', 'Start a solo game against the computer. Keep "Hints" on to get tips about every phase and every legal move. Good luck!'],
];

function openHelp(tab) { helpTab = tab || 'basics'; if (helpTab === 'tutorial') tutStep = 0; render(); }
function closeHelp() { helpTab = null; render(); }
function tutGo(n) { tutStep = Math.max(0, Math.min(TUTORIAL.length - 1, n)); render(); }
function toggleHints() { hintsOn = !hintsOn; localStorage.setItem('bhints', hintsOn ? '1' : '0'); render(); }

function helpHtml() {
  if (!helpTab) return '';
  const tabs = Object.entries(HELP_TABS).map(([k, v]) =>
    `<button class="tab ${helpTab === k ? 'on' : ''}" onclick="openHelp('${k}')">${v[0]}</button>`).join('') +
    `<button class="tab ${helpTab === 'tutorial' ? 'on' : ''}" onclick="openHelp('tutorial')">Tutorial</button>`;
  let body;
  if (helpTab === 'tutorial') {
    const [t, x] = TUTORIAL[tutStep];
    body = `<h3>${tutStep + 1}/${TUTORIAL.length}: ${t}</h3><p>${x}</p>
      <div><button ${tutStep === 0 ? 'disabled' : ''} onclick="tutGo(${tutStep - 1})">Back</button>
      ${tutStep === TUTORIAL.length - 1 ? '<button onclick="closeHelp()">Done</button>' : `<button onclick="tutGo(${tutStep + 1})">Next</button>`}</div>`;
  } else body = HELP_TABS[helpTab][1];
  return `<div class="overlay" onclick="if(event.target===this)closeHelp()"><div class="modal">
    <div class="tabs">${tabs}<button style="margin-left:auto" onclick="closeHelp()">✕</button></div>
    <div class="helpbody">${body}</div></div></div>`;
}

function hcp(cards) { return cards.reduce((n, c) => n + ({A:4, K:3, Q:2, J:1}[c[0]] || 0), 0); }

// Short contextual tip for the current phase, shown when hints are on.
function tipHtml(d) {
  if (!hintsOn || state.me == null) return '';
  let tip = '';
  const mine = d.hands[state.me];
  if (d.phase === 'bidding') {
    const pts = mine ? hcp(mine) : 0;
    tip = d.actor === state.me
      ? `You have <b>${pts} HCP</b>. ` + (pts >= 12 ? 'Enough to open or respond: bid your longest suit (15–17 balanced: 1NT).' : pts >= 6 ? 'Not enough to open; if partner opened, you can respond.' : 'A weak hand: usually pass.')
      : 'Bidding: wait for your turn. Count your points (A=4, K=3, Q=2, J=1).';
  } else if (d.phase === 'playing') {
    const trump = d.contract.text.includes('NT') ? 'No trumps.' : 'Trumps are the contract suit.';
    tip = d.actor === state.me
      ? (d.trick.length ? 'Follow suit if you can (gold cards are legal). Win the trick cheaply if possible.' : 'You lead: choose a card. Lead from long suits or top of a sequence.')
      : 'Watch the cards played. ' + trump;
    if (d.turn !== state.me && d.actor === state.me) tip += ' You are playing for dummy.';
  } else if (d.phase === 'done') tip = 'Hand over. Check the scoring tab to see how the score was calculated.';
  return tip ? `<div class="tip">💡 ${tip}</div>` : '';
}
