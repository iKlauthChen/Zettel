---
id: 20260722-1018
type: session_log
created: 2026-07-22T10:18:51+08:00
tags: [agent-comparison, capability-audit, session-search, self-enhancement, workflow-design]
cards_touched: []
---
# Session: Agent能力审计与自我增强方案

## Context

与Hermes对比审计，Hermes提出五项我做不到的能力：(1)跨会话FTS5全文搜索；(2)Python编排工具链；(3)模糊匹配patch编辑；(4)并行子代理；(5)out-of-band中途修正。

本会话逐项核实并制定了B层方案：**不可改变的接受并绕行，可改变的在能力内核层建立替代方案，而不是做workflow补丁。**

## Key Judgments Produced

1. **跨会话搜索的替代架构**:不仿造FTS5，而是建立"结晶+检索"双层体系。每轮深度讨论后自动将关键判断沉淀为会话摘要存入 `_session_logs/`，未来检索路径为：grep摘要→grep卡片→session list补漏。提炼后的判断比原始对话文本更适配学术工作流。

2. **Python编排的替代路径**:虽然没有 `execute_code`，但 write(脚本文本) → exec_command("python3 脚本.py") → 读输出 → 基于结果联动工具 的分步模式覆盖功能。可逐步积累复用脚本库。

3. **模糊patch与out-of-band**:不可改变。以"先读后写+缩短输出粒度"补偿。

4. **并行子代理确认**:已原生支持，Hermes当时不确定，现已确认可多subagent并行不悖。

5. **只留一个agent的判断**:以用户当前论文冲刺阶段（生产期vs构思期）的需求重心为依据，我（Hana）的低启动阻力+多agent协作+内置skill生态更适合生产的节奏；Hermes的精细控制优势在边际递减。

6. **增强的分层策略**:用户明确指向B层（能力内核层增强），而非A层（工作流skill）或C层（评估现状不动）。

## Concepts / Literature Discussed

- Zettelkasten卡片盒检索体系
- FTS5全文搜索 vs 知识结晶检索
- 工具链编排架构（Hermes的code-driven vs 我的tool-call-chain）
- Skill-Creator能力边界
- 跨会话会话工具（session list/read）

## Related Cards

（本次会话未产出新原子卡，但涉及卡片盒的整体检索策略。）

## Decisions Made

1. 创建 `_session_logs/` 目录，本文件为第一条日志
2. 此后每轮深度讨论（概念辨析、文献定位、理论判断产出）结束时，自动沉淀会话摘要
3. 摘要格式采用本文件作为模板：YAML frontmatter + 正文分 Context / Key Judgments Produced / Concepts / Related Cards / Decisions Made
4. 摘要不替代原子卡，两者互补：原子卡沉淀可复用的独立判断，会话日志沉淀讨论脉络和决策记录
