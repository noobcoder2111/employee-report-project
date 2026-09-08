from database.db import get_connection

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

new_employee = (
    "EMP999", "Test Employee", "IT", "Software Developer", 30, "Male",
    "2024-01-15", 75000.00, 5.0, 12, 95.5, 4.5, 5, 40, "Active"
)

conn = get_connection()
cursor = conn.cursor()
cursor.execute(INSERT_QUERY, new_employee)
conn.commit()
cursor.close()
conn.close()
print("✅ Test employee EMP999 inserted.")