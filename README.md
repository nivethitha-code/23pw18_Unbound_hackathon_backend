AgentFlow API 🧠
The intelligent backend for AgentFlow, providing the workflow execution engine, AI integration, and state management.

🚀 Overview
This FastAPI-based backend orchestrates the execution of multi-step AI workflows. It handles communication with the Unbound (Kimi) LLM API, manages state in Supabase, and ensures robust error handling and retry logic for agentic tasks.

✨ Features
Workflow Engine: Logic to execute steps sequentially, passing context from one step to another.
Reliable AI Integration: Robust client for the Unbound API (Kimi models) with automatic retries.
Validation Logic: Built-in verification steps to ensure AI outputs meet strict criteria (Contains, Regex, JSON Valid, etc.) before proceeding.
State Management: Persists workflow definitions and run history using Supabase (PostgreSQL).
RESTful API: Clean endpoints for managing workflows and retrieving history.
🛠️ Tech Stack
Language: Python 3.10+
Framework: FastAPI
Database: Supabase (PostgreSQL)
AI Provider: Unbound API (Kimi-k2p5, Kimi-instruct)
Libraries: httpx, pydantic, supabase-py
🚀 Getting Started
Clone the repository

bash
git clone https://github.com/nivethitha-code/23pw18_Unbound_hackathon_backend.git
cd 23pw18_Unbound_hackathon_backend
Create a Virtual Environment

bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
Install Dependencies

bash
pip install -r requirement.txt
Setup Environment Variables Create a 
.env
 file in the root directory:

env
UNBOUND_API_KEY=your_unbound_api_key
UNBOUND_API_URL=https://api.getunbound.ai/v1/chat/completions
SUPABASE_URL=your_supabase_url
SUPABASE_KEY=your_supabase_service_key
DATABASE_URL=your_database_connection_string
Run the Server

bash
uvicorn app.main:app --reload
The API will be available at http://localhost:8000. View documentation at http://localhost:8000/docs.
