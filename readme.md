# Gemini Autonomous Agent Demo

This project is a Flask-based web application demonstrating an autonomous agent powered by Google's Gemini models. The agent is capable of performing various tasks through tool integration, including real-time web search, email management, and news aggregation.

## Features

- **Interactive Chat Interface:** Seamless conversation with the Gemini agent.
- **Autonomous Capabilities:**
  - **Web Search:** Retrieves real-time information using Google Custom Search.
  - **Email Management:** Reads unread emails and sends new emails via Gmail integration.
  - **News Aggregator:** Fetches and summarizes the latest news from Google News RSS feeds.
- **Chat Management:** Create, load, and manage chat sessions with persistent history.

## Tools & Technologies

- **Backend:** [Flask](https://flask.palletsprojects.com/) (Python)
- **AI Model:** [Google Gemini](https://ai.google.dev/) (via `google-genai` SDK)
- **Search:** Google Custom Search JSON API
- **Email:** [SimpleGmail](https://github.com/jeremyephron/simplegmail)
- **News Extraction:** `feedparser`, `newspaper3k`, `googlenewsdecoder`
- **Frontend:** HTML/CSS (Jinja2 templates)

## Setup & Installation

### Prerequisites

- Python 3.8+
- A Google Cloud Project with the following APIs enabled:
  - Gemini API
  - Custom Search API
  - Gmail API

### Installation

1.  **Clone the repository:**
    ```bash
    git clone <repository-url>
    cd Gemini-Autonomous-Agent-Demo
    ```

2.  **Create and activate a virtual environment:**
    ```bash
    python3 -m venv .venv
    source .venv/bin/activate  # On Windows use `.venv\Scripts\activate`
    ```

3.  **Install dependencies:**
    ```bash
    pip install -r requirements.txt
    ```

### Configuration

1.  **Environment Variables:**
    Create a `.env` file in the root directory (use `.env.example` as a reference) and add your API keys:
    ```env
    GEMINI_API_KEY=your_gemini_api_key
    GEMINI_MAIN_MODEL=gemini-2.0-flash-exp
    GEMINI_QUICK_MODEL=gemini-2.0-flash-exp
    SEARCH_API_KEY=your_google_custom_search_api_key
    SEARCH_ENGINE_ID=your_search_engine_id
    PRIMARY_USER_MAIL=your_email@gmail.com
    ```

2.  **Gmail Credentials:**
    - Download your `client_secret.json` from the Google Cloud Console (OAuth 2.0 Client IDs).
    - Place it in the `gmail_credentials/` directory.
    - Run the initial setup script (if applicable) or ensure the app handles the initial OAuth flow to generate `gmail_token.json`.

## Usage

1.  **Run the application:**
    ```bash
    python app.py
    ```

2.  **Access the interface:**
    Open your browser and navigate to `http://127.0.0.1:7777`.

## Project Structure

- `app.py`: Main entry point for the Flask application.
- `routes.py`: API route definitions.
- `views.py`: Logic for chat handling and interactions.
- `utils.py`: Implementation of tool functions (Search, Email, News).
- `tool_declarations.py`: Definitions of tools exposed to the Gemini model.
- `templates/`: HTML templates for the frontend.
