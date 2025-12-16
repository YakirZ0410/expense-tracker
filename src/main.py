"""
Expense Tracker Analysis

This module provides utilities for loading, validating, analyzing,
and visualizing personal expense data stored in CSV format.
"""

import pandas as pd
import matplotlib.pyplot as plt


def load_expenses(csv_path: str) -> pd.DataFrame:
    """
    Load expenses from a CSV file and parse the date column.

    Args:
        csv_path (str): Path to the expenses CSV file.

    Returns:
        pd.DataFrame: DataFrame containing expense records with parsed dates.
    """
    df = pd.read_csv(csv_path)
    df["date"] = pd.to_datetime(df["date"])  # Convert date strings to datetime objects
    return df


def validate_expenses(df: pd.DataFrame) -> None:
    """
    Validate expense data integrity.

    Raises:
        ValueError: If missing or negative expense values are found.
    """
    if df["amount"].isnull().any():
        raise ValueError("Found missing values in amount column")

    if (df["amount"] < 0).any():
        raise ValueError("Found negative expense values")


def total_expenses(df: pd.DataFrame) -> float:
    """
    Calculate total amount of expenses.

    Args:
        df (pd.DataFrame): Expense data.

    Returns:
        float: Total expenses.
    """
    return df["amount"].sum()


def expenses_by_category(df: pd.DataFrame) -> pd.Series:
    """
    Aggregate expenses by category.

    Args:
        df (pd.DataFrame): Expense data.

    Returns:
        pd.Series: Total expenses per category (sorted descending).
    """
    return (
        df.groupby("category")["amount"]
        .sum()
        .sort_values(ascending=False)
    )


def expenses_by_month(df: pd.DataFrame) -> pd.Series:
    """
    Aggregate expenses by month.

    Args:
        df (pd.DataFrame): Expense data.

    Returns:
        pd.Series: Monthly expense totals.
    """
    df["month"] = df["date"].dt.to_period("M")
    return df.groupby("month")["amount"].sum().sort_index()


def add_date_parts(df: pd.DataFrame) -> pd.DataFrame:
    """
    Add derived date columns for easier filtering and analysis.

    Args:
        df (pd.DataFrame): Expense data.

    Returns:
        pd.DataFrame: DataFrame with year and month number columns added.
    """
    df["year"] = df["date"].dt.year
    df["month_num"] = df["date"].dt.month
    return df


def filter_expenses(
    df: pd.DataFrame,
    category: str | None = None,
    month: int | None = None
) -> pd.DataFrame:
    """
    Filter expenses by category and/or month.

    Args:
        df (pd.DataFrame): Expense data.
        category (str, optional): Category name to filter by.
        month (int, optional): Month number (1-12) to filter by.

    Returns:
        pd.DataFrame: Filtered expense records.
    """
    result = df

    if category:
        result = result[result["category"] == category]

    if month:
        result = result[result["month_num"] == month]

    return result


def plot_expenses_by_category(by_category: pd.Series, output_path: str) -> None:
    """
    Generate and save a bar chart of expenses by category.

    Args:
        by_category (pd.Series): Aggregated expenses per category.
        output_path (str): Path to save the output image.
    """
    ax = by_category.plot(kind="bar", title="Expenses by Category")
    ax.set_xlabel("Category")
    ax.set_ylabel("Amount")
    plt.tight_layout()
    plt.savefig(output_path)
    plt.close()


def plot_expenses_by_month(by_month: pd.Series, output_path: str) -> None:
    """
    Generate and save a line chart of expenses by month.

    Args:
        by_month (pd.Series): Aggregated expenses per month.
        output_path (str): Path to save the output image.
    """
    ax = by_month.plot(kind="line", marker="o", title="Expenses by Month")
    ax.set_xlabel("Month")
    ax.set_ylabel("Amount")
    plt.tight_layout()
    plt.savefig(output_path)
    plt.close()


def compute_kpis(df: pd.DataFrame) -> tuple[float, str, float]:
    """
    Compute key performance indicators (KPIs) for expenses.

    Returns:
        tuple: (total_spent, top_category, average_transaction)
    """
    total = df["amount"].sum()
    top_category = df.groupby("category")["amount"].sum().idxmax()
    avg_tx = df["amount"].mean()
    return total, top_category, avg_tx


def plot_top_expenses(df: pd.DataFrame, output_path: str, n: int = 5) -> None:
    """
    Generate and save a bar chart of the top N expenses.

    Args:
        df (pd.DataFrame): Expense data.
        output_path (str): Path to save the output image.
        n (int): Number of top expenses to display.
    """
    top = df.sort_values("amount", ascending=False).head(n)
    labels = top["description"] + " (" + top["category"] + ")"

    ax = top.set_index(labels)["amount"].plot(
        kind="bar",
        title=f"Top {n} Expenses"
    )
    ax.set_xlabel("")
    ax.set_ylabel("Amount")
    plt.tight_layout()
    plt.savefig(output_path)
    plt.close()


def export_category_report(df: pd.DataFrame, output_path: str) -> None:
    """
    Export a CSV report summarizing expenses by category.

    The report includes total amount and percentage of total spend.

    Args:
        df (pd.DataFrame): Expense data.
        output_path (str): Path to save the CSV report.
    """
    summary = (
        df.groupby("category")["amount"]
        .sum()
        .reset_index()
        .rename(columns={"amount": "total_amount"})
    )

    summary["percentage"] = (
        summary["total_amount"] / summary["total_amount"].sum() * 100
    )

    summary.sort_values("total_amount", ascending=False, inplace=True)
    summary.to_csv(output_path, index=False)


if __name__ == "__main__":
    # Load and validate data
    expenses = load_expenses("data/expenses.csv")
    validate_expenses(expenses)

    # Basic aggregations
    print(f"Total expenses: {total_expenses(expenses)}")

    by_category = expenses_by_category(expenses)
    print("\nExpenses by category:")
    print(by_category)

    by_month = expenses_by_month(expenses)
    print("\nExpenses by month:")
    print(by_month)

    # Feature engineering
    expenses = add_date_parts(expenses)

    # Example filtering
    food_january = filter_expenses(expenses, category="Food", month=1)
    print("\nFood expenses in January:")
    print(food_january[["date", "description", "amount"]])

    # Visualizations
    plot_expenses_by_category(by_category, "docs/expenses_by_category.png")
    plot_expenses_by_month(by_month, "docs/expenses_by_month.png")
    plot_top_expenses(expenses, "docs/top_expenses.png")

    # KPI summary
    total_kpi, top_cat_kpi, avg_tx_kpi = compute_kpis(expenses)
    print("\nKPI Summary:")
    print(f"- Total spent: {total_kpi:.2f}")
    print(f"- Top category: {top_cat_kpi}")
    print(f"- Average transaction: {avg_tx_kpi:.2f}")

    # Export report
    export_category_report(expenses, "docs/category_report.csv")
