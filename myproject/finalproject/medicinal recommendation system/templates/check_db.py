from main import db, app
from sqlalchemy import inspect

# Run inside the Flask app context
with app.app_context():
    inspector = inspect(db.engine)

    # List all tables
    tables = inspector.get_table_names()
    print("Tables in database:", tables)

    # If patient table exists, show its columns
    if "patient" in tables:
        columns = inspector.get_columns("patient")
        print("Patient table columns:")
        for col in columns:
            print(f"- {col['name']} ({col['type']})")
    else:
        print("❌ Patient table does not exist. Run db.create_all() to create it.")

