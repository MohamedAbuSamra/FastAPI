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

print("🚀 Starting FastAPI Development Server")

# Step 0: Install dependencies from requirements.txt
run("pip install -r requirements.txt", 0)

# Step 1: Generate migrations if needed
if not os.listdir("alembic/versions"):
    run('alembic revision --autogenerate -m "Initial tables"', 1)
else:
    print("🔸 Step 1: Migration file already exists, skipping autogenerate.")

# Step 2: Apply migrations
run("alembic upgrade head", 2)

# Step 3: Start FastAPI server
run("uvicorn app.main:app --reload", 3)