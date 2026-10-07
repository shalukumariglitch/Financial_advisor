import io
from datetime import date

import pandas as pd
import plotly.express as px
import streamlit as st

from utils.storage import (
    ensure_files,
    load_expenses,
    add_expense,
    delete_expense,
    load_budget,
    save_budget,
    load_goals,
    add_goal,
    save_goals
)
from utils.advisor import build_financial_advice, answer_finance_question


st.set_page_config(
    page_title="Student Budget & Financial Literacy Planner",
    page_icon="💰",
    layout="wide"
)

ensure_files()


def money(value):
    return f"₹{value:,.0f}"


def current_month_expenses(df):
    if df.empty:
        return df.copy()
    today = pd.Timestamp.today()
    return df[
        (df["date"].dt.month == today.month) &
        (df["date"].dt.year == today.year)
    ].copy()


def section_title(title, subtitle=""):
    st.markdown(f"## {title}")
    if subtitle:
        st.caption(subtitle)


budget_data = load_budget()
expenses = load_expenses()
month_df = current_month_expenses(expenses)
goals = load_goals()

monthly_budget = budget_data["monthly_budget"]
monthly_income = budget_data["monthly_income"]
total_spent = float(month_df["amount"].sum()) if not month_df.empty else 0.0
remaining = monthly_budget - total_spent
usage_percent = (total_spent / monthly_budget * 100) if monthly_budget > 0 else 0


with st.sidebar:
    st.title("StudentMoney AI")
    st.caption("Budget smarter. Learn finance. Build better habits.")

    page = st.radio(
        "Navigation",
        [
            "Dashboard",
            "Add Expense",
            "Expense History",
            "Budget Planner",
            "Savings Goals",
            "AI Financial Advisor",
            "Financial Literacy"
        ]
    )

    st.divider()
    st.write("Current month")
    st.metric("Budget", money(monthly_budget))
    st.metric("Spent", money(total_spent))
    st.metric("Remaining", money(remaining))

    if monthly_budget > 0:
        st.progress(min(usage_percent / 100, 1.0))
        st.caption(f"{usage_percent:.1f}% of budget used")


if page == "Dashboard":
    st.title("Student Budget & Financial Literacy Planner")
    st.write(
        "Track your daily expenses, understand spending patterns, and improve your financial decisions."
    )

    col1, col2, col3, col4 = st.columns(4)

    col1.metric("Monthly Budget", money(monthly_budget))
    col2.metric("Total Spent", money(total_spent))
    col3.metric(
        "Remaining",
        money(remaining),
        delta=f"{100 - usage_percent:.1f}% budget left" if monthly_budget > 0 else None
    )
    col4.metric("Transactions", len(month_df))

    st.divider()

    if month_df.empty:
        st.info("No expenses recorded for the current month yet.")
    else:
        chart_col1, chart_col2 = st.columns(2)

        category_summary = (
            month_df.groupby("category", as_index=False)["amount"].sum()
            .sort_values("amount", ascending=False)
        )

        with chart_col1:
            st.subheader("Category-wise Spending")
            fig = px.pie(
                category_summary,
                names="category",
                values="amount",
                hole=0.45
            )
            fig.update_layout(margin=dict(l=10, r=10, t=30, b=10))
            st.plotly_chart(fig, use_container_width=True)

        with chart_col2:
            st.subheader("Spending by Category")
            fig = px.bar(
                category_summary,
                x="category",
                y="amount",
                text_auto=".2s"
            )
            fig.update_layout(
                xaxis_title="",
                yaxis_title="Amount (₹)",
                margin=dict(l=10, r=10, t=30, b=10)
            )
            st.plotly_chart(fig, use_container_width=True)

        daily = (
            month_df.assign(day=month_df["date"].dt.date)
            .groupby("day", as_index=False)["amount"]
            .sum()
        )

        st.subheader("Daily Spending Trend")
        fig = px.line(
            daily,
            x="day",
            y="amount",
            markers=True
        )
        fig.update_layout(
            xaxis_title="Date",
            yaxis_title="Amount (₹)"
        )
        st.plotly_chart(fig, use_container_width=True)

    st.divider()
    st.subheader("Smart Insights")

    for tip in build_financial_advice(
        month_df,
        monthly_budget,
        monthly_income
    ):
        st.info(tip)


elif page == "Add Expense":
    section_title(
        "Add Expense",
        "Record your spending as soon as it happens."
    )

    categories = [
        "Food",
        "Transport",
        "Education",
        "Shopping",
        "Entertainment",
        "Health",
        "Rent",
        "Eating Out",
        "Gaming",
        "Other"
    ]

    with st.form("expense_form", clear_on_submit=True):
        col1, col2 = st.columns(2)

        with col1:
            expense_date = st.date_input(
                "Date",
                value=date.today()
            )
            category = st.selectbox(
                "Category",
                categories
            )

        with col2:
            amount = st.number_input(
                "Amount (₹)",
                min_value=1.0,
                step=10.0
            )
            description = st.text_input(
                "Description",
                placeholder="Example: Lunch with friends"
            )

        submitted = st.form_submit_button(
            "Add Expense",
            use_container_width=True
        )

        if submitted:
            add_expense(
                expense_date,
                category,
                amount,
                description
            )
            st.success("Expense added successfully.")
            st.rerun()


elif page == "Expense History":
    section_title(
        "Expense History",
        "Review and manage all recorded expenses."
    )

    if expenses.empty:
        st.info("No expenses have been recorded yet.")
    else:
        view = expenses.copy()
        view["date"] = view["date"].dt.strftime("%Y-%m-%d")
        view.index = range(1, len(view) + 1)

        st.dataframe(
            view,
            use_container_width=True
        )

        csv_data = view.to_csv(index=False).encode("utf-8")

        st.download_button(
            "Download Expenses as CSV",
            data=csv_data,
            file_name="student_expenses.csv",
            mime="text/csv"
        )

        st.divider()

        st.subheader("Delete an Expense")

        display_choices = {
            idx: f"{row['date']} | {row['category']} | {money(row['amount'])} | {row['description']}"
            for idx, row in expenses.iterrows()
        }

        selected = st.selectbox(
            "Choose transaction",
            options=list(display_choices.keys()),
            format_func=lambda x: display_choices[x]
        )

        if st.button("Delete Selected Expense"):
            delete_expense(selected)
            st.success("Expense deleted.")
            st.rerun()


elif page == "Budget Planner":
    section_title(
        "Monthly Budget Planner",
        "Set your budget and optional monthly income."
    )

    with st.form("budget_form"):
        new_income = st.number_input(
            "Monthly Income / Allowance (₹)",
            min_value=0.0,
            value=float(monthly_income),
            step=500.0
        )

        new_budget = st.number_input(
            "Monthly Spending Budget (₹)",
            min_value=1.0,
            value=float(monthly_budget),
            step=500.0
        )

        save = st.form_submit_button(
            "Save Budget",
            use_container_width=True
        )

        if save:
            save_budget(new_budget, new_income)
            st.success("Budget updated.")
            st.rerun()

    st.divider()

    st.subheader("Budget Status")

    progress = min(total_spent / monthly_budget, 1.0) if monthly_budget > 0 else 0
    st.progress(progress)

    if usage_percent < 70:
        st.success(f"You have used {usage_percent:.1f}% of your monthly budget.")
    elif usage_percent < 100:
        st.warning(f"You have used {usage_percent:.1f}% of your monthly budget.")
    else:
        st.error(f"You have used {usage_percent:.1f}% of your monthly budget.")

    if monthly_income > 0:
        st.subheader("50 / 30 / 20 Guideline")

        c1, c2, c3 = st.columns(3)
        c1.metric("Needs ~50%", money(monthly_income * 0.50))
        c2.metric("Wants ~30%", money(monthly_income * 0.30))
        c3.metric("Savings ~20%", money(monthly_income * 0.20))


elif page == "Savings Goals":
    section_title(
        "Savings Goals",
        "Create goals and track your progress."
    )

    with st.form("goal_form", clear_on_submit=True):
        goal_name = st.text_input(
            "Goal name",
            placeholder="Example: New laptop"
        )
        target = st.number_input(
            "Target amount (₹)",
            min_value=1.0,
            step=100.0
        )
        saved = st.number_input(
            "Already saved (₹)",
            min_value=0.0,
            step=100.0
        )

        if st.form_submit_button("Add Goal", use_container_width=True):
            if not goal_name.strip():
                st.error("Please enter a goal name.")
            else:
                add_goal(goal_name, target, saved)
                st.success("Savings goal added.")
                st.rerun()

    st.divider()

    if goals.empty:
        st.info("No savings goals added yet.")
    else:
        for idx, row in goals.iterrows():
            st.subheader(row["goal_name"])

            target = float(row["target_amount"])
            saved = float(row["saved_amount"])
            ratio = min(saved / target, 1.0) if target > 0 else 0

            st.progress(ratio)
            st.caption(
                f"{money(saved)} saved out of {money(target)} "
                f"({ratio * 100:.1f}%)"
            )

            col1, col2 = st.columns([3, 1])

            with col1:
                add_amount = st.number_input(
                    "Add savings",
                    min_value=0.0,
                    step=100.0,
                    key=f"goal_add_{idx}"
                )

            with col2:
                st.write("")
                st.write("")
                if st.button(
                    "Update",
                    key=f"goal_update_{idx}",
                    use_container_width=True
                ):
                    goals.loc[idx, "saved_amount"] = saved + add_amount
                    save_goals(goals)
                    st.rerun()

            st.divider()


elif page == "AI Financial Advisor":
    section_title(
        "AI Financial Advisor",
        "Ask questions about your current spending and general financial habits."
    )

    st.info(
        "This assistant uses rule-based financial analysis and does not require an API key."
    )

    question = st.text_input(
        "Ask a question",
        placeholder="Example: Where am I spending the most?"
    )

    if st.button("Ask Advisor", use_container_width=True):
        answer = answer_finance_question(
            question,
            month_df,
            monthly_budget,
            monthly_income
        )
        st.success(answer)

    st.divider()

    st.subheader("Automatic Recommendations")

    for tip in build_financial_advice(
        month_df,
        monthly_budget,
        monthly_income
    ):
        st.write("•", tip)


elif page == "Financial Literacy":
    section_title(
        "Financial Literacy Hub",
        "Short lessons for building stronger money habits."
    )

    lessons = {
        "1. Needs vs Wants": """
A need is something important for daily life, such as basic food, transport, education, rent, and essential healthcare.

A want improves comfort or enjoyment but is not always necessary, such as entertainment subscriptions, gaming purchases, frequent eating out, or impulse shopping.

Before buying something, ask: "Would my daily life seriously be affected if I did not buy this today?"
""",
        "2. The 50 / 30 / 20 Rule": """
A popular budgeting guideline is:

- 50% for needs
- 30% for wants
- 20% for savings or debt repayment

It is not a strict rule. Students with low income or high education costs may need different percentages.
""",
        "3. Emergency Fund": """
An emergency fund is money saved for unexpected essential expenses.

Examples include urgent travel, medical costs, device repair needed for study, or temporary income loss.

Start small. Even a ₹500 or ₹1,000 emergency buffer is better than having no reserve.
""",
        "4. Impulse Spending": """
Impulse spending happens when you buy without planning.

Try the 24-hour rule:
For non-essential purchases, wait one day before buying.

Many purchases feel less necessary after the waiting period.
""",
        "5. Saving First": """
Instead of spending first and saving whatever remains, reverse the process.

When money arrives:
1. Save a fixed amount.
2. Set aside essential expenses.
3. Spend the rest carefully.
""",
        "6. Digital Payment Awareness": """
UPI and card payments are convenient, but they can make spending feel less noticeable than cash.

Review your transaction history weekly and record even small digital payments.
"""
    }

    for title, content in lessons.items():
        with st.expander(title):
            st.write(content)

    st.divider()

    st.subheader("Quick Budget Quiz")

    q1 = st.radio(
        "Which is usually the best example of an emergency expense?",
        [
            "Buying a new game during a sale",
            "Urgent medical treatment",
            "Ordering food because you do not want to cook"
        ],
        index=None
    )

    q2 = st.radio(
        "What does the 20 in the 50/30/20 guideline usually represent?",
        [
            "Entertainment",
            "Savings or debt repayment",
            "Transport"
        ],
        index=None
    )

    if st.button("Check Answers"):
        score = 0

        if q1 == "Urgent medical treatment":
            score += 1

        if q2 == "Savings or debt repayment":
            score += 1

        st.success(f"You scored {score}/2.")
