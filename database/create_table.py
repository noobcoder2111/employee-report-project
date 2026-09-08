from database.db import get_connection

DROP_TABLE_QUERY = "DROP TABLE IF EXISTS employees;"

CREATE_TABLE_QUERY = """
CREATE TABLE employees (
    employee_id VARCHAR(10) PRIMARY KEY,
    employee_name VARCHAR(100) NOT NULL,
    department VARCHAR(50) NOT NULL,
    designation VARCHAR(50) NOT NULL,
    age INTEGER NOT NULL,
    gender VARCHAR(10) NOT NULL,
    joining_date DATE NOT NULL,
    salary NUMERIC(10, 2) NOT NULL,
    experience_years NUMERIC(4, 1) NOT NULL,
    projects_completed INTEGER NOT NULL,
    attendance_percentage NUMERIC(5, 2) NOT NULL,
    performance_score NUMERIC(4, 2) NOT NULL,
    leave_days INTEGER NOT NULL,
    training_hours INTEGER NOT NULL,
    status VARCHAR(10) NOT NULL
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
    print("✅ 'employees' table (re)created with the new schema.")

if __name__ == "__main__":
    create_table()