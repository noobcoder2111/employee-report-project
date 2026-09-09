import pandas as pd
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_absolute_error, r2_score

from database.read_data import fetch_production_df

FEATURE_COLUMNS = [
    "raw_material_used_kg",
    "downtime_minutes",
    "energy_consumed_kwh",
]
TARGET_COLUMN = "units_produced"


def prepare_data(df: pd.DataFrame):
    data = df[FEATURE_COLUMNS + [TARGET_COLUMN]].dropna()
    X = data[FEATURE_COLUMNS]
    y = data[TARGET_COLUMN]
    return X, y


def train_model():
    df = fetch_production_df()
    X, y = prepare_data(df)

    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42
    )

    model = RandomForestRegressor(n_estimators=100, random_state=42)
    model.fit(X_train, y_train)

    predictions = model.predict(X_test)
    mae = mean_absolute_error(y_test, predictions)
    r2 = r2_score(y_test, predictions)

    return model, {"mae": round(mae, 2), "r2_score": round(r2, 3)}


def predict_for_all(model, df: pd.DataFrame) -> pd.DataFrame:
    X = df[FEATURE_COLUMNS]
    df = df.copy()
    df["predicted_units"] = model.predict(X).round(0).astype(int)
    return df


def get_feature_importance(model) -> pd.DataFrame:
    importance_df = pd.DataFrame({
        "feature": FEATURE_COLUMNS,
        "importance": model.feature_importances_
    }).sort_values("importance", ascending=False)
    return importance_df


if __name__ == "__main__":
    model, metrics = train_model()
    print("=== Model Evaluation ===")
    print(f"Mean Absolute Error: {metrics['mae']} units")
    print(f"R² Score: {metrics['r2_score']}")

    df = fetch_production_df()
    df_with_predictions = predict_for_all(model, df)
    print("\n=== Sample Predictions ===")
    print(df_with_predictions[
        ["production_date", "machine_id", "units_produced", "predicted_units"]
    ].head(10))

    print("\n=== Feature Importance ===")
    print(get_feature_importance(model))