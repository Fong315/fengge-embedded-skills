# 峰哥嵌入式学习助手 Skill · STM32 / ESP32 学习路线与单片机答疑

**零基础怎样学单片机？STM32 怎么入门？ESP32S3 项目资料和硬件清单在哪里？**

峰哥嵌入式学习助手是公开可安装的中文 **Agent Skill**。它根据你的 C 语言、单片机和项目基础，提供下一步学习建议、一般技术解释，并从峰哥整理的资料中定位对应课程、视频和硬件清单。

**Chinese embedded-systems learning skill for Codex and compatible agents. Covers C, 8051, STM32, ESP32, RTOS, Linux, project hardware, competitions, and interviews.**

- 技能名称：**峰哥 · 嵌入式单片机答疑**
- 技能 ID：`wfeng-can-lvgl-ota`
- 当前版本：`1.6.2`
- 分发格式：标准 Agent Skill、WorkBuddy 专用包、普通聊天通用导入版

[公开介绍页](https://fong315.github.io/fengge-embedded-skills/) · [逐平台安装指南](https://fong315.github.io/fengge-embedded-skills/installation.html) · [输入与回答示例](https://fong315.github.io/fengge-embedded-skills/examples.html) · [常见问题](https://fong315.github.io/fengge-embedded-skills/faq.html) · [下载安装包](https://github.com/Fong315/fengge-embedded-skills/releases/latest)

## 适合谁？可以得到什么？

| 你的情况 | 可以用它做什么 |
| --- | --- |
| 刚学 C 语言或 51，不清楚学习顺序 | 确认下一步基础练习，获取单片机入门路线与视频入口 |
| 正在学 STM32、ESP32，遇到外设或代码问题 | 获得一般解释与排查步骤，结合具体型号、接线和报错继续定位 |
| 想做 ESP32S3、仪表盘或 RT-Thread 项目 | 找到对应项目 FAQ、器件清单和学习资料 |
| 准备蓝桥杯或嵌入式项目面试 | 定位原资料索引里的备赛与项目面试入口 |

技能采用中文师兄式交流。用户已经说明背景时会沿用；明确索要链接或要求直接回答时优先完成请求。CAN、LVGL、OTA 可作为一般技术话题讨论，当前包内没有独立专题全文。

## 先看一个例子

输入：“直接给我嵌入式单片机学习路线链接，不用问背景。”

> [嵌入式单片机学习路线](https://my.feishu.cn/docx/Vs5IdvCn6oOY5jxmoixcVXU1nQh?from=from_parent_docx)：峰哥资料索引中的学习路径和方法入口，覆盖 C 语言、51、STM32、ESP32、RTOS 与 Linux。

这是说明回答形式的编辑示例，实际措辞由客户端模型和上下文决定。[更多示例](docs/examples.md)还展示了 STM32 第一周练习建议，以及没有飞书正文时如何处理完整器件清单请求。

## 一条命令安装

使用 [Skills CLI](https://github.com/vercel-labs/skills)，需要 **Node.js 22.20 或更高版本**。

```bash
npx skills add Fong315/fengge-embedded-skills --skill wfeng-can-lvgl-ota
```

按提示选择要安装到的客户端。默认安装到当前项目；要在 **Codex 的所有项目中使用**：

```bash
npx skills add Fong315/fengge-embedded-skills --skill wfeng-can-lvgl-ota -a codex -g
```

安装后新建聊天；若客户端尚未刷新技能列表，再重启客户端。

## 不用命令行：下载安装包

| 安装包 | 适用场景 |
| --- | --- |
| [标准技能 ZIP](https://github.com/Fong315/fengge-embedded-skills/releases/latest/download/wfeng-can-lvgl-ota.zip) | 支持标准 Agent Skills 的客户端，以及豆包技能导入 |
| [WorkBuddy 专用 ZIP](https://github.com/Fong315/fengge-embedded-skills/releases/latest/download/wfeng-can-lvgl-ota-workbuddy.zip) | WorkBuddy 的“上传技能”入口，已包含中英文展示字段 |
| [通用导入版 Markdown](https://github.com/Fong315/fengge-embedded-skills/releases/latest/download/fengge-embedded-chat-import.md) | 中文完整文档，上传到普通聊天或放入自定义助手指令；下载文件名为 `fengge-embedded-chat-import.md` |

标准 ZIP 内含完整的 `wfeng-can-lvgl-ota` 文件夹。需要手动安装时，请复制整个文件夹，保留 `references` 目录。

## 各平台怎么用

| 平台 | 使用方式 |
| --- | --- |
| **GPT / Codex** | 使用上面的 CLI 命令，或将完整技能文件夹放入用户 `~/.agents/skills/`。Codex 中可用 `$wfeng-can-lvgl-ota` 显式调用，也可根据问题匹配技能描述。 |
| **DeepSeek Harness** | 支持用户 `~/.agents/skills/` 和项目 `.agents/skills/`，可以使用同一份标准包。具体安装路径以所用 Harness 配置为准。 |
| **WorkBuddy** | 在“专家·技能·连接器 → 技能 → 添加技能 → 上传技能”中选择 WorkBuddy 专用 ZIP，完成后选择本技能。 |
| **豆包工作 / 支持技能的桌面版** | 在技能管理入口上传标准 ZIP 或完整技能文件夹，等待客户端检查完成后选择使用。入口名称和可用能力取决于客户端版本及账户。 |
| **DeepSeek、豆包等普通聊天界面** | 上传通用导入版 Markdown，并要求按其中规则答疑。这是本次会话的参考上下文，不会自动注册为跨会话技能。 |

**GitHub 公开分发不等于各平台官方技能市场上架。** 本仓库提供可安装的文件和命令；是否在客户端自动发现、是否显示在平台市场，取决于各平台的支持和收录流程。

## 安装后这样提问

在 Codex 中：

```text
$wfeng-can-lvgl-ota 我是大二学生，会一点 C 语言，想学 STM32，帮我规划下一步。
```

也可以直接选择技能后提问：

- “直接给我 ESP32S3 项目的器件清单链接，不用问背景。”
- “STM32 的中断和轮询有什么区别？给我一个容易理解的例子。”
- “我已经会 STM32，下一步应该学 RT-Thread 还是做项目？”
- “蓝桥杯电子赛道应该怎么准备，有什么对应资料？”
- “汽车仪表盘项目面试时可能会被问什么？”

使用普通聊天导入版时，可在上传后发送：

```text
请把上传文件作为本次对话的“峰哥嵌入式答疑”指南，先阅读适用边界，再根据我的问题使用其中的资料索引。
```

## 能帮你做什么

- **学习路线**：结合基础和目标，梳理 C 语言、51、STM32、ESP32、RTOS 与嵌入式 Linux 的学习顺序。
- **技术答疑**：C 语言、单片机基础、STM32、ESP32/ESP32S3、RT-Thread，以及 CAN、LVGL、OTA 等主题。
- **资料导航**：从峰哥的资源索引中查找课程、FAQ、B站视频、焊接入门和项目硬件清单。
- **项目与就业准备**：汽车仪表盘、人脸识别等项目资料，以及蓝桥杯和嵌入式面试准备。

技能采用中文师兄式交流，用户明确索要链接或要求直接回答时会优先完成请求。课程推荐会标明其为峰哥提供的学习资源。

技能保存的是 **29 个不同的资料链接及答疑规则**，没有打包外链网页的全部正文。读取飞书内容需要客户端已有的访问工具与权限；没有正文时，助手应说明限制，不猜测课程的采购型号和数量。链接可访问性、课程内容和客户端支持可能随时间变化。

## 如何搜索到这个技能

在 GitHub 搜索仓库名 `fengge-embedded-skills`，或组合以下关键词：

```text
峰哥 嵌入式 skill
wfeng-can-lvgl-ota
STM32 ESP32 embedded agent skills
```

也可以在支持 Skills CLI 的终端尝试：

```bash
npx skills find wfeng-can-lvgl-ota
```

`skills find` 使用技能目录的索引，收录和搜索更新可能有延迟。搜不到时，直接使用本页的 `npx skills add Fong315/fengge-embedded-skills --skill wfeng-can-lvgl-ota`，或下载 Release 安装包；按仓库地址安装不依赖搜索结果。

## 常见疑问

**能在豆包或 DeepSeek 普通聊天里用吗？** 可以上传中文通用导入版，作为当前会话的学习参考。原生技能安装需要客户端支持技能加载。

**是不是能直接读取全部飞书资料？** 包内是资料索引。具体正文需要客户端已有的读取工具和访问权限；无法读取时应说明情况，不把猜测写成课程清单。

**需要专属 API Key 或先买课程吗？** 下载本仓库和技能包不需要专属 API Key 或课程购买凭证。模型账户、订阅、外链课程访问要求由相应服务决定。

**AI 联网看到介绍页，就会自动运行技能吗？** 介绍页帮助了解用途和找到安装入口。运行仍需要客户端加载；自动选用也取决于当前可用技能和请求匹配。

[阅读完整 FAQ](https://fong315.github.io/fengge-embedded-skills/faq.html)

## 仓库结构

```text
skills/wfeng-can-lvgl-ota/
├── SKILL.md                    # 技能入口、触发描述与适用边界
├── agents/openai.yaml          # Codex 中文展示名称与调用配置
└── references/
    ├── mentor-guide.md         # 详细答疑风格、分流和课程引导
    └── resources.md            # 资料链接索引
scripts/
├── build_skill.py              # 从原始文档生成标准包及平台适配包
├── validate_skill.py           # 校验格式、引用与打包结果
├── install_local.py            # 本地安装辅助工具
└── verify_codex.py             # 查询本机 Codex 技能目录
docs/                          # 公开介绍、安装、示例与 FAQ 的 Markdown 和静态 HTML
峰哥答疑单片机嵌入式-SKILL.md    # 原始资料
```

## 维护与构建

安装技能不需要 Python。只有维护源文档、重新生成发布包时才需要 Python 和开发依赖：

```bash
python -m pip install -r requirements-dev.txt
python scripts/build_skill.py
python scripts/validate_skill.py
python scripts/build_docs.py
python scripts/validate_docs.py
```

构建产物在 `dist/`。修改原始 Markdown 后重新构建；技能入口模板和平台适配逻辑位于 `scripts/build_skill.py`。`skills/` 内的内容是生成文件，直接修改后再次构建会被覆盖。

本地安装辅助脚本会向用户技能目录复制文件；目标已有不同内容时先在本工程中备份。也可以完全使用 CLI 或 ZIP 导入，不运行仓库脚本。

公开说明页由 `docs/*.md` 生成到同名 HTML，再由 GitHub Pages 从 `main` 分支的 `/docs` 发布。正文直接包含在 HTML 中，提供独立标题、摘要、规范地址和站点地图。`llms.txt` 只是辅助阅读索引；这些文件不保证任何搜索引擎收录、推荐或自动调用。

## 来源与归属

本技能基于峰哥提供的《峰哥答疑单片机嵌入式-SKILL.md》整理，保留原文的教学资料链接与品牌风格。外链课程、视频和其他学习材料的内容与权利归各自原作者；公开技能包不代表外链内容获得重新分发授权。“峰哥”经历只应引用有来源的资料，不应让 AI 编造自身经历。

官方格式与客户端说明：

- [Agent Skills 标准](https://agentskills.io/specification)
- [OpenAI / Codex 技能文档](https://learn.chatgpt.com/docs/build-skills)
- [DeepSeek Harness 技能文档](https://github.com/deepseek-ai/deepseek-harness/blob/master/docs/subsystems/skills.md)
- [WorkBuddy 技能规范](https://open.workbuddy.cn/docs/skill)
- [豆包独立技能接入指南](https://open.doubao.com/document/doubao-developer-guide/skill-integration-guide)
- [Skills CLI 安装与搜索](https://github.com/vercel-labs/skills)
