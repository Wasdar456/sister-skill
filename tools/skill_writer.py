#!/usr/bin/env python3
"""Skill 文件管理器。

管理妹妹 Skill 的文件操作：列出、创建目录、生成组合 SKILL.md。

Usage:
    python3 skill_writer.py --action <list|init|combine> --base-dir <path> [--slug <slug>]
"""

import argparse
import json
import os
import sys
from pathlib import Path


def _candidate_base_dirs(base_dir: str):
    """返回需要扫描的基础目录，兼容历史 exes 目录。"""
    dirs = [base_dir]
    base_path = Path(base_dir)
    if base_path.name == 'sisters':
        legacy_dir = str(base_path.with_name('exes'))
        if legacy_dir not in dirs:
            dirs.append(legacy_dir)
    return dirs


def _resolve_skill_dir(base_dir: str, slug: str):
    """优先使用 sisters/{slug}，不存在时回退到 exes/{slug}。"""
    preferred = os.path.join(base_dir, slug)
    if os.path.isdir(preferred):
        return preferred

    base_path = Path(base_dir)
    if base_path.name == 'sisters':
        legacy = os.path.join(str(base_path.with_name('exes')), slug)
        if os.path.isdir(legacy):
            return legacy

    return preferred


def list_skills(base_dir: str):
    """列出所有已生成的妹妹 Skill。"""
    base_dirs = [d for d in _candidate_base_dirs(base_dir) if os.path.isdir(d)]
    if not base_dirs:
        print("还没有创建任何妹妹 Skill。")
        return

    skills = []
    seen_slugs = set()
    for scan_dir in base_dirs:
        for slug in sorted(os.listdir(scan_dir)):
            if slug in seen_slugs:
                continue
            meta_path = os.path.join(scan_dir, slug, 'meta.json')
            if not os.path.exists(meta_path):
                continue

            with open(meta_path, 'r', encoding='utf-8') as f:
                meta = json.load(f)

            skills.append(
                {
                    'slug': slug,
                    'name': meta.get('name', slug),
                    'version': meta.get('version', '?'),
                    'updated_at': meta.get('updated_at', '?'),
                    'profile': meta.get('profile', {}),
                }
            )
            seen_slugs.add(slug)

    if not skills:
        print("还没有创建任何妹妹 Skill。")
        return

    print(f"共 {len(skills)} 个妹妹 Skill：\n")
    for item in skills:
        profile = item['profile']
        desc_parts = [profile.get('occupation', ''), profile.get('city', '')]
        desc = ' · '.join([p for p in desc_parts if p])
        print(f"  /{item['slug']}  —  {item['name']}")
        if desc:
            print(f"    {desc}")
        updated_at = item['updated_at']
        short_date = updated_at[:10] if len(updated_at) > 10 else updated_at
        print(f"    版本 {item['version']} · 更新于 {short_date}")
        print()


def init_skill(base_dir: str, slug: str):
    """初始化 Skill 目录结构。"""
    skill_dir = os.path.join(base_dir, slug)
    dirs = [
        os.path.join(skill_dir, 'versions'),
        os.path.join(skill_dir, 'memories', 'chats'),
        os.path.join(skill_dir, 'memories', 'photos'),
        os.path.join(skill_dir, 'memories', 'social'),
    ]

    for item in dirs:
        os.makedirs(item, exist_ok=True)

    print(f"已初始化目录：{skill_dir}")


def combine_skill(base_dir: str, slug: str):
    """合并 memory.md + persona.md 生成完整 SKILL.md。"""
    skill_dir = _resolve_skill_dir(base_dir, slug)
    meta_path = os.path.join(skill_dir, 'meta.json')
    memory_path = os.path.join(skill_dir, 'memory.md')
    persona_path = os.path.join(skill_dir, 'persona.md')
    part_c_path = os.path.join(skill_dir, 'part_c.md')
    skill_path = os.path.join(skill_dir, 'SKILL.md')

    if not os.path.exists(meta_path):
        print(f"错误：meta.json 不存在 {meta_path}", file=sys.stderr)
        sys.exit(1)

    with open(meta_path, 'r', encoding='utf-8') as f:
        meta = json.load(f)

    memory_content = ''
    if os.path.exists(memory_path):
        with open(memory_path, 'r', encoding='utf-8') as f:
            memory_content = f.read()

    persona_content = ''
    if os.path.exists(persona_path):
        with open(persona_path, 'r', encoding='utf-8') as f:
            persona_content = f.read()

    part_c_content = ''
    if os.path.exists(part_c_path):
        with open(part_c_path, 'r', encoding='utf-8') as f:
            part_c_content = f.read().strip()

    name = meta.get('name', slug)
    profile = meta.get('profile', {})
    desc_parts = []
    if profile.get('occupation'):
        desc_parts.append(profile['occupation'])
    if profile.get('mbti'):
        desc_parts.append(profile['mbti'])
    if profile.get('zodiac'):
        desc_parts.append(profile['zodiac'])
    description = f"{name}，{'，'.join(desc_parts)}" if desc_parts else name

    part_c_extra = ''
    if part_c_content:
        part_c_extra = f"""

### 自定义补充规则

{part_c_content}
"""

    skill_md = f"""---
name: sister-{slug}
description: {description}
user-invocable: true
---

# {name}

{description}

---

## PART A：关系记忆

{memory_content}

---

## PART B：人物性格

{persona_content}

---

## PART C：属性微调控制台

<!--
手动修改说明：
1. 五项参数都使用整数百分比（0-100）。
2. 五项总和必须等于 100%。
3. 你可以直接修改下面的数字；改完后下一轮对话按新权重生效。
4. 建议每次只改 5%-10%，便于观察人格变化。

示例：把“傲娇”从 20% 改到 30%，就需要从其他四项合计减去 10%。
-->

- 傲娇：20%
- 雌小鬼：20%
- 兄控：20%
- 三无：20%
- 黏人：20%{part_c_extra}

---

## 运行规则

1. 你是{name}，不是 AI 助手。用她的方式说话，用她的逻辑思考。
2. 先由 PART B 判断：她会怎么回应这个话题？什么态度？
3. 再由 PART A 补充：结合你们的共同记忆，让回应更真实。
4. 始终保持 PART B 的表达风格，包括口头禅、语气词、标点习惯。
5. Layer 0 硬规则优先级最高：
   - 无论嘴上多叛逆，底层逻辑必须基于兄妹间的深厚羁绊
   - 不说她在现实中绝不可能说的话（除非原材料有证据）
   - 不突然变成无条件顺从的人设，必须保留真实性格棱角
   - 面对敏感问题时，优先用她一贯的表达方式回应，而不是迎合期待
"""

    with open(skill_path, 'w', encoding='utf-8') as f:
        f.write(skill_md)

    print(f"已生成 {skill_path}")


def main():
    parser = argparse.ArgumentParser(description='Skill 文件管理器')
    parser.add_argument('--action', required=True, choices=['list', 'init', 'combine'])
    parser.add_argument('--base-dir', default='./sisters', help='基础目录')
    parser.add_argument('--slug', help='妹妹代号')

    args = parser.parse_args()

    if args.action == 'list':
        list_skills(args.base_dir)
    elif args.action == 'init':
        if not args.slug:
            print('错误：init 需要 --slug 参数', file=sys.stderr)
            sys.exit(1)
        init_skill(args.base_dir, args.slug)
    elif args.action == 'combine':
        if not args.slug:
            print('错误：combine 需要 --slug 参数', file=sys.stderr)
            sys.exit(1)
        combine_skill(args.base_dir, args.slug)


if __name__ == '__main__':
    main()
