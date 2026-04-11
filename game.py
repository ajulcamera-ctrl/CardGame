"""
game.py – Core game logic for the Telegram card game bot.

States
------
SETUP          – game object just created, waiting for players to join
WAITING_PLAYERS – at least one player has joined; game not yet started
PLAYING        – cards distributed, active player needs to pick a category
ROUND_EVAL     – evaluating the round (brief transitional state)
GAME_OVER      – one player has all cards; winner announced
"""

import random
from enum import Enum, auto
from card_packs import PACKS


class GameState(Enum):
    SETUP = auto()
    WAITING_PLAYERS = auto()
    PLAYING = auto()
    ROUND_EVAL = auto()
    GAME_OVER = auto()


MAX_PLAYERS = 6
MIN_PLAYERS = 1

# Sentinel user_id for the bot player (used in solo games)
BOT_USER_ID = -1


class Game:
    def __init__(self, chat_id: int, pack_key: str, creator_id: int):
        if pack_key not in PACKS:
            raise ValueError(f"Unknown pack '{pack_key}'. Choose from: {', '.join(PACKS)}")

        self.chat_id = chat_id
        self.pack_key = pack_key
        self.pack = PACKS[pack_key]
        self.creator_id = creator_id

        # Ordered list of player user_ids
        self.player_ids: list[int] = []
        # Display names  {user_id: name}
        self.player_names: dict[int, str] = {}
        # Each player's hand  {user_id: [Card, ...]}
        self.hands: dict[int, list] = {}

        self.state = GameState.SETUP
        self.active_player_index = 0   # index into self.player_ids
        self.round_number = 0
        self.bot_id: int | None = None  # set when a bot player is added for solo games

    # ------------------------------------------------------------------
    # Player management
    # ------------------------------------------------------------------

    def add_player(self, user_id: int, name: str) -> str:
        """Add a player to the game.  Returns a status message."""
        if self.state not in (GameState.SETUP, GameState.WAITING_PLAYERS):
            return "❌ Cannot join – the game has already started."
        if user_id in self.player_ids:
            return "⚠️ You have already joined."
        if len(self.player_ids) >= MAX_PLAYERS:
            return f"❌ The game is full ({MAX_PLAYERS} players max)."

        self.player_ids.append(user_id)
        self.player_names[user_id] = name
        self.state = GameState.WAITING_PLAYERS
        return f"✅ {name} joined the game! ({len(self.player_ids)}/{MAX_PLAYERS} players)"

    def remove_player(self, user_id: int) -> str:
        """Remove a player from the game."""
        if user_id not in self.player_ids:
            return "⚠️ You are not in this game."

        name = self.player_names[user_id]
        self.player_ids.remove(user_id)
        del self.player_names[user_id]
        self.hands.pop(user_id, None)

        if not self.player_ids:
            self.state = GameState.SETUP
        return f"👋 {name} has left the game."

    # ------------------------------------------------------------------
    # Game flow
    # ------------------------------------------------------------------

    def start_game(self, user_id: int) -> str:
        """Distribute cards and begin play.  Only the creator can call this."""
        if user_id != self.creator_id:
            return "❌ Only the game creator can start the game."
        if self.state != GameState.WAITING_PLAYERS:
            return "❌ Game cannot be started in its current state."
        if len(self.player_ids) < MIN_PLAYERS:
            return f"❌ Need at least {MIN_PLAYERS} player to start."

        # Solo mode: add a bot opponent automatically
        if len(self.player_ids) == 1:
            self.bot_id = BOT_USER_ID
            self.player_ids.append(self.bot_id)
            self.player_names[self.bot_id] = "🤖 Bot"

        self._deal_cards()
        self.state = GameState.PLAYING
        self.active_player_index = 0
        self.round_number = 1
        active_name = self.player_names[self.active_player]
        solo_note = "\n🤖 No other players? A Bot has joined as your opponent!" if self.bot_id else ""
        return (
            f"🃏 Game started with the *{self.pack.name}* pack!{solo_note}\n"
            f"Cards dealt to {len(self.player_ids)} players.\n"
            f"▶️ Round {self.round_number}: {active_name} goes first!"
        )

    def _deal_cards(self):
        """Shuffle the deck and distribute cards as evenly as possible."""
        deck = list(self.pack.cards)
        random.shuffle(deck)

        for pid in self.player_ids:
            self.hands[pid] = []

        for i, card in enumerate(deck):
            pid = self.player_ids[i % len(self.player_ids)]
            self.hands[pid].append(card)

    # ------------------------------------------------------------------
    # Round helpers
    # ------------------------------------------------------------------

    def bot_choose_stat(self) -> str | None:
        """Return the stat the bot will play (highest value on its top card).
        Returns None if the bot has no card or it is not the bot's turn."""
        if self.bot_id is None or self.active_player != self.bot_id:
            return None
        card = self.current_card(self.bot_id)
        if not card:
            return None
        return max(card.categories, key=lambda s: card.categories.get(s, 0))

    @property
    def active_player(self) -> int:
        return self.player_ids[self.active_player_index]

    def current_card(self, user_id: int):
        """Return the top card for a player (or None if they have no cards)."""
        hand = self.hands.get(user_id, [])
        return hand[0] if hand else None

    def play_round(self, chosen_stat: str) -> dict:
        """
        Evaluate a round given the stat chosen by the active player.

        Returns a result dict with keys:
          stat       – the chosen stat name
          values     – {player_id: value_of_top_card_for_stat}
          winner_id  – player_id of the round winner (or None for a draw)
          message    – human-readable summary string
          game_over  – True if the game has ended
        """
        if self.state != GameState.PLAYING:
            return {}

        self.state = GameState.ROUND_EVAL
        stat = chosen_stat

        # Collect the top card value for every (still active) player
        values = {}
        top_cards = {}
        for pid in self.player_ids:
            card = self.current_card(pid)
            if card:
                values[pid] = card.categories.get(stat, 0)
                top_cards[pid] = card

        # Determine winner(s) – higher is better for all stats
        max_val = max(values.values()) if values else 0
        winners = [pid for pid, val in values.items() if val == max_val]

        if len(winners) == 1:
            round_winner = winners[0]
        else:
            round_winner = None  # draw

        # Build the comparison table
        unit = self.pack.stat_units.get(stat, "")
        lines = [f"📊 *{stat}* results (Round {self.round_number}):"]
        for pid in self.player_ids:
            if pid in values:
                mark = "👑" if pid == round_winner else ("🤝" if round_winner is None and pid in winners else "  ")
                card_name = top_cards[pid].title
                val = values[pid]
                lines.append(f"{mark} {self.player_names[pid]}: {card_name} → {val} {unit}")

        if round_winner:
            winner_name = self.player_names[round_winner]
            lines.append(f"\n🏆 {winner_name} wins the round!")
        else:
            lines.append("\n🤝 It's a draw – everyone keeps their card!")

        # Transfer cards to winner (or keep in place on a draw)
        if round_winner is not None:
            for pid in list(self.player_ids):
                if pid in top_cards:
                    card = top_cards[pid]
                    self.hands[pid].remove(card)
                    self.hands[round_winner].append(card)
        else:
            # On a draw, rotate each player's top card to the bottom
            for pid in self.player_ids:
                if self.hands[pid]:
                    self.hands[pid].append(self.hands[pid].pop(0))

        # Remove players with no cards left
        eliminated = [pid for pid in list(self.player_ids) if not self.hands.get(pid)]
        for pid in eliminated:
            lines.append(f"💀 {self.player_names[pid]} is out of cards!")
            self.player_ids.remove(pid)

        # Check for game over
        game_over = len(self.player_ids) == 1
        if game_over:
            winner_id = self.player_ids[0]
            winner_name = self.player_names[winner_id]
            lines.append(f"\n🎉 *{winner_name} wins the entire game!* 🎉")
            self.state = GameState.GAME_OVER
        else:
            # Advance active player: winner becomes next active player
            if round_winner and round_winner in self.player_ids:
                self.active_player_index = self.player_ids.index(round_winner)
            else:
                # draw: advance to next in list
                self.active_player_index = (self.active_player_index + 1) % len(self.player_ids)
            self.round_number += 1
            next_name = self.player_names[self.active_player]
            lines.append(f"\n▶️ Round {self.round_number}: {next_name}'s turn!")
            self.state = GameState.PLAYING

        return {
            "stat": stat,
            "values": values,
            "winner_id": round_winner,
            "message": "\n".join(lines),
            "game_over": game_over,
        }

    # ------------------------------------------------------------------
    # Status helpers
    # ------------------------------------------------------------------

    def status_message(self) -> str:
        state_label = {
            GameState.SETUP: "Waiting for players to join",
            GameState.WAITING_PLAYERS: "Waiting for game to start",
            GameState.PLAYING: "In progress",
            GameState.ROUND_EVAL: "Evaluating round…",
            GameState.GAME_OVER: "Game over",
        }.get(self.state, str(self.state))

        lines = [
            f"🎮 *{self.pack.name} Pack* – {state_label}",
            f"👥 Players ({len(self.player_ids)}/{MAX_PLAYERS}):",
        ]
        for pid in self.player_ids:
            card_count = len(self.hands.get(pid, []))
            active_mark = "▶️ " if self.state == GameState.PLAYING and pid == self.active_player else "   "
            lines.append(f"  {active_mark}{self.player_names[pid]}: {card_count} cards")
        return "\n".join(lines)
