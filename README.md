# 🤖 Raj's Super-Bot: AI-Integrated Telegram Assistant

This is an advanced, multi-functional Telegram Bot built using Python, designed to showcase API integration, secure deployment practices, and conversational AI capabilities. The bot is deployed on the **Render** cloud service and monitored for 24/7 uptime.

---

## ✨ Key Features & Capabilities

* **🧠 AI Conversation:** Integrated with the **Google Gemini API** (`gemini-1.5-flash`) to handle complex queries, solve math problems, and generate creative text in real-time.
* **🌐 Secure Cloud Deployment:** Hosted on Render.com with a custom solution to ensure continuous operation.
* **🛡️ Security/Secrets Management:** Utilizes **Environment Variables** (`os.environ`) to securely handle sensitive data like the Bot Token and Gemini API Key, preventing exposure in public code.
* **⚙️ Utility Commands:**
    * `/start` (UI buttons for navigation)
    * `toss`: Simulates a coin flip (Random Logic).
    * `password`: Generates a strong, random 12-character password (Loop Logic).
    * `wiki <query>`: Fetches a 2-sentence summary from Wikipedia (API Integration/Exception Handling).
    * `youtube.com`: Processes video links (Multimedia Handling).

---

## 🛠️ Installation & Getting Started

### 1. Dependencies (Required Libraries)

The following libraries must be installed on your system or cloud environment:

```bash
pip install pyTelegramBotAPI google-generativeai yt-dlp Flask lxml
```
### 2. Secrets Configuration
### 2. Secrets Configuration

For the bot to run, you must set these two critical Environment Variables:

| Variable Name | Description | Source |
| :--- | :--- | :--- |
| **MY_TOKEN** | The unique token for your Telegram Bot (from BotFather). | Render Environment Variable |
| **GEMINI_KEY** | Your Google Generative AI API Key. | Render Environment Variable |

## ☁️ Deployment on Render (24/7 Uptime)
This bot is configured to run as a Web Service on Render using the Flask Keep-Alive strategy.

Start Command
The process is initiated using the following command:

```Bash
python my_bot.py
```
Architecture Note: Keep-Alive Solution
The project uses a multi-threaded approach: the threading module runs a small Flask server in the background (listening on the port provided by Render) while the main thread handles Telegram Polling. This prevents the Free Tier service from timing out and being shut down by the host.

## 👤 Author
Raj (B.Sc. Student, Python Developer)

