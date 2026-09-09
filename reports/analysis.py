import pandas as pd
from database.read_data import fetch_production_df


def get_summary_metrics(df: pd.DataFrame) -> dict:
    total_units = int(df["units_produced"].sum())
    total_defects = int(df["defective_units"].sum())
    defect_rate = round((total_defects / total_units) * 100, 2) if total_units > 0 else 0

    return {
        "total_records": len(df),
        "total_units_produced": total_units,
        "total_defective_units": total_defects,
        "defect_rate_percent": defect_rate,
        "total_downtime_minutes": int(df["downtime_minutes"].sum()),
        "total_raw_material_kg": round(df["raw_material_used_kg"].sum(), 2),
        "avg_energy_consumed_kwh": round(df["energy_consumed_kwh"].mean(), 2),
    }


def get_machine_breakdown(df: pd.DataFrame) -> pd.DataFrame:
    result = df.groupby("machine_id").agg(
        total_units=("units_produced", "sum"),
        total_defects=("defective_units", "sum"),
        total_downtime=("downtime_minutes", "sum"),
        avg_energy=("energy_consumed_kwh", "mean"),
    ).reset_index()
    result["avg_energy"] = result["avg_energy"].round(2)
    result["defect_rate_percent"] = (result["total_defects"] / result["total_units"] * 100).round(2)
    return result


def get_product_breakdown(df: pd.DataFrame) -> pd.DataFrame:
    result = df.groupby("product_name").agg(
        total_units=("units_produced", "sum"),
        total_defects=("defective_units", "sum"),
    ).reset_index()
    return result.sort_values("total_units", ascending=False)


def get_daily_trend(df: pd.DataFrame) -> pd.DataFrame:
    result = df.groupby("production_date").agg(
        total_units=("units_produced", "sum"),
        total_defects=("defective_units", "sum"),
    ).reset_index()
    result["production_date"] = result["production_date"].astype(str)
    return result.sort_values("production_date")


def get_shift_breakdown(df: pd.DataFrame) -> pd.DataFrame:
    result = df.groupby("shift").agg(
        total_units=("units_produced", "sum"),
        total_downtime=("downtime_minutes", "sum"),
    ).reset_index()
    return result


def filter_by_date(df: pd.DataFrame, selected_date: str) -> pd.DataFrame:
    """Filters records for one specific date (format: YYYY-MM-DD)."""
    df = df.copy()
    df["production_date"] = df["production_date"].astype(str)
    return df[df["production_date"] == selected_date]


if __name__ == "__main__":
    df = fetch_production_df()

    print("=== Summary ===")
    print(get_summary_metrics(df))

    print("\n=== Machine Breakdown ===")
    print(get_machine_breakdown(df))

    print("\n=== Product Breakdown ===")
    print(get_product_breakdown(df))

    print("\n=== Shift Breakdown ===")
    print(get_shift_breakdown(df))

    print("\n=== Daily Trend (first 5 rows) ===")
    print(get_daily_trend(df).head())