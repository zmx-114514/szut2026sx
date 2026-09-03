# ai-tool

苏州工学院 2026 级 25 届暑期实训团队作业 — AI 智能助手项目。

## 项目功能

本项目包含四个 Streamlit 应用：

### 1. AI 厨房助手 (`main.py`)
- 上传食材照片，AI 识别食材并推荐食谱
- 支持图片上传与流式对话
- 基于 LangChain + LangGraph 构建的 Agent

### 2. 智能万年历 (`calendar_app.py`)
- 农历/节气/节日/星座查询
- 实时天气查询（基于 wttr.in API）
- AI 日历助手问答（支持 OpenAI 兼容 API）

### 3. AI 伴侣 (`companion_app.py`)
- 五种人设随心切换：贴心伴侣、幽默段子手、深夜树洞、学习搭子、职场导师
- 流式对话，回复自然有温度
- 倾听与陪伴，提供情感支持（侧边栏可调回复风格、一键清空记录）

### 4. 看图搜索 Agent (`vision_app.py`)
- 上传图片或输入图片 URL，视觉模型识别图片内容
- Agent 自动调用联网搜索工具补充最新知识
- 工具调用过程实时可视化（st.status 展示思考链路）

## 项目结构

```
ai_tool/
├── app.py               # 主入口（st.navigation 动态导航 + 页面异步加载）
├── main.py              # AI 厨房助手应用逻辑（侧边栏含其他应用入口）
├── calendar_app.py      # 智能万年历 Streamlit 应用
├── companion_app.py     # AI 伴侣 Streamlit 应用
├── vision_app.py        # 看图搜索 Agent Streamlit 应用
├── image_agent.py       # 看图+联网搜索 Agent 定义
├── image_recognition.py # 视觉模型图片识别
├── models/              # 模型别名（qwen3/dsv3/dsv4f，每个模型一个文件）
├── test.py              # Agent 工具链测试
├── utils/
│   ├── __init__.py
│   ├── agent.py         # LangGraph Agent 定义（懒加载 + 双检锁）
│   ├── model.py         # 聊天模型初始化（懒加载 + 双检锁）
│   ├── vl_model.py      # 视觉模型初始化
│   ├── tools.py         # 工具集合（日期、天气、搜索、识图）
│   ├── send_msg.py      # 流式消息发送
│   ├── prewarm.py       # 进程级后台预热管理
│   ├── pageref.py       # 页面引用注册表（st.switch_page 跳转）
│   └── upload.py        # 图片上传服务
├── .env                 # 环境变量（不提交）
├── pyproject.toml
├── uv.lock
└── README.md
```

## 快速开始

```bash
# 安装依赖
uv sync

# 运行主页（推荐，左侧侧边栏导航各应用）
uv run streamlit run app.py

# 或直接运行单个应用（独立窗口）
uv run streamlit run main.py            # AI 厨房助手
uv run streamlit run calendar_app.py    # 智能万年历
uv run streamlit run companion_app.py   # AI 伴侣
uv run streamlit run vision_app.py      # 看图搜索 Agent
```

> 采用 `st.navigation` 动态导航，`app.py` 为唯一入口；重型模块由 `utils/prewarm.py` 后台异步导入，页面先渲染、就绪后自动呈现。

## 环境变量

在 `.env` 文件中配置以下变量：

| 变量名 | 说明 |
|--------|------|
| `OPENAI_API_KEY` | OpenAI 兼容 API 密钥 |
| `OPENAI_API_BASE` | API 基础地址 |
| `TAVILY_API_KEY` | Tavily 搜索 API 密钥 |
| `BEEIMG_API_BASE` | 图床 API 地址 |
| `BEEIMG_STORAGE_ID` | 图床存储 ID |
| `BEEIMG_TOKEN` | 图床访问令牌 |
| `VL_API_KEY` | 视觉模型 API 密钥 |
| `VL_BASE_URL` | 视觉模型 API 地址 |
| `VL_MODEL_NAME` | 视觉模型名称 |
