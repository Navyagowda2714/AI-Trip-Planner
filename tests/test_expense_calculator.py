import pytest

from utils.expense_calculator import Calculator
from tools.expense_calculator_tool import CalculatorTool


def test_multiply():
    assert Calculator.multiply(120, 4) == 480


def test_calculate_total():
    assert Calculator.calculate_total(100.0, 250.5, 49.5) == pytest.approx(400.0)
    assert Calculator.calculate_total() == 0


def test_daily_budget():
    assert Calculator.calculate_daily_budget(1000, 4) == 250


def test_daily_budget_handles_zero_days():
    assert Calculator.calculate_daily_budget(1000, 0) == 0


def test_calculator_tools_are_exposed_to_the_agent():
    names = {t.name for t in CalculatorTool().calculator_tool_list}
    assert names == {"estimate_total_hotel_cost", "calculate_total_expense", "calculate_daily_expense_budget"}


def test_daily_expense_tool_invocation():
    tools = {t.name: t for t in CalculatorTool().calculator_tool_list}
    assert tools["calculate_daily_expense_budget"].invoke({"total_cost": 900, "days": 3}) == 300
