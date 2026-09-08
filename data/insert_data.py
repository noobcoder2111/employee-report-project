from database.db import get_connection
from data.generate_data import generate_dataset

INSERT_QUERY = """
INSERT INTO employees (
    employee_id, employee_name, department, designation, age, gender,
    joining_date, salary, experience_years, projects_completed,
    attendance_percentage, performance_score, leave_days,
    training_hours, status
) VALUES (
    %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s
)
ON CONFLICT (employee_id) DO NOTHING;
"""


def insert_employees(num_employees: int = 80):
    df = generate_dataset(num_employees)

    conn = get_connection()
    cursor = conn.cursor()

    inserted_count = 0
    for _, row in df.iterrows():
        cursor.execute(INSERT_QUERY, (
            row["employee_id"],
            row["employee_name"],
            row["department"],
            row["designation"],
            row["age"],
            row["gender"],
            row["joining_date"],
            row["salary"],
            row["experience_years"],
            row["projects_completed"],
            row["attendance_percentage"],
            row["performance_score"],
            row["leave_days"],
            row["training_hours"],
            row["status"],
        ))
        inserted_count += cursor.rowcount

    conn.commit()
    cursor.close()
    conn.close()
    print(f"✅ Inserted {inserted_count} new employee records into PostgreSQL.")


if __name__ == "__main__":
    insert_employees(80)