import sqlite3
import os

db_path = 'e:\\代码记录\\Python\\客户定制\\技能树\\instance\\skill_tree.db'

def migrate():
    if not os.path.exists(db_path):
        print(f"DB not found at {db_path}")
        return

    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    try:
        # Check if 'mode' column exists
        cursor.execute("PRAGMA table_info(skill_trees)")
        columns = [column[1] for column in cursor.fetchall()]
        
        if 'mode' not in columns:
            print("Adding 'mode' column to 'skill_trees'...")
            cursor.execute("ALTER TABLE skill_trees ADD COLUMN mode TEXT DEFAULT 'tree'")
            conn.commit()
            print("Migration successful.")
        else:
            print("'mode' column already exists.")

    except Exception as e:
        print(f"Error during migration: {e}")
    finally:
        conn.close()

if __name__ == "__main__":
    migrate()
