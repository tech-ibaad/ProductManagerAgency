
import sqlite3

def initialize_product_db(path='db/product_manager.db'):
    conn = sqlite3.connect(path)
    cursor = conn.cursor()
    cursor.execute("PRAGMA foreign_keys = ON;")
    cursor.executescript("""
    CREATE TABLE IF NOT EXISTS Product_Categories (
        category_id TEXT PRIMARY KEY,
        name TEXT NOT NULL
    );
    CREATE TABLE IF NOT EXISTS Products (
        product_id TEXT PRIMARY KEY,
        name TEXT NOT NULL,
        description TEXT,
        category_id TEXT,
        status TEXT,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY (category_id) REFERENCES Product_Categories(category_id)
    );
    CREATE TABLE IF NOT EXISTS Features (
        feature_id TEXT PRIMARY KEY,
        product_id TEXT,
        name TEXT NOT NULL,
        description TEXT,
        status TEXT,
        priority INTEGER,
        FOREIGN KEY (product_id) REFERENCES Products(product_id)
    );
    CREATE TABLE IF NOT EXISTS Teams (
        team_id TEXT PRIMARY KEY,
        name TEXT NOT NULL,
        type TEXT
    );
    CREATE TABLE IF NOT EXISTS Team_Members (
        member_id TEXT PRIMARY KEY,
        name TEXT NOT NULL,
        role TEXT,
        email TEXT,
        team_id TEXT,
        FOREIGN KEY (team_id) REFERENCES Teams(team_id)
    );
    CREATE TABLE IF NOT EXISTS Tasks (
        task_id TEXT PRIMARY KEY,
        feature_id TEXT,
        assigned_to TEXT,
        title TEXT,
        status TEXT,
        due_date DATE,
        FOREIGN KEY (feature_id) REFERENCES Features(feature_id),
        FOREIGN KEY (assigned_to) REFERENCES Team_Members(member_id)
    );
    CREATE TABLE IF NOT EXISTS AI_Insights (
        insight_id TEXT PRIMARY KEY,
        product_id TEXT,
        generated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        type TEXT,
        content TEXT,
        FOREIGN KEY (product_id) REFERENCES Products(product_id)
    );
    CREATE TABLE IF NOT EXISTS User_Feedback (
        feedback_id TEXT PRIMARY KEY,
        product_id TEXT,
        source TEXT,
        content TEXT,
        rating INTEGER,
        submitted_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY (product_id) REFERENCES Products(product_id)
    );
    """)
    conn.commit()
    conn.close()
    print("📦 Database initialized.")

if __name__ == "__main__":
    initialize_product_db()
