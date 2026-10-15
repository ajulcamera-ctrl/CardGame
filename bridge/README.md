# ♠ Bridge – browser game for Raspberry Pi

Contract bridge (4 players) played in a browser; the server runs on your Pi.
Solo mode (you vs. three computer players) or multiplayer (up to 4 humans on one table; empty seats are filled by the computer).
Pure Python standard library – no dependencies.

## Run on the Pi

```bash
git clone <this repo> && cd CardGame/bridge
python3 server.py --port 7070          # or: docker compose up -d --build
```

Find the Pi's address with `hostname -I`, then open `http://<pi-ip>:7070` on any device on your network.

## Playing
- **Play solo**: you sit South, partnered with North (CPU) against East/West (CPU).
- **Multiplayer**: one person clicks *Create multiplayer table* and shares the 4-letter code; others enter it and *Join*. The host clicks *Start game*. Partners sit opposite (N–S vs E–W).
- Standard rules: bidding (Pass/X/XX, 1♣–7NT), declarer plays dummy, follow suit, trump contract.
- Scoring is duplicate-style per deal (with vulnerability, game/slam bonuses); running totals are shown.
- The computer uses simple heuristic bidding (point count) and play – beatable!
- Tables live in memory and are dropped after 6 idle hours or a server restart.

## Learning to play
- **Tutorial**: the lobby's *Tutorial* button opens a 9-step walkthrough (partnerships, counting points, bidding, trumps, declarer/dummy, tricks, scoring).
- **Rules**: the *Rules* button (lobby) or *Help* button (in game) opens tabs for Basics, Bidding, Play and Scoring.
- **Hints**: a tip bar during the game shows your high card points while bidding and play reminders (follow suit, playing for dummy). Toggle with *Hints: on/off*; the choice is remembered in the browser.
- The help content lives in `static/help.js`.

## Notes
- No authentication: only use on a trusted home network.
- Test the engine: `python3 -c "import engine"` from the `bridge` directory.
