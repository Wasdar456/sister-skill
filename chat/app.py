#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
妹妹聊天后端服务
启动后访问 http://localhost:5001
"""
from __future__ import unicode_literals

import os
import sys
import io
# 强制 UTF-8 输出，避免 ASCII codec 错误
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8')

import json
import uuid
from datetime import datetime
from pathlib import Path

# 把项目根目录加到 path，这样可以 import config
ROOT = Path(__file__).parent.parent
sys.path.insert(0, str(ROOT))
sys.path.insert(0, str(Path(__file__).parent))

from flask import Flask, request, jsonify, send_from_directory
from openai import OpenAI

import config

# ── 初始化 ──────────────────────────────────────────────────────────────
app = Flask(__name__, static_folder="static", static_url_path="")

# OpenAI 客户端
client_kwargs = {"api_key": config.OPENAI_API_KEY}
if config.OPENAI_BASE_URL:
    client_kwargs["base_url"] = config.OPENAI_BASE_URL
ai = OpenAI(**client_kwargs)

# 聊天记录目录
LOG_DIR = ROOT / config.CHAT_LOG_DIR
LOG_DIR.mkdir(parents=True, exist_ok=True)

# ── 读取 SKILL.md ────────────────────────────────────────────────────────
CORRECTIONS_FILE = ROOT / "sisters/meimei/corrections.md"

def load_meta() -> dict:
    """从 meta.json 读取人物元信息"""
    meta_path = ROOT / "sisters/meimei/meta.json"
    if meta_path.exists():
        with open(meta_path, "r", encoding="utf-8") as f:
            return json.load(f)
    return {"name": "???", "my_name": "我"}

SISTER_META = load_meta()

def load_skill() -> str:
    skill_path = ROOT / config.SKILL_PATH
    if not skill_path.exists():
        return "你是王欣彤，王梓涵的妹妹。"
    with open(skill_path, "r", encoding="utf-8") as f:
        content = f.read()
    # 去掉 frontmatter (--- ... ---) 留下正文
    lines = content.split("\n")
    if lines[0].strip() == "---":
        end = next((i for i, l in enumerate(lines[1:], 1) if l.strip() == "---"), None)
        if end:
            content = "\n".join(lines[end + 1:]).strip()
    return content

def load_corrections() -> str:
    """读取 corrections.md，提取 [纠正记录] 区域内容"""
    if not CORRECTIONS_FILE.exists():
        return ""
    with open(CORRECTIONS_FILE, "r", encoding="utf-8") as f:
        content = f.read()
    marker = "## [纠正记录]"
    if marker in content:
        return content.split(marker, 1)[1].strip()
    return ""

def build_system_prompt() -> str:
    """合并 SKILL.md + 纠正记录"""
    skill = load_skill()
    corrections = load_corrections()
    if corrections:
        corrections_block = f"\n\n## 【重要补充】以下是你被纠正过的点，请严格遵守：\n{corrections}\n"
        # 追加到运行规则前面
        return skill + corrections_block
    return skill

SYSTEM_PROMPT = build_system_prompt()

# ── 会话内存（进程内，重启后清空；持久化靠日志文件）────────────────────
sessions: dict[str, list] = {}


def get_session(session_id: str) -> list:
    if session_id not in sessions:
        sessions[session_id] = []
    return sessions[session_id]


# ── 日志工具 ──────────────────────────────────────────────────────────────
def log_path(session_id: str) -> Path:
    return LOG_DIR / f"{session_id}.json"


def load_history(session_id: str) -> list:
    p = log_path(session_id)
    if p.exists():
        with open(p, "r", encoding="utf-8") as f:
            return json.load(f)
    return []


def save_history(session_id: str, history: list):
    with open(log_path(session_id), "w", encoding="utf-8") as f:
        json.dump(history, f, ensure_ascii=False, indent=2)


# ── API 路由 ──────────────────────────────────────────────────────────────

@app.route("/")
def index():
    return send_from_directory("static", "index.html")


@app.route("/api/sister/info", methods=["GET"])
def sister_info():
    """返回当前人物信息（供前端动态渲染）"""
    return jsonify({
        "name": SISTER_META.get("name", "???"),
        "my_name": SISTER_META.get("my_name", "我"),
    })


@app.route("/api/session/new", methods=["POST"])
def new_session():
    """创建新会话"""
    sid = datetime.now().strftime("%Y%m%d_%H%M%S") + "_" + uuid.uuid4().hex[:6]
    sessions[sid] = []
    return jsonify({"session_id": sid})


@app.route("/api/session/list", methods=["GET"])
def list_sessions():
    """列出所有历史会话"""
    logs = sorted(LOG_DIR.glob("*.json"), key=lambda p: p.stat().st_mtime, reverse=True)
    result = []
    for log in logs[:30]:  # 最多显示 30 个
        try:
            with open(log, "r", encoding="utf-8") as f:
                history = json.load(f)
            if not history:
                continue
            # 找第一条用户消息作为会话标题
            first_user = next((m["content"] for m in history if m["role"] == "user"), "空会话")
            last_time = history[-1].get("time", "") if history else ""
            result.append({
                "session_id": log.stem,
                "title": first_user[:30] + ("…" if len(first_user) > 30 else ""),
                "message_count": len(history),
                "last_time": last_time,
            })
        except Exception:
            pass
    return jsonify(result)


@app.route("/api/session/<session_id>/load", methods=["GET"])
def load_session(session_id: str):
    """载入历史会话"""
    history = load_history(session_id)
    sessions[session_id] = history
    return jsonify({"session_id": session_id, "history": history})


@app.route("/api/chat", methods=["POST"])
def chat():
    """发送消息，获取回复"""
    body = request.get_json()
    session_id = body.get("session_id", "default")
    user_message = body.get("message", "").strip()

    if not user_message:
        return jsonify({"error": "消息不能为空"}), 400

    # ── 纠正指令检测 ─────────────────────────────────────────
    correction_types = ["纠正", "追加记忆", "调整性格"]
    is_correction = any(user_message.startswith(f"[{t}:") for t in correction_types)

    if is_correction:
        return handle_correction(user_message)

    history = get_session(session_id)

    # 追加用户消息
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    history.append({"role": "user", "content": user_message, "time": now})

    # 构建发给 API 的消息列表（不传 time 字段）
    messages = [{"role": "system", "content": build_system_prompt()}]
    messages += [{"role": m["role"], "content": m["content"]} for m in history]

    try:
        resp = ai.chat.completions.create(
            model=config.MODEL,
            messages=messages,
        )
        reply = resp.choices[0].message.content.strip()
    except Exception as e:
        return jsonify({"error": str(e)}), 500

    # 追加 AI 回复
    reply_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    history.append({"role": "assistant", "content": reply, "time": reply_time})

    # 持久化
    save_history(session_id, history)

    return jsonify({
        "reply": reply,
        "time": reply_time,
        "session_id": session_id,
    })


def handle_correction(msg: str) -> dict:
    """解析纠正指令，写入 corrections.md，返回确认消息"""
    now_str = datetime.now().strftime("%Y-%m-%d %H:%M")

    # 解析类型和内容
    import re
    match = re.match(r"\[(纠正|追加记忆|调整性格):\s*(.+)\]", msg, re.DOTALL)
    if not match:
        return jsonify({
            "reply": "⚠️ 格式不对，纠正指令格式：`[纠正: 具体内容]` 或 `[追加记忆: ...]` 或 `[调整性格: ...]`",
            "time": now_str,
            "session_id": "system",
        })

    corr_type = match.group(1)
    corr_content = match.group(2).strip()
    entry = f"*{now_str}* | {corr_type} | {corr_content}"

    # 追加到 corrections.md
    CORRECTIONS_FILE.parent.mkdir(parents=True, exist_ok=True)
    if not CORRECTIONS_FILE.exists():
        CORRECTIONS_FILE.write_text("# 纠正记录\n\n## [纠正记录]\n", encoding="utf-8")

    with open(CORRECTIONS_FILE, "a", encoding="utf-8") as f:
        f.write(f"{entry}\n")

    # 确认消息
    type_labels = {
        "纠正": "✅ 已记录为纠正，下遇到类似场景会避开",
        "追加记忆": "✅ 已追加到长期记忆库",
        "调整性格": "✅ 已调整性格描述",
    }

    return jsonify({
        "reply": type_labels.get(corr_type, "✅ 已记录") + f"\n\n📝 [{corr_type}]：{corr_content}",
        "time": now_str,
        "session_id": "system",
    })


@app.route("/api/session/<session_id>/clear", methods=["POST"])
def clear_session(session_id: str):
    """清空当前会话记忆（不删文件）"""
    sessions[session_id] = []
    p = log_path(session_id)
    if p.exists():
        p.unlink()
    return jsonify({"ok": True})


if __name__ == "__main__":
    print(f"✅ 妹妹已上线，访问 http://localhost:{config.PORT}")
    print(f"   人设：{config.SKILL_PATH}")
    print(f"   模型：{config.MODEL}")
    print(f"   日志：{LOG_DIR}")
    app.run(host="0.0.0.0", port=config.PORT, debug=False)
