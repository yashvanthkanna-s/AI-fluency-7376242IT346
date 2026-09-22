"""
Rule-Based Workflow - Follows predefined steps and conditions.
No LLM involved. Uses if/else logic to process expense data,
check budgets, and generate reports.
"""

import json
import os

DATA_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), "data")


def load_expenses():
    """Load expense data from the JSON file."""
    filepath = os.path.join(DATA_DIR, "expenses.json")
    with open(filepath, "r") as f:
        return json.load(f)


def load_budget():
    """Load budget configuration from the JSON file."""
    filepath = os.path.join(DATA_DIR, "budget.json")
    with open(filepath, "r") as f:
        return json.load(f)


# ---- Rule-based processing functions (all if/else, no LLM) ----

def calculate_category_totals(expenses):
    """Step 1: Add up spending per category."""
    totals = {}
    for expense in expenses:
        cat = expense["category"]
        totals[cat] = totals.get(cat, 0) + expense["amount"]
    return totals


def calculate_total_spending(expenses):
    """Step 2: Calculate total amount spent."""
    return sum(expense["amount"] for expense in expenses)


def check_budget_violations(category_totals, budget):
    """Step 3: Compare each category total against its budget limit."""
    violations = []
    within_budget = []

    for category, spent in category_totals.items():
        limit = budget["category_limits"].get(category, 0)
        if limit == 0:
            violations.append({
                "category": category,
                "spent": spent,
                "limit": limit,
                "status": "NO BUDGET SET"
            })
        elif spent > limit:
            violations.append({
                "category": category,
                "spent": spent,
                "limit": limit,
                "over_by": spent - limit,
                "status": "OVER BUDGET"
            })
        else:
            within_budget.append({
                "category": category,
                "spent": spent,
                "limit": limit,
                "remaining": limit - spent,
                "status": "OK"
            })

    return violations, within_budget


def find_top_expenses(expenses, n=5):
    """Step 4: Sort and pick the top N highest expenses."""
    sorted_expenses = sorted(expenses, key=lambda x: x["amount"], reverse=True)
    return sorted_expenses[:n]


def generate_alerts(total_spent, monthly_budget, violations):
    """Step 5: Generate warning alerts based on predefined rules."""
    alerts = []

    # Rule: If total spending exceeds monthly budget
    if total_spent > monthly_budget:
        alerts.append(
            f"ALERT: Total spending (Rs.{total_spent}) exceeds monthly budget (Rs.{monthly_budget}) "
            f"by Rs.{total_spent - monthly_budget}!"
        )

    # Rule: If total spending is more than 80% of budget
    elif total_spent > monthly_budget * 0.8:
        alerts.append(
            f"WARNING: You've used {(total_spent/monthly_budget)*100:.1f}% of your monthly budget."
        )

    # Rule: Per-category violations
    for v in violations:
        if v["status"] == "OVER BUDGET":
            alerts.append(
                f"ALERT: {v['category']} spending (Rs.{v['spent']}) is over budget "
                f"(limit: Rs.{v['limit']}) by Rs.{v['over_by']}!"
            )

    if not alerts:
        alerts.append("All good! Your spending is within budget limits.")

    return alerts


def generate_report(user_query):
    """
    Main workflow - runs all steps in a fixed order.
    The user_query is matched against predefined keywords to decide what to show.
    """
    expenses = load_expenses()
    budget = load_budget()

    query_lower = user_query.lower()

    print("\n" + "=" * 55)
    print("  RULE-BASED WORKFLOW - Processing your request")
    print("=" * 55)

    # Step 1: Always calculate totals
    category_totals = calculate_category_totals(expenses)
    total_spent = calculate_total_spending(expenses)

    # Route based on keywords (if/else, no AI)
    if "summary" in query_lower or "overview" in query_lower or "report" in query_lower:
        print(f"\n--- Monthly Expense Summary ---")
        print(f"Total Spent: Rs.{total_spent}")
        print(f"Monthly Budget: Rs.{budget['monthly_budget']}")
        print(f"Remaining: Rs.{budget['monthly_budget'] - total_spent}")
        print(f"\nCategory Breakdown:")
        for cat, amount in sorted(category_totals.items(), key=lambda x: x[1], reverse=True):
            limit = budget["category_limits"].get(cat, "N/A")
            print(f"  {cat:15s} -> Rs.{amount:>6}  (limit: Rs.{limit})")

    elif "budget" in query_lower or "over" in query_lower or "limit" in query_lower:
        violations, within = check_budget_violations(category_totals, budget)
        alerts = generate_alerts(total_spent, budget["monthly_budget"], violations)
        print(f"\n--- Budget Check ---")
        for alert in alerts:
            print(f"  >> {alert}")
        if within:
            print(f"\nCategories within budget:")
            for w in within:
                print(f"  {w['category']:15s} -> Rs.{w['spent']:>6} of Rs.{w['limit']} (Rs.{w['remaining']} left)")

    elif "top" in query_lower or "highest" in query_lower or "expensive" in query_lower:
        top = find_top_expenses(expenses)
        print(f"\n--- Top 5 Highest Expenses ---")
        for i, exp in enumerate(top, 1):
            print(f"  {i}. Rs.{exp['amount']:>6} - {exp['description']} ({exp['date']})")

    elif "food" in query_lower or "transport" in query_lower or "shopping" in query_lower:
        # Filter by mentioned category
        for cat_name in ["Food", "Transport", "Shopping", "Entertainment", "Education", "Utilities"]:
            if cat_name.lower() in query_lower:
                cat_expenses = [e for e in expenses if e["category"] == cat_name]
                cat_total = sum(e["amount"] for e in cat_expenses)
                limit = budget["category_limits"].get(cat_name, "N/A")
                print(f"\n--- {cat_name} Expenses ---")
                print(f"Total: Rs.{cat_total} (limit: Rs.{limit})")
                for exp in cat_expenses:
                    print(f"  {exp['date']} - {exp['description']:30s} Rs.{exp['amount']}")
                break

    else:
        # Default: show everything
        print(f"\n[No matching rule for your query. Showing full summary.]")
        print(f"\nTotal Spent: Rs.{total_spent} / Rs.{budget['monthly_budget']}")
        print(f"\nCategory Totals:")
        for cat, amount in sorted(category_totals.items(), key=lambda x: x[1], reverse=True):
            print(f"  {cat:15s} -> Rs.{amount}")

    print()


def main():
    print("=" * 60)
    print("  RULE-BASED WORKFLOW - Expense Analyzer")
    print("  (Predefined rules, no LLM, reads your private data)")
    print("=" * 60)
    print("\nAvailable commands: summary, budget check, top expenses,")
    print("food expenses, transport expenses, shopping expenses")
    print("Type 'quit' to exit.\n")

    while True:
        user_input = input("You: ").strip()
        if user_input.lower() in ("quit", "exit"):
            print("Goodbye!")
            break
        if not user_input:
            continue

        generate_report(user_input)


if __name__ == "__main__":
    main()
