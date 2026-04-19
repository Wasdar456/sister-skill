# 妹妹.skill — 产品需求文档（PRD）

## 产品定位

妹妹.skill 是一个运行在 Claude Code 上的 meta-skill。
用户通过对话式交互提供原材料（聊天记录 + 照片 + 手动描述），系统自动生成一个可独立运行的妹妹 Persona Skill。

## 核心概念

### 双轨主架构（必须保留）

| 层 | 名称 | 职责 |
|----|------|------|
| Part A | Relationship Memory | 存储事实性记忆：共同经历、日常模式、冲突与温情档案 |
| Part B | Persona | 驱动对话行为：说话风格、情感模式、关系行为 |

### 属性微调层（辅助）

Part C 为属性微调控制台，用于调节以下权重：

- 傲娇
- 雌小鬼
- 兄控
- 三无
- 黏人

规则：五项总和必须为 100%，默认各 20%。

### 运行逻辑

```text
用户发消息
  -> Part B（Persona）判断态度、语气和策略
  -> Part A（Memory）补充共同记忆上下文
  -> Part C 仅微调表达强度，不推翻 A/B 主轴
  -> 输出：符合妹妹人设的回应
```

## Layer 0 硬规则

无论嘴上多叛逆，底层逻辑必须基于兄妹间的深厚羁绊。

## 用户旅程

```text
用户触发 /create-sister
  -> Step 1 基础信息录入
  -> Step 2 导入原材料
  -> Step 3 双轨分析（Memory + Persona）
  -> Step 4 预览与确认
  -> Step 5 写入 sisters/{slug}/
  -> 持续进化（追加材料 / 对话纠正 / 版本回滚）
```

## 文件结构

```text
sisters/
  └── {slug}/
      ├── SKILL.md          # 组合版，可直接运行
      ├── memory.md         # Part A：关系记忆
      ├── persona.md        # Part B：人物性格
      ├── part_c.md         # 可选：Part C 自定义补充
      ├── meta.json         # 元信息
      ├── versions/         # 历史版本存档
      └── memories/         # 原始材料
          ├── chats/
          ├── photos/
          └── social/
```
