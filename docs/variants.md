---
title: 峰哥嵌入式学习助手的十个技能版本与安装入口
description: 按 STM32、ESP32、单片机零基础、C51、RT-Thread、嵌入式 Linux、项目面试、蓝桥杯与器件清单查找峰哥技能版本。每份提供独立安装 ID，共用答疑流程与资料。
---

# 选择一个峰哥技能版本

十个版本提供不同的展示名称和安装 ID，共用峰哥嵌入式学习助手的答疑流程和资料。选一个符合你习惯的名称即可。

| 展示名称 | 安装 ID | 描述重点 |
| --- | --- | --- |
| [峰哥 · 嵌入式学习助手](https://github.com/Fong315/fengge-embedded-skills/tree/main/skills/fengge-embedded-learning) | `fengge-embedded-learning` | 嵌入式学习规划、单片机答疑和项目资料导航 |
| [峰哥 · 单片机零基础入门](https://github.com/Fong315/fengge-embedded-skills/tree/main/skills/fengge-mcu-beginner) | `fengge-mcu-beginner` | 零基础单片机入门、学习顺序与第一步练习建议 |
| [峰哥 · STM32 学习路线](https://github.com/Fong315/fengge-embedded-skills/tree/main/skills/fengge-stm32-roadmap) | `fengge-stm32-roadmap` | STM32 入门路线、练习安排与常见问题答疑 |
| [峰哥 · ESP32 学习与资料](https://github.com/Fong315/fengge-embedded-skills/tree/main/skills/fengge-esp32-learning) | `fengge-esp32-learning` | ESP32 和 ESP32S3 学习答疑、项目资料与器件清单查找 |
| [峰哥 · C 语言与 51 单片机](https://github.com/Fong315/fengge-embedded-skills/tree/main/skills/fengge-c51-learning) | `fengge-c51-learning` | 嵌入式 C 语言基础、51 单片机入门与学习资料查找 |
| [峰哥 · RT-Thread 学习指南](https://github.com/Fong315/fengge-embedded-skills/tree/main/skills/fengge-rtthread-learning) | `fengge-rtthread-learning` | RT-Thread 入门、实时操作系统基础答疑与项目资料查找 |
| [峰哥 · 嵌入式 Linux 入门](https://github.com/Fong315/fengge-embedded-skills/tree/main/skills/fengge-embedded-linux) | `fengge-embedded-linux` | 嵌入式 Linux 和 ARM-Linux 入门学习与资料查找 |
| [峰哥 · 嵌入式项目面试](https://github.com/Fong315/fengge-embedded-skills/tree/main/skills/fengge-embedded-interview) | `fengge-embedded-interview` | 嵌入式项目面试准备、常见问题和资料查找 |
| [峰哥 · 蓝桥杯电子赛道](https://github.com/Fong315/fengge-embedded-skills/tree/main/skills/fengge-lanqiao-electronics) | `fengge-lanqiao-electronics` | 蓝桥杯电子赛道学习规划与备赛资料查找 |
| [峰哥 · 项目硬件清单](https://github.com/Fong315/fengge-embedded-skills/tree/main/skills/fengge-hardware-checklist) | `fengge-hardware-checklist` | 查找 ESP32S3、汽车仪表盘与其他嵌入式项目的器件清单入口 |

## 安装任意一个版本

例如，选择“峰哥 · STM32 学习路线”时运行下面的命令。

```bash
npx skills add Fong315/fengge-embedded-skills --skill fengge-stm32-roadmap -a codex -g
```

选择其他版本时，将 `--skill` 后面的值换成表中的 ID。安装后可在 Codex 中输入 `$` 加对应的 ID，选择该技能。

[下载十个标准技能文件夹](https://github.com/Fong315/fengge-embedded-skills/releases/latest/download/fengge-skill-variants.zip)，解压后将选中的完整文件夹导入支持标准 Agent Skills 的客户端。原版及其他平台格式见[安装指南](installation.html)。
