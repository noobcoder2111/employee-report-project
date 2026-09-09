from database.db import get_connection
from data.generate_data import generate_dataset

INSERT_QUERY = """
INSERT INTO production_records (
    production_date, product_name, machine_id, shift, operator_name,
    raw_material_used_kg, units_produced, defective_units,
    downtime_minutes, energy_consumed_kwh
) VALUES (
    %s, %s, %s, %s, %s, %s, %s, %s, %s, %s
);
"""


def insert_records(num_records: int = 300):
    df = generate_dataset(num_records)

    conn = get_connection()
    cursor = conn.cursor()

    for _, row in df.iterrows():
        cursor.execute(INSERT_QUERY, (
            row["production_date"],
            row["product_name"],
            row["machine_id"],
            row["shift"],
            row["operator_name"],
            row["raw_material_used_kg"],
            row["units_produced"],
            row["defective_units"],
            row["downtime_minutes"],
            row["energy_consumed_kwh"],
        ))

    conn.commit()
    cursor.close()
    conn.close()
    print(f"✅ Inserted {len(df)} production records into PostgreSQL.")


if __name__ == "__main__":
    insert_records(300)