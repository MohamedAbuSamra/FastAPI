import psycopg2
import subprocess

DB_NAME = "game_api_db"
DB_USER = "postgres"
DB_PASSWORD = "123456" 
DB_HOST = "localhost"
DB_PORT = "5432"

def create_db():
    try:
        conn = psycopg2.connect(
            dbname="postgres", user=DB_USER, password=DB_PASSWORD, host=DB_HOST, port=DB_PORT
        )
        conn.autocommit = True
        cur = conn.cursor()
        cur.execute(f"SELECT 1 FROM pg_database WHERE datname = '{DB_NAME}'")
        exists = cur.fetchone()
        if not exists:
            cur.execute(f"CREATE DATABASE {DB_NAME}")
            print(f"✅ Created database '{DB_NAME}'")
        else:
            print(f"⚠️  Database '{DB_NAME}' already exists")
        cur.close()
        conn.close()
    except Exception as e:
        print("❌ DB creation failed:", e)

def run_migrations():
    print("📦 Running Alembic migrations...")
    subprocess.run(["alembic", "upgrade", "head"])

if __name__ == "__main__":
    create_db()
    run_migrations()