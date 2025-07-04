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
  import_products.py  # CSV import script
alembic/      # Database migrations
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

---

## ⚙️ Manual Setup (Step by Step)

1. Install dependencies:

   ```bash
   pip install -r requirements.txt
   ```

2. Set up `.env` with your database URL, user, password, and secret key:

   ```env
   DATABASE_URL=postgresql://postgres:your_password@localhost:5432/game_api_db
   SECRET_KEY=your_secret_key_here
   ```

3. (Optional) To create a local PostgreSQL database and apply migrations automatically, run:

   ```bash
   python scripts/setup_db.py
   ```

   - This script creates the `game_api_db` database locally and runs Alembic migrations.
   - ⚠️ Skip this step if you are using a cloud-hosted database like Render.com, GCP, or any alternative PostgreSQL host and have set the `DATABASE_URL` accordingly.

4. Generate initial migration files (for tables) from your models:

   ```bash
   alembic revision --autogenerate -m "Initial tables"
   ```

5. Run migrations:

   ```bash
   alembic upgrade head
   ```

6. Start server:

   ```bash
   uvicorn app.main:app --reload
   ```

7. Open the server on this port `http://localhost:8000/`

8. Access Swagger docs at: `http://localhost:8000/docs`

---

See code for details on endpoints and usage.
