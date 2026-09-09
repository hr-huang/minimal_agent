import sys
from pathlib import Path

PROJECT_DIR = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(PROJECT_DIR))

from tools import calculator, get_current_time


def test_calculator() -> None:
    assert calculator("(18 * 7 + 5) / 2") == "65.5"


def test_calculator_rejects_code() -> None:
    try:
        calculator("__import__('os').system('echo unsafe')")
    except ValueError:
        pass
    else:
        raise AssertionError("calculator should reject function calls")


def test_get_current_time() -> None:
    result = get_current_time("Asia/Shanghai")
    assert "+08:00" in result
