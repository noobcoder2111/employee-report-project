from flask import Flask, render_template, request, send_file, make_response
import io
import pandas as pd

from database.read_data import fetch_production_df
from reports.analysis import (
    get_summary_metrics,
    get_machine_breakdown,
    get_product_breakdown,
    get_shift_breakdown,
    get_daily_trend,
    filter_by_date,
)
from ml.model import train_model, predict_for_all, get_feature_importance

app = Flask(__name__)

trained_model, model_metrics = train_model()


def get_filtered_data():
    """Reads DB and applies date filter if the user selected one."""
    df = fetch_production_df()
    df["production_date"] = df["production_date"].astype(str)
    selected_date = request.args.get("date", "")
    if selected_date:
        df = filter_by_date(df, selected_date)
    return df, selected_date


def build_report_context():
    df, selected_date = get_filtered_data()

    summary = get_summary_metrics(df)
    machines = get_machine_breakdown(df)
    products = get_product_breakdown(df)
    shifts = get_shift_breakdown(df)
    daily_trend = get_daily_trend(df)

    df_with_predictions = predict_for_all(trained_model, df) if len(df) > 0 else df
    feature_importance = get_feature_importance(trained_model)

    return {
        "summary": summary,
        "machines": machines.to_dict(orient="records"),
        "products": products.to_dict(orient="records"),
        "shifts": shifts.to_dict(orient="records"),
        "daily_trend": daily_trend.to_dict(orient="records"),
        "records": df_with_predictions.to_dict(orient="records"),
        "model_metrics": model_metrics,
        "feature_importance": feature_importance.to_dict(orient="records"),
        "selected_date": selected_date,
    }


@app.route("/")
def home():
    context = build_report_context()
    return render_template("index.html", **context)


@app.route("/download/excel")
def download_excel():
    df, _ = get_filtered_data()
    output = io.BytesIO()
    with pd.ExcelWriter(output, engine="openpyxl") as writer:
        df.to_excel(writer, index=False, sheet_name="Production Report")
    output.seek(0)
    return send_file(
        output,
        mimetype="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
        as_attachment=True,
        download_name="production_report.xlsx",
    )


@app.route("/download/pdf")
def download_pdf():
    from reportlab.lib.pagesizes import landscape, A4
    from reportlab.lib import colors
    from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer
    from reportlab.lib.styles import getSampleStyleSheet

    df, selected_date = get_filtered_data()

    buffer = io.BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=landscape(A4))
    styles = getSampleStyleSheet()
    elements = []

    title_text = "Soap Factory Production Report"
    if selected_date:
        title_text += f" — {selected_date}"
    elements.append(Paragraph(title_text, styles["Title"]))
    elements.append(Spacer(1, 12))

    summary = get_summary_metrics(df)
    summary_lines = [f"{k.replace('_', ' ').title()}: {v}" for k, v in summary.items()]
    for line in summary_lines:
        elements.append(Paragraph(line, styles["Normal"]))
    elements.append(Spacer(1, 20))

    table_data = [list(df.columns)] + df.astype(str).values.tolist()
    table = Table(table_data, repeatRows=1)
    table.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#1a2a3a")),
        ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
        ("FONTSIZE", (0, 0), (-1, -1), 6),
        ("GRID", (0, 0), (-1, -1), 0.5, colors.grey),
        ("ROWBACKGROUNDS", (0, 1), (-1, -1), [colors.white, colors.HexColor("#f4f6f9")]),
    ]))
    elements.append(table)

    doc.build(elements)
    buffer.seek(0)

    return send_file(
        buffer,
        mimetype="application/pdf",
        as_attachment=True,
        download_name="production_report.pdf",
    )


if __name__ == "__main__":
    import os
    port = int(os.environ.get("PORT", 5000))
    app.run(debug=True, host="0.0.0.0", port=port)