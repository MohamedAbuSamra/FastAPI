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

# Step 1: Start FastAPI server
run("uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload", 1)