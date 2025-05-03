> ⚠️ This project is still under active development. Features and structure may change.
# 📝 Telegram Feedback Bot

A feedback collection bot for restaurants, built with **Python**, **aiogram**, **MySQL**, and **Docker**.  
This project was designed to simulate real-world backend logic and integration in a clean, scalable architecture.

---

## 🚀 Features

- 🔐 User registration (auto-detects Telegram ID & name)
- ⭐️ Users can rate the restaurant and leave a written review
- 👮 Admins can view and respond to user reviews
- 🧾 User profile command with review stats
- 🧠 Cached review progress and admin list for faster access
- 🧠 Formatted review summaries with converted ratings and readable dates
- 🗂️ Linked admin replies to specific reviews
- 🪵 Logging and error tracking
- 🌐 Planned web interface (PHP frontend reading JSON from Python backend)
- 🤖 Gemini AI integration (planned: auto-generating admin replies)
- 📊 Review analytics (planned)
- 📦 Dockerized: includes MySQL & phpMyAdmin for local development

---

## 📂 Project Structure

```
.
├── app/
│   ├── bot/
│   │   ├── handlers/            # Handlers for Telegram bot interactions
│   │   │   └── profile_handler.py
│   │   ├── keyboard.py
│   │   └── telegram_bot.py
│   ├── cache/
│   │   └── admin.py             # Cached admin logic
│   ├── database/
│   │   ├── connection.py
│   │   ├── reviews.py
│   │   └── users.py
│   ├── logic/
│   │   └── functions.py         # Reusable logic and utilities
│   ├── web/
│   │   └── gemini.py            # Gemini API integration
│   └── main.py                  # Entry point
├── docker-compose.yml
├── Dockerfile
├── .env.example
└── requirements.txt
```

---

## 🛠️ Technologies Used

- **Python 3.10**
- **aiogram 2.25.1**
- **MySQL 8.0**
- **Docker & Docker Compose**
- **dotenv for env management**
- **aiohttp 3.8.6** — for async interaction with external services (e.g., Gemini)
- **Flask 2.3.3** — for exposing API endpoints (planned)
- **Logging, error handling, async I/O**

---

## ⚙️ Getting Started

1. Clone the repository:
   ```bash
   git clone https://github.com/tikoarm/python-feedback.git
   cd python-feedback
   ```

2. Add your `.env` file:
   ```
   TG_TOKEN=your_telegram_token
   TG_BOT_USERNAME=your_bot_username

   GEMINI_API_KEY=your_gemini_api_key

   MYSQL_HOST=db
   MYSQL_PORT=3306
   MYSQL_USER=root
   MYSQL_PASSWORD=root
   MYSQL_DATABASE=feedback_db
   ```

3. Run the project:
   ```bash
   docker-compose up --build
   ```

4. Visit [localhost:8080](http://localhost:8080) for phpMyAdmin (user: root / pass: root)

---

## 📌 Status

🟢 Core functionality working  
🔄 Gemini API integration in progress  
🌐 Web interface planned (PHP + JSON API)

---

## 👨‍💻 Author

Developed by **Tigran Kocharov**  
📧 tiko.nue@icloud.com

---

## 📄 License & Use

This bot was developed for personal portfolio use.  
It may be reused for educational or non-commercial purposes with proper credit.