import os
import subprocess
from dotenv import load_dotenv

load_dotenv()

def run(command, step):
    print(f"\n🔹 Step {step}: Running `{command}`")
    try:
        subprocess.run(command, shell=True, check=True)
        print(f"✅ Step {step} complete\n")
    except subprocess.CalledProcessError:
        print(f"❌ Step {step} failed\n")
        exit(1)

def has_unapplied_migrations():
    result = subprocess.run("alembic heads", shell=True, capture_output=True, text=True)
    heads = result.stdout.strip()
    current = subprocess.run("alembic current", shell=True, capture_output=True, text=True).stdout.strip()
    return heads not in current

print("🚀 Starting FastAPI Development Server")

# Step 0: Install dependencies from requirements.txt
run("pip install -r requirements.txt", 0)

# Step 1: Always autogenerate a new migration for any model changes
run('alembic revision --autogenerate -m "Auto migration"', 1)

# Step 2: Check and apply unapplied migrations
if has_unapplied_migrations():
    run("alembic upgrade head", 2)
else:
    print("✅ Step 2: Database is up to date. No migrations to apply.\n")

# Step 3: Start FastAPI server
run("uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload", 3)