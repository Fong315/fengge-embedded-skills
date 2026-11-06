"""Validate portable files, resource preservation, and distributable archives."""
from pathlib import Path
import hashlib
import json
import re
import zipfile

import yaml

ROOT = Path(__file__).resolve().parents[1]
NAME = "wfeng-can-lvgl-ota"


def require(condition, message):
    if not condition:
        raise ValueError(message)


def metadata(path):
    text = path.read_text(encoding="utf-8")
    require(text.startswith("---\n"), f"Missing frontmatter: {path}")
    data = yaml.safe_load(text.split("---", 2)[1])
    require(isinstance(data, dict), f"Invalid YAML mapping: {path}")
    require(data.get("name") == NAME, f"Unexpected skill name: {path}")
    description = data.get("description")
    require(isinstance(description, str) and 0 < len(description) <= 1024, f"Invalid description: {path}")
    return data, text


def validate():
    standard = ROOT / "skills" / NAME
    wb = ROOT / "dist" / "workbuddy" / NAME
    meta, text = metadata(standard / "SKILL.md")
    require(set(meta) <= {"name", "description", "metadata", "license", "compatibility", "allowed-tools"}, "Non-portable top-level metadata")
    require(all(isinstance(v, str) for v in meta.get("metadata", {}).values()), "Metadata values must be strings")
    for relative in re.findall(r"\]\(((?:references|agents)/[^)]+)\)", text):
        require((standard / relative).is_file(), f"Missing reference: {relative}")
    wbmeta, wbtext = metadata(wb / "SKILL.md")
    for field in ("display_name", "display_name_en", "description_zh", "description_en", "version", "author"):
        require(isinstance(wbmeta.get(field), str) and wbmeta[field], f"Missing WorkBuddy field: {field}")
    for relative in re.findall(r"@(references/[^\s，。]+)", wbtext):
        require((wb / relative).is_file(), f"Missing WorkBuddy reference: {relative}")
        require((wb / relative).read_bytes() == (standard / relative).read_bytes(), f"Platform content differs: {relative}")
    interface = yaml.safe_load((standard / "agents" / "openai.yaml").read_text(encoding="utf-8"))
    require(interface["policy"]["allow_implicit_invocation"] is True, "Implicit invocation disabled")
    require(25 <= len(interface["interface"]["short_description"]) <= 64, "Invalid Codex UI description length")
    require("$" + NAME in interface["interface"]["default_prompt"], "Default prompt missing skill name")

    for archive, folder, prefix in ((ROOT / "dist" / f"{NAME}.zip", standard, NAME + "/"), (ROOT / "dist" / f"{NAME}-workbuddy.zip", wb, "")):
        expected = {prefix + p.relative_to(folder).as_posix(): p.read_bytes() for p in folder.rglob("*") if p.is_file()}
        with zipfile.ZipFile(archive) as z:
            require(z.testzip() is None, f"Invalid archive: {archive}")
            require(set(z.namelist()) == set(expected), f"Archive contents differ: {archive}")
            require(all(z.read(k) == v for k, v in expected.items()), f"Stale archive: {archive}")

    manifest = json.loads((ROOT / "dist" / "manifest.json").read_text(encoding="utf-8"))
    source = ROOT / "峰哥答疑单片机嵌入式-SKILL.md"
    require(hashlib.sha256(source.read_bytes()).hexdigest() == manifest["source_sha256"], "Source changed after build")
    for relative, digest in manifest["files"].items():
        require(hashlib.sha256((standard / relative).read_bytes()).hexdigest() == digest, f"Stale manifest: {relative}")
    urls = lambda content: set(re.findall(r"https?://[^\s<>`）)\"']+", content))
    combined = "\n".join(p.read_text(encoding="utf-8") for p in standard.rglob("*") if p.is_file())
    require(urls(source.read_text(encoding="utf-8")) <= urls(combined), "Source resource links lost")
    standalone = (ROOT / "dist" / "峰哥嵌入式答疑-通用导入版.md").read_text(encoding="utf-8")
    require(not re.search(r"\]\((?:references|agents)/", standalone), "Standalone document has unresolved references")
    print(f"PASS: portable skill, WorkBuddy manifest, references, archives, {manifest['source_url_count']} original URLs, standalone import")


if __name__ == "__main__":
    validate()
