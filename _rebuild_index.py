#!/usr/bin/env python3
"""Rebuild zettel indices: tags, links, terms (jieba), entities, embeddings.

Usage:
  python3 _rebuild_index.py            # rebuild all
  python3 _rebuild_index.py --tags     # tags + links only (fast)
  python3 _rebuild_index.py --terms    # terms only
  python3 _rebuild_index.py --full     # rebuild all including embedding placeholders

Requirements: pip install jieba numpy
"""

import json, re, os, sys
from pathlib import Path
from collections import defaultdict

CARDS_DIR = os.path.expanduser("~/zettel/cards")
INDEX_DIR = os.path.expanduser("~/zettel/_index")

# ── Chinese & English stopwords ──────────────────────────────────
ZH_STOP = set("""
的 了 在 是 我 有 和 就 不 人 都 一 一个 上 也 很 到 说 要 去 你
会 着 没有 看 好 自己 这 他 她 它 们 那 些 什么 这个 那个 怎么
而 为 以 能 之 与 及 但 或 被 从 对 被 把 向 让 将 所
如 更 又 还 因 其 最 中 于 只 多 大 小 可 已 且 若 非
各 种 时 年 行 等 均 则 即 比 做 每 别 某 该 哪 谁 何
第 几 些 点 面 来 出 过 后 前 能 再 才 已 经 曾 便 仍 还
既 虽 然 因 为 所 以 但 是 可 是 却 于 由 于 关 于 因 此
需要 问题 逻辑 通过 这种 而是 相关 理解 概念 框架 核心 条件
本身 方式 政治 提供 意义 层面 就是 完全 存在 如果 在于 全面
系统 还有 包括 一种 之间 分析 发展 不同 成为 进行 过程 区别
主要 内容 同时 之间 研究 可能 原则 重要 重新 方面 转化 基本
本文 而言 关系 认识 强调 还是 视角 观点 解释 超越 基于 形成
定义 提出 认为 作为 没有 通过 可以 这里 因此 第一 第二 第三
首先 其次 最后 体现 展开 领域 结构 表现 具有 进入 讨论 论述
""".split())

EN_STOP = {
    'the', 'and', 'that', 'this', 'with', 'from', 'which', 'their',
    'have', 'will', 'what', 'when', 'than', 'then', 'also', 'more',
    'been', 'were', 'does', 'some', 'about', 'into', 'through',
    'between', 'while', 'there', 'where', 'after', 'other', 'such',
    'both', 'each', 'over', 'very', 'just', 'because', 'could',
    'should', 'would', 'these', 'those', 'being', 'made', 'much',
    'has', 'had', 'its', 'who', 'whom', 'whose', 'here', 'why',
    'can', 'may', 'might', 'must', 'shall', 'upon', 'without',
    'across', 'among', 'before', 'below', 'during', 'above',
    'however', 'although', 'though', 'rather', 'almost', 'within',
    'well', 'also', 'yet', 'thus', 'still', 'here', 'there',
    'ever', 'never', 'using', 'used', 'use', 'get', 'got',
    'make', 'made', 'take', 'took', 'see', 'saw', 'known',
    'know', 'show', 'shown', 'new', 'old', 'one', 'two',
}

# ── Helpers ──────────────────────────────────────────────────────
def get_body(text):
    m = re.split(r'^---\s*\n.*?\n---\s*\n', text, maxsplit=1, flags=re.DOTALL)
    return m[1] if len(m) > 1 else text

def get_card_id(text, filename):
    m = re.search(r'^id:\s*(.+)', text, re.MULTILINE)
    return m.group(1).strip() if m else Path(filename).stem

def clean_body(body):
    body = re.sub(r'```.*?```', '', body, flags=re.DOTALL)
    body = re.sub(r'\[([^\]]+)\]\([^)]+\)', r'\1', body)
    body = re.sub(r'[#*_>`~|]', ' ', body)
    return body

def is_meaningful(w):
    if len(w) < 2: return False
    if w.isdigit(): return False
    if w.lower() in EN_STOP or w in ZH_STOP: return False
    if all(c in '，。、；：？！""''（）【】《》—…··・/\\|#*-+=' for c in w): return False
    return True

# ── Index builders ───────────────────────────────────────────────
def build_tags_and_links(card_files):
    """Rebuild tags.json and links_graph.json."""
    tags = defaultdict(list)
    links = defaultdict(lambda: {"out": [], "in": []})

    for cf in card_files:
        text = cf.read_text(encoding='utf-8')
        cid = get_card_id(text, cf.name)

        # Tags from frontmatter
        tm = re.search(r'^tags:\s*\[(.*?)\]', text, re.MULTILINE | re.DOTALL)
        if tm:
            for t in tm.group(1).split(','):
                t = t.strip().strip('"').strip("'")
                if t and cid not in tags[t]:
                    tags[t].append(cid)

        # Wikilinks from body
        body = get_body(text)
        for ref in re.findall(r'\[\[([^\]]+?)\]\]', body):
            ref = ref.split('|')[0].strip()
            if cid not in links[ref]["in"]:
                links[ref]["in"].append(cid)
            if ref not in links[cid]["out"]:
                links[cid]["out"].append(ref)

    with open(f"{INDEX_DIR}/tags.json", 'w') as f:
        json.dump(dict(tags), f, ensure_ascii=False, indent=2)
    with open(f"{INDEX_DIR}/links_graph.json", 'w') as f:
        json.dump(dict(links), f, ensure_ascii=False, indent=2)

    n_edges = sum(len(v['out']) for v in links.values())
    n_cards_with_tags = len({c for v in tags.values() for c in v})
    print(f"  tags.json:      {len(tags)} tags → {n_cards_with_tags} cards")
    print(f"  links_graph.json: {len(links)} nodes, {n_edges} edges")
    return tags, links

def build_terms(card_files):
    """Rebuild term_inverted.json using jieba segmentation."""
    import jieba
    inverted = {}

    for cf in card_files:
        text = cf.read_text(encoding='utf-8')
        cid = get_card_id(text, cf.name)
        body = clean_body(get_body(text))

        words = jieba.lcut(body)
        en_words = re.findall(r'\b[a-zA-Z]{4,}\b', body)

        seen = set()
        for w in words + en_words:
            w = w.strip()
            if not w or not is_meaningful(w) or w in seen:
                continue
            seen.add(w)
            if w not in inverted:
                inverted[w] = []
            if len(inverted[w]) < 200:
                inverted[w].append(cid)

    with open(f"{INDEX_DIR}/term_inverted.json", 'w') as f:
        json.dump(inverted, f, ensure_ascii=False, indent=2)
    print(f"  term_inverted.json: {len(inverted)} unique terms")
    return inverted

def build_entities(card_files):
    """Rebuild entities.json — extract capitalized English named entities."""
    entities = defaultdict(set)
    ent_pat = re.compile(r'\b[A-Z][a-zA-Z]{3,}(?:\s+[A-Z][a-zA-Z]+)*\b')

    for cf in card_files:
        text = cf.read_text(encoding='utf-8')
        cid = get_card_id(text, cf.name)
        for m in ent_pat.findall(text)[:10]:
            entities[m].add(cid)

    # Keep entities mentioned in 2+ cards, sort
    result = {k: sorted(v) for k, v in entities.items() if len(v) >= 2}
    with open(f"{INDEX_DIR}/entities.json", 'w') as f:
        json.dump(result, f, ensure_ascii=False, indent=2)
    print(f"  entities.json:  {len(result)} entities")
    return result

def build_embeddings(card_files):
    """Extend embeddings.npy with zero-vec placeholders for new cards."""
    import numpy as np

    meta_path = f"{INDEX_DIR}/embeddings_meta.json"
    npy_path = f"{INDEX_DIR}/embeddings.npy"

    if not os.path.exists(meta_path):
        print("  embeddings: no existing embeddings found, skipping")
        return

    old_meta = json.load(open(meta_path))
    old_ids = set(old_meta["ids"])

    all_ids = []
    for cf in card_files:
        text = cf.read_text(encoding='utf-8')
        all_ids.append(get_card_id(text, cf.name))

    new_ids = [cid for cid in all_ids if cid not in old_ids]
    if not new_ids:
        print(f"  embeddings: all {len(all_ids)} cards already indexed, skipping")
        return

    old_emb = np.load(npy_path)
    n_new = len(new_ids)
    new_emb = np.zeros((n_new, old_emb.shape[1]), dtype=old_emb.dtype)
    combined = np.vstack([old_emb, new_emb])
    np.save(npy_path, combined)

    old_meta["ids"].extend(new_ids)
    for nid in new_ids:
        old_meta["hashes"].append(f"ph_{nid[:14]}")
    with open(meta_path, 'w') as f:
        json.dump(old_meta, f, ensure_ascii=False, separators=(',', ':'))

    print(f"  embeddings: {old_emb.shape[0]} → {combined.shape[0]} vectors ({n_new} new zero-vec)")

# ── Main dispatch ────────────────────────────────────────────────
if __name__ == "__main__":
    mode = sys.argv[1] if len(sys.argv) > 1 else "--full"

    print(f"Scanning {CARDS_DIR}...")
    card_files = sorted(Path(CARDS_DIR).glob("*.md"))
    print(f"Found {len(card_files)} cards\n")

    if mode in ("--full", "--all"):
        build_tags_and_links(card_files)
        build_terms(card_files)
        build_entities(card_files)
        build_embeddings(card_files)
    elif mode == "--tags":
        build_tags_and_links(card_files)
    elif mode == "--terms":
        build_terms(card_files)
    elif mode in ("--entities", "--ents"):
        build_entities(card_files)
    elif mode == "--embeddings":
        build_embeddings(card_files)
    else:
        print(f"Unknown mode: {mode}")
        print("Usage: python3 _rebuild_index.py [--full|--tags|--terms|--entities|--embeddings]")
        sys.exit(1)

    print("\nDone.")
