"""
game_manager.py – Manages multiple simultaneous Game instances, one per chat.
"""

from datetime import datetime, timedelta, timezone

from game import Game

# Games idle for longer than this will be automatically removed
_GAME_TTL_HOURS = 24
# Cleanup runs at most once per hour to avoid overhead on every request
_CLEANUP_INTERVAL_SECONDS = 3600


class GameManager:
    def __init__(self):
        # {chat_id: Game}
        self._games: dict[int, Game] = {}
        self._last_cleanup: datetime = datetime.now(timezone.utc)

    def create_game(self, chat_id: int, pack_key: str, creator_id: int) -> Game:
        """Create (or replace) a game for the given chat."""
        game = Game(chat_id, pack_key, creator_id)
        self._games[chat_id] = game
        return game

    def get_game(self, chat_id: int) -> Game | None:
        """Return the active game for a chat, or None.
        Also triggers periodic cleanup of stale games."""
        self._cleanup_stale_games()
        return self._games.get(chat_id)

    def remove_game(self, chat_id: int) -> None:
        """Remove a finished or abandoned game."""
        self._games.pop(chat_id, None)

    def has_game(self, chat_id: int) -> bool:
        return chat_id in self._games

    def _cleanup_stale_games(self) -> None:
        """Remove games that have been idle for longer than _GAME_TTL_HOURS.
        Runs at most once per _CLEANUP_INTERVAL_SECONDS to limit overhead."""
        now = datetime.now(timezone.utc)
        if (now - self._last_cleanup).total_seconds() < _CLEANUP_INTERVAL_SECONDS:
            return
        self._last_cleanup = now
        cutoff = now - timedelta(hours=_GAME_TTL_HOURS)
        stale = [cid for cid, g in self._games.items() if g.last_activity < cutoff]
        for cid in stale:
            del self._games[cid]
