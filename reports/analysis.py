import pandas as pd
from database.read_data import fetch_employees_df


def get_summary_metrics(df: pd.DataFrame) -> dict:
    """High-level numbers for the top of the dashboard."""
    return {
        "total_employees": len(df),
        "average_salary": round(df["salary"].mean(), 2),
        "average_performance": round(df["performance_score"].mean(), 2),
        "average_attendance": round(df["attendance_percentage"].mean(), 2),
        "active_count": int((df["status"] == "Active").sum()),
        "inactive_count": int((df["status"] == "Inactive").sum()),
    }


def get_department_breakdown(df: pd.DataFrame) -> pd.DataFrame:
    """Employee count and average performance per department."""
    result = df.groupby("department").agg(
        employee_count=("employee_id", "count"),
        avg_performance=("performance_score", "mean"),
        avg_salary=("salary", "mean"),
    ).reset_index()
    result["avg_performance"] = result["avg_performance"].round(2)
    result["avg_salary"] = result["avg_salary"].round(2)
    return result


def get_top_performers(df: pd.DataFrame, n: int = 5) -> pd.DataFrame:
    """Top N employees by performance score."""
    return df.sort_values("performance_score", ascending=False).head(n)[
        ["employee_id", "employee_name", "department", "performance_score"]
    ]


def get_low_performers(df: pd.DataFrame, n: int = 5) -> pd.DataFrame:
    """Bottom N employees by performance score."""
    return df.sort_values("performance_score", ascending=True).head(n)[
        ["employee_id", "employee_name", "department", "performance_score"]
    ]


def get_joins_by_year(df: pd.DataFrame) -> pd.DataFrame:
    """Count of employees who joined in each year."""
    joining_dates = pd.to_datetime(df["joining_date"])
    year_counts = joining_dates.dt.year.value_counts().sort_index()
    result = year_counts.reset_index()
    result.columns = ["year", "employee_count"]
    return result


if __name__ == "__main__":
    df = fetch_employees_df()

    print("=== Summary Metrics ===")
    print(get_summary_metrics(df))

    print("\n=== Department Breakdown ===")
    print(get_department_breakdown(df))

    print("\n=== Top 5 Performers ===")
    print(get_top_performers(df))

    print("\n=== Bottom 5 Performers ===")
    print(get_low_performers(df))

    print("\n=== Joins by Year ===")
    print(get_joins_by_year(df))