
from agency_swarm.tools import BaseTool
from pydantic import Field
import sqlite3

class ProductDatabaseTool(BaseTool):
    query: str = Field(..., description="The SQL SELECT query to run.")
    db_path: str = Field(default="db/product_manager.db", description="Path to the SQLite database.")

    def run(self) -> str:
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            cursor.execute(self.query)
            rows = cursor.fetchall()
            columns = [desc[0] for desc in cursor.description]
            result = [dict(zip(columns, row)) for row in rows]
            conn.close()
            return f"✅ Query returned {len(result)} rows:\n{result}"
        except Exception as e:
            return f"❌ Error running query: {e}"
