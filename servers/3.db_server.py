import sqlite3
import json
from mcp.server.fastmcp import FastMCP

DB_PATH = "data.db"
mcp = FastMCP("SQLiteServer")

def init_db():
    conn = sqlite3.connect(DB_PATH)
    conn.execute("CREATE TABLE IF NOT EXISTS users (id INTEGER PRIMARY KEY, name TEXT, email TEXT)")
    conn.commit()
    conn.close()

init_db()

@mcp.tool()
def query(sql: str) -> str:
    """Execute a SELECT query and return JSON."""
    try:
        conn = sqlite3.connect(DB_PATH)
        cur = conn.cursor()
        cur.execute(sql)
        rows = cur.fetchall()
        cols = [desc[0] for desc in cur.description] if cur.description else []
        result = [dict(zip(cols, row)) for row in rows]
        conn.close()
        return json.dumps(result, indent=2)
    except Exception as e:
        return f"Error: {e}"

@mcp.tool()
def insert(table: str, data: str) -> str:
    """Insert a row (data as JSON object) into a table."""
    try:
        record = json.loads(data)
        columns = ', '.join(record.keys())
        placeholders = ', '.join(['?' for _ in record])
        values = list(record.values())
        conn = sqlite3.connect(DB_PATH)
        cur = conn.cursor()
        cur.execute(f"INSERT INTO {table} ({columns}) VALUES ({placeholders})", values)
        conn.commit()
        conn.close()
        return f"Inserted into {table}"
    except Exception as e:
        return f"Error: {e}"

if __name__ == "__main__":
    mcp.run()