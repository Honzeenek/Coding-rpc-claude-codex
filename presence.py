#!/usr/bin/env python3
from pypresence import Presence
import psutil
import time
import sys

CLIENT_ID_CLAUDE = "1495774494474637504"
CLIENT_ID_CODEX = "1495782123678990396"

CLAUDE_RENDERERS = {"Claude Helper (Renderer)"}
CODEX_RENDERERS = {"Codex Helper (Renderer)"}
CODEX_CLI_NAMES = {"codex", "codex-cli"}


def detect_app():
    claude = False
    codex = False
    for proc in psutil.process_iter(['name']):
        try:
            name = proc.info['name'] or ""
            if name in CLAUDE_RENDERERS:
                claude = True
            if name in CODEX_RENDERERS or name in CODEX_CLI_NAMES:
                codex = True
        except (psutil.NoSuchProcess, psutil.AccessDenied):
            continue
    if codex:
        return "codex"
    if claude:
        return "claude"
    return None


def connect(client_id):
    rpc = Presence(client_id)
    rpc.connect()
    return rpc


def main():
    current_app = None
    rpc = None
    start_time = None

    while True:
        try:
            app = detect_app()

            if app != current_app:
                if rpc is not None:
                    try:
                        rpc.clear()
                        rpc.close()
                    except Exception:
                        pass
                    rpc = None

                current_app = app
                start_time = int(time.time()) if app else None

                if app == "claude":
                    rpc = connect(CLIENT_ID_CLAUDE)
                    rpc.update(
                        details="Thinking together",
                        state="Using Claude Desktop",
                        large_image="claude_logo",
                        large_text="Claude",
                        start=start_time,
                    )
                    print("-> Claude", flush=True)
                elif app == "codex":
                    rpc = connect(CLIENT_ID_CODEX)
                    rpc.update(
                        details="Shipping code",
                        state="Coding with Codex",
                        large_image="codex_logo",
                        large_text="Codex",
                        start=start_time,
                    )
                    print("-> Codex", flush=True)
                else:
                    print("-> Idle", flush=True)

            time.sleep(15)
        except KeyboardInterrupt:
            if rpc is not None:
                try:
                    rpc.clear()
                    rpc.close()
                except Exception:
                    pass
            print("\nStopped.")
            break
        except Exception as e:
            print(f"Error: {e}", flush=True)
            if rpc is not None:
                try:
                    rpc.close()
                except Exception:
                    pass
                rpc = None
            current_app = None
            time.sleep(30)


if __name__ == "__main__":
    main()
