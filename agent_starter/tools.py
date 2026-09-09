import ast
import operator
from datetime import datetime
from zoneinfo import ZoneInfo


_BINARY_OPERATORS = {
    ast.Add: operator.add,
    ast.Sub: operator.sub,
    ast.Mult: operator.mul,
    ast.Div: operator.truediv,
    ast.FloorDiv: operator.floordiv,
    ast.Mod: operator.mod,
    ast.Pow: operator.pow,
}

_UNARY_OPERATORS = {
    ast.UAdd: operator.pos,
    ast.USub: operator.neg,
}


def _eval_node(node: ast.AST) -> float | int:
    if isinstance(node, ast.Constant) and isinstance(node.value, (int, float)):
        return node.value

    if isinstance(node, ast.BinOp) and type(node.op) in _BINARY_OPERATORS:
        left = _eval_node(node.left)
        right = _eval_node(node.right)

        if isinstance(node.op, ast.Pow) and abs(right) > 12:
            raise ValueError("Exponent is too large")

        return _BINARY_OPERATORS[type(node.op)](left, right)

    if isinstance(node, ast.UnaryOp) and type(node.op) in _UNARY_OPERATORS:
        return _UNARY_OPERATORS[type(node.op)](_eval_node(node.operand))

    raise ValueError("Unsupported expression")


def calculator(expression: str) -> str:
    """Safely evaluate a basic arithmetic expression."""
    tree = ast.parse(expression, mode="eval")
    result = _eval_node(tree.body)
    return str(result)


def get_current_time(timezone: str = "Asia/Shanghai") -> str:
    """Return the current time in an IANA timezone."""
    now = datetime.now(ZoneInfo(timezone))
    return now.isoformat(timespec="seconds")


TOOL_SCHEMAS = [
    {
        "type": "function",
        "function": {
            "name": "calculator",
            "description": "Calculate a basic arithmetic expression exactly. Use this instead of doing arithmetic mentally.",
            "parameters": {
                "type": "object",
                "properties": {
                    "expression": {
                        "type": "string",
                        "description": "Arithmetic expression such as (18 * 7 + 5) / 2",
                    }
                },
                "required": ["expression"],
                "additionalProperties": False,
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "get_current_time",
            "description": "Get the current local time for a requested IANA timezone.",
            "parameters": {
                "type": "object",
                "properties": {
                    "timezone": {
                        "type": "string",
                        "description": "IANA timezone, for example Asia/Shanghai or America/Los_Angeles",
                        "default": "Asia/Shanghai",
                    }
                },
                "additionalProperties": False,
            },
        },
    },
]


TOOL_FUNCTIONS = {
    "calculator": calculator,
    "get_current_time": get_current_time,
}
