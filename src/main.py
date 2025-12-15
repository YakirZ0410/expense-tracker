import pandas as pd

def load_expenses(csv_path):
    df = pd.read_csv(csv_path)
    return df

def total_expenses(df):
    return df["amount"].sum()

def expenses_by_category(df):
    return (
        df.groupby("category")["amount"]
        .sum()
        .sort_values(ascending=False)
    )



if __name__ == "__main__":
    expenses = load_expenses("data/expenses.csv")
    total = total_expenses(expenses)
    print(f"Total expenses: {total}")

    by_category = expenses_by_category(expenses)
    print("\nExpenses by category:")
    print(by_category)