import pandas as pd

def load_expenses(csv_path):
    df = pd.read_csv(csv_path)
    df["date"] = pd.to_datetime(df["date"])  # convert string -> datetime
    return df


def total_expenses(df):
    return df["amount"].sum()

def expenses_by_category(df):
    return (
        df.groupby("category")["amount"]
        .sum()
        .sort_values(ascending=False)
    )

def expenses_by_month(df):
    df["month"] = df["date"].dt.to_period("M")
    return df.groupby("month")["amount"].sum().sort_index()

def add_date_parts(df):
    df["year"] = df["date"].dt.year
    df["month_num"] = df["date"].dt.month
    return df

def filter_expenses(df, category=None, month=None):
    result = df

    if category:
        result = result[result["category"] == category]

    if month:
        result = result[result["month_num"] == month]

    return result


if __name__ == "__main__":
    expenses = load_expenses("data/expenses.csv")
    total = total_expenses(expenses)
    print(f"Total expenses: {total}")

    by_category = expenses_by_category(expenses)
    print("\nExpenses by category:")
    print(by_category)

    by_month = expenses_by_month(expenses)
    print("\nExpenses by month:")
    print(by_month)

    expenses = add_date_parts(expenses)

    print(expenses)

    food_january = filter_expenses(expenses, category="Food", month=1)
    print("\nFood expenses in January:")
    print(food_january[["date", "description", "amount"]])


