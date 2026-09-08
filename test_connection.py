from database.db import get_connection

try:
    conn = get_connection()
    print("✅ Connected to PostgreSQL successfully!")

    # Quick check: ask PostgreSQL for its version
    cursor = conn.cursor()
    cursor.execute("SELECT version();")
    db_version = cursor.fetchone()
    print("PostgreSQL version:", db_version)

    cursor.close()
    conn.close()
    print("Connection closed.")

except Exception as e:
    print("❌ Connection failed.")
    print("Error:", e)