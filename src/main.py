import pandas as pd
import matplotlib.pyplot as plt

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

def plot_expenses_by_category(by_category, output_path):
    ax = by_category.plot(kind="bar", title="Expenses by Category")
    ax.set_xlabel("Category")
    ax.set_ylabel("Amount")
    plt.tight_layout()
    plt.savefig(output_path)
    plt.close()

def plot_expenses_by_month(by_month, output_path):
    ax = by_month.plot(kind="line", marker="o", title="Expenses by Month")
    ax.set_xlabel("Month")
    ax.set_ylabel("Amount")
    plt.tight_layout()
    plt.savefig(output_path)
    plt.close()

def compute_kpis(df):
    total = df["amount"].sum()
    top_category = df.groupby("category")["amount"].sum().idxmax()
    avg_tx = df["amount"].mean()
    return total, top_category, avg_tx

def plot_top_expenses(df, output_path, n=5):
    top = df.sort_values("amount", ascending=False).head(n)  # לוקח את N ההוצאות הגדולות
    labels = top["description"] + " (" + top["category"] + ")"  # טקסט לכל עמודה

    ax = top.set_index(labels)["amount"].plot(kind="bar", title=f"Top {n} Expenses")
    ax.set_xlabel("")
    ax.set_ylabel("Amount")
    plt.tight_layout()
    plt.savefig(output_path)
    plt.close()

def export_category_report(df, output_path):
    summary = (
        df.groupby("category")["amount"]
        .sum()
        .reset_index()
        .rename(columns={"amount": "total_amount"})
    )

    summary["percentage"] = summary["total_amount"] / summary["total_amount"].sum() * 100
    summary = summary.sort_values("total_amount", ascending=False)

    summary.to_csv(output_path, index=False)

def validate_expenses(df):
    if df["amount"].isnull().any():
        raise ValueError("Found missing values in amount")

    if (df["amount"] < 0).any():
        raise ValueError("Found negative expense values")


if __name__ == "__main__":
    expenses = load_expenses("data/expenses.csv")
    validate_expenses(expenses)

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

    plot_expenses_by_category(by_category, "docs/expenses_by_category.png")
    print("\nSaved chart: docs/expenses_by_category.png")

    plot_expenses_by_month(by_month, "docs/expenses_by_month.png")
    print("Saved chart: docs/expenses_by_month.png")

    total_kpi, top_cat_kpi, avg_tx_kpi = compute_kpis(expenses)

    print("\nKPI Summary:")
    print(f"- Total spent: {total_kpi:.2f}")
    print(f"- Top category: {top_cat_kpi}")
    print(f"- Average transaction: {avg_tx_kpi:.2f}")

    plot_top_expenses(expenses, "docs/top_expenses.png", n=5)
    print("Saved chart: docs/top_expenses.png")

    export_category_report(expenses, "docs/category_report.csv")
    print("Saved report: docs/category_report.csv")
