"""Python 代码执行工具

提供受限的 Python 表达式/代码执行能力，供 Agent 调用。
注意：这是教学级实现，不应该直接用于不可信生产环境。
"""

import ast
import io
import contextlib

from tools.registry import register_tool


@register_tool(
    name="python_executor",
    description="执行 Python 代码并返回输出结果，适用于数学计算、数据处理和代码验证。",
    parameters={
        "type": "object",
        "properties": {
            "code": {
                "type": "string",
                "description": "需要执行的 Python 代码",
            }
        },
        "required": ["code"],
    },
)
def python_executor(code: str) -> str:
    """执行 Python 代码并捕获标准输出。"""

    # 基础危险操作拦截
    blocked = [
        "import os",
        "import subprocess",
        "import sys",
        "__import__",
        "open(",
    ]

    for item in blocked:
        if item in code:
            return f"禁止执行危险操作: {item}"

    try:
        ast.parse(code)

        output = io.StringIO()
        with contextlib.redirect_stdout(output):
            exec(code, {"__builtins__": {}}, {})

        result = output.getvalue()
        return result if result else "执行完成，无输出"

    except Exception as e:
        return f"执行错误: {e}"
