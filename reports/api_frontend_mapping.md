# 前端-后端接口字段映射对照表

## 说明
对照现有 `frontend/app.js` 与 `frontend/index.html` 梳理前端发起的请求入参与期望接收的出参字段，防止后续联调报错。

## 已实现接口清单
| 视图/模块 | 前端触发动作 | 调用的后端 URL | 请求方法 | 关键请求字段 (Request Body) | 期望返回字段 |
| :---: | :--- | :--- | :---: | :--- | :--- |
| **全局初始化** | 应用启动时预加载全量题目数据 | `/api/questions` | `GET` | 无 | `[{id, stem, options, subject}]` 题目对象数组 |
| **全局初始化** | 应用启动时预加载考点数据集资源 | `/api/datasets` | `GET` | 无 | `[{id, name, concept_list, subject}]` 知识点/数据集数组 |
| **全局初始化** | 应用启动时探测服务健康与运行模式 | `/api/health` | `GET` | 无 | `{ mode: "online" \| "local" }` 服务运行模式标识 |
| **专项刷题** | 提交所选答案并获取判分与解析 | `/api/answer` | `POST` | `{question_id, selected}` | `{correct_key, correct, dimensions, misconception, explanation}` 答题结果与解析 |
| **导师对话** | 向导师发送提问并获取回复 | `/api/tutor` | `POST` | `{question_id, message}` | `{reply, mode}` 导师回复内容与来源模式 |
