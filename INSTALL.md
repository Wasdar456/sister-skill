# sister-skill 安装说明

仓库地址：
https://github.com/Wasdar456/sister-skill

---

## Claude Code 安装

### 项目内安装

在项目根目录执行：

```bash
mkdir -p .claude/skills
git clone https://github.com/Wasdar456/sister-skill .claude/skills/create-sister
```

### 全局安装

```bash
git clone https://github.com/Wasdar456/sister-skill ~/.claude/skills/create-sister
```

### OpenClaw 安装

```bash
git clone https://github.com/Wasdar456/sister-skill ~/.openclaw/workspace/skills/create-sister
```

---

## 依赖安装（可选）

```bash
cd .claude/skills/create-sister  # 或你的安装路径
pip3 install -r requirements.txt
```

当前可选依赖主要是 `Pillow`，用于照片 EXIF 解析。

---

## 快速开始

1. 在 Claude Code 中输入 `/create-sister`。
2. 根据提示填写妹妹代号与基础画像。
3. 导入聊天记录/截图/照片或直接口述。
4. 生成完成后使用 `/{slug}` 对话。

---

## 原材料准备建议

### 微信聊天记录

1. 打开微信聊天窗口。
2. 手动复制关键聊天到 txt 文件，或直接截图上传。
3. 在创建流程里选择对应导入方式。

### QQ 聊天记录

1. 打开 QQ 设置并导出聊天记录（txt/mht）。
2. 上传文件后按提示解析。

### 口述补充

如果没有文件，也可以直接描述妹妹的说话风格、日常习惯和关键记忆。

---

## 常见问题

### Q: 数据会上传到云端吗？
A: 不会。原材料与生成文件默认保存在本地目录 `sisters/{slug}/`。

### Q: 可以同时创建多个妹妹 Skill 吗？
A: 可以。每个妹妹会生成独立目录。

### Q: 创建后还能修改吗？
A: 可以。使用 `/update-sister {slug}` 追加内容，或在对话中纠正后自动更新。

### Q: 我想删除怎么办？
A: 使用 `/delete-sister {slug}` 或 `/let-go {slug}`。
