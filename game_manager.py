"""
game_manager.py – Manages multiple simultaneous Game instances, one per chat.
"""

from game import Game


class GameManager:
    def __init__(self):
        # {chat_id: Game}
        self._games: dict[int, Game] = {}

    def create_game(self, chat_id: int, pack_key: str, creator_id: int) -> Game:
        """Create (or replace) a game for the given chat."""
        game = Game(chat_id, pack_key, creator_id)
        self._games[chat_id] = game
        return game

    def get_game(self, chat_id: int) -> Game | None:
        """Return the active game for a chat, or None."""
        return self._games.get(chat_id)

    def remove_game(self, chat_id: int) -> None:
        """Remove a finished or abandoned game."""
        self._games.pop(chat_id, None)

    def has_game(self, chat_id: int) -> bool:
        return chat_id in self._games
