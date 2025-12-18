from fastapi import FastAPI
from pydantic import BaseModel
import sqlite3
from typing import Optional
from fastapi.staticfiles import StaticFiles

app = FastAPI(title="Expense Tracker API")
app.mount("/app", StaticFiles(directory="frontend", html=True), name="frontend")

conn = sqlite3.connect("expenses.db", check_same_thread=False)
cursor = conn.cursor()

@app.get("/")
def root():
    return {"message": "Expense Tracker API is running"}


class Expense(BaseModel):
    amount: float
    category: str
    description: str
    date: str  # format: YYYY-MM-DD



@app.post("/expenses")
def create_expense(expense: Expense):
    cursor.execute(
        "INSERT INTO expenses (amount, category, description, date) VALUES (?, ?, ?, ?)",
        (expense.amount, expense.category, expense.description, expense.date),
    )
    conn.commit()
    return {"message": "Expense saved to database"}



from typing import Optional

@app.get("/expenses")
def get_expenses(
    category: Optional[str] = None,
    min_amount: Optional[float] = None,
    from_date: Optional[str] = None,
    to_date: Optional[str] = None,
):
    query = "SELECT id, amount, category, description, date FROM expenses"
    params = []

    conditions = []

    if category:
        conditions.append("category = ?")
        params.append(category)

    if min_amount:
        conditions.append("amount >= ?")
        params.append(min_amount)

    if from_date:
        conditions.append("date >= ?")
        params.append(from_date)

    if to_date:
        conditions.append("date <= ?")
        params.append(to_date)

    if conditions:
        query += " WHERE " + " AND ".join(conditions)

    cursor.execute(query, params)
    rows = cursor.fetchall()

    expenses = []
    for row in rows:
        expenses.append({
            "id": row[0],
            "amount": row[1],
            "category": row[2],
            "description": row[3],
            "date": row[4],
        })

    return expenses



# create table (if not exists)
cursor.execute("""
CREATE TABLE IF NOT EXISTS expenses (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    amount REAL,
    category TEXT,
    description TEXT
)
""")
conn.commit()

# add date column only if missing
cursor.execute("PRAGMA table_info(expenses)")
cols = [row[1] for row in cursor.fetchall()]  # row[1] = column name

if "date" not in cols:
    cursor.execute("ALTER TABLE expenses ADD COLUMN date TEXT")
    conn.commit()


