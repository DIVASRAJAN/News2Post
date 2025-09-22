# News2Post
News2Post is a tool that fetches the latest news about any topic from the web and automatically converts it into a ready-to-share social media post.

## Features

- Fetches recent news articles using Serper API
- Summarizes and converts news into LinkedIn-style posts using Gemini LLM
- FastAPI backend for easy integration
- Ready for deployment with Uvicorn
- Uses `uv` as the package manager for fast dependency management

## Getting Started

### Prerequisites

- Python 3.8+
- [uv](https://github.com/astral-sh/uv) package manager

### Installation

1. **Clone the repository:**
   ```bash
   git clone https://github.com/yourusername/News2Post.git
   cd News2Post
   ```

2. **Install dependencies using `uv`:**
   ```bash
   uv pip install -r requirements.txt
   ```

3. **Set up environment variables:**

   Create a `.env` file in the project root:
   ```properties
   serper_api_key = "your-serper-api-key"
   gemini_key = "your-gemini-api-key"
   ```

### Running the App

Start the FastAPI server with Uvicorn:
```bash
uvicorn api.main:app --reload
```

## Project Structure

```
News2Post/
├── api/
│   ├── main.py         # FastAPI app entry point
│   ├── agent.py        # News fetching and post generation logic
│   └── prompts.yaml    # LLM prompt templates
├── .env                # API keys and secrets
├── requirements.txt    # Python dependencies
└── README.md           # Project documentation
```

## Usage

Send a request to the API endpoint with your topic of interest, and receive a LinkedIn-ready post based on the latest news.
