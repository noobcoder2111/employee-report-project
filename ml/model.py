import pandas as pd
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_absolute_error, r2_score

from database.read_data import fetch_employees_df

FEATURE_COLUMNS = [
    "experience_years",
    "attendance_percentage",
    "training_hours",
    "projects_completed",
    "leave_days",
    "salary",
]
TARGET_COLUMN = "performance_score"


def prepare_data(df: pd.DataFrame):
    """Selects features/target and drops incomplete rows."""
    data = df[FEATURE_COLUMNS + [TARGET_COLUMN]].dropna()
    X = data[FEATURE_COLUMNS]
    y = data[TARGET_COLUMN]
    return X, y


def train_model():
    """
    Trains a RandomForestRegressor to predict performance_score
    from employee work-pattern features. Returns the trained model
    plus evaluation metrics on a held-out test set.
    """
    df = fetch_employees_df()
    X, y = prepare_data(df)

    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42
    )

    model = RandomForestRegressor(n_estimators=100, random_state=42)
    model.fit(X_train, y_train)

    predictions = model.predict(X_test)
    mae = mean_absolute_error(y_test, predictions)
    r2 = r2_score(y_test, predictions)

    return model, {"mae": round(mae, 3), "r2_score": round(r2, 3)}


def predict_for_all(model, df: pd.DataFrame) -> pd.DataFrame:
    """Adds a predicted_performance column for every employee."""
    X = df[FEATURE_COLUMNS]
    df = df.copy()
    df["predicted_performance"] = model.predict(X).round(2)
    return df


def get_feature_importance(model) -> pd.DataFrame:
    """Shows which features the model relied on most."""
    importance_df = pd.DataFrame({
        "feature": FEATURE_COLUMNS,
        "importance": model.feature_importances_
    }).sort_values("importance", ascending=False)
    return importance_df


if __name__ == "__main__":
    model, metrics = train_model()
    print("=== Model Evaluation ===")
    print(f"Mean Absolute Error: {metrics['mae']}")
    print(f"R² Score: {metrics['r2_score']}")

    df = fetch_employees_df()
    df_with_predictions = predict_for_all(model, df)
    print("\n=== Sample Predictions ===")
    print(df_with_predictions[
        ["employee_id", "employee_name", "performance_score", "predicted_performance"]
    ].head(10))

    print("\n=== Feature Importance ===")
    print(get_feature_importance(model))