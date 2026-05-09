# RAG Retrieval Agent

企业级 Retrieval Agent（RAG 检索 Agent）示例。

## 功能

- 内部规范检索
- 历史 PR 检索
- 架构文档检索
- OpenAI Embedding
- ChromaDB 向量库
- FastAPI HTTP 服务
- GitHub 可直接托管运行

---

## 启动方式

### 1. 安装依赖

```bash
pip install -r requirements.txt
```

### 2. 配置环境变量

```bash
cp .env.example .env
```

编辑 `.env`

```bash
OPENAI_API_KEY=sk-xxxx
```

### 3. 构建向量数据库

```bash
python ingest.py
```

### 4. 启动 API 服务

```bash
uvicorn app:app --reload
```

### 5. 调用接口

```bash
curl -X POST http://127.0.0.1:8000/ask \
  -H "Content-Type: application/json" \
  -d '{"query":"如何优化订单查询接口性能？"}'
```

---

## GitHub 部署

上传整个项目到 GitHub 即可。

支持：

- Railway
- Render
- Fly.io
- ECS
- Docker
- Kubernetes

---

## API 文档

启动后访问：

http://127.0.0.1:8000/docs
