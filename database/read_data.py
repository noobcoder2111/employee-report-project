import pandas as pd
from database.db import get_connection

SELECT_QUERY = "SELECT * FROM employees;"


def fetch_employees_df() -> pd.DataFrame:
    """
    Reads all employee records from PostgreSQL and returns them
    as a pandas DataFrame. This is the single source of truth
    for every report/analysis in this project.
    """
    conn = get_connection()
    df = pd.read_sql(SELECT_QUERY, conn)
    conn.close()
    return df


if __name__ == "__main__":
    df = fetch_employees_df()
    print(df.head(10))
    print(f"\nTotal records fetched from PostgreSQL: {len(df)}")
    print("\nColumn types:")
    print(df.dtypes)