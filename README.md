# 🤖 AI-Based Attendance & Work Pattern Analysis Chatbot

An intelligent HRMS add-on that analyzes employee attendance, work hours, and leave trends through a conversational interface. Built with **FastAPI**, **Flask**, and **Groq AI (Llama 3)**, it features secure **Natural Language to SQL (NL2SQL)** conversion and privacy-preserving data summarization.

---

## 🚀 Key Features

* **Conversational Analytics:** Ask questions like *"Who was late last week?"* or *"Show attendance trends for @Rahul"* in plain English.
* **Smart Autocomplete:** WhatsApp-style `@mention` feature to easily find and select employees in the chat.
* **Visual Insights:** Automatically generates line charts and graphs for work hour trends and engagement.
* **Zero Data Leakage:**
    * **NL2SQL:** Only database schema is sent to the LLM; data stays local.
    * **Summarization:** Sensitive PII (Names, Emails) is hashed (SHA-256) before being sent to the AI for analysis, ensuring privacy.
* **Work Engagement Scoring:** Calculates engagement percentages based on check-in/out duration.

## 🛠️ Tech Stack

* **Backend:** FastAPI (Python), SQLAlchemy
* **Frontend:** Flask (Python), HTML5, CSS3, jQuery UI
* **AI & LLM:** Groq API (Llama 3 70B Model)
* **Database:** SQLite (MVP), scalable to PostgreSQL/MySQL
* **Data Analysis:** Pandas, Matplotlib
* **Security:** `hashlib` for SHA-256 anonymization

---

## 📂 Project Structure

```text
chatbot-mvp/
├── backend/
│   ├── main.py              # FastAPI Entry Point
│   ├── core/config.py       # Environment Configuration
│   ├── services/
│   │   ├── nl2sql.py        # AI SQL Generation
│   │   ├── summarization.py # Privacy-preserving Summary
│   │   └── analysis.py      # Pandas & Matplotlib Logic
│   └── models/              # DB Schema & Pydantic Models
├── frontend/
│   ├── app.py               # Flask Entry Point
│   ├── templates/index.html # Chat Interface
│   └── static/              # CSS & JS
├── .env                     # API Keys (Not committed)
├── requirements.txt         # Python Dependencies
└── run.bat                  # One-click startup script

```

## ⚙️ Installation & Setup

### 1. Clone the Repository

```bash
git clone [https://github.com/yourusername/hrms-chatbot-mvp.git](https://github.com/yourusername/hrms-chatbot-mvp.git)
cd hrms-chatbot-mvp

```

### 2. Create Virtual Environment

```bash
# Windows
python -m venv venv
.\venv\Scripts\activate

# Mac/Linux
python3 -m venv venv
source venv/bin/activate

```

### 3. Install Dependencies

```bash
pip install -r requirements.txt

```

### 4. Configure Environment

Create a `.env` file in the root directory and add your Groq API key:

```ini
GROQ_API_KEY=gsk_your_actual_groq_api_key_here
HASH_SALT=my_secret_salt_value

```

### 5. Initialize Database

The application automatically creates the SQLite database (`hrms_mvp.db`) and seeds it with sample dummy data on the first run.

---

## 🏃‍♂️ How to Run

### Method 1: One-Click Script (Windows)

Double-click the `run.bat` file in the root directory. It will start both the Backend and Frontend servers automatically.

### Method 2: Manual Start

**Terminal 1 (Backend):**

```bash
uvicorn backend.main:app --reload --port 8000

```

**Terminal 2 (Frontend):**

```bash
python frontend/app.py

```

Access the application at: **http://127.0.0.1:5000**

---

## 🛡️ Security & Privacy Architecture

This project strictly adheres to data privacy requirements:

1. **NL2SQL:** The AI never sees actual row data when generating SQL queries. It only sees table names and column definitions.
2. **Summarization:** Before analysis data is sent to the LLM:
* Names/Emails are replaced with tokens (e.g., `Rahul` -> `EMP_a1b2c3`).
* The LLM analyzes the tokenized data.
* The system de-anonymizes the response locally before showing it to the user.



---

## 🧪 Testing

To test the application, try these queries in the chat:

1. *Type `@` and select a name.*
2. *"Show me the attendance records for @Rahul Sharma"*
3. *"Calculate the average work hours for all employees this week"*
4. *"Who has the most late arrivals?"*

---

## 🤝 Contributing

1. Fork the repository.
2. Create a feature branch (`git checkout -b feature/AmazingFeature`).
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`).
4. Push to the branch (`git push origin feature/AmazingFeature`).
5. Open a Pull Request.

## 📄 License

Distributed under the MIT License. See `LICENSE` for more information.

```

```
