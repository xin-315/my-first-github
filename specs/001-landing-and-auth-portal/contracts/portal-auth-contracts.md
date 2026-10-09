# 交互与接口契约规约 (Phase 1: Contracts)

**功能编号**：`001-landing-and-auth-portal`  
**关联规格**：`specs/001-landing-and-auth-portal/spec.md`  
**完成时间**：2026-10-08  

---

## 1. 前端视图流转契约 (Frontend View Lifecycle Contract)

### 1.1 根容器切换：`switchRootView(targetView, options)`
负责在“产品介绍门户 (`#portal-landing`)”与“平时的学习控制台 (`#app-shell`)”之间进行无缝切换。

```typescript
type RootView = 'portal' | 'workspace';

interface SwitchViewOptions {
  /** 如果切换到控制台，默认激活的子视图 (默认 'quiz') */
  targetTab?: 'quiz' | 'tutor' | 'graph' | 'report';
  
  /** 伴随切换的学生登录档案 (若由卡片直接点击) */
  userProfile?: StudentProfile;
  
  /** 是否更新 URL Hash (例如 #portal, #workspace) */
  updateHash?: boolean;
}

function switchRootView(targetView: RootView, options?: SwitchViewOptions): void;
```

**行为规范与约束**：
1. 若 `targetView === 'workspace'`：
   - `#portal-landing` 节点添加 `.view-hidden` 样式（渐隐动效 150ms），随后 `display: none`。
   - `#app-shell` 节点移除 `hidden` 属性，`display: flex`。
   - 触发一次 ECharts 图表 resize（`window.dispatchEvent(new Event('resize'))`），保证控制台雷达图尺寸精准渲染。
2. 若 `targetView === 'portal'`：
   - `#app-shell` 节点 `display: none`。
   - `#portal-landing` 节点 `display: block`，平滑淡入。

---

### 1.2 学籍身份鉴权契约：`loginStudent(identifier, password, options)`

```typescript
interface LoginResult {
  success: boolean;
  message: string;
  user?: StudentProfile;
  sessionToken?: string;
}

function loginStudent(
  identifier: string, 
  password?: string, 
  remember: boolean = true
): LoginResult;
```

**响应码与逻辑规则**：
- 若输入匹配预设成员 ID（如 `50106070`, `吴宇轩`）：自动装载组长档案及 5 天连续打卡记录，返回 `success: true`。
- 若输入任意其他姓名/学号（如 `张同学`）：自动创建临时学生档案（首字符作为头像），返回 `success: true`。
- 若登录成功：自动同步左侧栏 `#current-user-name`, `#current-user-role`, `#current-user-avatar`。

---

## 2. 后端 OpenAPI 契约草案 (Optional Backend Endpoints)

当需要将学籍持久化到后端服务时，FastAPI 后端将暴露以下兼容端点：

### 2.1 `GET /api/auth/demo-users`
获取预设课题组成员列表供前端卡片渲染。

```json
{
  "status": "ok",
  "data": [
    {
      "id": "50106070",
      "name": "吴宇轩",
      "role": "Project Manager & Team Lead",
      "preferred_subject": "law",
      "avatar": "吴"
    },
    {
      "id": "50106038",
      "name": "林泳桐",
      "role": "Lead Business Analyst",
      "preferred_subject": "econ",
      "avatar": "林"
    }
  ]
}
```

### 2.2 `POST /api/auth/login`
验证学生学号并签发会话标识。

**Request Body**:
```json
{
  "student_id": "50106070",
  "password": "optional_password"
}
```

**Response 200 OK**:
```json
{
  "status": "ok",
  "session_token": "sess_50106070_20261008",
  "user": {
    "id": "50106070",
    "name": "吴宇轩",
    "role": "Project Manager & Team Lead",
    "preferred_subject": "law",
    "avatar": "吴",
    "streak_days": 5
  }
}
```
