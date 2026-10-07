# Student Budget & Financial Literacy Planner

A complete Streamlit project for helping students manage monthly budgets, record expenses, understand spending habits, set savings goals, and learn basic financial literacy.

## Main Features

- Monthly budget setup
- Optional income/allowance tracking
- Daily expense entry
- Expense categories
- Automatic total spending calculation
- Remaining budget calculation
- Percentage of budget used
- Category-wise expense analysis
- Pie chart and bar chart
- Daily spending trend
- Expense history
- Delete transactions
- CSV export
- Savings goals
- 50/30/20 budgeting guidance
- Rule-based AI Financial Advisor
- Personalized spending recommendations
- Financial literacy lessons
- Mini financial quiz
- No paid API required
- Data stored locally in CSV files

## Project Structure

```text
student_budget_financial_literacy_planner/
│
├── app.py
├── requirements.txt
├── README.md
│
├── .streamlit/
│   └── config.toml
│
├── data/
│   ├── budget.csv
│   ├── expenses.csv
│   ├── goals.csv
│   └── sample_expenses.csv
│
└── utils/
    ├── advisor.py
    └── storage.py
```

## Installation

Make sure Python is installed.

Open Command Prompt or terminal inside the project folder.

Install the required libraries:

```bash
pip install -r requirements.txt
```

## Run the Project

```bash
streamlit run app.py
```

Streamlit will normally open the project automatically in your browser.

If it does not, open:

```text
http://localhost:8501
```

## Suggested Project Title

StudentMoney AI — Student Budget & Financial Literacy Planner

## Problem Statement

Many students struggle to manage their monthly money effectively. Expenses such as food, travel, shopping, education, entertainment, subscriptions, and digital payments can quickly add up. Students often do not maintain a clear record of where their money is being spent, making it difficult to understand spending habits, control unnecessary expenses, or plan the remaining monthly budget.

Traditional budgeting methods may require manual calculations or complicated spreadsheets, while many financial applications can be overwhelming for beginners. Students also may not have enough practical knowledge about budgeting, savings, emergency funds, needs versus wants, and responsible spending.

Therefore, there is a need for a simple, student-friendly digital solution that helps students record daily expenses, monitor their monthly budget, identify spending patterns, receive simple financial suggestions, and improve their financial literacy.

## Solution Statement

StudentMoney AI is a simple AI-assisted web application built using Python and Streamlit. It helps students manage their monthly budget and understand their spending habits through an easy-to-use dashboard.

Students can enter a monthly budget and optional monthly income, then record daily expenses with amount, category, description, and date. The application automatically calculates total spending, remaining budget, percentage of budget used, category-wise spending, and daily spending trends.

The system includes an AI-style Financial Advisor that analyses the student's spending data using intelligent rule-based logic. It can identify high-spending categories, detect when the user is approaching or exceeding the monthly budget, estimate savings rate, and provide simple personalized suggestions.

The application also provides financial literacy lessons covering needs versus wants, emergency funds, impulse spending, saving strategies, digital payment awareness, and the 50/30/20 budgeting guideline.

The project does not require any paid API key and can run entirely on a local computer.

## Future Improvements

- User login system
- Cloud database
- Real AI chatbot using an LLM API
- Budget forecasting using machine learning
- Receipt scanning
- Automatic expense categorization
- UPI/SMS transaction import
- Monthly PDF reports
- Parent/student linked dashboards
