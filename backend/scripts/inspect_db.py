"""Utility script to inspect the contents of runix_dev.db."""

import sqlite3
from pathlib import Path

db_path = Path("runix_dev.db")
if not db_path.exists():
    # Also check backend/runix_dev.db
    alt_path = Path("backend/runix_dev.db")
    if alt_path.exists():
        db_path = alt_path
    else:
        print("Database file runix_dev.db not found.")
        exit(1)

conn = sqlite3.connect(db_path)
cursor = conn.cursor()

tables_query = (
    "SELECT name FROM sqlite_master WHERE type='table' AND name NOT LIKE 'sqlite_%';"
)
tables = cursor.execute(tables_query).fetchall()

print(f"\n[Database]: {db_path.resolve()}\n")
print(f"{'TABLE NAME':<25} {'ROW COUNT':<10}")
print("-" * 35)

for (t,) in tables:
    # Safe table name inspection for local development utility
    count = cursor.execute(f"SELECT count(*) FROM [{t}];").fetchone()[0]  # noqa: S608
    print(f"{t:<25} {count:<10}")

print("\n" + "=" * 50)
print("[USERS]:")
print("-" * 50)
for row in cursor.execute("SELECT id, email, display_name FROM users LIMIT 5;"):
    print(f"ID: {row[0]}\nEmail: {row[1]}\nName: {row[2]}\n")

print("=" * 50)
print("[PROJECTS]:")
print("-" * 50)
proj_query = "SELECT id, name, slug, template, visibility FROM projects LIMIT 5;"
for row in cursor.execute(proj_query):
    print(
        f"ID: {row[0]}\nName: {row[1]}\nSlug: {row[2]}\n"
        f"Template: {row[3]}\nVisibility: {row[4]}\n"
    )

conn.close()
