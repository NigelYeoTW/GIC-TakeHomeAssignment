# Café Employee Manager

## Prerequisites

- [Docker](https://docs.docker.com/get-docker/) and Docker Compose

> For local development without Docker, you also need Python 3.11+, Node.js 20+, PostgreSQL, and [Poetry](https://python-poetry.org/docs/#installation).

---

## Running with Docker (recommended)

1. Copy the environment file and set a database password:

   ```bash
   cp .env.example .env
   ```

   Edit `.env` and set `DB_PASSWORD` to a value of your choice.

2. Build and start all services:

   ```bash
   docker compose up --build
   ```

3. In a separate terminal, seed the database with sample data:

   ```bash
   docker compose exec backend poetry run python seed.py
   ```

The app is available at `http://localhost`.
Backend API docs are available at `http://localhost:8000/docs`.

---

## Running locally (without Docker)

### Backend

1. Install dependencies:

   ```bash
   cd backend
   poetry install
   ```

2. Set up the environment file:

   ```bash
   cp .env.example .env.local
   ```

   Edit `backend/.env.local` and fill in your PostgreSQL credentials:

   ```env
   ENV=local
   DB_HOST=localhost
   DB_PORT=5432
   DB_NAME=cafe_manager
   DB_USER=postgres
   DB_PASSWORD=yourpassword
   UPLOAD_DIR=uploads
   ALLOWED_ORIGINS=["http://localhost:5173"]
   PORT=8000
   ```

3. Create the database:
    ```bash
    psql -U postgres -c "CREATE DATABASE cafe_manager;"
    ```
    > On Windows if `psql` is not recognised, use the full path: `& "C:\Program Files\PostgreSQL\{version}\bin\psql.exe" -U postgres -c "CREATE DATABASE cafe_manager;"`

4. Seed the database:

   **Mac/Linux:**
    ```bash
    ENV=local poetry run python seed.py
    ```
   **Windows:**
    ```powershell
    $env:ENV="local"; poetry run python seed.py
    ```

5. Start the API server:

   **Mac/Linux:**
    ```bash
    ENV=local poetry run uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
    ```
   **Windows:**
    ```powershell
    $env:ENV="local"; poetry run uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
    ```

   API available at `http://localhost:8000` · Interactive docs at `http://localhost:8000/docs`.

### Frontend

1. Install dependencies:

   ```bash
   cd frontend
   npm install
   ```

2. Start the dev server:

   ```bash
   npm run dev
   ```

   App available at `http://localhost:5173`.

   > Vite proxies `/api` and `/uploads` to `http://localhost:8000`, so no CORS configuration is needed locally.

---

## Running tests

**Mac/Linux:**
```bash
cd backend
ENV=local poetry run pytest
```

**Windows:**
```powershell
cd backend
$env:ENV="local"; poetry run pytest
```

---

## Live URL

https://gic-takehomeassignment-cafemanager.onrender.com/

---

## Architecture Notes

The backend follows a layered architecture where routers handle HTTP concerns, services contain business logic, and repositories abstract database access. Dependencies are injected via FastAPI's `Depends`, which serves the same role as Autofac in a .NET project, registering and resolving dependencies without tight coupling between layers. The project also applies the Mediator pattern to decouple request handling from business logic, though at this scale it is not strictly necessary. It was included intentionally to meet the assessment criteria and to demonstrate how the pattern would benefit a larger codebase where many handlers would otherwise need direct references to multiple services.
