# 🤖 AI ChatRobo — Full-Stack AI Chatbot (Python + Groq LLM)

AI ChatRobo is a \*\*full-stack AI chatbot application built entirely in Python\*\*, featuring user authentication, chat history persistence, real-time streaming responses, and a modern Streamlit UI.  

It uses \*\*Groq’s LLM API (LLaMA 3.1)\*\* for ultra-fast inference and a \*\*FastAPI backend\*\* for authentication and data handling.


## 🚀 Key Features


### 🔐 Authentication System

- User registration \& login

- Secure password handling

- Session-based authentication

- Logout \& session reset


### 💬 Intelligent Chat Interface

- Real-time AI responses (token streaming)

- Persistent multi-chat history per user

- Automatic chat title generation

- Sidebar chat navigation 


### 🧠 AI Engine

- Groq LLM integration (`llama-3.1-8b-instant`)

- System-prompt controlled responses

- Streaming completions for fast UX


### 🗂 Chat History Management

- Per-user chat storage

- Create, switch, and delete chats

- Clear entire chat history

- Client-side cache + backend sync


## 🗄 Database & Persistence

AI ChatRobo uses SQLite with SQLAlchemy ORM to manage persistent data storage.

Key Highlights:

SQLite database (chatbot.db)

SQLAlchemy ORM for database abstraction

Session-based database access

Safe connection handling using dependency injection

Why SQLite + SQLAlchemy?

Lightweight and easy to configure

Ideal for local development and academic projects

Easily upgradeable to PostgreSQL/MySQL in production

The database layer ensures reliable storage of user data and chat history, making the application scalable and production-ready.


### 🎨 Modern UI (Streamlit)

- Custom login \& signup UI

- Responsive two-column landing page

- Sidebar navigation

- Clean dark-theme styling

- Custom assets \& icons


## 🧱 Tech Stack


### Frontend

- \*\*Streamlit\*\*

- Custom CSS

- Session state management


### Backend

- \*\*FastAPI\*\*

- REST APIs for:

&nbsp; - Authentication

&nbsp; - Chat history storage

&nbsp; - Session handling


### AI / LLM

- \*\*Groq API\*\*

- Model: `llama-3.1-8b-instant`

- Streaming responses enabled


### Other

- Python 3.10+

- Requests

- dotenv

- UUID-based chat IDs


## 📁 Project Structure

ai\_chatbot/

│

├── app.py # Streamlit frontend (UI + AI logic)

├── main.py # FastAPI backend entry point

├── auth.py # Authentication logic

├── reset\_password.py # Password reset utilities

├── debug\_auth.py # Auth debugging \& testing

├── verify\_backend.py # Backend verification

│

├── assets/

│ ├── robot.png

│ └── robot\_v2.png

│

├── users.json # User \& chat storage (ignored in git)

├── .env # Environment variables (ignored)

├── .gitignore

├── requirements.txt

└── README.md


## ⚙️ Setup Instructions


### 1️⃣ Clone the Repository

git clone https://github.com/AnikaS-23/ai-chatbot-proj.git

cd ai-chatbot-proj

2️⃣ Create Virtual Environment

python -m venv venv

venv\\Scripts\\activate   # Windows

3️⃣ Install Dependencies

pip install -r requirements.txt

4️⃣ Environment Variables

Create a .env file:

GROQ\_API\_KEY=your\_groq\_api\_key\_here

▶️ Running the Application

Start Backend (FastAPI)

python main.py

Backend runs at:

http://localhost:8000

Start Frontend (Streamlit)

streamlit run app.py

Frontend runs at:

http://localhost:8501


## 🧪 How It Works (Architecture)

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


## 🔒 Security Notes

API keys stored in .env

Sensitive files ignored via .gitignore

Passwords are never exposed in the frontend


## Author

Anika Sharma

Computer Science Engineering (Data Science)



