"""
Tools for the expense tracking agent.
Structured the same way as the lab's tools.py — each tool is a function,
with JSON Schema descriptions for the LLM to read.
"""

import json
import os
import ast
import operator

DATA_DIR = os.path.join(os.path.dirname(__file__), "data")


# ===================== TOOL FUNCTIONS =====================

def read_expenses() -> str:
    """Read all expenses from the user's private data file."""
    filepath = os.path.join(DATA_DIR, "expenses.json")
    with open(filepath, "r") as f:
        expenses = json.load(f)
    return json.dumps(expenses, indent=2)


def read_budget() -> str:
    """Read the budget configuration."""
    filepath = os.path.join(DATA_DIR, "budget.json")
    with open(filepath, "r") as f:
        budget = json.load(f)
    return json.dumps(budget, indent=2)


def _load_expenses_data(expenses_json=None):
    if expenses_json:
        try:
            return json.loads(expenses_json)
        except Exception:
            pass
    filepath = os.path.join(DATA_DIR, "expenses.json")
    with open(filepath, "r", encoding="utf-8") as f:
        return json.load(f)


def _load_budget_data(budget_json=None):
    if budget_json:
        try:
            return json.loads(budget_json)
        except Exception:
            pass
    filepath = os.path.join(DATA_DIR, "budget.json")
    with open(filepath, "r", encoding="utf-8") as f:
        return json.load(f)


def calculate_totals(expenses_json: str = None) -> str:
    """Calculate total spending and per-category totals from expense data."""
    expenses = _load_expenses_data(expenses_json)
    category_totals = {}
    total = 0
    for exp in expenses:
        cat = exp["category"]
        category_totals[cat] = category_totals.get(cat, 0) + exp["amount"]
        total += exp["amount"]
    return json.dumps({"total_spent": total, "category_totals": category_totals}, indent=2)


def check_budget(totals_json: str = None, budget_json: str = None) -> str:
    """Compare spending totals against budget limits and find violations."""
    budget = _load_budget_data(budget_json)
    if totals_json:
        try:
            totals = json.loads(totals_json)
        except Exception:
            totals = json.loads(calculate_totals())
    else:
        totals = json.loads(calculate_totals())

    results = {
        "total_spent": totals["total_spent"],
        "monthly_budget": budget["monthly_budget"],
        "over_total": totals["total_spent"] > budget["monthly_budget"],
        "categories": []
    }
    for cat, spent in totals["category_totals"].items():
        limit = budget["category_limits"].get(cat, 0)
        results["categories"].append({
            "category": cat, "spent": spent, "limit": limit,
            "over": spent > limit, "difference": spent - limit
        })
    return json.dumps(results, indent=2)


def filter_expenses(category: str = "", expenses_json: str = None) -> str:
    """Filter expenses by a specific category."""
    expenses = _load_expenses_data(expenses_json)
    if category:
        filtered = [e for e in expenses if e.get("category", "").lower() == category.lower()]
    else:
        filtered = expenses
    return json.dumps(filtered, indent=2)


def get_top_expenses(n: int = 5, expenses_json: str = None) -> str:
    """Get the top N most expensive items."""
    expenses = _load_expenses_data(expenses_json)
    try:
        n = int(n)
    except Exception:
        n = 5
    sorted_exp = sorted(expenses, key=lambda x: x.get("amount", 0), reverse=True)
    return json.dumps(sorted_exp[:n], indent=2)


# Safe calculator (same pattern as lab's tools.py - never use eval)
_OPS = {ast.Add: operator.add, ast.Sub: operator.sub,
        ast.Mult: operator.mul, ast.Div: operator.truediv, ast.USub: operator.neg}

def _evaluate(node):
    if isinstance(node, ast.Constant) and isinstance(node.value, (int, float)):
        return node.value
    if isinstance(node, ast.BinOp) and type(node.op) in _OPS:
        return _OPS[type(node.op)](_evaluate(node.left), _evaluate(node.right))
    if isinstance(node, ast.UnaryOp) and type(node.op) in _OPS:
        return _OPS[type(node.op)](_evaluate(node.operand))
    raise ValueError("Unsupported expression")

def calculator(expression: str) -> str:
    """Evaluate a basic arithmetic expression safely."""
    try:
        return str(_evaluate(ast.parse(expression, mode="eval").body))
    except Exception as error:
        return f"Calculator error: {error}"


# Map tool names to functions (same pattern as lab)
TOOL_FUNCTIONS = {
    "read_expenses": read_expenses,
    "read_budget": read_budget,
    "calculate_totals": calculate_totals,
    "check_budget": check_budget,
    "filter_expenses": filter_expenses,
    "get_top_expenses": get_top_expenses,
    "calculator": calculator,
}

# JSON Schema descriptions for the LLM (same format as lab's tools.py)
TOOLS = [
    {"type": "function", "function": {
        "name": "read_expenses",
        "description": "Read all expense records from the user's private expense data file.",
        "parameters": {"type": "object", "properties": {}, "required": []}}},
    {"type": "function", "function": {
        "name": "read_budget",
        "description": "Read the user's budget configuration with monthly budget and per-category limits.",
        "parameters": {"type": "object", "properties": {}, "required": []}}},
    {"type": "function", "function": {
        "name": "calculate_totals",
        "description": "Calculate total spending and per-category totals from the private expense data.",
        "parameters": {"type": "object",
                        "properties": {},
                        "required": []}}},
    {"type": "function", "function": {
        "name": "check_budget",
        "description": "Compare spending totals against budget limits. Identifies over-budget categories and differences.",
        "parameters": {"type": "object",
                        "properties": {},
                        "required": []}}},
    {"type": "function", "function": {
        "name": "filter_expenses",
        "description": "Filter expenses to show only a specific category (e.g. Food, Transport, Shopping).",
        "parameters": {"type": "object",
                        "properties": {"category": {"type": "string", "description": "Category name to filter by"}},
                        "required": ["category"]}}},
    {"type": "function", "function": {
        "name": "get_top_expenses",
        "description": "Get the top N most expensive purchases.",
        "parameters": {"type": "object",
                        "properties": {"n": {"type": "integer", "description": "Number of top expenses to return (e.g. 3 or 5)"}},
                        "required": []}}},
    {"type": "function", "function": {
        "name": "calculator",
        "description": "Evaluate an arithmetic expression using + - * / and brackets.",
        "parameters": {"type": "object",
                        "properties": {"expression": {"type": "string"}},
                        "required": ["expression"]}}},
]


if __name__ == "__main__":
    print("read_expenses()  -> loaded", len(json.loads(read_expenses())), "records")
    print("read_budget()    ->", read_budget())
    print("calculator('3930 - 3000') ->", calculator("3930 - 3000"))
