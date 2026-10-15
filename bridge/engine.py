"""Contract bridge engine: bidding, play, scoring and a simple computer player."""
import random
import time

SEATS = ["N", "E", "S", "W"]
SEAT_NAMES = ["North", "East", "South", "West"]
SUITS = "CDHS"  # ascending bid order; NT is above spades
RANKS = "23456789TJQKA"
HCP = {"J": 1, "Q": 2, "K": 3, "A": 4}
VUL_CYCLE = [(0, 0), (1, 0), (0, 1), (1, 1), (1, 0), (0, 1), (1, 1), (0, 0),
             (0, 1), (1, 1), (0, 0), (1, 0), (1, 1), (0, 0), (1, 0), (0, 1)]
BOT_DELAY = 0.9
TRICK_DELAY = 1.6


def card_rank(c):
    return RANKS.index(c[0])


def sort_hand(cards):
    return sorted(cards, key=lambda c: (SUITS.index(c[1]), card_rank(c)), reverse=True)


def side(seat):
    return seat % 2  # 0 = North/South, 1 = East/West


def parse_bid(call):
    """'3NT' -> (3, 4); '1C' -> (1, 0)."""
    level = int(call[0])
    den = 4 if call[1:] == "NT" else SUITS.index(call[1:])
    return level, den


def score_contract(level, den, doubled, vul, tricks):
    """Score from the declaring side's point of view (negative if defeated)."""
    need = 6 + level
    mult = (1, 2, 4)[doubled]
    if tricks < need:
        down = need - tricks
        if doubled == 0:
            return -(down * (100 if vul else 50))
        if vul:
            pen = 200 + 300 * (down - 1)
        else:
            pen = sum(100 if i == 0 else 200 if i < 3 else 300 for i in range(down))
        return -(pen * (doubled))
    per = 20 if den < 2 else 30
    base = level * per + (10 if den == 4 else 0)
    trick_pts = base * mult
    total = trick_pts
    total += 500 if trick_pts >= 100 and vul else 300 if trick_pts >= 100 else 50
    if level == 6:
        total += 750 if vul else 500
    elif level == 7:
        total += 1500 if vul else 1000
    total += (0, 50, 100)[doubled]
    over = tricks - need
    if doubled == 0:
        total += over * per
    else:
        total += over * (100 if not vul else 200) * doubled
    return total


def hcp(hand):
    return sum(HCP.get(c[0], 0) for c in hand)


class Deal:
    def __init__(self, board, dealer, hands=None):
        self.board = board
        self.dealer = dealer
        vul = VUL_CYCLE[(board - 1) % 16]
        self.vul = vul  # (NS vulnerable, EW vulnerable)
        if hands is None:
            deck = [r + s for r in RANKS for s in SUITS]
            random.shuffle(deck)
            hands = [sort_hand(deck[i * 13:(i + 1) * 13]) for i in range(4)]
        self.hands = hands
        self.original = [list(h) for h in hands]
        self.calls = []  # (seat, call)
        self.turn = dealer
        self.phase = "bidding"  # bidding | playing | done
        self.contract = None  # dict(level, den, doubled, declarer)
        self.leader = None
        self.trick = []  # list of (seat, card)
        self.trick_done_at = None
        self.tricks_won = [0, 0]
        self.last_trick = None
        self.trick_history = []
        self.result = None

    # ---- bidding ----
    def last_bid(self):
        for i in range(len(self.calls) - 1, -1, -1):
            seat, call = self.calls[i]
            if call[0].isdigit():
                return i, seat, call
        return None

    def legal_calls(self):
        if self.phase != "bidding":
            return []
        out = ["P"]
        lb = self.last_bid()
        floor = 0
        if lb:
            level, den = parse_bid(lb[2])
            floor = (level - 1) * 5 + den + 1
            last_non_pass = [c for c in self.calls[lb[0] + 1:] if c[1] != "P"]
            if not last_non_pass and side(lb[1]) != side(self.turn):
                out.append("X")
            elif (len(last_non_pass) == 1 and last_non_pass[0][1] == "X"
                  and side(last_non_pass[0][0]) != side(self.turn)):
                out.append("XX")
        for v in range(floor, 35):
            level, den = divmod(v, 5)
            out.append("%d%s" % (level + 1, "NT" if den == 4 else SUITS[den]))
        return out

    def bid(self, seat, call):
        if self.phase != "bidding" or seat != self.turn:
            raise ValueError("Not your turn to bid")
        if call not in self.legal_calls():
            raise ValueError("Illegal call")
        self.calls.append((seat, call))
        self.turn = (seat + 1) % 4
        lb = self.last_bid()
        if lb is None:
            if len(self.calls) == 4:
                self._finish(passed_out=True)
        elif len(self.calls) - lb[0] - 1 >= 3:
            level, den = parse_bid(lb[2])
            dbl = 0
            for _, c in self.calls[lb[0]:]:
                if c == "X":
                    dbl = 1
                elif c == "XX":
                    dbl = 2
            declarer = lb[1]
            for s, c in self.calls:
                if c[0].isdigit() and side(s) == side(lb[1]) and parse_bid(c)[1] == den:
                    declarer = s
                    break
            self.contract = dict(level=level, den=den, doubled=dbl, declarer=declarer)
            self.phase = "playing"
            self.leader = (declarer + 1) % 4
            self.turn = self.leader

    def _finish(self, passed_out=False):
        self.phase = "done"
        if passed_out:
            self.result = dict(text="Passed out", ns=0, ew=0)

    # ---- play ----
    @property
    def trump(self):
        if not self.contract or self.contract["den"] == 4:
            return None
        return SUITS[self.contract["den"]]

    @property
    def dummy(self):
        return (self.contract["declarer"] + 2) % 4 if self.contract else None

    def dummy_visible(self):
        return self.phase == "done" or (self.phase == "playing" and
                                        (len(self.trick) + sum(self.tricks_won)) > 0)

    def controller(self, seat):
        """Seat whose human (or bot) makes the play for `seat`."""
        return self.contract["declarer"] if seat == self.dummy else seat

    def legal_plays(self, seat=None):
        seat = self.turn if seat is None else seat
        hand = self.hands[seat]
        if self.trick:
            led = self.trick[0][1][1]
            follow = [c for c in hand if c[1] == led]
            if follow:
                return follow
        return list(hand)

    def play(self, seat, card):
        if self.phase != "playing" or seat != self.turn or self.trick_done_at:
            raise ValueError("Cannot play now")
        if card not in self.legal_plays(seat):
            raise ValueError("Illegal card")
        self.hands[seat].remove(card)
        self.trick.append((seat, card))
        if len(self.trick) == 4:
            self.trick_done_at = time.time()
        else:
            self.turn = (seat + 1) % 4

    def trick_winner(self):
        led = self.trick[0][1][1]
        trump = self.trump

        def key(t):
            c = t[1]
            if trump and c[1] == trump:
                return (2, card_rank(c))
            if c[1] == led:
                return (1, card_rank(c))
            return (0, 0)
        return max(self.trick, key=key)[0]

    def resolve_trick(self):
        w = self.trick_winner()
        self.tricks_won[side(w)] += 1
        self.last_trick = list(self.trick)
        self.trick_history.append(dict(
            plays=[dict(seat=seat, card=card) for seat, card in self.trick],
            winner=w,
        ))
        self.trick = []
        self.trick_done_at = None
        self.turn = w
        if sum(self.tricks_won) == 13:
            self._score()

    def _score(self):
        self.phase = "done"
        c = self.contract
        decl_side = side(c["declarer"])
        made = self.tricks_won[decl_side]
        pts = score_contract(c["level"], c["den"], c["doubled"], bool(self.vul[decl_side]), made)
        ns = pts if decl_side == 0 else -pts
        need = 6 + c["level"]
        diff = made - need
        txt = "%s %s" % (contract_str(c), "made" if diff >= 0 else "down %d" % -diff)
        if diff > 0:
            txt += " +%d" % diff
        self.result = dict(text=txt, ns=ns, ew=-ns)


def contract_str(c):
    return "%d%s%s by %s" % (c["level"], "NT" if c["den"] == 4 else SUITS[c["den"]],
                             ("", "X", "XX")[c["doubled"]], SEATS[c["declarer"]])
