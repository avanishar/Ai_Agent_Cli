# 🤖 AI Agent CLI + Web App

An AI-powered tool that can **generate files, edit content, and chat with an AI assistant** — built using Python, Flask, and OpenRouter API.

---

## 🚀 Features

✨ Generate multiple file types:

* 📄 Article (.txt)
* 📝 Study Notes (.txt)
* ❓ Q&A (.txt)
* 📊 Excel Spreadsheet (.xlsx)
* 📃 Word Document (.docx)
* 📑 PDF Report (.pdf)
* 📊 PowerPoint Presentation (.pptx)

💬 AI Chat (with memory)

* Real-time streaming responses
* Multi-turn conversation support

🛠️ File Editing

* Modify existing files using AI instructions

📜 History Tracking

* Stores generated files and chat logs

🌐 Web Interface + CLI

* Modern UI with chat panel
* Terminal-based CLI support

---

## 🧠 Tech Stack

* **Backend:** Python, Flask
* **AI API:** OpenRouter
* **Frontend:** HTML, CSS, JavaScript
* **Database:** SQLite
* **Libraries:**

  * openpyxl (Excel)
  * python-docx (Word)
  * reportlab (PDF)
  * python-pptx (Presentation)

---

## 📂 Project Structure

```
AI_Agent_Cli/
│── agent.py          # Core AI logic
│── app.py            # Flask web server
│── cli.py            # CLI interface
│── history.py        # Database handling
│── templates/
│   └── index.html    # Web UI
│── outputs/          # Generated files
│── .env              # API key (not uploaded)
│── README.md
```

---

## ⚙️ Setup & Installation

### 1️⃣ Clone the repository

```bash
git clone https://github.com/avanishar/Ai_Agent_Cli.git
cd Ai_Agent_Cli
```

---

### 2️⃣ Install dependencies

```bash
pip install -r requirements.txt
```

---

### 3️⃣ Add API Key

Create a `.env` file:

```
OPENROUTER_API_KEY=your_api_key_here
```

---

### 4️⃣ Run the app

#### 🌐 Web App

```bash
python app.py
```

Open: http://127.0.0.1:5000

#### 💻 CLI

```bash
python cli.py
```



## 📸 Screenshots (Add Later)

* UI dashboard
* Chat interface
* Generated files



## 🔥 Future Improvements

* User authentication
* Cloud file storage
* More AI models support
* Dark/light theme toggle
* Deployment (Render / Railway)

---

## 🎯 Use Cases

* Students → generate notes & assignments
* Developers → quick documentation
* Job prep → interview Q&A
* Content creators → structured content

---

## ⚠️ Important

* Do NOT upload `.env` file
* Keep API keys secure

---

## 👩‍💻 Author

**Avani Sharma**
3rd Year CSE Student

---

## ⭐ If you like this project

Give it a ⭐ on GitHub!
