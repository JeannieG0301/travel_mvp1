# travel_mvp1 上线部署说明

> 将 Web 应用部署到公网，生成可分享 URL。

---

## 开发团队执行部署（前置条件与步骤）

**说明**：Render / Railway 部署需在平台 Web 界面完成，无法通过纯命令行执行。开发团队需完成以下步骤。

### 前置条件（必须先完成）

1. **初始化 Git 并推送到 GitHub**：
   ```bash
   cd travel_mvp1
   git init
   git add .
   git commit -m "Initial commit"
   # 在 GitHub 创建 travel_mvp1 仓库后：
   git remote add origin https://github.com/你的用户名/travel_mvp1.git
   git branch -M main
   git push -u origin main
   ```

2. **获取 DeepSeek API Key**：在 [DeepSeek 开放平台](https://platform.deepseek.com/) 创建并复制。

### 执行部署（以 Render 为例）

1. 注册/登录 [Render](https://render.com)（可用 GitHub 登录）
2. **New → Web Service**，选择 GitHub 中的 `travel_mvp1` 仓库
3. 填写配置（见下方「Render 配置速查表」）
4. 在 **Environment** 添加 `DEEPSEEK_API_KEY`（由项目负责人提供或自行添加）
5. 点击 **Create Web Service**，等待构建完成
6. 复制生成的 URL（如 `https://travel-mvp1-xxx.onrender.com`），汇报给项目经理 tom

### Render 配置速查表

| 配置项 | 值 |
|--------|-----|
| Name | travel-mvp1 |
| Region | Singapore |
| Runtime | Python |
| Build Command | `pip install -r requirements.txt` |
| Start Command | `uvicorn backend.app:app --host 0.0.0.0 --port $PORT` |

---

## 一、部署平台选择

推荐使用 **Render** 或 **Railway**，二者均支持 Python、提供免费额度、自动注入 `PORT`。

| 平台    | 免费额度 | 国内访问 | 说明                   |
|---------|----------|----------|------------------------|
| Render  | 有       | 一般     | 配置简单，支持 render.yaml |
| Railway | 有（有限）| 一般     | 部署快，支持 Procfile  |
| Fly.io  | 有       | 一般     | 需配置 fly.toml        |

本文以 **Render** 为例说明，Railway 步骤类似。

---

## 二、部署前准备

1. **代码推送到 GitHub**（若尚未推送）：
   ```bash
   git init
   git add .
   git commit -m "Initial commit"
   git remote add origin https://github.com/你的用户名/travel_mvp1.git
   git push -u origin main
   ```

2. **获取 DeepSeek API Key**：在 [DeepSeek 开放平台](https://platform.deepseek.com/) 创建并复制。

---

## 三、Render 部署步骤

1. 登录 [Render](https://render.com)，点击 **New → Web Service**。

2. **连接仓库**：选择 GitHub 中的 `travel_mvp1` 仓库。

3. **配置构建与启动**：
   | 配置项      | 值                                                         |
   |-------------|------------------------------------------------------------|
   | Name        | travel-mvp1（或其他名称）                                  |
   | Region      | Singapore（可选，离国内较近）                               |
   | Runtime     | Python                                                     |
   | Build Command | `pip install -r requirements.txt`                       |
   | Start Command | `uvicorn backend.app:app --host 0.0.0.0 --port $PORT`   |

4. **环境变量**：
   | Key             | Value              |
   |-----------------|--------------------|
   | DEEPSEEK_API_KEY | （你的 API Key）  |

   在 Dashboard → Environment 中添加，**不要**提交到代码仓库。

5. 点击 **Create Web Service**，等待构建与部署完成。

6. 部署成功后，Render 会提供 URL，如：`https://travel-mvp1-xxx.onrender.com`

---

## 四、Railway 部署步骤（备选）

1. 登录 [Railway](https://railway.app)，点击 **New Project**。

2. 选择 **Deploy from GitHub repo**，选择 `travel_mvp1`。

3. Railway 会自动识别 `Procfile`，使用：
   ```
   web: uvicorn backend.app:app --host 0.0.0.0 --port $PORT
   ```

4. 在项目 **Variables** 中添加：
   | Key             | Value              |
   |-----------------|--------------------|
   | DEEPSEEK_API_KEY | （你的 API Key）  |

5. 点击 **Generate Domain** 生成公网 URL。

---

## 五、环境变量说明

| 变量名            | 必填 | 说明                                      |
|-------------------|------|-------------------------------------------|
| DEEPSEEK_API_KEY  | 是   | DeepSeek API 密钥，用于调用 LLM 生成行程  |
| PORT              | 否   | 由平台自动注入，无需手动配置               |

---

## 六、访问方式

部署成功后，使用平台提供的 URL 访问，例如：

- **Render**：`https://你的服务名.onrender.com`
- **Railway**：`https://你的项目.up.railway.app`

打开后为单页 Web 应用：表单填写 → 生成行程 → 查看结果。API 与前端同源，无需跨域配置。

---

## 七、本地验证

部署前可在本地模拟生产环境：

```bash
PORT=8000 uvicorn backend.app:app --host 0.0.0.0 --port $PORT
```

---

## 八、故障排查

| 现象         | 可能原因               | 处理                         |
|--------------|------------------------|------------------------------|
| 502 Bad Gateway | 启动命令或端口错误 | 确认 Start Command 使用 `$PORT` |
| 生成失败     | API Key 未配置或无效   | 检查 DEEPSEEK_API_KEY        |
| 构建失败     | 依赖安装失败           | 检查 requirements.txt、Python 版本 |

---

## 九、部署完成后

- 将公网 URL 告知项目经理 tom，用于更新 BACKLOG #12
- 在 BACKLOG 或项目文档中记录部署 URL 及部署日期

---

## 十、部署执行状态说明

| 环节 | 执行方 | 说明 |
|------|--------|------|
| Git 推送到 GitHub | 开发团队 | 本地执行 `git init`、`git push` |
| 创建 Render/Railway 账号 | 开发团队 | 在平台官网注册（可用 GitHub 登录） |
| 创建 Web Service、配置环境变量 | 开发团队 | 在平台 Dashboard 完成 |
| 获取公网 URL | 平台自动生成 | 部署成功后展示 |
| 汇报 URL 给项目经理 | 开发团队 | 将 URL 提供给 tom，更新 BACKLOG #12 |
