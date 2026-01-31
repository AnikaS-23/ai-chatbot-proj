# AI ChatRobo — Full-Stack Conversational Intelligence

AI ChatRobo is a high-performance, full-stack AI chatbot application built entirely in Python. The platform features a decoupled architecture, utilizing a **FastAPI** backend for robust data orchestration and a **Streamlit** frontend for a modern, responsive user experience. 

By leveraging **Groq’s LLaMA 3.1** inference engine, AI ChatRobo delivers near-instantaneous, streaming AI responses with persistent chat memory.


## 🛠 Technical Architecture

The application follows a client-server model to ensure scalability and separation of concerns:

* **Frontend:** Streamlit-based SPA (Single Page Application) with custom CSS and complex session state management.
* **Backend:** FastAPI REST API managing business logic, authentication, and database transactions.
* **Inference Layer:** Groq Cloud API utilizing the `llama-3.1-8b-instant` model for high-throughput NLP.
* **Data Layer:** SQLite with SQLAlchemy ORM, providing a reliable persistent storage solution for users and chat telemetry.


## 🚀 Key Features

### 🔐 Secure Authentication & Identity
* **User Management:** Full registration and login workflows with secure password handling.
* **Session Security:** Industry-standard hashing and session-based authentication to maintain state across refreshes.
* **Data Isolation:** User data is partitioned at the database level to ensure privacy between accounts.

### 💬 Intelligent Chat Interface
* **Real-Time Streaming:** Implements token-by-token streaming for a dynamic UX and reduced perceived latency.
* **Persistent Context:** Multi-chat history allows users to maintain various independent conversation threads.
* **Auto-Titling:** Intelligent generation of chat titles based on the initial user prompt.

### 🗄 Database & Persistence
* **SQLAlchemy ORM:** Provides an abstraction layer for easy migration to enterprise databases like PostgreSQL or MySQL.
* **Thread Safety:** Implements dependency injection for safe, concurrent database connections.


## 🧱 Tech Stack

| Component         | Technology                         |
| :---------------- | :--------------------------------- |
| **Language**      | Python 3.10+                       |
| **Backend**       | FastAPI                            |
| **Frontend**      | Streamlit                          |
| **AI Engine**     | Groq (LLaMA 3.1 8B)                |
| **Database**      | SQLite + SQLAlchemy                |
| **Integrations**  | Requests, Dotenv, Pydantic         |

---

## 📁 Project Structure
```text

ai_chatbot/
│
|- app.py                 # Streamlit Frontend (UI & State Logic)
|- main.py                # FastAPI Server (API Entry Point)
|- auth.py                # Identity & Access Management
|- reset_password.py      # Administrative Security Utilities
│
|- database.py            # Database connection (SQLite + SQLAlchemy)
|- models.py              # Database models
|- seed_db.py             # Initial database seeding
│
|- assets/                # Branding & UI Graphics
│
|- requirements.txt       # Project dependencies
|-.env                    # Environment variables (local only)
|- .gitignore             # Version control exclusions
|- chatbot.db             # SQLite database (local)
```

Note: .env, virtual environment files, and database files are excluded from version control for security and best practices.

## ⚙️ Setup Instructions


### 1️⃣ Clone the Repository
```bash
git clone https://github.com/AnikaS-23/ai-chatbot-proj.git

cd ai-chatbot-proj
```

2️⃣ Create Virtual Environment
```bash

python -m venv venv

venv\\Scripts\\activate   # Windows
```

3️⃣ Install Dependencies
```bash

pip install -r requirements.txt
```

4️⃣ Environment Variables

Create a .env file:
```env

GROQ\_API\_KEY=your\_groq\_api\_key\_here
```

▶️ Running the Application

Start Backend (FastAPI)
```bash 

python main.py
```

Backend runs at:
```arduino

http://localhost:8000
```

Start Frontend (Streamlit)
```bash

streamlit run app.py
```

Frontend runs at:
```arduino

http://localhost:8501
```

---

### 🧪 How It Works (Architecture)

User (Browser)

&nbsp;  ↓

Streamlit Frontend

&nbsp;  ↓ REST API

FastAPI Backend

&nbsp;  ↓

Groq LLM API

- Frontend handles UI \& session state

- Backend manages auth \& chat persistence

- Groq handles AI inference

- Chat responses are streamed token-by-token

---

### 🔒 Security Notes

API keys stored in .env

Sensitive files ignored via .gitignore

Passwords are never exposed in the frontend


## Author

Anika Sharma

Computer Science Engineering (Data Science)



