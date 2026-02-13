"""Add missing columns to investor_profiles table."""
import sqlite3

conn = sqlite3.connect('elida.db')
cursor = conn.cursor()

# Check existing columns
cursor.execute('PRAGMA table_info(investor_profiles)')
existing_cols = [col[1] for col in cursor.fetchall()]
print(f"Existing columns: {existing_cols}")

# Add ethical_filters if missing
if 'ethical_filters' not in existing_cols:
    cursor.execute('ALTER TABLE investor_profiles ADD COLUMN ethical_filters TEXT DEFAULT "[]"')
    print("Added ethical_filters column")
else:
    print("ethical_filters already exists")

# Add investment_horizon if missing
if 'investment_horizon' not in existing_cols:
    cursor.execute('ALTER TABLE investor_profiles ADD COLUMN investment_horizon TEXT DEFAULT "3-5 years"')
    print("Added investment_horizon column")
else:
    print("investment_horizon already exists")

conn.commit()

# Verify
cursor.execute('PRAGMA table_info(investor_profiles)')
final_cols = [col[1] for col in cursor.fetchall()]
print(f"Final columns: {final_cols}")

conn.close()
print("Done!")
