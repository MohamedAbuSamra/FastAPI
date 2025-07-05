# Game Store API

**Live Demo:** [https://game-store-fastapi.onrender.com](https://game-store-fastapi.onrender.com)

# FastAPI Backend Project

> **Note:** Before starting, create a `.env` file in the project root with the following content (adjust values as needed):
>
> ```env
> DATABASE_URL=postgresql://postgres:your_password@localhost:5432/game_api_db
> SECRET_KEY=b7e2c8e1c9f44e2e8a1d4f6b7c2e5a8f9d3c6b1a7e4f2c9d8b6a3e7c5f1b2d4a
> ALGORITHM=HS256
> ACCESS_TOKEN_EXPIRE_MINUTES=30
> ```
>
> The default local database connection details (DB name, user, password, host, port) can be found in `scripts/setup_db.py`.

## Features

- User authentication with JWT
- Product and order management
- PostgreSQL with SQLAlchemy ORM
- Alembic migrations
- CSV import script for products
- Swagger UI at `/docs`

### 🗂️ Database Schema Overview

The PostgreSQL database consists of four main tables, all using **timestamp fields** (`created_at`, `updated_at`, `deleted_at`) for data lifecycle tracking and **soft deletion**.

- **users**: Stores account credentials and timestamps for tracking registration, updates, and soft deletions.
- **products**: Contains item details (name, price, description, etc.) and country-based `location`. Includes lifecycle timestamps.
- **orders**: Records purchase history by linking users to products. Tracks order creation and supports soft delete.
- **countries**: Static reference table mapping ISO codes to country names.

#### 🧩 ER Diagram

```
users (id, created_at, updated_at, deleted_at)
products (id, location → countries.iso, created_at, updated_at, deleted_at)
orders (user_id → users.id, product_id → products.id, created_at, updated_at, deleted_at)
countries (iso, name)
```

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
templates/    # HTML templates for the app (e.g., landing page)
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
2. Starts the FastAPI development server at `http://localhost:8000`

> **Note:** Database migrations are now handled manually. See the section below for migration commands.

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
   SECRET_KEY=b7e2c8e1c9f44e2e8a1d4f6b7c2e5a8f9d3c6b1a7e4f2c9d8b6a3e7c5f1b2d4a
   # For production, generate your own strong random secret key!
   ```

4. (Optional) To create a local PostgreSQL database and apply migrations automatically, run:

   ```bash
   python scripts/setup_db.py
   ```

   - This script creates the `game_api_db` database locally and runs Alembic migrations.
   - ⚠️ Skip this step if you are using a cloud-hosted database like Render.com, GCP, or any alternative PostgreSQL host and have set the `DATABASE_URL` accordingly.

---

## 🛠️ Database Migration Commands (Manual)

> **Note:** Migrations are no longer handled automatically by `scripts/prepare.py`. Use the following Alembic commands to manage migrations manually:

- **Create a new migration after changing models:**

  ```bash
  alembic revision --autogenerate -m "Describe your migration"
  ```

- **Apply all pending migrations:**

  ```bash
  alembic upgrade head
  ```

- **Check current migration state:**

  ```bash
  alembic current
  ```

- **Show all migration history:**

  ```bash
  alembic history
  ```

---

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

See code for details on endpoints and usage.

- Example users are provided in the seed data (see `seed/users.csv`). You can use these credentials to log in, obtain a JWT token, and use the system:
  - Username: `admin`, Password: `admin`
  - Username: `m.abusamra`, Password: `123456`
