"""Table management: seats, humans vs bots, and per-player views."""
import random
import secrets
import time

import bot
from engine import Deal, SEATS, SEAT_NAMES, SUITS, contract_str, side, sort_hand, BOT_DELAY, TRICK_DELAY

BOT_NAMES = ["Ada", "Bernie", "Cleo", "Dex"]


class Table:
    def __init__(self, code):
        self.code = code
        self.names = [None] * 4
        self.tokens = [None] * 4
        self.is_bot = [False] * 4
        self.host = None
        self.deal = None
        self.board = 0
        self.score = [0, 0]
        self.history = []
        self.touched = time.time()
        self.last_action = time.time()
        self.started = False
        self.solo = False

    def join(self, name, seat=None):
        free = [i for i in range(4) if self.tokens[i] is None and not self.is_bot[i]]
        if self.started:
            # a human may take over a bot seat in a running game
            free = [i for i in range(4) if self.is_bot[i]]
        if seat is not None and seat in free:
            pick = seat
        elif free:
            pick = free[0]
        else:
            raise ValueError("Table is full")
        token = secrets.token_hex(8)
        self.tokens[pick] = token
        self.is_bot[pick] = False
        self.names[pick] = (name or "Player")[:16]
        if self.host is None:
            self.host = pick
        return token, pick

    def seat_of(self, token):
        return self.tokens.index(token) if token in self.tokens and token else None

    def start(self, solo=False):
        self.solo = solo
        for i in range(4):
            if self.tokens[i] is None:
                self.is_bot[i] = True
                self.names[i] = BOT_NAMES[i] + " (CPU)"
        self.started = True
        self.new_deal()

    def new_deal(self):
        self.board += 1
        dealer = (self.board - 1) % 4
        self.deal = Deal(self.board, dealer)
        self.last_action = time.time()

    def _controller(self, d, seat):
        if (self.solo and d.phase == "playing" and d.contract
                and side(d.contract["declarer"]) == 0 and side(seat) == 0):
            return 2
        return d.controller(seat)

    def _controller_is_bot(self, d):
        seat = d.turn if d.phase == "bidding" else self._controller(d, d.turn)
        return self.is_bot[seat]

    def advance(self):
        """Let computer players and trick timers move the game along."""
        d = self.deal
        if not d or d.phase == "done":
            return
        now = time.time()
        if d.phase == "playing" and d.trick_done_at:
            if now - d.trick_done_at >= TRICK_DELAY:
                d.resolve_trick()
                self._record(d)
                self.last_action = time.time()
            return
        if now - self.last_action < BOT_DELAY or not self._controller_is_bot(d):
            return
        if d.phase == "bidding":
            call = bot.bot_call(d, d.turn)
            if call not in d.legal_calls():
                call = "P"
            d.bid(d.turn, call)
        else:
            d.play(d.turn, bot.bot_play(d, d.turn))
        self.last_action = time.time()

    def _record(self, d):
        if d.phase == "done" and d.result and not getattr(d, "recorded", False):
            d.recorded = True
            self.score[0] += d.result["ns"]
            self.score[1] += d.result["ew"]
            self.history.append(dict(board=d.board, text=d.result["text"], ns=d.result["ns"], ew=d.result["ew"]))

    def bid(self, token, call):
        seat = self.seat_of(token)
        if seat is None:
            raise ValueError("Not seated")
        self.deal.bid(seat, call)
        self.last_action = time.time()
        self._record(self.deal)

    def play(self, token, card):
        seat = self.seat_of(token)
        d = self.deal
        if seat is None or d.phase != "playing" or self._controller(d, d.turn) != seat:
            raise ValueError("Not your turn")
        d.play(d.turn, card)
        self.last_action = time.time()

    def next_deal(self, token):
        if self.seat_of(token) is None:
            raise ValueError("Not seated")
        if self.deal and self.deal.phase == "done":
            self.new_deal()

    def view(self, token):
        self.advance()
        self._record(self.deal) if self.deal else None
        me = self.seat_of(token)
        v = dict(code=self.code, started=self.started, me=me, host=self.host,
                 seats=[dict(name=self.names[i], bot=self.is_bot[i], seat=SEATS[i]) for i in range(4)],
                 score=dict(ns=self.score[0], ew=self.score[1]), history=self.history[-10:])
        d = self.deal
        if not d:
            return v
        playing = d.phase in ("playing", "done")
        turn_seat = d.turn if d.phase != "done" else None
        actor = None
        if d.phase == "bidding":
            actor = d.turn
        elif d.phase == "playing" and not d.trick_done_at:
            actor = self._controller(d, d.turn)
        hands = [None] * 4
        counts = [len(h) for h in d.hands]
        for i in range(4):
            show = d.phase == "done" or i == me
            if playing and d.contract and i == d.dummy and d.dummy_visible():
                show = True
            if playing and d.contract and me == d.contract["declarer"] and i == d.dummy:
                show = True if d.dummy_visible() else show
            if (playing and self.solo and me == 2 and d.contract
                    and side(d.contract["declarer"]) == 0 and side(i) == 0):
                show = True
            if show:
                hands[i] = list(d.hands[i]) if d.phase != "done" else sort_hand(d.original[i])
        v["deal"] = dict(
            board=d.board, dealer=d.dealer, vul=list(d.vul), phase=d.phase, turn=turn_seat,
            actor=actor, calls=[dict(seat=s, call=c) for s, c in d.calls],
            hands=hands, counts=counts, trick=[dict(seat=s, card=c) for s, c in d.trick],
            last_trick=[dict(seat=s, card=c) for s, c in (d.last_trick or [])],
            tricks=list(d.tricks_won), trump=d.trump,
            contract=dict(text=contract_str(d.contract), declarer=d.contract["declarer"], dummy=d.dummy)
            if d.contract else None,
            result=d.result,
        )
        if me is not None and actor == me:
            if d.phase == "bidding":
                v["deal"]["legal"] = d.legal_calls()
            else:
                v["deal"]["legal"] = d.legal_plays(d.turn)
        return v
