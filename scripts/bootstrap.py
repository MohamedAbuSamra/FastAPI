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

print("🚀 Bootstrapping FastAPI Database and Seeding Data")

# Step 1: Create database and apply migration
run("python scripts/setup_db.py", 1)

# Step 2: Seed products
run("python scripts/import_data.py product seed/products.csv", 2)

# Step 3: Seed users
run("python scripts/import_data.py user seed/users.csv", 3)

print("🏁 Bootstrap complete. You can now run `python scripts/prepare.py` to launch the server.")