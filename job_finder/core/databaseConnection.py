import os
import psycopg2
from dotenv import load_dotenv

load_dotenv()

class DatabaseConnection:
    def __init__(self):
        self.connection = None
        self.cursor = None

    def connect(self):
        """Establish a database connection."""
        try:
            self.connection = psycopg2.connect(
                user=os.getenv("user"),
                password=os.getenv("password"),
                host=os.getenv("host"),
                port=os.getenv("port"),
                dbname=os.getenv("dbname")
            )
            self.cursor = self.connection.cursor()
            print("Database connection established.")
        except Exception as e:
            print(f"Database connection failed: {e}")
            raise e

    def execute(self, query, params=None):
        """Safely execute a SQL query."""
        try:
            self.cursor.execute(query, params)
        except Exception as e:
            print(f"SQL execution failed: {e}")
            print("Query:", query)
            print("Params:", params)
            raise e

    def commit(self):
        """Commit the transaction."""
        if self.connection:
            self.connection.commit()

    def close(self):
        """Close cursor + connection."""
        try:
            if self.cursor:
                self.cursor.close()
            if self.connection:
                self.connection.close()
            print("✓ Database connection closed.")
        except Exception as e:
            print(f"⚠ Error closing database connection: {e}")


if __name__ == "__main__":
    db = DatabaseConnection()
    try:
        db.connect()
        # Lightweight connectivity check (non-destructive).
        db.execute("SELECT NOW();")
        print("Current database time:", db.cursor.fetchone()[0])
    except Exception as e:
        print(f"Operation failed: {e}")
    finally:
        db.close()
