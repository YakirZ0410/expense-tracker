Expense Tracker (Full-Stack + Data Analysis)

Expense Tracker is a full-stack application for logging personal expenses and generating data-driven insights.
The project combines a FastAPI backend with SQLite, a simple frontend UI, and a Python data analysis module that produces reports and visualizations.

This repository demonstrates skills in backend development, frontend integration, and practical data analysis using real-world data.

---

Features

Web Application

- Add expenses (date, amount, category, description)
- View all expenses in a responsive table (live data from SQLite)
- Clean UI with client-side validation

Data Analysis & Reporting

- Load and validate expense data from CSV
- Aggregate expenses by category and by month
- Compute KPIs:
  - Total expenses
  - Top spending category
  - Average transaction value
- Generate visual reports:
  - Expenses by category (bar chart)
  - Expenses by month (line chart)
  - Top expenses (bar chart)
- Export CSV report with category percentages

---

Tech Stack

Backend: FastAPI, SQLite
Frontend: HTML, CSS, JavaScript
Data Analysis: Python, Pandas, Matplotlib

---

Project Structure

expense-tracker/
├── backend/ – FastAPI app + SQLite DB
├── frontend/ – HTML / CSS / JS UI
├── src/ – Data analysis & reporting utilities
├── data/ – CSV data (sample / exported)
├── docs/ – Charts, reports, screenshots
├── README.md
└── requirements.txt

---

How to Run Locally

1. Install dependencies
   pip install -r requirements.txt

2. Run the backend (serves the frontend as well)
   uvicorn backend.main:app --reload --port 8001

3. Open the application
   Web UI: http://127.0.0.1:8001/app/
   API endpoint (JSON): http://127.0.0.1:8001/expenses

---

Data Analysis & Reports

Run the analysis module:
python src/expense_analysis.py

Generated outputs:

- docs/expenses_by_category.png
- docs/expenses_by_month.png
- docs/top_expenses.png
- docs/category_report.csv

---

Demo

Expenses by Category:
docs/expenses_by_category.png

Expenses by Month:
docs/expenses_by_month.png

Top Expenses:
docs/top_expenses.png

Category Report:
docs/category_report.csv

---

Roadmap / Improvements

- Normalize categories (e.g. Food / FOOD / food → Food)
- Handle missing or invalid dates in raw data
- Add filters in the UI (category, date range, minimum amount)
- Add delete/edit functionality for expenses
- Add KPI summary endpoint (/expenses/summary)
- Extend analysis with trend detection and simple forecasting

---

Author

Yakir Zindani
Computer Science graduate with interest in Data Analysis, AI, and full-stack development.
