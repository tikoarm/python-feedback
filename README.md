# 📝 Telegram Feedback Bot

A feedback collection bot for restaurants, built with **Python**, **aiogram**, **MySQL**, **Flask**, and **Docker**, featuring admin moderation, **Gemini AI** integration, analytics, and a simple PHP frontend. 
This project simulates real-world backend logic and integration in a clean, scalable architecture.

## 💡 Why This Project Matters

This bot simulates real-world backend challenges:  
handling authentication, database structure, user feedback logic, and admin moderation — all in a modular and production-like environment. It demonstrates my backend thinking and integration ability.

It also showcases logging architecture, code quality tooling (flake8 + black), and clean async design patterns.

---

## 🚀 Features

- 🔐 User registration (auto-detects Telegram ID & name)
- ⭐️ Users can rate the restaurant and leave a written review
- 👮 Admins can view and respond to user reviews  
  🚧 Admin reply system planned (moderation via bot)
- 🧾 User profile command with review stats
- 🧠 Cached review progress and admin list for faster access
- 🧠 Formatted review summaries with converted ratings and readable dates
- 🗂️ Linked admin replies to specific reviews
- 🪵 Logging and error tracking
- 📂 Online log viewer: view `info`, `warning`, or `error` logs through a PHP frontend
- 🌐 Simple frontend (PHP): renders user reviews via JSON API
- 🤖 Gemini AI integration
- 📊 Review analytics: stats by day, week, month, and average ratings
- 📦 Dockerized: includes MySQL & phpMyAdmin for local development
- 🧪 `code_check.py`: runs flake8 & black checks with timestamped logs
- 💬 messenger layer to decouple Telegram bot logic and avoid circular imports

---

## 📂 Project Structure

```
.
├── app/
│   ├── bot/
│   │   ├── handlers/            # Handlers for Telegram bot interactions
│   │   │   ├── profile_handler.py
│   │   │   └── admin_handler.py
│   │   ├── keyboard.py
│   │   ├── messenger.py            # Abstraction over Telegram bot for safe messaging
│   │   └── telegram_bot.py
│   ├── cache/
│   │   ├── admin.py             # Cached admin logic
│   │   └── api_keys.py          # API key cache and validation
│   ├── database/
│   │   ├── connection.py
│   │   ├── reviews.py
│   │   └── users.py
│   ├── logic/
│   │   └── functions.py         # Reusable logic and utilities
│   ├── web/
│   │   ├── api.py               # Flask API routes
│   │   └── gemini.py            # Gemini API integration
│   └── main.py                  # Entry point
├── docker-compose.yml
├── Dockerfile
├── .env
└── requirements.txt
```

---

## 🛠️ Technologies Used

- **Python 3.10**
- **aiogram 2.25.1**
- **MySQL 8.0**
- **Flask 2.3.3** — for exposing API endpoints
- **Docker & Docker Compose**
- **dotenv** — for environment variable management
- **aiohttp 3.8.6** — for async interaction with external services (e.g., Gemini)
- **google-generativeai** — Gemini AI for dynamic response generation
- **requests** — for HTTP calls from bot to Flask
- **multiprocessing** — to run Telegram bot and web server in parallel
- **phpMyAdmin** — included via Docker for local database management
- **Logging, error handling, async I/O**
- **flake8 & black** — code style checking and auto-formatting

---

## 🔌 API Endpoints

- `POST /apikey/add` — Generates a new API key  
- `GET /review_list/<user_id>` — Returns user reviews
- `GET /logs/view` — Shows all system logs

---

## 🔧 Work in Progress / Planned

- ✅ Admins can now reply to user reviews (with Telegram-based moderation)
- 🔄 Health check endpoint for uptime monitoring and CI/CD readiness
- 🖥️ VPS deployment complete — auto-start via systemd service (`utils/feedback.service`)
- 🔁 CI/CD pipeline planned: GitHub → auto-deploy to VPS container on push
- 📡 Secure exposure via NGINX reverse proxy with subdomain routing

---

## 🧠 Tech Highlights

- Uses `asyncio` and `aiogram` for high-concurrency Telegram handling  
- Modular architecture with separation of bot, logic, web, and cache  
- SQL logic written manually — no ORM used  
- Production-ready structure with environment separation and Docker  
- Admin dashboard logic with analytics & review moderation
- Internal code checker script with timestamped logs (flake8 + black)
- Unified messaging abstraction via `messenger.py` for clean communication

---

## 🧾 .env Configuration Example

```env
TG_TOKEN=your_telegram_token
TG_BOT_USERNAME=your_bot_username

GEMINI_API_KEY=your_gemini_api_key

MYSQL_HOST=db
MYSQL_PORT=3306
MYSQL_USER=root
MYSQL_PASSWORD=root
MYSQL_DATABASE=feedback_db

API_ADMIN_KEY=your_api_admin_key
API_DOMAIN=http://app:5050
```

---
## ✅ Code Quality

This repo includes a `code_check.py` script to run `flake8`, `black`, `isort`, and `bandit`, with timestamped logs for each check. This helps ensure code consistency, import order, and basic security hygiene.

Automated code checks are enforced via a script to maintain style, import sorting, and security best practices.

---

## 👨‍💻 Author

Developed by **Tigran Kocharov**  
GitHub: [tikoarm](https://github.com/tikoarm)  
📧 tiko.nue@icloud.com

---

## 🌍 Demo Access

- Website: [feedback.tikoarm.com](https://feedback.tikoarm.com)

> API and database access available on request.

---

## 📄 License & Use

This bot was developed for personal portfolio use.  
It may be reused for educational or non-commercial purposes with proper credit.
