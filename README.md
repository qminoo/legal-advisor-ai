# Legal Advisor Chatbot

An AI-powered legal advisor chatbot that provides responses to legal questions using OpenAI's language models.

## Features

- FastAPI backend with OpenAI integration
- Streamlit frontend for user interaction
- Conversation history tracking
- Docker support
- PostgreSQL database integration

## Prerequisites

- Python 3.8+
- OpenAI API key

## Installation

1. Clone the repository:

```bash
git clone https://github.com/qminoo/ai-legal-advisor
cd ai-legal-advisor
```

2. Create and activate a virtual environment:

```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:

```bash
pip install -r requirements.txt
```

4. Copy `.env.example` to `.env` and fill in your OpenAI API key:

```bash
cp .env.example .env
```

## Running the Application

### Backend

```bash
cd backend
uvicorn app.main:app --reload
```

### Frontend

```bash
cd frontend
streamlit run app.py
```

## License

[MIT License](LICENSE)
