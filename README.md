# Legal Advisor Chatbot

An AI-powered legal advisor chatbot that provides responses to legal questions using OpenAI's language models.

## Overview

This application allows users to ask legal questions and receive AI-generated responses through a simple web interface. The system uses OpenAI's language models to generate contextually appropriate legal advice while maintaining conversation history.

## Features

- FastAPI backend with OpenAI integration for processing legal queries
- Streamlit frontend providing an intuitive chat interface
- Conversation history tracking and display
- Environment variable configuration for secure API key management
- Basic error handling for API failures
- Docker support for containerized deployment
- PostgreSQL database for conversation storage
- LangChain integration for enhanced LLM capabilities

## Prerequisites

- Python 3.12+
- OpenAI API key
- PostgreSQL
- Docker and Docker Compose

## Installation

1. Clone the repository:

```bash
git clone https://github.com/qminoo/legal-advisor-ai
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

4. Copy `.env.example` to `.env` and configure your environment variables:

```bash
cp .env.example .env
```

5. Configure your `.env` file with the following variables:

```bash
OPENAI_API_KEY=your_api_key_here

POSTGRES_USER="your_db_user"
POSTGRES_PASSWORD="your_db_password"
POSTGRES_DB="your_db_name"
```

## Running the Application

### Backend

1. Navigate to the backend directory:

```bash
cd backend
```

2. Start the FastAPI server:

```bash
uvicorn app.main:app --reload --port 8000
```

The backend API will be available at `http://localhost:8000`

### Frontend

1. Open a new terminal and navigate to the frontend directory:

```bash
cd frontend
```

2. Start the Streamlit application:

```bash
streamlit run app.py
```

The frontend interface will be available at `http://localhost:8501`

## Docker Deployment

If you prefer to run the application using Docker:

1. Build and start the containers:

```bash
docker-compose up --build
```

2. Access the application:

- Frontend: `http://localhost:8501`
- Backend API: `http://localhost:8000`

## Application Architecture

### Backend

- FastAPI framework for API endpoints
- `/chat` endpoint for processing legal questions
- `/chat-history` endpoint for retrieving conversation history
- OpenAI API integration for generating responses
- PostgreSQL database for storing conversations
- LangChain framework for enhanced LLM capabilities

### Frontend

- Streamlit-based user interface
- Input field for legal questions
- Response display area
- Conversation history view
- Basic styling for improved readability

## Legal Advisor Implementation

### Approach to Legal Context

- System prompts configured to establish the AI's role as a legal advisor
- Implementation of disclaimers to clarify that responses are informational, not formal legal advice
- Structured prompt templates to ensure consistent and professional responses
- Focus on general legal information and guidance while encouraging users to seek professional legal counsel for specific cases

## Development Approach

This project was developed with a focus on:

- Clean, maintainable code structure
- Proper error handling
- Secure API key management
- Clear documentation
- Regular, focused Git commits with descriptive messages

## License

[MIT License](LICENSE)
