# 实现计划：产品介绍与迎新登录门户 (Landing & Auth Portal)

**分支**：`001-landing-and-auth-portal` | **日期**：2026-10-08 | **规格**：[spec.md](spec.md)  
**输入**：来自 `specs/001-landing-and-auth-portal/spec.md` 的功能规格

---

## 概要

针对用户反馈“当前界面不伦不类、直接进入冷峻高密度的 Eval Harness 导致体验突兀”的问题，设计并落地**高颜值大学生理工科智能助学产品介绍与迎新登录门户 (Landing & Auth Portal)**。
该门户作为整个系统的第一接待站，清晰传达阿伯丁大学 JC2001 Group 5 的项目定位、错因图谱核心创新价值及四大功能模块；内置课题组 10 人核心成员学籍档案快速登入通道；支持一键平滑过渡至日常刷题与排雷工作台（“平时的界面”），并在工作台提供随时返回产品介绍页面的双向通道。

---

## 技术背景

- **语言/运行环境**：原生 ES6+ JavaScript, HTML5, CSS3（与已有前端代码零摩擦融合）
- **后端服务**：FastAPI (Python 3.11/3.13), Uvicorn 异步服务，静态挂载模式
- **依赖管理**：零外部新增前端打包依赖（无 Webpack/Vite 编译负担，秒开秒测），沿用已安装的 ECharts 5.5.1 CDN
- **状态存储**：浏览器本地持久化缓存（`localStorage`：`smartstudy_auth_session`, `smartstudy_theme`）
- **目标平台**：现代 Chromium 浏览器 / Firefox / Edge / Safari，自适应移动端与桌面端
- **性能指标**：首页加载时间 < 100ms，门户与工作台视图切换延迟 < 150ms（60fps 硬件加速过渡）
- **核心约束**：
  1. 严格遵守 JC2001 本科生软件工程规范，不进行商业级过度设计；
  2. 保持对已有 114 个自动化后端测试与已部署的 `/api/diagnose` 逻辑 100% 零破坏兼容；
  3. 符合零根目录污染、外科手术式精准修改与空间整洁原则。

---

## 宪章检查 (Constitution Checks)

| 检查项 | 状态 | 评估与正当化理由 |
| :--- | :--- | :--- |
| **本科生能力边界** | ✅ 通过 | 采用经典 SPA 双容器轻量切换模式，逻辑清晰可解释，答辩时易于向导师阐述。 |
| **测试与质量回归** | ✅ 通过 | 不破坏任何已有路由与数据模型，保证现有 `pytest tests/` 保持 100% 通过率。 |
| **文件操作纪律** | ✅ 通过 | 新增文档全部归集于 `specs/001-landing-and-auth-portal/`，禁止根目录污染。 |
| **既有代码完整性** | ✅ 通过 | 原有 `#app-shell` 控制台逻辑一律作为受保护的受控子容器，仅做增量包裹与桥接。 |

---

## 项目结构

### 规范工件 (此功能)

```text
specs/001-landing-and-auth-portal/
├── spec.md              # 需求工程与用户故事规格书
├── plan.md              # 本实施计划文件
├── research.md          # 第 0 阶段：架构抉择与状态机转换
├── data-model.md        # 第 1 阶段：学生身份与会话数据模型
├── contracts/           # 第 1 阶段：视图流转与接口契约
│   └── portal-auth-contracts.md
└── quickstart.md        # 第 1 阶段：一键启动与验收核对单
```

### 源代码变动区域 (Repository Layout)

```text
frontend/
├── index.html           # 增量嵌入 #portal-landing 门户结构，与 #app-shell 协同
├── style.css            # 增量添加产品介绍门户与角色卡片的响应式样式
└── app.js               # 增量注入 switchRootView、initAuthPortal 与预设账号联动逻辑
```

**结构决策**：采用内聚扩展模式，将介绍门户作为前端根层级的第一级路由器。用户未登录或主动查看介绍时展示 `#portal-landing`，进入后激活原有的 `#app-shell` 工作台。

---

## 复杂度跟踪

*无需填报（未触发任何架构门禁违规，无过度设计引入）。*

---

## 实施阶段任务分解 (Work Breakdown)

### 阶段 0: 架构与技术调研 (已完成)
- [x] 产出 `research.md`：解决 SPA 容器切换、localStorage 持久化及双模主题自适应方案。

### 阶段 1: 模型与契约设计 (已完成)
- [x] 产出 `spec.md`：明确产品介绍、角色选择、返回主页三大需求。
- [x] 产出 `data-model.md`：标准化 `StudentProfile`、`AuthSession` 及预设账号。
- [x] 产出 `contracts/portal-auth-contracts.md`：定义 `switchRootView` 与 `loginStudent`。
- [x] 产出 `quickstart.md`：制定快速启动与三步验收核验单。

### 阶段 2: 精准实施编码 (Ready to Execute)
1. **HTML 骨架注入** (`frontend/index.html`)：在 `#app-shell` 前注入现代感 `#portal-landing` 门户节点；在 `#app-sidebar` 内注入“返回产品首页”通道。
2. **CSS 样式补充** (`frontend/style.css`)：编写 Hero 横幅、四大功能卡片网格、预设身份一键切换面板及流畅转场动效。
3. **JS 逻辑连接** (`frontend/app.js`)：实现 `initAuthPortal()`、`switchRootView()`、预设角色快捷载入及双向平滑切换。
4. **验证与回归**：启动服务验证交互、运行 pytest 测试套件并截取验收图景。
