"""Install verified local skill locations, backing up changed files first."""
from pathlib import Path
from datetime import datetime
import hashlib
import json
import os
import re
import shutil

ROOT = Path(__file__).resolve().parents[1]
NAME = "wfeng-can-lvgl-ota"
HOME_DIR = Path.home()


def install():
    standard = ROOT / "skills" / NAME
    if not (standard / "SKILL.md").is_file():
        raise SystemExit("Run python scripts/build_skill.py first")
    # Shared directory documented by both Codex and DeepSeek Harness.
    agents_home = Path(os.environ.get("DSH_AGENTS_HOME") or HOME_DIR / ".agents")
    destinations = [("Codex / DeepSeek Harness", standard, HOME_DIR / ".agents" / "skills" / NAME)]
    if agents_home.resolve() != (HOME_DIR / ".agents").resolve():
        destinations.append(("DeepSeek Harness custom agents home", standard, agents_home / "skills" / NAME))
    wb_skills = HOME_DIR / ".workbuddy" / "skills"
    if wb_skills.is_dir():
        matches = []
        for entry in wb_skills.glob("*/SKILL.md"):
            match = re.search(r"(?m)^name:\s*[\"']?([^\s\"']+)", entry.read_text(encoding="utf-8-sig"))
            if match and match.group(1) == NAME:
                matches.append(entry.parent)
        if len(matches) > 1:
            raise SystemExit("Multiple WorkBuddy copies found; resolve duplicate skill identities first")
        destinations.append(("WorkBuddy", ROOT / "dist" / "workbuddy" / NAME, matches[0] if matches else wb_skills / NAME))

    for platform, source, target in destinations:
        if not (source / "SKILL.md").is_file():
            raise SystemExit(f"Missing {platform} package. Run python scripts/build_skill.py first.")

    stamp = datetime.now().strftime("%Y%m%d-%H%M%S-%f")
    report = []
    for index, (platform, source, target) in enumerate(destinations):
        changed = [p for p in source.rglob("*") if p.is_file() and (not (target / p.relative_to(source)).is_file() or p.read_bytes() != (target / p.relative_to(source)).read_bytes())]
        backup = None
        if changed and target.exists():
            backup = ROOT / "backups" / stamp / str(index) / target.name
            shutil.copytree(target, backup)
        for path in changed:
            dest = target / path.relative_to(source)
            dest.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(path, dest)
        for path in source.rglob("*"):
            if path.is_file() and path.read_bytes() != (target / path.relative_to(source)).read_bytes():
                raise RuntimeError(f"Copy verification failed: {path}")
        report.append({"platform": platform, "path": str(target), "changed_files": len(changed), "backup": str(backup) if backup else None, "sha256": hashlib.sha256((target / "SKILL.md").read_bytes()).hexdigest()})
    result = ROOT / "dist" / "installation-report.json"
    # Keep prior backup records across idempotent reruns.
    previous = json.loads(result.read_text(encoding="utf-8")) if result.exists() else []
    for item in report:
        if not item["backup"]:
            item["backup"] = next((old.get("backup") for old in previous if old["path"] == item["path"]), None)
    result.write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(report, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    install()
