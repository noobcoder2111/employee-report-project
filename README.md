# Employee AI/ML Report Dashboard

A full-stack demo project that stores employee data in PostgreSQL, analyzes it with pandas, predicts performance scores using a machine learning model, and displays everything in a live, dynamic web dashboard built with Flask.

## Architecture

User → Browser → Flask → PostgreSQL → Pandas → ML Model → Report → HTML/CSS/JS → Browser


- **PostgreSQL** stores all employee records (source of truth)
- **Flask** serves the web app and coordinates data flow on every request
- **Pandas** reads data from PostgreSQL and computes report metrics
- **Scikit-learn (RandomForestRegressor)** predicts each employee's performance score
- **Jinja2 + Bootstrap + Chart.js** render the dashboard in the browser

## Tech Stack

- Backend: Python, Flask
- Database: PostgreSQL, psycopg2
- Data/ML: pandas, numpy, scikit-learn
- Frontend: HTML, CSS, Bootstrap, Chart.js
- Config: python-dotenv (.env) for secure credentials

## Project Structure


employee-report-project/
├── app.py # Flask entry point, main route
├── requirements.txt
├── .env # DB credentials (not committed)
├── database/
│ ├── db.py # Connection logic
│ ├── create_table.py # Table schema
│ └── read_data.py # Fetches data as DataFrame
├── data/
│ ├── generate_data.py # Dummy data generator
│ └── insert_data.py # Inserts data into PostgreSQL
├── ml/
│ └── model.py # Trains RandomForestRegressor, predicts scores
├── reports/
│ └── analysis.py # Pandas-based metric calculations
├── templates/
│ └── index.html # Dashboard UI (Jinja2 + Bootstrap + Chart.js)
└── static/
└── css/style.css # Custom styling





## ML Component

**Problem type:** Regression
**Target:** `performance_score` (1.0–5.0 scale)
**Features:** `experience_years`, `attendance_percentage`, `training_hours`, `projects_completed`, `leave_days`, `salary`
**Algorithm:** RandomForestRegressor (100 trees)
**Evaluation:** Mean Absolute Error (MAE) ≈ 0.25, R² ≈ 0.66 on held-out test data (80/20 split)
**Most important feature:** `experience_years` (~39% importance), followed by `training_hours` (~21%)

The model trains once when the Flask app starts, then predicts a score for every employee on every page load using their live database values.

## How to Run

1. Activate the virtual environment:
```powershell
   .\venv\Scripts\Activate.ps1
```
2. Install dependencies (first time only):
```powershell
   pip install -r requirements.txt
```
3. Ensure `.env` contains valid PostgreSQL credentials.
4. Create the table (first time only):
```powershell
   python -m database.create_table
```
5. Generate and insert dummy data (first time only):
```powershell
   python -m data.insert_data
```
6. Run the app:
```powershell
   python app.py
```
7. Open your browser to `http://127.0.0.1:5000/`

## Common Errors & Solutions

| Error | Cause | Fix |
|---|---|---|
| `ModuleNotFoundError: No module named 'database'` | Ran a script directly instead of as a module | Use `python -m database.script_name` from the project root |
| PowerShell blocks activation script | Execution policy restriction | `Set-ExecutionPolicy -Scope CurrentUser -ExecutionPolicy RemoteSigned` |
| `password authentication failed` | Wrong `.env` credentials | Check `DB_USER`/`DB_PASSWORD` in `.env` |
| Pandas/numpy fail to install (Meson/vswhere errors) | Package version predates Python 3.14 wheel support | Use `pandas>=2.3.3`, `numpy>=2.3.2` |