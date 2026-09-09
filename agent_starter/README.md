# Agent Starter

一个最小但完整的 **Tool Calling Agent** 项目。

它不是固定工作流。每一轮都由模型决定：

1. 直接回答；或
2. 调用一个/多个工具；
3. 读取工具返回结果；
4. 再继续判断，直到给出最终答案。

## 项目结构

```text
agent_starter/
├── .env.example
├── README.md
├── agent.py          # Agent 循环：LLM -> Tool -> Observation -> LLM
├── config.py         # 环境变量配置
├── main.py           # 命令行入口
├── requirements.txt
├── requirements-dev.txt
├── tools.py          # 工具定义、Schema、真实 Python 函数
└── tests/
    └── test_tools.py
```

## 1. 创建虚拟环境

Windows PowerShell：

```powershell
cd agent_starter
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

## 2. 安装依赖

```powershell
pip install -r requirements.txt
```

如果还要运行测试：

```powershell
pip install -r requirements-dev.txt
```

## 3. 配置模型

复制：

```powershell
Copy-Item .env.example .env
```

然后填写自己的 API Key：

```env
LLM_API_KEY=your_api_key_here
LLM_BASE_URL=https://api.deepseek.com
LLM_MODEL=deepseek-chat
LLM_TEMPERATURE=0.2
AGENT_MAX_STEPS=8
```

这里使用 OpenAI Python SDK 连接 OpenAI-compatible 接口，因此也可以替换为其他兼容服务，只需要修改环境变量。

## 4. 启动

```powershell
python main.py
```

例如输入：

```text
帮我计算 (18 * 7 + 5) / 2，并告诉我上海现在几点。
```

模型会先决定调用 `calculator` 和 `get_current_time`，拿到真实工具结果后，再组织最终答案。

## 5. Agent 核心流程

```text
User
  |
  v
LLM
  |
  |-- 不需要工具 --------------------> Final Answer
  |
  |-- tool_call
          |
          v
       Python Tool
          |
          v
      Observation
          |
          +---------------------------> LLM
```

真正让它成为 Agent 的关键不是 `if/else`，而是：**下一步动作由模型根据当前上下文动态选择，并且工具执行结果会重新进入下一轮决策。**

## 6. 如何新增一个工具

以 `tools.py` 为例，需要同时做两件事：

### A. 写真实 Python 函数

```python
def search_weather(city: str) -> str:
    ...
```

### B. 给模型一个 Tool Schema

```python
{
    "type": "function",
    "function": {
        "name": "search_weather",
        "description": "查询城市天气",
        "parameters": {
            "type": "object",
            "properties": {
                "city": {"type": "string"}
            },
            "required": ["city"]
        }
    }
}
```

最后把函数注册到 `TOOL_FUNCTIONS`：

```python
TOOL_FUNCTIONS = {
    "calculator": calculator,
    "get_current_time": get_current_time,
    "search_weather": search_weather,
}
```

## 7. 测试

```powershell
pytest -q
```

测试重点先放在真实工具层，因为 Agent 的 LLM 输出天然具有一定随机性；之后可以再增加 mock LLM、集成测试和端到端测试。
