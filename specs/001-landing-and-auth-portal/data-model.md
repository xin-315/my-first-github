# 数据模型设计规约 (Phase 1: Data Model)

**功能编号**：`001-landing-and-auth-portal`  
**关联规格**：`specs/001-landing-and-auth-portal/spec.md`  
**完成时间**：2026-10-08  

---

## 1. 核心实体模型 (Core Entities)

### 1.1 学生档案与身份实体 (StudentProfile)
描述使用智学罗盘的在校学生或课题组成员身份信息。

```typescript
interface StudentProfile {
  /** 唯一学号或虚拟标识 (例如: "50106070", "50106038", "guest_01") */
  id: string;
  
  /** 学生真实姓名或昵称 (例如: "吴宇轩", "林泳桐", "访客学生") */
  name: string;
  
  /** 课程内角色或专业身份 (例如: "Team Lead & PM", "Lead BA", "BSc BMIS") */
  role: string;
  
  /** 头像简称字符 (例如: "吴", "林", "客") */
  avatarText: string;
  
  /** 主修或优先进入研习学科 ("law" | "cs" | "econ" | "se") */
  preferredSubject: 'law' | 'cs' | 'econ' | 'se';
  
  /** 连续学习打卡天数 (用于控制台 Streak 激励) */
  streakDays: number;
  
  /** 是否为预设演示账号 */
  isDemoAccount: boolean;
}
```

### 1.2 会话状态实体 (AuthSession)
存储在客户端 `localStorage` (`smartstudy_auth_session`) 中的当前登录会话。

```typescript
interface AuthSession {
  /** 会话临时鉴权令牌 */
  sessionToken: string;
  
  /** 关联的学生档案主体 */
  user: StudentProfile;
  
  /** 登录时间戳 (ISO 8601) */
  loginTime: string;
  
  /** 记住登录状态标志位 */
  rememberMe: boolean;
}
```

### 1.3 门户导航与视图状态 (PortalViewState)
控制首页产品落地页与核心控制台之间的流转与记忆。

```typescript
interface PortalViewState {
  /** 当前主激活视窗: 'portal' (产品介绍页) | 'workspace' (刷题控制台) */
  activeRootView: 'portal' | 'workspace';
  
  /** 快捷直达控制台的目标 Tab: 'quiz' | 'tutor' | 'graph' | 'report' */
  targetWorkspaceTab: 'quiz' | 'tutor' | 'graph' | 'report';
  
  /** 是否自动跳过介绍页 (根据用户设置) */
  skipPortalOnLaunch: boolean;
}
```

---

## 2. 预设课题组演示数据集 (Pre-seeded Demo Accounts)

系统预置以下符合阿伯丁大学 JC2001 Group 5 实名学籍的演示用户：

| 学号 (ID) | 姓名 (Name) | 团队分工与专业角色 (Role) | 优先研习学科 | 头像 | 演示密码 |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **50106070** | **吴宇轩** | **Project Manager & Team Lead** | ⚖️ 民商法学 (`law`) | 吴 | `123456` |
| **50106038** | **林泳桐** | **Lead Business Analyst (需求组)** | 📈 计量经济 (`econ`) | 林 | `123456` |
| **50106045** | **王思鉴** | **System Architect (架构组)** | 💻 计算机体系 (`cs`) | 王 | `123456` |
| **50106065** | **江昊** | **PoC Lead Developer (开发组)** | ⚙️ 软件工程 (`se`) | 江 | `123456` |
| **50106034** | **谢炜昕** | **QA & Technical Report Lead (质保组)** | ⚖️ 民商法学 (`law`) | 谢 | `123456` |
| **guest** | **访客体验生** | **Guest Learner (全权限速通体验)** | ⚙️ 软件工程 (`se`) | 客 | *(免密)* |

---

## 3. 状态校验与边界规则 (Validation Rules)

1. **学号格式规则**：支持 8 位阿伯丁标准学号（以 `501` 开头）或 2-10 字符汉字/英文姓名。
2. **密码兼容性**：预设账号密码均统一为 `123456`；访客账号免密一键登入；自建测试账号不设强密码校验限制。
3. **退登与数据自洁**：登出操作清除 `smartstudy_auth_session`，但保留用户的刷题雷达进度在本地快照中。
