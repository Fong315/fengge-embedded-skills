"""Read Codex's actual skill catalog without starting a model conversation."""
from pathlib import Path
import json
import queue
import shutil
import subprocess
import threading

ROOT = Path(__file__).resolve().parents[1]
proc = subprocess.Popen([shutil.which("codex"), "app-server", "--stdio"], stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.DEVNULL, text=True, encoding="utf-8", creationflags=getattr(subprocess, "CREATE_NO_WINDOW", 0))
messages = queue.Queue()


def read():
    for line in proc.stdout:
        try:
            messages.put(json.loads(line))
        except json.JSONDecodeError:
            pass


def send(payload):
    proc.stdin.write(json.dumps(payload) + "\n")
    proc.stdin.flush()


def reply(message_id):
    while True:
        message = messages.get(timeout=30)
        if message.get("id") == message_id:
            if "error" in message:
                raise RuntimeError(message["error"])
            return message["result"]


threading.Thread(target=read, daemon=True).start()
try:
    send({"id": 1, "method": "initialize", "params": {"clientInfo": {"name": "local_skill_check", "version": "1.0.0"}, "capabilities": {"experimentalApi": True}}})
    reply(1)
    send({"method": "initialized", "params": {}})
    send({"id": 2, "method": "skills/list", "params": {"cwds": [str(ROOT)], "forceReload": True}})
    result = reply(2)
    matches = [s for group in result.get("data", []) for s in group.get("skills", []) if s.get("name") == "wfeng-can-lvgl-ota"]
    report = {"matches": matches, "count": len(matches)}
    (ROOT / "dist" / "codex-discovery.json").write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding="utf-8")
    print(json.dumps(report, ensure_ascii=False, indent=2))
    if len(matches) != 1 or not matches[0].get("enabled", True):
        raise SystemExit("Expected exactly one enabled skill")
finally:
    proc.terminate()
    try:
        proc.wait(timeout=5)
    except subprocess.TimeoutExpired:
        proc.kill()
