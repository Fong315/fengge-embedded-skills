"""Render public Markdown guides as crawlable static GitHub Pages documents."""
from html import escape
from pathlib import Path
from xml.etree.ElementTree import Element, SubElement, tostring
import json

import markdown
import yaml

from build_skill import VARIANT_ARCHIVE, VARIANTS

ROOT = Path(__file__).resolve().parents[1]
DOCS = ROOT / "docs"
BASE = "https://fong315.github.io/fengge-embedded-skills/"
REPO = "https://github.com/Fong315/fengge-embedded-skills"
PAGES = [("index", "技能介绍"), ("installation", "安装指南"), ("examples", "使用示例"), ("faq", "常见问题"), ("variants", "版本")]


def write_variant_index():
    rows = "\n".join(f"| [{title}]({REPO}/tree/main/skills/{name}) | `{name}` | {focus} |" for name, title, focus in VARIANTS)
    source = f'''---
title: 峰哥嵌入式学习助手的十个技能版本与安装入口
description: 按 STM32、ESP32、单片机零基础、C51、RT-Thread、嵌入式 Linux、项目面试、蓝桥杯与器件清单查找峰哥技能版本。每份提供独立安装 ID，共用答疑流程与资料。
---

# 选择一个峰哥技能版本

十个版本提供不同的展示名称和安装 ID，共用峰哥嵌入式学习助手的答疑流程和资料。选一个符合你习惯的名称即可。

| 展示名称 | 安装 ID | 描述重点 |
| --- | --- | --- |
{rows}

## 安装任意一个版本

例如，选择“峰哥 · STM32 学习路线”时运行下面的命令。

```bash
npx skills add Fong315/fengge-embedded-skills --skill fengge-stm32-roadmap -a codex -g
```

选择其他版本时，将 `--skill` 后面的值换成表中的 ID。安装后可在 Codex 中输入 `$` 加对应的 ID，选择该技能。

[下载十个标准技能文件夹]({REPO}/releases/latest/download/{VARIANT_ARCHIVE})，解压后将选中的完整文件夹导入支持标准 Agent Skills 的客户端。原版及其他平台格式见[安装指南](installation.html)。
'''
    (DOCS / "variants.md").write_text(source, encoding="utf-8", newline="\n")


def build():
    write_variant_index()
    skill = (ROOT / "skills" / "wfeng-can-lvgl-ota" / "SKILL.md").read_text(encoding="utf-8")
    version = yaml.safe_load(skill.split("---", 2)[1])["metadata"]["version"]
    sitemap = Element("urlset", xmlns="http://www.sitemaps.org/schemas/sitemap/0.9")
    for slug, label in PAGES:
        source = (DOCS / f"{slug}.md").read_text(encoding="utf-8")
        _, frontmatter, body = source.split("---", 2)
        meta = yaml.safe_load(frontmatter)
        renderer = markdown.Markdown(extensions=["tables", "fenced_code", "toc", "attr_list"], extension_configs={"toc": {"toc_depth": "2"}})
        content = renderer.convert(body)
        canonical = BASE if slug == "index" else BASE + slug + ".html"
        nav = "".join(f'<a href="{s}.html"' + (' aria-current="page"' if s == slug else '') + f'>{t}</a>' for s, t in PAGES)
        structured = {
            "@context": "https://schema.org", "@type": "SoftwareSourceCode",
            "name": "峰哥嵌入式学习助手", "alternateName": "Fengge Embedded Learning Skill",
            "description": meta["description"], "codeRepository": REPO,
            "url": BASE, "version": version, "inLanguage": "zh-CN",
            "programmingLanguage": "Markdown", "isAccessibleForFree": True,
        }
        html = f'''<!doctype html>
<html lang="zh-CN">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>{escape(meta["title"])}</title>
  <meta name="description" content="{escape(meta["description"], quote=True)}">
  <meta name="robots" content="index,follow">
  <link rel="canonical" href="{canonical}">
  <link rel="stylesheet" href="style.css">
  <link rel="sitemap" type="application/xml" href="{BASE}sitemap.xml">
  <meta property="og:type" content="website">
  <meta property="og:locale" content="zh_CN">
  <meta property="og:title" content="{escape(meta["title"], quote=True)}">
  <meta property="og:description" content="{escape(meta["description"], quote=True)}">
  <meta property="og:url" content="{canonical}">
  <meta property="og:site_name" content="峰哥嵌入式学习助手">
  <script type="application/ld+json">{json.dumps(structured, ensure_ascii=False).replace('</', '<' + chr(92) + '/')}</script>
</head>
<body>
  <a class="skip" href="#main">跳到正文</a>
  <header class="site-header"><div class="header-inner">
    <a class="brand" href="index.html"><span class="brand-icon" aria-hidden="true">F</span><span>峰哥<span class="brand-sub">嵌入式学习助手</span></span></a>
    <nav aria-label="主导航">{nav}</nav>
    <a class="github" href="{REPO}">GitHub ↗</a>
  </div></header>
  <div class="layout">
    <aside aria-label="本页目录"><span class="eyebrow">本页内容</span>{renderer.toc}</aside>
    <main id="main"><div class="page-meta"><span>中文 · EMBEDDED LEARNING</span><span>v{escape(version)}</span></div>
      <article>{content}</article>
      <div class="next-step"><strong>把下一步学习任务说清楚。</strong><span>选择适合你的客户端，带着一个真实问题开始。</span><a href="installation.html">查看安装指南 →</a></div>
    </main>
  </div>
  <footer><span>峰哥 · 嵌入式单片机答疑</span><div><a href="{slug}.md">本页 Markdown</a><a href="llms.txt">阅读索引</a><a href="sitemap.xml">站点地图</a><a href="{REPO}/issues">反馈问题</a></div><p>公开说明与安装资料。搜索收录和技能调用由相应平台决定。</p></footer>
</body>
</html>
'''
        (DOCS / f"{slug}.html").write_text(html, encoding="utf-8", newline="\n")
        SubElement(SubElement(sitemap, "url"), "loc").text = canonical
    (DOCS / "sitemap.xml").write_bytes(b'<?xml version="1.0" encoding="utf-8"?>\n' + tostring(sitemap, encoding="utf-8"))
    links = "\n".join(f"- [{label}]({BASE}{slug}.html): [Markdown]({BASE}{slug}.md)" for slug, label in PAGES)
    (DOCS / "llms.txt").write_text(f"# 峰哥嵌入式学习助手 / Fengge Embedded Learning Skill\n\n> 中文嵌入式学习路线、单片机答疑与项目资料导航。Skill ID: wfeng-can-lvgl-ota。\n\n{links}\n- [技能入口]({REPO}/blob/main/skills/wfeng-can-lvgl-ota/SKILL.md)\n- [版本下载]({REPO}/releases/latest)\n\n索引供阅读工具使用，不表示任何平台已收录、安装或启用技能。示例为编辑示例，资料包包含链接而非全部飞书正文。\n", encoding="utf-8", newline="\n")
    print(f"Built {len(PAGES)} static documentation pages, sitemap and reading index")


if __name__ == "__main__":
    build()
