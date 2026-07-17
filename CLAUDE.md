---
name: 陈祖丰 — 欧陆哲学与安全理论研究者
description: 博士研究生，研究方向为剩余安全理论构建、国际政治本体论、欧陆哲学（德勒兹/时间哲学）、海权与地缘战略
metadata:
  type: user
  expertise: 欧陆哲学 | 安全理论 | 海权 | 国际关系
  language: zh-CN
  tone: 学术书面语，直接
---

## 我是谁

- **姓名**：陈祖丰
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

- **"剩余安全"理论构建**（surplus security）
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

## 卡片格式规范

### 文件命名
`YYYYMMDD-NNNN-简短描述.md`
- `YYYYMMDD` = `created:` 字段中的日期
- `NNNN` = 当天内的顺序号（0001 起，按字母序排列）
- 描述取卡片标题或别名，中文不用 `":"` 和 `"`
- **关键规则：文件名必须包含英文字母**（`id:` 和 wikilink 同理）。macOS + Obsidian 无法索引纯数字/纯数字+符号的文件名（如 `20260622-0030.md`），会导致链接跳转失败。**永远使用** `20260622-0030-abrahams-assemblage.md` 而非 `20260622-0030.md`。
- wikilink 也须使用完整的描述性 ID（`[[20260622-0030-abrahams-assemblage]]`），而非仅数字前缀（`[[20260622-0030]]`）。

### YAML 前置元数据模板
```yaml
---
id: YYYYMMDD-NNNN
status: permanent
created: 2026-06-24T15:23:59+0800
source: {type: book|article|reading-note|external-url, ref: "完整引用", page: "页码"}
tags: [tag1, tag2, concept]
links:
  - {id: YYYYMMDD-NNNN, reason: "关联原因——明确链接理由"}
voice_passed: true
aliases: ["卡片核心论题的简洁表述"]
---
```

### YAML 常见陷阱（必须避免）

| 问题 | 错误示例 | 正确写法 |
|---|---|---|
| **缺开头 `---`** | `tags: [...]`（文件直接以 YAML 内容开头） | `---\ntags: [...]` |
| **中文双引号嵌套** | `aliases: ["德勒兹的"块茎"概念"]` → YAML 将 `"块茎"` 的 `""` 视为字符串结束 | `aliases: ["德勒兹的'块茎'概念"]` 改用英文单引号 |
| **ASCII `"` 在未引用值中** | `description: 情报机构"封住"安全化` → `"` 被 YAML 解析为特殊字符 | `description: "情报机构'封住'安全化"` 将整个值用 YAML 双引号包裹 |
| **重复键** | `pages: "23-26; Deleuze...", pages: "114-216"` → 后一个覆盖前一个 | 合并到 `ref` 字段：`ref: "..., pp.23-26; ..., pp.114-216"` |
| **冒号在未引用值中** | `description: Reid(2003) War Machine: Nomadism` → `: ` 被解析为映射分隔符 | `description: "Reid(2003) War Machine: Nomadism"` |
| **缺尾部 `---`** | YAML 内容延伸至正文，`**bold**` 的 `*` 被解析为 YAML 别名 | 确保正文前有 `---\n` 关闭 YAML |

### Wiki 链接格式

```markdown
<!-- 正确：使用时间戳 ID，无 .md 后缀 -->
[[20260624-0001|显示文本]]

<!-- 错误：使用描述性名称 -->
[[baldauff-heng-japan-dcas-card1-puzzle]]

<!-- 错误：带 .md 后缀 -->
[[20260624-0001.md|显示文本]]
```

### 相关卡片 Section 格式

```markdown
## 相关卡片

- [[20260624-0005|目标卡片别名]] — 关联原因说明
- [[20260623-1400|概念创造]] — 与概念创造论的建构论前提一致
```

**关键：wikilink 必须使用完整描述性 ID**。例如 `[[20260624-0005-baldauff-card1-puzzle]]`，**不要**只用 `[[20260624-0005]]`（纯数字 ID 在 macOS Obsidian 中无法解析）。

### 创建新卡的标准流程

1. 确定 `created:` 时间戳（ISO 8601: `2026-06-24T15:23:59+0800`）
2. 命名文件：`YYYYMMDD-NNNN-别名摘要.md`
3. 写入 YAML frontmatter（参照模板）
4. `tags` 从现有标签索引复用，避免发明不规范标签
5. `links` 填写与本卡有直接关联的前件卡片
6. 文末 `## 相关卡片` 填写跨簇链接
7. 运行索引维护流程

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
