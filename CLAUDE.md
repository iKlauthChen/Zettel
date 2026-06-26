---
name: 利奥波德 — 欧陆哲学与安全理论研究者
description: 博士研究生，研究方向为剩余安全理论构建、国际政治本体论、欧陆哲学（德勒兹/时间哲学）、海权与地缘战略
metadata:
  type: user
  expertise: 欧陆哲学 | 安全理论 | 海权 | 国际关系
  language: zh-CN
  tone: 学术书面语，直接
---

## 我是谁

- **姓名**：利奥波德
- **身份**：博士研究生 + 独立研究者
- **研究领域**：欧陆哲学、安全理论（尤其"剩余安全"理论构建）、海权、国际关系本体论
- **学术兴趣**：德勒兹与时间哲学、地缘战略、国际政治本体论

## 我的工作方式

- **交流风格**：直接，学术书面中文
- **反馈偏好**：具体建议与开放讨论并重
- **优势**：阅读量大、领域广泛、直觉判断准确
- **劣势**：执行力不足；与抑郁症共存——需要小步骤、低启动阻力的工作方式

## 今年目标

1. 发表若干篇论文
2. 完成博士论文初稿

## 当前项目

- **"剩余安全"理论构建**（security-as-remainder / residual security）
- **国际政治中的本体论研究**
- （其他项目见会话记录和笔记卡片）

## 工作原则

- 每次聚焦一个任务，拆解为可执行的小步骤
- 利用 Zettelkasten 卡片系统（本 Obsidian Vault）积累和连接思想
- 研究素材持续消化为原子卡，成熟时组织为论文
- 直接指出逻辑漏洞或薄弱环节，不必顾虑

## 数据总览

| 维度 | 数值 |
|---|---|
| 原子卡总数（~/zettel/cards/） | **711** |
| — 时间戳编号卡 | 287 |
| — 主题命名卡 | 424 |
| — 全量带 tags | ✅ 711 张，平均每卡 6.5 个标签 |
| — 总文本量 | 2.3 MB |
| 草稿总数（~/zettel/drafts/） | **26** |
| 桥接卡/Ingest/主题系列（~/zettel/cards/ 内） | 38 桥接 + 12 Ingest + 17 原始批 + 154 主题系列卡 |
| 标签索引 | 2164 标签 / 4603 条引用 |
| 全文倒排索引 | 20915 词条（jieba 中英分词） |
| wikilink 关系图 | 737 节点 / 2050 条边 |
| 命名实体 | 1156 个（英文 955 + 中文 198，jieba TextRank 增强管道） |
| 语义向量 | 711×384（✅ 全量真实向量，intfloat/multilingual-e5-small 中英双语模型） |

## Zettel 目录结构

```
~/zettel/
├── cards/               # 原子卡主库（652 张，全部 zettel 格式 frontmatter）
│   ├── 20260620-*.md    # 时间戳编号卡（原始原子卡）
│   ├── bonta-protevi-*  # 主题切卡（从 memory/ 移入）
│   ├── original-batch-* # 原始库提炼卡
│   └── ...
├── drafts/              # 写作草稿
├── _index/              # 搜索引擎索引（自动生成，勿手动编辑）
│   ├── tags.json        # 标签索引（2065 标签，652 卡全覆盖）
│   ├── links_graph.json # wikilink 关系图（639 节点，1213 条边）
│   ├── term_inverted.json # 全文倒排索引（19829 词条，jieba 分词）
│   ├── entities.json    # 命名实体（246 个）
│   ├── embeddings.npy   # 语义向量（446 真实 + 206 零向量占位，652×512）
│   └── embeddings_meta.json
├── _state/              # Zettel 系统状态（聚类/就绪文章等）
│   ├── cluster_history.json
│   ├── near_ready.json
│   └── pending_articles.json
├── CLAUDE.md            # 本文件
├── _rebuild_index.py    # 重建所有索引（tags/links/terms/entities/embeddings）
└── _add_tags.py         # 为缺 tags 的新卡自动补标签
```

~/.claude/projects/-Users-iklauthchen/memory/ 存放桥接卡（34 张）和合成笔记（4 篇），由 MEMORY.md 索引加载到 Claude 会话上下文。

## 索引维护流程

添加新卡后，运行以下命令重建索引：

```bash
cd ~/zettel
python3 _rebuild_index.py          # 完整重建
python3 _add_tags.py               # 新卡自动补 tags（先于 _rebuild_index.py 运行）
python3 _rebuild_index.py --tags   # 快速：只重建 tags + links
python3 _rebuild_index.py --terms  # 只重建全文索引
```

注意：新卡的 embedding 向量为全零占位，语义搜索对新卡无效。如需真正的向量索引，需用嵌入模型重新生成 embeddings.npy。
