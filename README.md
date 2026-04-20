# Discord Rich Presence — Claude & Codex (macOS)

Background script that shows **"Using Claude Desktop"** or **"Coding with Codex"** on your Discord profile based on which app is running locally.

![MIT license](https://img.shields.io/badge/license-MIT-blue.svg)

## How it works

`presence.py` polls running processes every 15 seconds. When it sees Claude Desktop or Codex, it connects to Discord's local IPC socket (via [pypresence](https://github.com/qwertyquerty/pypresence)) and sets a Rich Presence activity. When both apps quit, it clears the activity.

## Setup

1. Clone the repo:
   ```bash
   git clone https://github.com/<you>/RPC.git && cd RPC
   ```

2. Create a venv and install deps:
   ```bash
   python3 -m venv .venv
   .venv/bin/pip install -r requirements.txt
   ```

3. Run it:
   ```bash
   .venv/bin/python3 presence.py
   ```
   You should see `-> Claude` / `-> Codex` / `-> Idle`. That's it — the script ships with default Discord application IDs so it works out of the box.

## Using your own Discord application (optional)

If you want your own app name / custom assets instead of the defaults:

1. Create a Discord Application at https://discord.com/developers/applications.
2. Upload two Rich Presence assets named exactly `claude_logo` and `codex_logo`.
3. Copy `config.example.json` to `config.json` and paste your Application IDs, **or** export env vars:
   ```bash
   export CLIENT_ID_CLAUDE=...
   export CLIENT_ID_CODEX=...
   ```

Env vars take precedence over `config.json`, which takes precedence over the built-in defaults.

## Run at login (launchd)

1. Copy the template plist and fill in your repo path:
   ```bash
   sed "s|{{REPO_PATH}}|$PWD|g" com.example.discordpresence.plist.example \
     > ~/Library/LaunchAgents/com.$USER.discordpresence.plist
   ```

2. Load it:
   ```bash
   launchctl load ~/Library/LaunchAgents/com.$USER.discordpresence.plist
   launchctl list | grep discordpresence
   ```

### Managing the agent

```bash
# stop
launchctl unload ~/Library/LaunchAgents/com.$USER.discordpresence.plist
# start
launchctl load ~/Library/LaunchAgents/com.$USER.discordpresence.plist
# logs
tail -f presence.log presence.err
```

## Requirements

- macOS (process detection uses macOS-specific app names — see Contributing below for Linux/Windows)
- Python 3.9+
- Discord **desktop app** running (browser Discord does not expose the IPC socket)
- Discord → Settings → Activity Privacy → **Display current activity** = ON
- Custom asset icons can take up to ~10 min to appear after upload

## Troubleshooting

- `Discord not running or connection failed` → open the Discord desktop app.
- Presence shows nothing → check Activity Privacy, and confirm asset names match (`claude_logo`, `codex_logo`) if using your own Discord app.
- Wrong process detected → run `ps aux | grep -iE "claude|codex"` and adjust `CLAUDE_RENDERERS` / `CODEX_RENDERERS` / `CODEX_CLI_NAMES` in `presence.py`.

## Contributing

PRs welcome — especially:
- Linux / Windows process detection
- Additional AI coding tools (Cursor, Zed, Aider, etc.)
- A proper CLI for configuring Client IDs and the plist

## License

MIT — see [LICENSE](LICENSE).
