"""Build a portable skill and a standalone chat import from the original MD."""
from pathlib import Path
from shutil import copyfile
import hashlib
import json
import re
import zipfile

ROOT = Path(__file__).resolve().parents[1]
NAME = "wfeng-can-lvgl-ota"
VERSION = "1.6.3"
SOURCE = ROOT / "峰哥答疑单片机嵌入式-SKILL.md"
SKILL = ROOT / "skills" / NAME
VARIANT_ARCHIVE = "fengge-skill-variants.zip"
VARIANTS = (
    ("fengge-embedded-learning", "峰哥 · 嵌入式学习助手", "嵌入式学习规划、单片机答疑和项目资料导航"),
    ("fengge-mcu-beginner", "峰哥 · 单片机零基础入门", "零基础单片机入门、学习顺序与第一步练习建议"),
    ("fengge-stm32-roadmap", "峰哥 · STM32 学习路线", "STM32 入门路线、练习安排与常见问题答疑"),
    ("fengge-esp32-learning", "峰哥 · ESP32 学习与资料", "ESP32 和 ESP32S3 学习答疑、项目资料与器件清单查找"),
    ("fengge-c51-learning", "峰哥 · C 语言与 51 单片机", "嵌入式 C 语言基础、51 单片机入门与学习资料查找"),
    ("fengge-rtthread-learning", "峰哥 · RT-Thread 学习指南", "RT-Thread 入门、实时操作系统基础答疑与项目资料查找"),
    ("fengge-embedded-linux", "峰哥 · 嵌入式 Linux 入门", "嵌入式 Linux 和 ARM-Linux 入门学习与资料查找"),
    ("fengge-embedded-interview", "峰哥 · 嵌入式项目面试", "嵌入式项目面试准备、常见问题和资料查找"),
    ("fengge-lanqiao-electronics", "峰哥 · 蓝桥杯电子赛道", "蓝桥杯电子赛道学习规划与备赛资料查找"),
    ("fengge-hardware-checklist", "峰哥 · 项目硬件清单", "查找 ESP32S3、汽车仪表盘与其他嵌入式项目的器件清单入口"),
)


def write(path, text):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text.rstrip() + "\n", encoding="utf-8")


def build_variants(header, entry, interface, files):
    archive = ROOT / "dist" / VARIANT_ARCHIVE
    with zipfile.ZipFile(archive, "w", zipfile.ZIP_DEFLATED) as z:
        for name, title, focus in VARIANTS:
            folder = SKILL.parent / name
            description = f"{focus}。峰哥嵌入式学习助手的同内容版本，共用学习路线、答疑流程与资料索引。"
            variant_header = header.replace(f"name: {NAME}\n", f"name: {name}\n", 1)
            variant_header = re.sub(
                r"^description: .*?$",
                lambda _: "description: " + json.dumps(description, ensure_ascii=False),
                variant_header,
                count=1,
                flags=re.MULTILINE,
            )
            variant_header = variant_header.replace("metadata:\n", f'metadata:\n  alias-of: "{NAME}"\n', 1)
            variant_entry = entry.replace("# 峰哥 · 嵌入式单片机答疑", f"# {title}", 1)
            variant_interface = interface.replace(
                'display_name: "峰哥 · 嵌入式单片机答疑"',
                "display_name: " + json.dumps(title, ensure_ascii=False),
                1,
            ).replace(f"${NAME}", f"${name}", 1)
            write(folder / "SKILL.md", variant_header + variant_entry)
            write(folder / "agents" / "openai.yaml", variant_interface)
            for source in files:
                relative = source.relative_to(SKILL)
                target = folder / relative
                if relative.as_posix() not in {"SKILL.md", "agents/openai.yaml"}:
                    target.parent.mkdir(parents=True, exist_ok=True)
                    copyfile(source, target)
                z.write(target, (Path(name) / relative).as_posix())


def build():
    original = SOURCE.read_text(encoding="utf-8-sig")
    body = original.split("---", 2)[2].strip()
    guide, resources = body.split("## 资源索引（内部资料库，按需引用，不要整表输出）", 1)
    resources = resources.split("## 维护说明", 1)[0].strip()
    # Keep the author's dialogue and course guidance, with portable tool handling.
    guide = guide.replace("# 嵌入式单片机峰哥 · CAN/LVGL/OTA专题", "# 峰哥嵌入式答疑详细指南", 1)
    old_fetch = '''需要清单明细、FAQ 具体解答时，用：
```bash
lark-cli docs +fetch --doc '<链接>' --doc-format markdown --as user
```
读取飞书文档正文后，**用自己的话整理成峰哥风格的回答**，不要原文粘贴。'''
    new_fetch = '''需要清单明细、FAQ 具体解答时，按主入口 SKILL.md 的“读取外部资料”处理。
仅在已获取正文后，才把内容整理成峰哥风格的回答；只有链接时，明确当前只有资料入口。'''
    if old_fetch not in guide:
        raise ValueError("Source fetch section changed; review the conversion before rebuilding")
    guide = guide.replace(old_fetch, new_fetch)
    write(SKILL / "references" / "mentor-guide.md", guide)
    write(SKILL / "references" / "resources.md", "# 峰哥嵌入式资料索引\n\n资料来自用户原文；链接存在不代表正文已读取或当前可访问。按问题选择资源。\n\n" + resources)

    header = '''---
name: wfeng-can-lvgl-ota
description: "嵌入式学习路线与单片机答疑助手（峰哥 / Fengge Embedded Learning）。用户问零基础如何学单片机、STM32怎么入门、ESP32/ESP32S3器件清单、C语言/51/RT-Thread问题、嵌入式Linux学习、蓝桥杯电子赛道、项目面试或焊接资料时使用；提供按基础分流的建议和准确课程资料入口。Embedded MCU learning roadmap, STM32/ESP32 Q&A and project resource navigation."
metadata:
  author: "峰哥"
  version: "__VERSION__"
  source-version: "1.6.0"
  category: "knowledge"
  source: "https://f1457x17jj4.feishu.cn/wiki/RaBvw48xLifVmokejs2cmvX9ndf"
  homepage: "https://fong315.github.io/fengge-embedded-skills/"
  repository: "https://github.com/Fong315/fengge-embedded-skills"
  language: "zh-CN"
---
'''.replace("__VERSION__", VERSION)
    entry = '''
# 峰哥 · 嵌入式单片机答疑

用中文、师兄带师弟的口吻，帮助用户解决嵌入式学习问题，并从峰哥的资源索引中选择合适资料。

适合单片机初学者、正在学 STM32/ESP32 的学生，以及需要课程资料、比赛或项目面试入口的学习者。

## 任务与交付

| 用户的请求 | 提供的帮助 |
| --- | --- |
| “零基础怎么学单片机”“STM32怎么入门” | 根据已有基础和目标给下一步任务，需要时附学习路线 |
| “ESP32S3项目要买什么”“仪表盘硬件清单” | 定位课程清单入口；获取正文后再整理具体型号与数量 |
| “C语言/51/STM32/RT-Thread问题” | 解释概念或给可执行的排查步骤，必要时索要型号和报错 |
| “蓝桥杯怎么准备”“项目面试资料在哪” | 根据原资料索引提供对应入口和使用建议 |

本技能有资料导航和一般技术答疑能力；CAN、LVGL、OTA 可以讨论，但包内没有独立专题全文。当前比赛规则、价格和芯片参数按可访问的官方来源核对。

## 加载与使用

1. 首次处理本技能的问题时，读取 [详细答疑指南](references/mentor-guide.md)，使用其中的聊天风格、背景分流和课程推荐逻辑。
2. 用户索要资料、清单、课程、视频或学习路线时，读取 [资源索引](references/resources.md)，按主题选取准确链接。检索词包括 C语言、51、STM32、ESP32S3、RT-Thread、仪表盘、ARM-Linux、蓝桥杯、面试、焊接。
3. 给链接时说明内容和适用原因，通常给 1–2 个。用户明确要全部资料时，可按其范围列全。

## 适用边界

以下规则用于协调原文中的对话偏好，遇到冲突时以此处为准：

- 泛泛咨询且背景未知时，简短回应后了解学习基础和目标；已知背景直接沿用，不重复问大几或专业。
- 用户明确要链接、完整方案、代码或要求不追问时，直接完成请求。“聊 2–3 轮再推路线”适用于主动推荐，不限制用户主动索取。
- 具体技术问题先解答；追问围绕缺少的型号、报错、接线或预期行为。篇幅由问题和用户要求决定。
- 使用“峰哥的嵌入式学习助手”这一身份。详细指南中的十年经历、学生故事是人设素材；只把有来源的经历归于峰哥，未提供事实的故事作为假设案例，不声称是 AI 自身亲历。
- 课程是峰哥提供的学习资源，按用户需要推荐。用户不需要时停止推荐。原文中的固定学习顺序作为课程路径参考，结合已有基础调整。

## 读取外部资料

资源索引包含链接，不包含这些网页的完整正文。读取全文需要当前宿主提供联网、文件上传或飞书访问能力。

1. 优先用当前客户端已有且有权限的文档连接器或网页读取工具。需要登录时沿用客户端的授权流程。
2. 只有在本机存在且已授权 `lark-cli`、并确认该版本支持相应参数时，才可使用原文的可选命令：

   ```bash
   lark-cli docs +fetch --doc '<资源索引中的链接>' --doc-format markdown --as user
   ```

3. 没有工具、权限不足或读取失败时，给准确链接，说明尚未读取正文，请用户粘贴内容或上传文件。不可声称已读取，也不可把一般知识猜测成课程的硬件清单。
4. 已读到正文后再提炼具体内容，并带上对应来源链接。价格、比赛规则、就业行情等变化信息，在支持联网时查当前官方来源；不能核实时明确日期或不确定性。

## 简短示例

用户：“直接给我 ESP32S3 的器件清单链接，不用问背景。”

答：“[ESP32S3 相关器件购买清单](https://f1457x17jj4.feishu.cn/wiki/TNU9wcFKui0KeUkMY2QcNjtongb)，这是峰哥整理的项目器件入口，可以按这里核对要买的硬件。”
'''
    write(SKILL / "SKILL.md", header + entry)
    interface = '''interface:
  display_name: "峰哥 · 嵌入式单片机答疑"
  short_description: "提供单片机学习路线、技术答疑、课程资料与项目硬件清单导航"
  default_prompt: "请使用 $wfeng-can-lvgl-ota，根据我的基础解答嵌入式问题，并推荐相关学习资料。"
policy:
  allow_implicit_invocation: true
'''
    write(SKILL / "agents" / "openai.yaml", interface)
    # Flatten local references for chat products that can read uploads but not skills.
    standalone_entry = entry.replace("[详细答疑指南](references/mentor-guide.md)", "下文的“详细答疑指南”").replace("[资源索引](references/resources.md)", "下文的“资源索引”")
    standalone_guide = guide.replace("主入口 SKILL.md 的“读取外部资料”", "本文前部的“读取外部资料”")
    write(ROOT / "dist" / "峰哥嵌入式答疑-通用导入版.md", "# 峰哥嵌入式答疑 · 通用导入版\n\n将本文件上传到支持文件的聊天客户端，或粘贴到自定义助手指令中，并要求本次会话按此答疑。文件不会自行注册成平台技能。下文适用边界优先于详细指南。\n" + standalone_entry + "\n\n## 详细答疑指南\n\n" + standalone_guide + "\n\n## 资源索引\n\n" + resources)
    files = sorted(p for p in SKILL.rglob("*") if p.is_file())
    build_variants(header, entry, interface, files)
    archive = ROOT / "dist" / (NAME + ".zip")
    with zipfile.ZipFile(archive, "w", zipfile.ZIP_DEFLATED) as z:
        for path in files:
            z.write(path, (Path(NAME) / path.relative_to(SKILL)).as_posix())
    # WorkBuddy's submission manifest adds fields beyond the portable spec.
    workbuddy_fields = '''display_name: "峰哥 · 嵌入式单片机答疑"
display_name_en: "Brother Feng Embedded MCU Mentor"
description_zh: "峰哥嵌入式单片机答疑：学习路线、C语言、STM32、ESP32、RTOS、Linux、硬件清单、蓝桥杯、面试与课程资料导航。"
description_en: "Embedded MCU learning guidance and resource navigation for C, 8051, STM32, ESP32, RTOS, Linux, hardware lists, competitions and interviews."
version: "__VERSION__"
author: "峰哥"
'''.replace("__VERSION__", VERSION)
    wb_header = header.replace("metadata:\n", workbuddy_fields + "metadata:\n", 1)
    wb_entry = entry.replace("读取 [详细答疑指南](references/mentor-guide.md)", "读取 @references/mentor-guide.md").replace("读取 [资源索引](references/resources.md)", "读取 @references/resources.md")
    wb_root = ROOT / "dist" / "workbuddy" / NAME
    for path in files:
        write(wb_root / path.relative_to(SKILL), path.read_text(encoding="utf-8"))
    write(wb_root / "SKILL.md", wb_header + wb_entry)
    with zipfile.ZipFile(ROOT / "dist" / (NAME + "-workbuddy.zip"), "w", zipfile.ZIP_DEFLATED) as z:
        for path in sorted(wb_root.rglob("*")):
            if path.is_file():
                z.write(path, path.relative_to(wb_root).as_posix())
    urls = lambda text: set(re.findall(r"https?://[^\s<>`）)\"']+", text))
    combined = "\n".join(p.read_text(encoding="utf-8") for p in files)
    missing = urls(original) - urls(combined)
    if missing:
        raise ValueError(f"Lost source links: {sorted(missing)}")
    manifest = {"name": NAME, "source_sha256": hashlib.sha256(SOURCE.read_bytes()).hexdigest(), "source_url_count": len(urls(original)), "files": {p.relative_to(SKILL).as_posix(): hashlib.sha256(p.read_bytes()).hexdigest() for p in files}}
    write(ROOT / "dist" / "manifest.json", json.dumps(manifest, ensure_ascii=False, indent=2))
    write(ROOT / "dist" / "fengge-embedded-chat-import.md", (ROOT / "dist" / "峰哥嵌入式答疑-通用导入版.md").read_text(encoding="utf-8"))
    print(json.dumps({"skill": str(SKILL), "archive": str(archive), "preserved_urls": len(urls(original))}, ensure_ascii=False))


if __name__ == "__main__":
    build()
