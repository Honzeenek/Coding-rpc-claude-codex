# Discord Rich Presence — Claude & Codex (macOS)

Background script that shows **"Using Claude"** or **"Coding with Codex"** on your Discord profile based on which app is running locally.

## Setup

1. Clone and enter the repo:
   ```bash
   git clone <your-repo-url> RPC && cd RPC
   ```

2. Create a Discord Application at https://discord.com/developers/applications
   - Upload two Rich Presence assets named exactly `claude_logo` and `codex_logo`
   - Copy the **Application ID** and paste it into `presence.py` as `CLIENT_ID`

3. Create a venv and install deps:
   ```bash
   python3 -m venv .venv
   .venv/bin/pip install -r requirements.txt
   ```

4. Test it:
   ```bash
   .venv/bin/python3 presence.py
   ```
   You should see `Connected to Discord.` followed by `-> Claude` / `-> Codex` / `-> Idle`.

5. Install as a launchd agent so it runs at login:
   ```bash
   # Edit com.hanz.discordpresence.plist — replace /Users/janpalenik with your path
   cp com.hanz.discordpresence.plist ~/Library/LaunchAgents/
   launchctl load ~/Library/LaunchAgents/com.hanz.discordpresence.plist
   launchctl list | grep discordpresence
   ```

## Requirements

- Discord **desktop app** must be running (browser Discord does not expose the IPC socket)
- Discord Settings → Activity Privacy → **Display current activity** must be ON
- Custom asset icons can take up to ~10 min to appear after upload

## Managing the agent

```bash
# stop
launchctl unload ~/Library/LaunchAgents/com.hanz.discordpresence.plist
# start
launchctl load ~/Library/LaunchAgents/com.hanz.discordpresence.plist
# logs
tail -f presence.log presence.err
```

## Troubleshooting

- `Discord not running or connection failed` → open the Discord desktop app.
- Presence shows nothing → check Activity Privacy setting, and confirm asset names match (`claude_logo`, `codex_logo`).
- Wrong process detected → run `ps aux | grep -iE "claude|codex"` and adjust `CLAUDE_PROCESSES` / `CODEX_PROCESSES` in `presence.py`.
