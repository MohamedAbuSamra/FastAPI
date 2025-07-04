# FastAPI Backend Project

## Features

- User authentication with JWT
- Product and order management
- PostgreSQL with SQLAlchemy ORM
- Alembic migrations
- CSV import script for products
- Swagger UI at `/docs`

## Requirements

- **Python 3.9+** (The project was developed and tested with Python 3.11.7, but should work with any Python 3.9 or newer)

## Project Structure

```
app/
  core/        # Config, security, and core logic
  models/      # SQLAlchemy models
  schemas/     # Pydantic schemas
  routers/     # API endpoints
  db.py        # Database session and engine
  main.py      # FastAPI app entrypoint
scripts/
  seed_data.py        # Seeds products and users from CSV files
alembic/      # Database migrations
seed/         # CSV files for initial data (products, users)
requirements.txt
.env           # Environment variables
```

## 🚀 Quickstart (One Command)

To get started, you can run either of the following scripts:

### 🔹 One-time Setup (Bootstrap)

Use this when running the project for the first time to set up the database and seed it with initial data:

```bash
python scripts/bootstrap.py
```

This script performs the following:

1. Creates the local PostgreSQL database (if not already created)
2. Seeds initial data into `products` and `users` tables from CSV files located in the `seed/` folder

### 🔹 Development Launch

Use this every time you want to start the development server:

```bash
python scripts/prepare.py
```

This script performs the following:

1. Installs dependencies from `requirements.txt`
2. Generates Alembic migrations (if none exist)
3. Applies migrations
4. Starts the FastAPI development server at `http://localhost:8000`

### 🔹 Seed Data Only

If you want to seed the products and users tables (without creating the database), use:

```bash
python scripts/seed_data.py
```

This script will:

1. Seed initial data into `products` and `users` tables from CSV files located in the `seed/` folder

---

## ⚙️ Manual Setup (Step by Step)

1. (Recommended) Create and activate a virtual environment:

   ```bash
   python -m venv .venv
   source .venv/bin/activate  # On Windows use `.venv\Scripts\activate`
   ```

2. Install dependencies:

   ```bash
   pip install -r requirements.txt
   ```

3. Set up `.env` with your database URL, user, password, and secret key:

   ```env
   DATABASE_URL=postgresql://postgres:your_password@localhost:5432/game_api_db
   SECRET_KEY=your_secret_key_here
   ```

4. (Optional) To create a local PostgreSQL database and apply migrations automatically, run:

   ```bash
   python scripts/setup_db.py
   ```

   - This script creates the `game_api_db` database locally and runs Alembic migrations.
   - ⚠️ Skip this step if you are using a cloud-hosted database like Render.com, GCP, or any alternative PostgreSQL host and have set the `DATABASE_URL` accordingly.

5. Generate initial migration files (for tables) from your models:

   ```bash
   alembic revision --autogenerate -m "Initial tables"
   ```

6. Run migrations:

   ```bash
   alembic upgrade head
   ```

7. Start server:

   ```bash
   uvicorn app.main:app --reload
   ```

8. Open the server on this port `http://localhost:8000/`

9. Access Swagger docs at: `http://localhost:8000/docs`

---

## 📁 Files and Folders to Ignore

The following files and folders are ignored by git (see `.gitignore`) and should not be committed:

- `.env`, `.env.*` – Environment variables and secrets
- `.venv/` – Local Python virtual environment
- `__pycache__/`, `*.pyc`, `*.pyo`, `*.pyd` – Python cache/bytecode
- `.DS_Store` – macOS system files
- `.vscode/` – VS Code editor settings
- `.mypy_cache/`, `.pytest_cache/` – Test/type checking caches
- `*.log` – Log files
- Alembic and app subfolder caches

These are ignored to keep your repository clean and secure.

See code for details on endpoints and usage.
