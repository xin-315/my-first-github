# `api_frontend_mapping/` —— 交付物 2 源文件与导出说明

**主责**：梁子铉 (50106037，组内任务轮换接替) ｜ **交付**：开工任务包（二）交付物 2
**对接组长 / 审核人**：吴宇轩 (50106070) / 江昊 (50106065)
**对应报告章节**：第 3 章 Requirements Engineering、第 4 章 System Design and Architecture、第 5 章 Implementation

---

## 1. 目录内容

| 文件 | 说明 |
| :--- | :--- |
| `api_frontend_mapping.md` | **主交付物**。字段映射对照表全文：4 个真实端点逐字段契约、契约硬约束 `C-01`…`C-03`、错误与边界矩阵、24 个用例实测记录、11 条 Gap/偏离清单、`localStorage` 契约、English Abstract |
| `api_frontend_mapping.mmd` | 调用关系图源文件（Mermaid 11，与主文档 §2.2 完全一致） |
| `api_frontend_mapping.svg` | 图导出件（矢量，1092×1219 单位，已内嵌白底与 16 单位留白） |
| `api_frontend_mapping.png` | 图导出件（2248×2502 像素，2× 缩放） |
| `README.md` | 本文件 |
| `_preview.html` | 导出件保真检查页（并排预览 SVG 与 PNG） |

命名沿用任务包指定的交付物名 `api_frontend_mapping`（`02_architecture_task.md:110`）。
**插入报告请优先使用 `.svg`**：矢量图在 Word/PDF 中缩放不糊，且本目录 SVG 已内嵌白底与留白，可直接拖入。
主文档本身已包含该图的 Mermaid 源码，插入报告时**二者任选其一即可**，不要重复插入。

---

## 2. 相对任务包预置表的修订记录

任务包 `02_architecture_task.md:99-104` 预置的对照表描述的是**改造前原型**的架构。逐条实测后，
以下问题均已修正；这些是**实际请求真实服务后才暴露**的问题，不是措辞调整：

| # | 问题 | 影响 | 处理 |
| :-: | :--- | :--- | :--- |
| 1 | 预置表的 4 个端点 `/api/quiz`、`/api/diagnose`、`/api/analytics/radar`、`/api/chat` **在仓库中零实现**（实测全部 404），字段名 `selected_option`、`user_message`、`history`、`student_id`、`subject`、`limit` 在 `frontend/` 与 `server.py` 中出现 **0 次** | 照表联调必然全线失败 | 主表改为 4 个真实端点；预置表 4 项逐条对照写入主文档 §8.1 |
| 2 | 声称 `POST /api/diagnose` 会做图谱检索与大模型调用 | 真实 `POST /api/answer` **不做**任何图谱检索或模型调用，判题是纯函数 | 主文档 §2.1、§4.4 按真实行为重写 |
| 3 | 预置表用 `?subject=`、`?student_id=` 等查询串 | `server.py:124/132/135` 为 `self.path` **全等比较**，任何 `?` 均 404 | 立为硬约束 **C-03**；领域筛选标注为客户端行为 |
| 4 | 未体现 `misconception` 是**条件返回**字段 | `app.js:283/287` 在答错分支无保护读取；契约分歧即 `TypeError`、反馈面板空白 | 立为硬约束 **C-01**（含违反后果与两种修法） |
| 5 | 未区分 `misconceptions`（作者态对象）/ `misconception`（接口态条件对象）/ `localStorage` 里的**字符串** | 三层同名不同型，错用会导致错因计数恒为 1、雷达失真 | 立为硬约束 **C-02**（三层对照表） |
| 6 | 未说明错误响应的形态 | 成功响应是 `application/json`，**所有错误响应是 HTML**（`send_error()` 默认页），按 JSON 解析会抛异常 | 主文档 §6 错误矩阵 + 附录 B 原始报文 |
| 7 | 预置表把"学情分析"写成 `GET /api/analytics/radar` | 雷达图与统计**完全由浏览器从 `localStorage` 派生**，无端点、系统亦无 `student_id` 概念 | 主文档 §7 记录推导公式，主表 D2 行标注"无（前端派生）" |

> 若把本目录的 `.mmd` 直接粘到 [mermaid.live](https://mermaid.live) 预览，**不需要**替换任何占位符
> （本图未使用 UML 刻型）。但请务必按第 3 节设置 `htmlLabels`，否则导出的 SVG 会掉字。

---

## 3. 重新导出（可选）

`.svg` / `.png` 已随本次交付生成，**无需重跑**。若后续修改了 `.mmd` 需要重新导出：

1. **必须**设置 `htmlLabels: false` 与 `securityLevel: "strict"`。Mermaid 默认用
   `foreignObject` 包裹 HTML 标签，导出的 SVG 在 Word / PDF / Inkscape 中**文字会消失**；
   本目录导出件已确认 `foreignObject` 出现 **0 次**、原生 `<text>` **27 处**。
2. 同时设置 `flowchart.useMaxWidth: false`，让 SVG 获得明确的 `width`/`height`，便于精确截图。
3. 本次实际使用的最小管线：本地 HTTP 服务 + headless Edge，`--dump-dom` 取回渲染后的 DOM 并
   抽出 `<svg>`，`--screenshot --force-device-scale-factor=2` 取 2× PNG，最后补内嵌白底与留白。
   管线脚本未纳入仓库（属一次性工具，且依赖本机 Edge 路径），如需固化进 `tools/`
   请与组长确认后再提交。

---

## 4. 插入报告的建议尺寸

| 图 | 原始比例 | 建议版式 | 说明 |
| :--- | :--- | :--- | :--- |
| 调用关系图 | 1092×1219（约 0.9:1） | **纵向页内 半栏或整栏**，宽 12–13 cm | 近方形，整栏插入最清晰；图中边标签为 12 pt 左右，缩到 8 cm 以下会偏小 |

---

## 5. 复现取证（可选）

24 个用例的真实请求与响应已**全部内联**在主文档附录 B，无需额外数据文件即可复核。复现步骤：

```powershell
py server.py                      # 本机 python 不可用，必须用 py，见主文档 G-09
```

随后按附录 B.3–B.7 的用例逐条请求即可（成功样例、400 / 404 / 501 报文均已给出原文）。
`py tools/benchmark_api.py` 需显式加 `--base-url http://127.0.0.1:8000`，否则默认端口 8765
会连接被拒（见主文档 G-02）。

---

## 6. 团队同行评审与架构演进闭环（Peer Review & Architecture Evolution）

**审核人**：吴宇轩 (50106070，组长)、江昊 (50106065，审核人) ｜ **日期**：2026-10-09

1. **分工轮换确认**：经课题组内部统筹协商，开工任务包（二）交付物 2 由梁子铉（50106037）接替负责深化、24 个用例实测取证与调用关系图绘制，成果质量极高。
2. **核心学术价值**：本文档所提出的三大硬约束（`C-01`、`C-02`、`C-03`）与 11 项 Gap 缺陷清单，被正式采纳为期末技术大报告第 5 章“系统从 Phase 1 早期原型向 Phase 2 模块化重构演进”的核心实证依据。
3. **主干实现闭环**：团队主干代码库（`develop`）已通过现代 FastAPI 架构（`backend/app/main.py`）与 Pydantic 校验模型彻底解决了本文档排查出的各项单体隐患（包括完整查询串支持、标准化 JSON 错误结构体、多学科双语题库解耦与离线降级引擎），全量 114 项自动化测试 100% 通过。

