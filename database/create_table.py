from database.db import get_connection

DROP_TABLE_QUERY = "DROP TABLE IF EXISTS production_records;"

CREATE_TABLE_QUERY = """
CREATE TABLE production_records (
    record_id SERIAL PRIMARY KEY,
    production_date DATE NOT NULL,
    product_name VARCHAR(100) NOT NULL,
    machine_id VARCHAR(20) NOT NULL,
    shift VARCHAR(20) NOT NULL,
    operator_name VARCHAR(100) NOT NULL,
    raw_material_used_kg NUMERIC(8, 2) NOT NULL,
    units_produced INTEGER NOT NULL,
    defective_units INTEGER NOT NULL,
    downtime_minutes INTEGER NOT NULL,
    energy_consumed_kwh NUMERIC(8, 2) NOT NULL
);
"""

def create_table():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(DROP_TABLE_QUERY)
    cursor.execute(CREATE_TABLE_QUERY)
    conn.commit()
    cursor.close()
    conn.close()
    print("✅ 'production_records' table created (soap factory schema).")

if __name__ == "__main__":
    create_table()