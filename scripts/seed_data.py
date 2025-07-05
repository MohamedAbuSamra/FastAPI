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

print("🚀 Seeding FastAPI Database Data (Countries, Products & Users)")

# Step 1: Seed countries
run("python scripts/import_data.py country seed/countries.csv", 1)

# Step 2: Seed products
run("python scripts/import_data.py product seed/products.csv", 2)

# Step 3: Seed users
run("python scripts/import_data.py user seed/users.csv", 3)

print("🏁 Seeding complete. You can now run `python scripts/prepare.py` to launch the server.") 