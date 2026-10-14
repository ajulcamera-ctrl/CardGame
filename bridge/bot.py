"""Simple computer player: heuristic bidding and card play."""
from engine import SUITS, RANKS, card_rank, hcp, parse_bid, side


def _suit_cards(hand, s):
    return [c for c in hand if c[1] == s]


def _points(hand):
    pts = hcp(hand)
    for s in SUITS:
        n = len(_suit_cards(hand, s))
        pts += 3 if n == 0 else 2 if n == 1 else 1 if n == 2 else 0
    return pts


def _game_level(den):
    return 3 if den == 4 else 4 if den >= 2 else 5


def _lowest_bid(legal, den):
    tag = "NT" if den == 4 else SUITS[den]
    for c in legal:
        if c[0].isdigit() and c[1:] == tag:
            return c
    return None


def bot_call(deal, seat):
    hand = deal.hands[seat]
    legal = deal.legal_calls()
    me = side(seat)
    counts = {s: len(_suit_cards(hand, s)) for s in SUITS}
    pts = _points(hand)
    balanced = min(counts.values()) >= 2 and max(counts.values()) <= 4 + (1 if sorted(counts.values())[-1] == 5 else 0)
    balanced = sorted(counts.values()) in ([2, 3, 4, 4], [3, 3, 3, 4], [2, 3, 3, 5])
    bids = [(s, c) for s, c in deal.calls if c[0].isdigit()]
    if not bids:
        if hcp(hand) < 12 and pts < 13:
            return "P"
        if balanced and 15 <= hcp(hand) <= 17 and "1NT" in legal:
            return "1NT"
        majors = [s for s in "SH" if counts[s] >= 5]
        if majors:
            den = max(majors, key=lambda s: (counts[s], SUITS.index(s)))
        else:
            den = max("DC", key=lambda s: (counts[s], SUITS.index(s)))
        return _lowest_bid(legal, SUITS.index(den)) or "P"

    partner_bids = [c for s, c in bids if s == (seat + 2) % 4]
    side_bids = [(s, c) for s, c in bids if side(s) == me]
    est = 0
    if partner_bids:
        est = 13 if side_bids[0][0] == (seat + 2) % 4 else 8
    # Opponents opened and partner silent: stay quiet unless strong.
    if not partner_bids and not any(s == seat for s, _ in bids):
        if hcp(hand) < 13:
            return "P"
    total = pts + est
    if total >= 37:
        cap = 7
    elif total >= 33:
        cap = 6
    else:
        cap = 0 if total < 20 else 1 if total < 23 else 2 if total < 25 else 3 if total < 26 else 5
    if not est and cap > 2:
        cap = 2

    # Pick a denomination.
    den = None
    if partner_bids:
        pden = parse_bid(partner_bids[-1])[1]
        if pden < 4 and counts[SUITS[pden]] >= 3:
            den = pden
        elif pden == 4:
            den = 4
    if den is None:
        longest = max(SUITS, key=lambda s: (counts[s], SUITS.index(s)))
        if counts[longest] >= 5:
            den = SUITS.index(longest)
        elif balanced:
            den = 4
    if den is None:
        return "P"
    if total >= 26 and cap < 6:
        target = _game_level(den)
        call = _lowest_bid(legal, den)
        if call and int(call[0]) <= target:
            call = "%d%s" % (target, "NT" if den == 4 else SUITS[den])
            return call if call in legal else "P"
        return "P"
    call = _lowest_bid(legal, den)
    if call and int(call[0]) <= cap:
        return call
    return "P"


def _winning(deal, trick):
    led = trick[0][1][1]
    trump = deal.trump

    def key(t):
        c = t[1]
        if trump and c[1] == trump:
            return (2, card_rank(c))
        return (1, card_rank(c)) if c[1] == led else (0, 0)
    return max(trick, key=key)


def bot_play(deal, seat):
    hand = deal.hands[seat]
    legal = deal.legal_plays(seat)
    trump = deal.trump
    low = lambda cs: min(cs, key=card_rank)
    high = lambda cs: max(cs, key=card_rank)
    if not deal.trick:
        sides = [c for c in legal if c[1] != trump] or legal
        # Cash an ace if we have one, else lead from the longest suit.
        aces = [c for c in sides if c[0] == "A"]
        if aces:
            return aces[0]
        by_suit = {}
        for c in sides:
            by_suit.setdefault(c[1], []).append(c)
        suit = max(by_suit, key=lambda s: (len(by_suit[s]), card_rank(high(by_suit[s]))))
        cards = sorted(by_suit[suit], key=card_rank, reverse=True)
        if len(cards) >= 2 and card_rank(cards[0]) - card_rank(cards[1]) == 1 and card_rank(cards[0]) >= 9:
            return cards[0]
        return cards[3] if len(cards) >= 4 else cards[-1] if len(cards) < 3 else cards[1] if card_rank(cards[0]) >= 11 else cards[-1]
    win_seat, win_card = _winning(deal, deal.trick)
    partner_winning = side(win_seat) == side(seat)
    led = deal.trick[0][1][1]
    last = len(deal.trick) == 3

    def beats(c):
        return _winning(deal, deal.trick + [(seat, c)])[0] == seat
    winners = [c for c in legal if beats(c)]
    if partner_winning and not (last is False and card_rank(win_card) < 9 and winners and legal[0][1] == led and False):
        return low(legal)
    if winners:
        return low(winners)
    # Cannot win: discard the lowest card (prefer non-trump).
    non_trump = [c for c in legal if c[1] != trump] or legal
    return low(non_trump)
