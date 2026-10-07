import pandas as pd


ESSENTIAL_CATEGORIES = {"Education", "Food", "Transport", "Health", "Rent"}
OPTIONAL_CATEGORIES = {"Shopping", "Entertainment", "Gaming", "Eating Out", "Other"}


def build_financial_advice(expenses, monthly_budget, monthly_income):
    tips = []

    total = float(expenses["amount"].sum()) if not expenses.empty else 0.0
    remaining = monthly_budget - total
    usage = (total / monthly_budget * 100) if monthly_budget > 0 else 0

    if total == 0:
        tips.append(
            "Start by recording every expense for at least one week. "
            "Small purchases are often the easiest spending leaks to miss."
        )
        return tips

    if usage >= 100:
        tips.append(
            "Your spending has reached or exceeded your monthly budget. "
            "Pause non-essential purchases and review the largest spending categories first."
        )
    elif usage >= 85:
        tips.append(
            "You have already used more than 85% of your budget. "
            "Keep the remaining spending focused on essential needs."
        )
    elif usage >= 65:
        tips.append(
            "Your budget is being used quickly. Check whether this spending pace is sustainable "
            "for the number of days left in the month."
        )
    else:
        tips.append(
            "Your overall spending is currently within a comfortable portion of the monthly budget."
        )

    by_category = (
        expenses.groupby("category")["amount"]
        .sum()
        .sort_values(ascending=False)
    )

    if not by_category.empty:
        top_category = by_category.index[0]
        top_amount = float(by_category.iloc[0])
        top_share = (top_amount / total * 100) if total > 0 else 0

        tips.append(
            f"Your largest spending category is {top_category}, accounting for "
            f"{top_share:.1f}% of your recorded expenses."
        )

        optional_total = sum(
            float(amount)
            for category, amount in by_category.items()
            if category in OPTIONAL_CATEGORIES
        )

        if optional_total / total >= 0.35:
            tips.append(
                "A large share of your spending is in optional categories. "
                "Try setting a weekly limit for entertainment, shopping, eating out, or gaming."
            )

    if monthly_income > 0:
        saving_capacity = monthly_income - total
        if saving_capacity > 0:
            saving_rate = saving_capacity / monthly_income * 100
            if saving_rate >= 20:
                tips.append(
                    f"Based on your recorded income and expenses, your current saving rate is about "
                    f"{saving_rate:.1f}%. That is a strong position if these figures represent the full month."
                )
            elif saving_rate >= 10:
                tips.append(
                    f"Your estimated saving rate is about {saving_rate:.1f}%. "
                    "Consider gradually moving toward a 20% savings target if your essential costs allow it."
                )
            else:
                tips.append(
                    f"Your estimated saving rate is only about {max(saving_rate, 0):.1f}%. "
                    "Look for one recurring optional expense you can reduce."
                )

    if remaining > 0:
        tips.append(
            f"You currently have ₹{remaining:,.0f} left from your monthly budget."
        )
    else:
        tips.append(
            f"You are ₹{abs(remaining):,.0f} above the planned monthly budget."
        )

    return tips


def answer_finance_question(question, expenses, monthly_budget, monthly_income):
    q = question.lower().strip()

    total = float(expenses["amount"].sum()) if not expenses.empty else 0.0
    remaining = monthly_budget - total

    if not q:
        return "Ask me about budgeting, saving, overspending, category-wise expenses, or financial habits."

    if any(word in q for word in ["remaining", "left", "budget left"]):
        if remaining >= 0:
            return f"You have ₹{remaining:,.0f} remaining from your monthly budget."
        return f"You are ₹{abs(remaining):,.0f} above your monthly budget."

    if any(word in q for word in ["spent", "spending", "total expense"]):
        return f"Your recorded expenses total ₹{total:,.0f}."

    if "highest" in q or "most" in q or "largest" in q:
        if expenses.empty:
            return "You do not have any recorded expenses yet."
        grouped = expenses.groupby("category")["amount"].sum().sort_values(ascending=False)
        cat = grouped.index[0]
        amount = float(grouped.iloc[0])
        return f"Your highest spending category is {cat}, with ₹{amount:,.0f} spent."

    if "save" in q or "saving" in q:
        if monthly_income > 0:
            suggested = monthly_income * 0.20
            return (
                f"A common starting target is to save around 20% of income when practical. "
                f"For your entered monthly income, that would be about ₹{suggested:,.0f}. "
                f"Adjust it based on essential expenses."
            )
        return (
            "A simple strategy is to save first, not last. Set aside a fixed amount as soon as money arrives, "
            "then plan spending from what remains."
        )

    if "50" in q and "30" in q and "20" in q:
        return (
            "The 50/30/20 rule suggests using about 50% of income for needs, 30% for wants, "
            "and 20% for savings or debt repayment. It is a guideline, not a strict rule."
        )

    if "emergency" in q:
        return (
            "An emergency fund is money kept for unexpected essential costs. "
            "A useful long-term goal is 3–6 months of essential expenses, built gradually."
        )

    if "overspend" in q or "control" in q:
        return (
            "To control overspending, set category limits, review expenses weekly, "
            "wait 24 hours before non-essential purchases, and reduce one recurring expense at a time."
        )

    tips = build_financial_advice(expenses, monthly_budget, monthly_income)
    return " ".join(tips[:2])
