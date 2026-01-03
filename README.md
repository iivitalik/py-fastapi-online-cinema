# 🎬 Cinema API Service

<p align="center">
  <img src="https://img.shields.io/badge/FastAPI-005571?style=for-the-badge&logo=fastapi" alt="FastAPI">
  <img src="https://img.shields.io/badge/PostgreSQL-316192?style=for-the-badge&logo=postgresql" alt="Postgres">
  <img src="https://img.shields.io/badge/Docker-2496ED?style=for-the-badge&logo=docker" alt="Docker">
  <img src="https://img.shields.io/badge/Celery-37814A?style=for-the-badge&logo=celery" alt="Celery">
</p>

A high-performance Cinema Management API built with **FastAPI**. This project features a robust microservice architecture including a shopping cart system, user interactions (likes, ratings, comments), and automated background tasks for security token management.

---

## 🌟 Key Features

### 🔐 Security & Auth
* **JWT Authentication** — Secure login and session management with access/refresh tokens.
* **Email Activation** — User registration flow with automated activation via unique tokens.
* **Role-Based Access** — Permission levels for `USER`, `MODERATOR`, and `ADMIN`.

### 🎬 Movie Catalog Logic
* **Advanced Filtering** — Search movies by title, year, IMDb score, or genres.
* **User Interactions** — Like/dislike system, numerical ratings (1-10), and "Favorites" list.
* **Comments** — Review system with support for nested replies.

### 🛒 Commerce System
* **Shopping Cart** — Manage items before purchase.
* **Checkout** — Secure purchase logic that prevents duplicate acquisitions.

### ⚙️ Background Tasks & Infrastructure
* **Celery Worker** — Periodic cleanup of expired activation and reset tokens.
* **Dockerized** — Fully containerized environment (PostgreSQL, Redis, Celery, App).

---

## 🚀 Installation & Run

###  Run 
```bash
docker-compose up --build
git clone [https://github.com/iivitalik/py-fastapi-online-cinema.git]
cd cinema-api

python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt

python -m app.seed

uvicorn app.main:app --reload
```

## 🛠 Project Structure

| Directory / File | Responsibility |
| :--- | :--- |
| **`app/main.py`** | Application entry point and router registration |
| **`app/database.py`** | Database connection and SessionLocal configuration |
| **`app/models.py`** | SQLAlchemy database models (Tables) |
| **`app/schemas.py`** | Pydantic models for data validation (DTOs) |
| **`app/routers/`** | API route modules (Auth, Movies, Cart, Admin, Interactions) |
| **`app/utils/`** | Security helpers, JWT logic, and shared utilities |
| **`app/worker/`** | Celery task definitions and background processing |
| **`app/seed/`** | Scripts for populating the database with initial data |
| **`docker-compose.yml`** | Multi-container Docker infrastructure configuration |

## 📊 Visual Previews

### 🔐 Docs
<div align="center">

| Interactive Swagger (Docs) |
|:---:|
| <img src="images/doc.png" width="800"> |

</div>
