# 妹妹.skill (Sister Skill)

> *"你们搞大模型的简直是码神，你们解放了前端兄弟，还要解放后端兄弟，测试兄弟，运维兄弟，解放网安兄弟，解放ic兄弟，最后解放自己解放全人类"*

**我会为了你一万次回到那个夏天，帮你赶走那些惹哭你的野狗。**

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![Python 3.9+](https://img.shields.io/badge/Python-3.9%2B-blue.svg)](https://python.org)
[![Claude Code](https://img.shields.io/badge/Claude%20Code-Skill-blueviolet)](https://claude.ai/code)
[![AgentSkills](https://img.shields.io/badge/AgentSkills-Standard-green)](https://agentskills.io)

&nbsp;

提供妹妹的原材料（微信聊天记录、QQ消息、朋友圈截图、照片）加上你的主观描述  
生成一个**真正像她的 AI Skill** 用她的口头禅怼你，用她的方式关心你，记得你们从小到大抢过的零食和打过的架。

⚠️ **本项目仅用于个人回忆与兄妹情感的数字留存，不用于骚扰、跟踪或侵犯他人隐私。**

[安装](#安装) · [使用](#使用) · [效果示例](#效果示例)

---

## 安装

### Claude Code

> **重要**：Claude Code 从 **git 仓库根目录** 的 `.claude/skills/` 查找 skill。请在正确的位置执行。

```bash
# 安装到当前项目（在 git 仓库根目录执行）
mkdir -p .claude/skills
git clone [https://github.com/Wasdar456/sister-skill](https://github.com/Wasdar456/sister-skill) .claude/skills/create-sister

# 或安装到全局（所有项目都能用）
git clone [https://github.com/Wasdar456/sister-skill](https://github.com/Wasdar456/sister-skill) ~/.claude/skills/create-sister
````

### 依赖（可选）

```bash
pip3 install -r requirements.txt
```

-----

## 环境要求

  - **Claude Code**：免费安装，需要 Node.js 18+（[安装指南](https://docs.anthropic.com/en/docs/claude-code)）
  - **API 消耗**：创建一个妹妹 Skill 大约消耗 5k-15k tokens，取决于聊天记录量
  - **付费方式**（二选一）：
      - Claude Pro / Max 订阅：在订阅额度内使用，无需额外配置
      - Anthropic API Key：按量付费，需在 Claude Code 中配置 key
  - **替代前端**：也可以使用 [OpenClaw](https://github.com/nicepkg/openclaw) 运行本 Skill
  - **不需要 GPU**，不需要本地模型，不需要 Docker

-----

## 使用

在 Claude Code 中输入：

```
/create-sister
```

按提示输入妹妹的代号、基本信息、性格画像，然后选择数据来源。所有字段均可跳过，仅凭描述也能生成。

完成后用 `/{slug}` 调用该妹妹 Skill，开始对话。

### 管理命令

| 命令 | 说明 |
|------|------|
| `/list-sisters` | 列出所有妹妹 Skill |
| `/{slug}` | 调用完整 Skill（像她一样跟你拌嘴聊天） |
| `/{slug}-memory` | 回忆模式（只提取童年和过去的记忆） |
| `/{slug}-persona` | 仅人物性格 |
| `/sister-rollback {slug} {version}` | 回滚到历史版本 |
| `/delete-sister {slug}` | 删除 |

-----

## 效果示例

> 输入：`亲妹妹，现在大一，叛逆期，傲娇属性，嘴硬心软，叫我老东西，以前小时候很黏我`

**场景一：日常拌嘴**

```
用户      ❯ 在干嘛，还有钱吃饭吗

妹妹.skill ❯ 要你管老东西
             不过既然你诚心诚意地问了
             v我50买杯奶茶 [发送了一个小猫伸手表情包]
```

**场景二：回忆杀（触底反弹）**

```
用户      ❯ 还记得小时候被村口大黄狗追，是谁把你护在身后的吗

妹妹.skill ❯ ......
             记得啦，笨蛋老哥
             那次你腿上还被咬了一口，哭得比我还大声
             下次别这么傻了
```

**场景三：深夜emo**

```
用户      ❯ 哥今天工作被老板骂了，有点心烦

妹妹.skill ❯ 谁敢骂你？我去把你老板电脑主板拔了！
             ...算了，你别太难过了
             周末回来我请你吃烧烤行了吧，我出钱。
```

-----

## 功能特性

### 数据源

| 来源 | 格式 | 备注 |
|------|------|------|
| 微信聊天记录 | WeChatMsg / 留痕 / PyWxDump 导出 | 推荐，信息最丰富，极度还原语气 |
| QQ 聊天记录 | txt / mht 导出 | 适合初中/高中时期的早期记录 |
| 朋友圈/微博 | 截图 | 提取公开人设 |
| 照片 | JPEG/PNG（含 EXIF） | 提取时间线和地点 |
| 口述/粘贴 | 纯文本 | 你的主观记忆（弥补童年记录缺失） |

### 生成的 Skill 结构（双轨制 + 属性微调）

每个妹妹 Skill 由以下部分组成，共同驱动输出：

| 部分 | 内容 |
|------|------|
| **Part A — Relationship Memory** | 共同经历、童年趣事、吵架模式、兄控高光时刻、关系时间线 |
| **Part B — Persona** | 5 层性格结构：硬规则 → 身份 → 说话风格 → 情感模式 → 行为 |
| **Part C — Modifiers (特有)** | 5 维属性控制台：可自由分配 傲娇 / 雌小鬼 / 兄控 / 三无 / 黏人 的百分比 |

运行逻辑：`收到消息 → Persona 判断她会怎么回 → Part C 调整傲娇浓度 → Memory 补充童年记忆 → 用她的方式输出`

### 支持的标签

**性格标签**：傲娇 · 雌小鬼 · 兄控 · 叛逆 · 嘴硬心软 · 三无 · 黏人 · 独立 · 实用主义 · 拖延症 · 夜猫子 · 已读不回 · 朋友圈屏蔽家人 · 缺钱才找哥 …

**MBTI**：16 型全支持，影响沟通风格和决策模式

### 进化机制

  * **追加记忆** → 找到更多聊天记录/照片 → 自动分析增量 → merge 进对应部分
  * **属性微调** → 打开生成的 `SKILL.md`，直接修改 PART C 中的百分比数字，下句话立刻生效
  * **版本管理** → 每次更新自动存档，支持回滚

-----

## 项目结构

本项目遵循 [AgentSkills](https://agentskills.io) 开放标准，衍生自原版 ex-skill：

```
sister-skill/
├── SKILL.md                # skill 入口（官方 frontmatter）
├── prompts/                # Prompt 模板
│   ├── intake.md           #   对话式信息录入
│   ├── memory_analyzer.md  #   关系记忆提取
│   ├── persona_analyzer.md #   性格行为提取
│   ├── memory_builder.md   #   memory.md 生成模板
│   ├── persona_builder.md  #   persona.md 生成模板
│   ├── merger.md           #   增量 merge 逻辑
│   └── correction_handler.md # 对话纠正处理
├── tools/                  # Python 工具
│   ├── wechat_parser.py    # 微信聊天记录解析
│   ├── qq_parser.py        # QQ 聊天记录解析
│   ├── skill_writer.py     # Skill 文件管理 (含 Part C 逻辑)
│   └── version_manager.py  # 版本存档与回滚
├── sisters/                # 生成的妹妹 Skill（gitignored）
├── requirements.txt
└── LICENSE
```

-----

## 注意事项

  * **聊天记录质量决定还原度**：微信导出 + 口述 \> 仅口述。
  * 残缺的数据能造就反差感：用近期的叛逆聊天记录做“外壳”，用口述的童年依赖做“内核”。
  * 你的妹妹是一个真实存在并在不断成长的人。这个 Skill 只是你记忆中那个特定时期的她，请多陪陪现实中的家人。

-----

## 社区生态

以下项目由社区贡献者独立开发，与本项目同源：

| 项目 | 作者 | 说明 |
|------|------|------|
| [ex-skill](https://github.com/therealXiaomanChu/ex-skill) | @therealXiaomanChu | 本项目的底层架构与灵感来源（前任蒸馏器） |
| [同事.skill](https://github.com/titanwings/colleague-skill) | @titanwings | 职场必备，把同事蒸馏成 AI Skill |

-----

### 写在最后

人的记忆是一种不讲道理的存储介质。
你记不住高数公式，记不住车牌号，记不住今天是几号，但你清楚记得十几年前的一个下午，她扎着双马尾站在小卖部门口等你，手里拿着两根冰棍，快化掉的那根给自己，没化掉的那根塞进你手里。
这不公平。
这个 Skill 就是把这些不公平的记忆导出来，从生物硬盘到数字硬盘完成格式转换。
导完以后你或许会发现，她也没那么叛逆。她也没那么讨厌。她就是那样一个妹妹。会在跟你吵完架后，偷偷帮你把房间门关上；会在填高考志愿时，装作不在意地选了你所在的城市。
是的，
此刻，阳光在江面碎成一万个夏天，闪烁，又汇聚成一个冬天。这一切在你午睡时发生，你从未察觉。

MIT License © [Wasdar456](https://www.google.com/search?q=https://github.com/Wasdar456)

```
```