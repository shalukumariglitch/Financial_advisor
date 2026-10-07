from pathlib import Path
import pandas as pd

DATA_DIR = Path("data")
DATA_DIR.mkdir(exist_ok=True)

EXPENSE_FILE = DATA_DIR / "expenses.csv"
BUDGET_FILE = DATA_DIR / "budget.csv"
GOAL_FILE = DATA_DIR / "goals.csv"


def ensure_files():
    if not EXPENSE_FILE.exists():
        pd.DataFrame(columns=[
            "date", "category", "amount", "description"
        ]).to_csv(EXPENSE_FILE, index=False)

    if not BUDGET_FILE.exists():
        pd.DataFrame([{
            "monthly_budget": 10000,
            "monthly_income": 0
        }]).to_csv(BUDGET_FILE, index=False)

    if not GOAL_FILE.exists():
        pd.DataFrame(columns=[
            "goal_name", "target_amount", "saved_amount"
        ]).to_csv(GOAL_FILE, index=False)


def load_expenses():
    ensure_files()
    df = pd.read_csv(EXPENSE_FILE)
    if not df.empty:
        df["date"] = pd.to_datetime(df["date"])
        df["amount"] = pd.to_numeric(df["amount"], errors="coerce").fillna(0)
    return df


def save_expenses(df):
    df.to_csv(EXPENSE_FILE, index=False)


def add_expense(date, category, amount, description):
    df = load_expenses()
    new_row = pd.DataFrame([{
        "date": pd.to_datetime(date),
        "category": category,
        "amount": float(amount),
        "description": description.strip()
    }])
    df = pd.concat([df, new_row], ignore_index=True)
    save_expenses(df)


def delete_expense(index_value):
    df = load_expenses()
    if index_value in df.index:
        df = df.drop(index_value).reset_index(drop=True)
        save_expenses(df)


def load_budget():
    ensure_files()
    df = pd.read_csv(BUDGET_FILE)
    if df.empty:
        return {"monthly_budget": 10000.0, "monthly_income": 0.0}
    row = df.iloc[0]
    return {
        "monthly_budget": float(row.get("monthly_budget", 10000)),
        "monthly_income": float(row.get("monthly_income", 0))
    }


def save_budget(monthly_budget, monthly_income):
    pd.DataFrame([{
        "monthly_budget": float(monthly_budget),
        "monthly_income": float(monthly_income)
    }]).to_csv(BUDGET_FILE, index=False)


def load_goals():
    ensure_files()
    return pd.read_csv(GOAL_FILE)


def save_goals(df):
    df.to_csv(GOAL_FILE, index=False)


def add_goal(goal_name, target_amount, saved_amount):
    df = load_goals()
    row = pd.DataFrame([{
        "goal_name": goal_name.strip(),
        "target_amount": float(target_amount),
        "saved_amount": float(saved_amount)
    }])
    df = pd.concat([df, row], ignore_index=True)
    save_goals(df)
