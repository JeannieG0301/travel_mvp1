# travel_mvp1 - 新西兰自驾行程规划

基于 LLM 的行程规划应用，MVP1 支持新西兰自驾。

## 快速启动

### 1. 安装依赖

```bash
pip install -r requirements.txt
```

### 2. 配置环境变量

在项目根目录创建 `.env` 文件，设置：

```
DEEPSEEK_API_KEY=your_api_key
```

### 3. 启动 Web 服务（API + 前端）

```bash
# 在项目根目录执行
uvicorn backend.app:app --reload --host 0.0.0.0 --port 8000
```

浏览器打开 http://localhost:8000 即可使用。

### 4. CLI 入口（可选）

```bash
python main.py -l 奥克兰 -r 南岛 -m 3 -d 7 -t 2
```

## 前后端分离开发（可选）

- **后端**：`uvicorn backend.app:app --port 8000`
- **前端**：用任意静态服务器托管 `frontend/`，如 `npx serve frontend -p 3000`
- 在 `frontend/index.html` 中（或通过 `<script>` 设置 `window.API_BASE = 'http://localhost:8000'`）配置 API 地址

后端已配置 CORS，支持跨域请求。
