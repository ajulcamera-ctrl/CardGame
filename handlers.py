"""
handlers.py – Telegram command handlers and inline-button callbacks.

Commands
--------
/start               – welcome message & list of commands
/newgame <pack>      – create a new game (pack: animals|movies|countries|technology)
/join                – join the current game in this chat
/gamestart           – start the game (creator only)
/status              – show current game status
/quit                – leave the current game
"""

import time

from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ContextTypes
from telegram.helpers import escape_markdown

from game import GameState, MAX_PLAYERS
from game_manager import GameManager

game_manager = GameManager()

# ---------------------------------------------------------------------------
# Per-user rate limiting (prevents command/callback spam)
# ---------------------------------------------------------------------------
_RATE_LIMIT_SECONDS = 1.0
_user_last_cmd: dict[int, float] = {}


def _is_rate_limited(user_id: int) -> bool:
    """Return True if the user has sent a command too recently."""
    now = time.monotonic()
    if now - _user_last_cmd.get(user_id, 0.0) < _RATE_LIMIT_SECONDS:
        return True
    _user_last_cmd[user_id] = now
    return False

HELP_TEXT = (
    "🃏 *Card Game Bot*\n\n"
    "Commands:\n"
    "/newgame <pack> – Start a new game\n"
    "  Packs: `animals`, `movies`, `countries`, `technology`,\n"
    "         `supercars`, `f1`, `space`, `mountains`\n"
    "/join – Join the current game\n"
    "/gamestart – Start the game (creator only)\n"
    "/status – Show current game status\n"
    "/quit – Leave the current game\n\n"
    "How to play:\n"
    "1️⃣  One player creates a game with /newgame\n"
    "2️⃣  Other players join with /join (optional – play solo against 🤖 Bot!)\n"
    "3️⃣  Creator starts with /gamestart\n"
    "4️⃣  Active player picks a category – each stat shows ↑ (highest wins) or ↓ (lowest wins)!\n"
    "5️⃣  Winner takes all cards played that round.\n"
    "6️⃣  Last player standing wins 🏆\n\n"
    "💡 *Solo mode:* Use /newgame then /gamestart without anyone else joining – a Bot will be your opponent!"
)


async def cmd_start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    if _is_rate_limited(update.effective_user.id):
        return
    await update.message.reply_text(HELP_TEXT, parse_mode="Markdown")


async def cmd_new_game(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    chat_id = update.effective_chat.id
    user = update.effective_user

    if _is_rate_limited(user.id):
        return

    args = context.args
    if not args:
        await update.message.reply_text(
            "Usage: /newgame <pack>\nPacks: animals, movies, countries, technology, supercars, f1, space, mountains"
        )
        return

    pack_key = args[0].lower()
    if pack_key not in ("animals", "movies", "countries", "technology", "supercars", "f1", "space", "mountains"):
        await update.message.reply_text(
            "❌ Unknown pack. Choose from: animals, movies, countries, technology, supercars, f1, space, mountains"
        )
        return

    # Warn if a game is already in progress
    existing = game_manager.get_game(chat_id)
    if existing and existing.state not in (GameState.GAME_OVER,):
        await update.message.reply_text(
            "⚠️ A game is already running. It will be replaced with a new one."
        )

    game = game_manager.create_game(chat_id, pack_key, user.id)
    # Creator automatically joins; the return message is incorporated inline below
    game.add_player(user.id, user.first_name)

    esc_name = escape_markdown(user.first_name, version=2)
    esc_pack = escape_markdown(game.pack.name, version=2)
    player_count = len(game.player_ids)
    await update.message.reply_text(
        f"🎮 New *{esc_pack}* game created by {esc_name}\\!\n"
        f"Players: {player_count}/{MAX_PLAYERS}\n\n"
        f"Others can join with /join\\. Start the game with /gamestart\\.",
        parse_mode="MarkdownV2",
    )


async def cmd_join(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    chat_id = update.effective_chat.id
    user = update.effective_user

    if _is_rate_limited(user.id):
        return

    game = game_manager.get_game(chat_id)
    if not game:
        await update.message.reply_text("❌ No game in progress. Use /newgame <pack> to start one.")
        return

    msg = game.add_player(user.id, user.first_name)
    await update.message.reply_text(msg)


async def cmd_game_start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    chat_id = update.effective_chat.id
    user = update.effective_user

    if _is_rate_limited(user.id):
        return

    game = game_manager.get_game(chat_id)
    if not game:
        await update.message.reply_text("❌ No game in progress. Use /newgame <pack> to start one.")
        return

    msg = game.start_game(user.id)
    await update.message.reply_text(msg, parse_mode="MarkdownV2")

    if game.state == GameState.PLAYING:
        await _send_active_card(update, context, game)


async def cmd_status(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    chat_id = update.effective_chat.id

    if _is_rate_limited(update.effective_user.id):
        return

    game = game_manager.get_game(chat_id)
    if not game:
        await update.message.reply_text("❌ No game in progress.")
        return
    await update.message.reply_text(game.status_message(), parse_mode="MarkdownV2")


async def cmd_quit(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    chat_id = update.effective_chat.id
    user = update.effective_user

    if _is_rate_limited(user.id):
        return

    game = game_manager.get_game(chat_id)
    if not game:
        await update.message.reply_text("❌ No game in progress.")
        return

    msg = game.remove_player(user.id)
    await update.message.reply_text(msg)

    if game.state == GameState.GAME_OVER or not game.player_ids:
        game_manager.remove_game(chat_id)


# ---------------------------------------------------------------------------
# Inline button callback – active player picks a stat category
# ---------------------------------------------------------------------------

async def button_callback(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    query = update.callback_query
    await query.answer()

    chat_id = query.message.chat.id
    user = query.from_user

    if _is_rate_limited(user.id):
        return

    game = game_manager.get_game(chat_id)
    if not game:
        await query.edit_message_text("⚠️ No active game or it's not your turn.")
        return

    async with game.lock:
        # Re-check state inside the lock to prevent race conditions
        if game.state != GameState.PLAYING:
            await query.edit_message_text("⚠️ No active game or it's not your turn.")
            return

        # Only the active player may choose
        if user.id != game.active_player:
            active_name = game.player_names[game.active_player]
            await query.answer(f"⛔ Wait – it's {active_name}'s turn!", show_alert=True)
            return

        chosen_stat = query.data

        # Validate that chosen_stat is one of the valid stat names for this pack
        if chosen_stat not in game.pack.stat_names:
            await query.answer("⛔ Invalid stat choice.", show_alert=True)
            return

        result = game.play_round(chosen_stat)
        game_over = result.get("game_over", False)
        message = result.get("message", "")
    # Lock released – perform I/O outside the critical section

    if not result:
        await query.edit_message_text("⚠️ Could not evaluate round.")
        return

    await query.edit_message_text(message, parse_mode="MarkdownV2")

    if game_over:
        game_manager.remove_game(chat_id)
    else:
        # Show the next card for the new active player
        await _send_active_card_to_chat(context, chat_id, game)


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

async def _send_active_card(update: Update, context: ContextTypes.DEFAULT_TYPE, game) -> None:
    """Send the active player's top card with category buttons to the chat."""
    await _send_active_card_to_chat(context, update.effective_chat.id, game)


async def _send_active_card_to_chat(context: ContextTypes.DEFAULT_TYPE, chat_id: int, game) -> None:
    active_id = game.active_player
    card = game.current_card(active_id)
    if not card:
        return

    # If it's the bot's turn, resolve it automatically without showing a card prompt
    bot_stat = game.bot_choose_stat()
    if bot_stat is not None:
        async with game.lock:
            result = game.play_round(bot_stat)
        if not result:
            return
        await context.bot.send_message(
            chat_id=chat_id,
            text=result["message"],
            parse_mode="MarkdownV2",
        )
        if result["game_over"]:
            game_manager.remove_game(chat_id)
        else:
            await _send_active_card_to_chat(context, chat_id, game)
        return

    active_name = game.player_names[active_id]
    unit_map = game.pack.stat_units

    # Build card display (MarkdownV2 formatted)
    esc_title = escape_markdown(card.title, version=2)
    esc_name = escape_markdown(active_name, version=2)
    lines = [
        f"🃏 *{esc_title}*",
        f"👤 {esc_name}'s turn – pick a category\\!",
        "",
    ]
    for stat, val in card.categories.items():
        unit = unit_map.get(stat, "")
        direction = " ↓" if stat in game.pack.lower_is_better else " ↑"
        esc_stat = escape_markdown(stat, version=2)
        esc_unit = escape_markdown(unit, version=2)
        lines.append(f"  • {esc_stat}: {val} {esc_unit}{direction}".rstrip())

    # One button per stat (↑ highest wins, ↓ lowest wins)
    buttons = [
        [InlineKeyboardButton(
            f"{stat} {'↓' if stat in game.pack.lower_is_better else '↑'}",
            callback_data=stat,
        )]
        for stat in game.pack.stat_names
    ]
    keyboard = InlineKeyboardMarkup(buttons)

    await context.bot.send_message(
        chat_id=chat_id,
        text="\n".join(lines),
        parse_mode="MarkdownV2",
        reply_markup=keyboard,
    )
