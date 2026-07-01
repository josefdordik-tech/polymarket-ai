import sqlite3

DB = "poly.db"

def init_db():
    conn = sqlite3.connect(DB)
    cur = conn.cursor()

    cur.execute("""
    CREATE TABLE IF NOT EXISTS markets (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        question TEXT,
        slug TEXT UNIQUE,
        volume REAL,
        liquidity REAL,
        token_yes TEXT,
        token_no TEXT,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
    """)

    cur.execute("""
    CREATE TABLE IF NOT EXISTS price_ticks (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        market_slug TEXT,
        token_id TEXT,
        price REAL,
        side TEXT,
        ts TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
    """)

    conn.commit()
    conn.close()

if __name__ == "__main__":
    init_db()
    print("DB READY")
