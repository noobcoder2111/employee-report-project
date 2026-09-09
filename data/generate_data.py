import random
from datetime import date, timedelta
import pandas as pd

random.seed(42)

PRODUCTS = ["Bathing Soap 100g", "Bathing Soap 150g", "Detergent Bar 250g",
            "Handwash Soap 75g", "Glycerin Soap 100g"]

MACHINES = ["M-101", "M-102", "M-103", "M-104"]

SHIFTS = ["Morning", "Evening", "Night"]

OPERATOR_NAMES = ["Rahul Sharma", "Priya Verma", "Amit Gupta", "Sneha Singh",
                  "Vikram Patel", "Anjali Kumar", "Rohan Reddy", "Neha Nair",
                  "Karan Iyer", "Pooja Joshi"]


def random_production_date(days_back: int) -> date:
    """Returns a date within the last `days_back` days from today."""
    return date.today() - timedelta(days=random.randint(0, days_back))


def generate_record(record_number: int) -> dict:
    machine = random.choice(MACHINES)
    shift = random.choice(SHIFTS)

    # Downtime affects how much can be produced in that shift
    downtime_minutes = random.randint(0, 90)
    # A shift is roughly 480 minutes; less downtime = more effective production time
    effective_minutes = max(50, 480 - downtime_minutes)

    raw_material_used_kg = round(random.uniform(80, 250), 2)

    # Units produced loosely tied to raw material and effective time, with noise
    base_units = (raw_material_used_kg * random.uniform(8, 12)) * (effective_minutes / 480)
    units_produced = max(50, int(base_units + random.uniform(-40, 40)))

    # Defect rate roughly 1-6%, slightly worse with more downtime (rushed/interrupted runs)
    defect_rate = random.uniform(0.01, 0.04) + (downtime_minutes / 90) * 0.02
    defective_units = int(units_produced * defect_rate)

    energy_consumed_kwh = round(raw_material_used_kg * random.uniform(0.4, 0.7), 2)

    return {
        "production_date": random_production_date(60),
        "product_name": random.choice(PRODUCTS),
        "machine_id": machine,
        "shift": shift,
        "operator_name": random.choice(OPERATOR_NAMES),
        "raw_material_used_kg": raw_material_used_kg,
        "units_produced": units_produced,
        "defective_units": defective_units,
        "downtime_minutes": downtime_minutes,
        "energy_consumed_kwh": energy_consumed_kwh,
    }


def generate_dataset(num_records: int = 300) -> pd.DataFrame:
    records = [generate_record(i + 1) for i in range(num_records)]
    df = pd.DataFrame(records)
    return df.sort_values("production_date").reset_index(drop=True)


if __name__ == "__main__":
    df = generate_dataset(300)
    print(df.head(10))
    print(f"\nTotal records generated: {len(df)}")