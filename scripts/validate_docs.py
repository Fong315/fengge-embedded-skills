"""Check the public site's crawlable content, metadata, and local navigation."""
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import unquote, urlsplit
from xml.etree import ElementTree
import json
import re

import yaml

from build_docs import BASE, DOCS, PAGES, ROOT


class Page(HTMLParser):
    def __init__(self, text):
        super().__init__(convert_charrefs=True)
        self.links, self.ids, self.canonical = [], set(), []
        self.meta, self.h1, self.main = {}, 0, False
        self.jsonld, self.reading_json, self.lang = [], False, ""
        self.feed(text)

    def handle_starttag(self, tag, attrs):
        data = dict(attrs)
        if "id" in data:
            if data["id"] in self.ids:
                raise ValueError(f"Duplicate anchor: {data['id']}")
            self.ids.add(data["id"])
        if tag == "html":
            self.lang = data.get("lang")
        if tag == "h1":
            self.h1 += 1
        if tag == "main":
            self.main = True
        if tag == "meta":
            self.meta[data.get("name", data.get("property"))] = data.get("content")
        if tag == "link" and data.get("rel") == "canonical":
            self.canonical.append(data.get("href"))
        if "href" in data:
            self.links.append(data["href"])
        if tag == "script":
            if data.get("type") != "application/ld+json":
                raise ValueError("Public documentation should not depend on executable scripts")
            self.reading_json = True

    def handle_endtag(self, tag):
        if tag == "script":
            self.reading_json = False

    def handle_data(self, text):
        if self.reading_json:
            self.jsonld.append(text)


def validate():
    pages = {}
    for slug, _ in PAGES:
        path = DOCS / f"{slug}.html"
        pages[path.name] = Page(path.read_text(encoding="utf-8"))
    for name, page in pages.items():
        expected = BASE if name == "index.html" else BASE + name
        assert page.canonical == [expected], f"Wrong canonical URL: {name}"
        assert page.lang == "zh-CN" and page.h1 == 1 and page.main, f"Missing semantic content: {name}"
        assert page.meta.get("description") and page.meta.get("viewport"), f"Missing metadata: {name}"
        assert page.meta.get("robots") == "index,follow", f"Unintended indexing exclusion: {name}"
        data = json.loads("".join(page.jsonld))
        assert data["codeRepository"] == "https://github.com/Fong315/fengge-embedded-skills"
        assert "aggregateRating" not in data and "review" not in data, "Unverified social proof"
        for href in page.links:
            link = urlsplit(href)
            if link.scheme or link.netloc:
                continue
            target_name = unquote(link.path) or name
            target = (DOCS / target_name).resolve()
            assert target.is_relative_to(DOCS.resolve()) and target.is_file(), f"Missing local link: {name} -> {href}"
            if link.fragment and target.suffix == ".html":
                assert unquote(link.fragment) in pages[target.name].ids, f"Missing anchor: {name} -> {href}"
    tree = ElementTree.parse(DOCS / "sitemap.xml")
    urls = {element.text for element in tree.findall(".//{*}loc")}
    assert urls == {BASE if slug == "index" else BASE + slug + ".html" for slug, _ in PAGES}
    readme = (ROOT / "README.md").read_text(encoding="utf-8")
    for target in re.findall(r"\]\(([^)]+)\)", readme):
        parsed = urlsplit(target)
        if not parsed.scheme and not parsed.netloc and parsed.path:
            assert (ROOT / unquote(parsed.path)).is_file(), f"Missing README target: {target}"
    skill = yaml.safe_load((ROOT / "skills/wfeng-can-lvgl-ota/SKILL.md").read_text(encoding="utf-8").split("---", 2)[1])
    assert skill["metadata"]["homepage"] == BASE
    assert f"`{skill['metadata']['version']}`" in readme, "README version differs"
    print(f"PASS: {len(pages)} public HTML pages, metadata, local links and anchors, sitemap, README, skill homepage")


if __name__ == "__main__":
    validate()
