"""Validate portable files, resource preservation, and distributable archives."""
from pathlib import Path
import hashlib
import json
import re
import zipfile

import yaml

from build_skill import NAME, ROOT, VARIANT_ARCHIVE, VARIANTS, VERSION


def require(condition, message):
    if not condition:
        raise ValueError(message)


def metadata(path, name=NAME):
    text = path.read_text(encoding="utf-8")
    require(text.startswith("---\n"), f"Missing frontmatter: {path}")
    data = yaml.safe_load(text.split("---", 2)[1])
    require(isinstance(data, dict), f"Invalid YAML mapping: {path}")
    require(data.get("name") == name, f"Unexpected skill name: {path}")
    description = data.get("description")
    require(isinstance(description, str) and 0 < len(description) <= 1024, f"Invalid description: {path}")
    return data, text


def validate_variants(standard, original, original_text, interface):
    names = {name for name, _, _ in VARIANTS}
    require(len(VARIANTS) == len(names) == 10 and NAME not in names, "Expected ten distinct variant IDs")
    base_files = {path.relative_to(standard) for path in standard.rglob("*") if path.is_file()}
    base_body = original_text.split("---", 2)[2].strip().partition("\n")[2]
    expected = {}
    for name, title, _ in VARIANTS:
        require(re.fullmatch(r"[a-z0-9]+(?:-[a-z0-9]+)*", name) and len(name) <= 64, f"Invalid variant ID: {name}")
        folder = standard.parent / name
        meta, text = metadata(folder / "SKILL.md", name)
        require(meta["metadata"] == {**original["metadata"], "alias-of": NAME}, f"Variant metadata differs: {name}")
        require(meta["metadata"]["version"] == VERSION, f"Wrong version: {name}")
        heading, _, body = text.split("---", 2)[2].strip().partition("\n")
        require(heading == f"# {title}" and body == base_body, f"Variant changed the core skill: {name}")
        variant_ui = yaml.safe_load((folder / "agents/openai.yaml").read_text(encoding="utf-8"))
        require(variant_ui["interface"]["display_name"] == title, f"Wrong display name: {name}")
        prompt = interface["interface"]["default_prompt"].replace(f"${NAME}", f"${name}", 1)
        require(variant_ui["interface"]["default_prompt"] == prompt, f"Default prompt missing ID: {name}")
        require(variant_ui["policy"] == interface["policy"], f"Invocation policy differs: {name}")
        variant_files = {path.relative_to(folder) for path in folder.rglob("*") if path.is_file()}
        require(variant_files == base_files, f"Variant file set differs: {name}")
        for relative in variant_files:
            data = (folder / relative).read_bytes()
            if relative.as_posix() not in {"SKILL.md", "agents/openai.yaml"}:
                require(data == (standard / relative).read_bytes(), f"Variant resource differs: {name}/{relative}")
            expected[(Path(name) / relative).as_posix()] = data
    with zipfile.ZipFile(ROOT / "dist" / VARIANT_ARCHIVE) as archive:
        require(sorted(archive.namelist()) == sorted(expected), "Variant archive file set differs")
        require(all(archive.read(path) == data for path, data in expected.items()), "Variant archive has stale files")
    print(f"PASS: {len(names)} independently named variants with matching core and references")


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
    validate_variants(standard, meta, text, interface)

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
    require(standalone == (ROOT / "dist" / "fengge-embedded-chat-import.md").read_text(encoding="utf-8"), "Standalone download aliases differ")
    print(f"PASS: portable skill, WorkBuddy manifest, references, archives, {manifest['source_url_count']} original URLs, standalone import")


if __name__ == "__main__":
    validate()
