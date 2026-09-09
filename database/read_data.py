import pandas as pd
from database.db import get_connection

SELECT_QUERY = "SELECT * FROM production_records;"


def fetch_production_df() -> pd.DataFrame:
    conn = get_connection()
    df = pd.read_sql(SELECT_QUERY, conn)
    conn.close()
    return df


if __name__ == "__main__":
    df = fetch_production_df()
    print(df.head(10))
    print(f"\nTotal records fetched: {len(df)}")