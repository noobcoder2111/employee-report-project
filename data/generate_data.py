import random
from datetime import date, timedelta
import pandas as pd

random.seed(42)  # ensures same "random" data every time we run this

DEPARTMENTS = ["IT", "HR", "Sales", "Finance", "Marketing", "Operations"]

DESIGNATIONS_BY_DEPT = {
    "IT": ["Software Developer", "Senior Developer", "QA Engineer", "DevOps Engineer"],
    "HR": ["HR Executive", "HR Manager", "Recruiter"],
    "Sales": ["Sales Executive", "Sales Manager", "Account Manager"],
    "Finance": ["Accountant", "Financial Analyst", "Finance Manager"],
    "Marketing": ["Marketing Executive", "SEO Specialist", "Marketing Manager"],
    "Operations": ["Operations Executive", "Operations Manager"],
}

FIRST_NAMES = ["Rahul", "Priya", "Amit", "Sneha", "Vikram", "Anjali", "Rohan",
               "Neha", "Karan", "Pooja", "Arjun", "Divya", "Sanjay", "Kavita",
               "Manish", "Ritu", "Ajay", "Swati", "Deepak", "Meena"]
LAST_NAMES = ["Sharma", "Verma", "Gupta", "Singh", "Patel", "Kumar", "Reddy",
              "Nair", "Iyer", "Joshi", "Mehta", "Chopra", "Malhotra", "Rao"]


def random_joining_date():
    start = date(2018, 1, 1)
    end = date(2025, 12, 31)
    delta_days = (end - start).days
    return start + timedelta(days=random.randint(0, delta_days))


def generate_employee(emp_number: int) -> dict:
    department = random.choice(DEPARTMENTS)
    designation = random.choice(DESIGNATIONS_BY_DEPT[department])

    experience_years = round(random.uniform(0.5, 15.0), 1)
    age = min(60, int(22 + experience_years + random.randint(-2, 5)))

    # Base salary loosely tied to experience, with some randomness
    base_salary = 25000 + (experience_years * 4000) + random.uniform(-5000, 8000)
    salary = round(max(20000, base_salary), 2)

    projects_completed = max(0, int(experience_years * random.uniform(1.5, 3.5)))
    attendance_percentage = round(random.uniform(75, 100), 2)
    training_hours = random.randint(5, 60)
    leave_days = random.randint(0, 25)

    # Performance score loosely correlated with attendance, experience, training
    perf_base = (
        (attendance_percentage / 100) * 2.0
        + min(experience_years / 15, 1.0) * 1.5
        + (training_hours / 60) * 1.0
        + random.uniform(-0.5, 0.5)
    )
    performance_score = round(min(5.0, max(1.0, perf_base)), 2)

    status = "Active" if random.random() > 0.12 else "Inactive"

    return {
        "employee_id": f"EMP{emp_number:03d}",
        "employee_name": f"{random.choice(FIRST_NAMES)} {random.choice(LAST_NAMES)}",
        "department": department,
        "designation": designation,
        "age": age,
        "gender": random.choice(["Male", "Female"]),
        "joining_date": random_joining_date(),
        "salary": salary,
        "experience_years": experience_years,
        "projects_completed": projects_completed,
        "attendance_percentage": attendance_percentage,
        "performance_score": performance_score,
        "leave_days": leave_days,
        "training_hours": training_hours,
        "status": status,
    }


def generate_dataset(num_employees: int = 80) -> pd.DataFrame:
    records = [generate_employee(i + 1) for i in range(num_employees)]
    return pd.DataFrame(records)


if __name__ == "__main__":
    df = generate_dataset(80)
    print(df.head(10))
    print(f"\nTotal records generated: {len(df)}")