from flask import Flask, render_template

from database.read_data import fetch_employees_df
from reports.analysis import (
    get_summary_metrics,
    get_department_breakdown,
    get_top_performers,
    get_low_performers,
    get_joins_by_year,
)
from ml.model import train_model, predict_for_all, get_feature_importance

app = Flask(__name__)

# Train the model once when the app starts, so we don't retrain on every page load
trained_model, model_metrics = train_model()


@app.route("/")
def home():
    df = fetch_employees_df()

    summary = get_summary_metrics(df)
    departments = get_department_breakdown(df)
    top_performers = get_top_performers(df)
    low_performers = get_low_performers(df)
    joins_by_year = get_joins_by_year(df)

    df_with_predictions = predict_for_all(trained_model, df)
    feature_importance = get_feature_importance(trained_model)

    return render_template(
        "index.html",
        summary=summary,
        departments=departments.to_dict(orient="records"),
        top_performers=top_performers.to_dict(orient="records"),
        low_performers=low_performers.to_dict(orient="records"),
        joins_by_year=joins_by_year.to_dict(orient="records"),
        employees=df_with_predictions.to_dict(orient="records"),
        model_metrics=model_metrics,
        feature_importance=feature_importance.to_dict(orient="records"),
    )


if __name__ == "__main__":
    import os
    port = int(os.environ.get("PORT", 5000))
    app.run(debug=True, host="0.0.0.0", port=port)