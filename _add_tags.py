#!/usr/bin/env python3
"""Auto-tag cards that are missing the `tags:` field in frontmatter.

Usage:
  python3 _add_tags.py              # tag all untagged cards
  python3 _add_tags.py --dry-run    # preview only, no changes
  python3 _add_tags.py --clean      # remove junk tags too

Uses jieba TF-IDF keyword extraction from card body.
"""

import re, os, sys
from pathlib import Path

CARDS_DIR = os.path.expanduser("~/zettel/cards")

ZH_STOP = set("""
需要 问题 逻辑 通过 这种 而是 结构 空间 相关 理论 理解 概念 框架
核心 条件 本身 本体论 方式 政治 提供 意义 层面 就是 完全 存在
如果 在于 全面 系统 还有 包括 一种 之间 分析 发展 不同 成为
进行 过程 区别 主要 内容 同时 之间 研究 可能 原则 重要 重新
方面 转化 基本 本文 而言 关系 认识 一个 强调 还是 视角 观点
解释 超越 基于 形成 定义 提出 认为 作为 没有 通过 这个 可以
这里 因此 第一 第二 第三 首先 其次 最后 但 是 及 其 与 从
体现 展开 领域 结构 表现 具有 进入 讨论 论述 相关 给出 指出
主题 思路 揭示 叙述 总结 过渡 呈现 构成 支撑 列举 谈及 引用
""".split())

JUNK_TAGS = {"------", "-----", "---", "", " ", None}

def get_body(text):
    m = re.split(r'^---\s*\n.*?\n---\s*\n', text, maxsplit=1, flags=re.DOTALL)
    return m[1] if len(m) > 1 else ""

def frontmatter_and_rest(text):
    m = re.match(r'^(---\s*\n.*?\n)---\s*\n?(.*)', text, re.DOTALL)
    return (m.group(1), m.group(2)) if m else ("", text)

def clean_body(body):
    body = re.sub(r'```.*?```', '', body, flags=re.DOTALL)
    body = re.sub(r'\[([^\]]+)\]\([^)]+\)', r'\1', body)
    body = re.sub(r'[#*_>`~|]', ' ', body)
    body = re.sub(r'\{\{[^}]+\}\}', '', body)
    return body

def extract_tags(body, card_id):
    """Generate tags using jieba TF-IDF + filename prefix."""
    import jieba.analyse

    # Card name prefix as a tag (author/source)
    prefix = card_id.split('-')[0]
    tags = [prefix]

    body = clean_body(body)
    kws = jieba.analyse.extract_tags(body, topK=12, withWeight=False)

    for kw in kws:
        kw = kw.strip()
        if len(kw) < 2: continue
        if kw in ZH_STOP or kw in tags: continue
        tags.append(kw)

    # Dedup preserving order
    seen = set()
    deduped = []
    for t in tags:
        if t not in seen:
            seen.add(t)
            deduped.append(t)
    return deduped[:10]

def tag_one(fpath, dry_run=False):
    text = open(fpath, encoding='utf-8').read()

    # Skip if already tagged
    if re.search(r'^tags:', text, re.MULTILINE):
        return False

    body = get_body(text)
    card_id = Path(fpath).stem
    tags = extract_tags(body, card_id)

    if not tags:
        return False

    front, rest = frontmatter_and_rest(text)
    front_lines = front.split('\n')

    # Find closing ---
    close_idx = None
    for i, line in enumerate(front_lines):
        if line.strip() == '---':
            close_idx = i
    if close_idx is None:
        return False

    tag_line = f"tags: [{', '.join(tags)}]"
    front_lines.insert(close_idx, tag_line)
    new_front = '\n'.join(front_lines)
    new_text = f"{new_front}\n{rest}"

    if not dry_run:
        with open(fpath, 'w', encoding='utf-8') as f:
            f.write(new_text)
    return list(tags)

def clean_junk_tags(fpath, dry_run=False):
    """Remove obviously bad tags from any card."""
    text = open(fpath, encoding='utf-8').read()
    m = re.search(r'^tags:\s*\[(.*?)\]', text, re.MULTILINE)
    if not m:
        return False

    original = m.group(0)
    tags = [t.strip() for t in m.group(1).split(',')]
    cleaned = [t for t in tags if t not in JUNK_TAGS and len(t) > 1]

    if len(cleaned) != len(tags):
        new_line = f"tags: [{', '.join(cleaned)}]"
        if not dry_run:
            text = text.replace(original, new_line)
            with open(fpath, 'w', encoding='utf-8') as f:
                f.write(text)
        return True
    return False

if __name__ == "__main__":
    dry_run = "--dry-run" in sys.argv
    do_clean = "--clean" in sys.argv

    tag_files = sorted(Path(CARDS_DIR).glob("*.md"))
    tagged = 0
    cleaned = 0

    for cf in tag_files:
        result = tag_one(str(cf), dry_run)
        if result:
            if dry_run:
                print(f"  [DRY-RUN] {cf.name} → {result}")
            else:
                print(f"  ✅ {cf.name} → {result}")
            tagged += 1

    if do_clean:
        for cf in tag_files:
            if clean_junk_tags(str(cf), dry_run):
                if dry_run:
                    print(f"  [DRY-RUN] cleaned {cf.name}")
                else:
                    print(f"  🧹 cleaned {cf.name}")
                cleaned += 1

    print(f"\nTagged: {tagged}, Cleaned: {cleaned}")
    if dry_run:
        print("(dry run — no files changed)")
