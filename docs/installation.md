---
title: 峰哥嵌入式 Skill 安装指南：Codex、DeepSeek Harness、WorkBuddy 和豆包
description: 如何安装峰哥嵌入式学习助手：Codex 一条命令全局安装，DeepSeek Harness 使用标准技能目录，WorkBuddy 和豆包导入 ZIP；普通聊天可上传完整中文 Markdown。
---

# 安装峰哥嵌入式学习助手

技能 ID：`wfeng-can-lvgl-ota`。展示名称：**峰哥 · 嵌入式单片机答疑**。

[了解技能用途](index.html) · [查看回答示例](examples.html) · [解决常见问题](faq.html)

## 先选适合你的版本

| 你在使用什么 | 安装入口 |
| --- | --- |
| Codex 或兼容标准 Agent Skills 的客户端 | [标准技能 ZIP](https://github.com/Fong315/fengge-embedded-skills/releases/latest/download/wfeng-can-lvgl-ota.zip)，也可使用下方 CLI |
| WorkBuddy | [WorkBuddy 专用 ZIP](https://github.com/Fong315/fengge-embedded-skills/releases/latest/download/wfeng-can-lvgl-ota-workbuddy.zip) |
| 豆包工作 / 支持技能的桌面版 | [标准技能 ZIP](https://github.com/Fong315/fengge-embedded-skills/releases/latest/download/wfeng-can-lvgl-ota.zip) |
| 普通 DeepSeek、豆包等聊天界面 | [中文通用导入版 Markdown](https://github.com/Fong315/fengge-embedded-skills/releases/latest/download/fengge-embedded-chat-import.md) |

## Codex：一条命令安装

需要 Node.js 22.20 或更高版本。安装到用户技能目录，在所有项目中使用：

```bash
npx skills add Fong315/fengge-embedded-skills --skill wfeng-can-lvgl-ota -a codex -g
```

希望只在当前项目使用时，去掉 `-g`。安装后新建聊天；必要时重启客户端刷新列表。

首次调用：

```text
$wfeng-can-lvgl-ota 我已经学过 C 语言和 51，想入门 STM32。请给我下一步任务和相关资料。
```

也可以解压标准包，将整个 `wfeng-can-lvgl-ota` 文件夹放进用户 `~/.agents/skills/` 或项目 `.agents/skills/`。保留 `SKILL.md`、`references` 和 `agents`，避免只复制入口文件。

## DeepSeek Harness：使用标准技能目录

DeepSeek Harness 官方支持项目 `.agents/skills/`、`.dsh/skills/`，以及用户技能目录。下载标准 ZIP 后，将完整文件夹放入当前配置生效的目录，再开启新会话或刷新技能列表。

“DeepSeek Harness”是具备工具与技能能力的宿主。直接使用 DeepSeek 模型的其他软件，需要遵循该软件自己的技能配置。普通网页聊天可使用下方的 Markdown 导入方式。

## WorkBuddy：上传专用 ZIP

1. 下载 WorkBuddy 专用 ZIP。
2. 在“专家·技能·连接器 → 技能 → 添加技能 → 上传技能”选择安装包，入口以当前客户端为准。
3. 完成检查后选择“峰哥 · 嵌入式单片机答疑”，发送一条学习问题。

专用包带有 WorkBuddy 的中英文展示字段。无需先安装 Python 或运行仓库构建脚本。

## 豆包工作 / 桌面版：导入完整技能

1. 下载标准 ZIP。
2. 在客户端技能管理的上传入口选择 ZIP，或解压后导入完整技能文件夹。
3. 按客户端提示完成检查并启用，再选择技能提问。

不同版本和账户可能提供不同入口。若没有技能导入功能，可使用普通聊天导入版。公开包的导入不代表该技能已经出现在豆包官方市场。

## 普通聊天：上传中文完整文档

下载文件 `fengge-embedded-chat-import.md`，内容为中文。将它上传到支持读取文档的聊天界面，再输入：

```text
请阅读上传的“峰哥嵌入式答疑”文档，按其中的适用边界和资料索引回答。我已经会 C 语言基础，想知道怎样入门 STM32。
```

该文件为本次会话提供上下文。跨会话是否保留由客户端决定。

## 安装后找不到或没有自动使用？

- 在技能列表搜索“峰哥”或 `wfeng-can-lvgl-ota`，确认已启用。
- 新建聊天，显式选择技能；Codex 也可输入 `$wfeng-can-lvgl-ota`。
- 手动安装时，检查目录内是否直接有大写 `SKILL.md`，引用文件是否完整。
- 使用普通聊天时，确认附件已被读取；这种方式没有原生技能列表。

自动选用取决于当前可用技能和请求匹配情况。[常见问题](faq.html)解释了网页发现、技能安装和自动调用的区别。

## 获取更新和反馈

在 [Releases](https://github.com/Fong315/fengge-embedded-skills/releases/latest) 下载最新版本，或通过所用安装器的更新功能更新技能。反馈时请提供客户端名称、版本和实际操作步骤：[提交问题](https://github.com/Fong315/fengge-embedded-skills/issues)。
