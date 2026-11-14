---
title: 单片机学习与嵌入式学习｜STM32、ESP32 入门路线 · 峰哥 AI Skill
description: 峰哥的中文 Agent Skill 提供零基础单片机入门、嵌入式学习路线、STM32 和 ESP32 答疑。可按手上的开发板规划点灯、按键、串口等练习，查找项目资料，并在 Codex、WorkBuddy 等客户端安装使用。
---

# 单片机学习与嵌入式学习

峰哥嵌入式学习助手是一个可安装的中文 **Agent Skill**。零基础可以用它规划单片机入门练习。已经在学 STM32 或 ESP32，可以带着芯片型号、接线和报错提问，或查找对应的学习路线、视频和项目资料。

**Fengge Embedded Learning Skill** helps Chinese-speaking learners plan an embedded MCU learning roadmap and find STM32, ESP32, RTOS and project resources.

[查看安装方法](installation.html) · [选择技能版本](variants.html) · [入门问答](faq.html) · [GitHub 源码](https://github.com/Fong315/fengge-embedded-skills)

## 这是什么技能？

这是一个以 Markdown 指令和参考资料组成的学习辅助技能，技能 ID 为 `wfeng-can-lvgl-ota`，客户端展示名称为“峰哥 · 嵌入式单片机答疑”。它采用师兄带师弟的中文交流方式，覆盖学习规划、一般技术答疑和资料导航。

技能包包含 **29 个不同的原始资料链接**，涵盖 C 语言、51 单片机、STM32、ESP32/ESP32S3、RT-Thread、ARM-Linux、焊接、蓝桥杯电子赛道、汽车仪表盘和项目面试资料。

## 适合谁使用？

- 刚接触 C 语言或单片机，希望知道先学什么、怎样练习的学生。
- 正在学习 STM32、ESP32，希望获得解释、排查思路和对应资料的学习者。
- 已有单片机基础，准备 RTOS 项目、蓝桥杯或嵌入式面试的人。
- 希望在 Codex、DeepSeek Harness、WorkBuddy 或支持技能的豆包客户端里使用中文嵌入式学习指导的人。

## 零基础单片机入门 {#mcu-basics}

手上已有开发板，可以从点亮一颗 LED 开始。第一步是看懂板上 LED 对应的引脚，烧录一个程序，让 LED 按预期亮灭。再加一个按键，观察输入如何改变输出。把板子型号和 C 语言基础告诉 Skill，它会帮你安排下一步，并找到相应的 51 单片机或其他入门资料。

可以问：“我只学过一点 C 语言，手上有一块 51 单片机开发板。第一次点灯从哪里开始，怎么确认程序烧进去了？”

## 嵌入式学习路线 {#embedded-roadmap}

想系统学习时，可以把已经会的内容和想做的项目列出来。刚学 C 语言，可以先练数字输入输出和串口。已经会用单片机完成小项目，可以根据项目需求，决定是继续练外设、学习 RT-Thread 等实时操作系统，还是开始接触嵌入式 Linux。

可以问：“我会用 STM32 做按键和串口实验，下一步做什么项目能练到定时器和中断？”

## STM32 入门与学习路线 {#stm32}

可以先用 GPIO 点亮 LED、读取按键，再用串口打印状态，随后用定时器或中断完成一个小练习。遇到外设不工作时，提供开发板型号、接线、关键代码和异常现象，Skill 可以帮你按步骤缩小排查范围，并给出 STM32 常见问题资料入口。

[看 STM32 第一周练习示例](examples.html#stm32-first-week) · [查看 STM32 学习路线版的安装 ID](variants.html)

## ESP32 入门与学习路线 {#esp32}

初次上手可以先运行简单程序并在串口监视器里看到输出，再尝试 Wi-Fi 扫描或联网。准备做 ESP32-S3 项目时，可以询问对应的常见问题、项目资料和原始器件清单入口。有清单正文时，再逐项核对型号与数量。

可以问：“我用的是 ESP32-S3，已经能烧录程序，但串口没有输出。请告诉我先检查什么。”

[看 ESP32-S3 器件清单回答示例](examples.html#hardware-list) · [查看 ESP32 学习版的安装 ID](variants.html)

## 项目、竞赛与面试资料

| 你可能正在问 | 可以得到什么 |
| --- | --- |
| 汽车仪表盘项目需要哪些硬件？ | 对应课程器件清单入口，读到正文后再核对型号和数量 |
| 蓝桥杯电子赛道怎么准备？项目面试有哪些资料？ | 原资料索引里的备赛和项目面试入口 |

## 支持哪些 AI 客户端？

| 客户端 | 使用方式 |
| --- | --- |
| Codex | 通过 Skills CLI 安装标准包，或放入 `.agents/skills`；安装后可按任务匹配或用技能名称调用 |
| DeepSeek Harness | 标准技能目录安装；使用当前 Harness 支持的技能加载配置 |
| WorkBuddy | 下载 WorkBuddy 专用 ZIP，在客户端上传并启用 |
| 豆包工作 / 支持技能的桌面版 | 在技能管理中导入标准 ZIP 或技能文件夹，按客户端提示启用 |
| DeepSeek、豆包等普通聊天 | 上传完整 Markdown 导入版，作为本次会话的学习参考 |

客户端版本、账户权限和工具能力会影响使用方式。普通聊天上传文档只为当前会话提供上下文。详细步骤见[安装指南](installation.html)。

## 怎样安装？

已使用 Codex 的用户，可以运行：

```bash
npx skills add Fong315/fengge-embedded-skills --skill wfeng-can-lvgl-ota -a codex -g
```

Skills CLI 需要 Node.js 22.20 或更高版本。也可以直接[下载标准技能 ZIP](https://github.com/Fong315/fengge-embedded-skills/releases/latest/download/wfeng-can-lvgl-ota.zip)、[WorkBuddy 专用 ZIP](https://github.com/Fong315/fengge-embedded-skills/releases/latest/download/wfeng-can-lvgl-ota-workbuddy.zip) 或[中文通用导入版](https://github.com/Fong315/fengge-embedded-skills/releases/latest/download/fengge-embedded-chat-import.md)。

## 第一次可以怎么问？

```text
$wfeng-can-lvgl-ota 我是大二学生，会 C 语言基础，想入门 STM32。请结合我的基础给下一步练习任务和相关资料。
```

不确定效果时，先看[使用示例](examples.html)：它们说明输入、回答形式和资料读取边界，便于你判断是否适合自己。

## 能力范围与资料来源

包内保存答疑规则和资料索引，**没有同步全部飞书正文，也不会自动控制开发板**。获取外链正文需要客户端已有的读取能力与权限。无法读取时会给出对应入口，并说明没有确认具体内容。一般技术解释需要结合你的芯片、代码和实验结果验证。

课程和资料来自峰哥原始文档，外链内容归各自原作者。GitHub 仓库和安装包公开可访问，官方技能市场的上架与审核由各平台独立处理。

## 官方格式和客户端依据

- [Agent Skills 格式规范](https://agentskills.io/specification)
- [OpenAI / Codex 技能加载与调用说明](https://learn.chatgpt.com/docs/build-skills)
- [DeepSeek Harness 技能发现机制](https://github.com/deepseek-ai/deepseek-harness/blob/master/docs/subsystems/skills.md)
- [WorkBuddy 技能规范](https://open.workbuddy.cn/docs/skill)
- [豆包独立技能接入指南](https://open.doubao.com/document/doubao-developer-guide/skill-integration-guide)

遇到安装或回答问题，可到 [GitHub Issues](https://github.com/Fong315/fengge-embedded-skills/issues) 提交客户端版本、操作步骤和可公开的报错信息。
