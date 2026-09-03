# ai-tool

苏州工学院 2026 级 25 届暑期实训团队作业 — AI 智能助手项目。

## 项目功能

本项目包含三个 Streamlit 应用：

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

## 项目结构

```
ai_tool/
├── app.py               # 统一入口（侧边栏切换三个应用）
├── main.py              # AI 厨房助手 Streamlit 应用
├── calendar_app.py      # 智能万年历 Streamlit 应用
├── companion_app.py     # AI 伴侣 Streamlit 应用
├── test.py              # Agent 工具链测试
├── utils/
│   ├── __init__.py
│   ├── agent.py         # LangGraph Agent 定义
│   ├── model.py         # 聊天模型初始化
│   ├── tools.py         # 工具集合（日期、天气、搜索）
│   ├── send_msg.py      # 流式消息发送
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

# 运行统一入口（推荐）
uv run streamlit run app.py

# 或单独运行各应用
uv run streamlit run main.py            # AI 厨房助手
uv run streamlit run calendar_app.py    # 智能万年历
uv run streamlit run companion_app.py   # AI 伴侣
```

> 统一入口 `app.py` 通过左侧侧边栏在三个应用间切换。

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
