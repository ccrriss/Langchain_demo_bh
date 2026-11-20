# AI Cooking Assistant

A personal full-stack learning project built while following a LangChain video tutorial, with a FastAPI backend and Next.js chat interface. Enter ingredients or a cooking question to receive recipe suggestions, preparation steps, and AI-generated assessments of nutrition and cooking difficulty.

**Status:** Local demo; development is temporarily paused while continuing other LangChain / LangGraph studies.

## Demo

![AI Cooking Assistant displaying a recipe response with Markdown formatting and an external image](docs/images/cooking-assistant-demo.png)

Local running screenshot showing the chat interface and a rendered recipe response.

## Features

- **Recipe suggestions:** A LangChain `create_agent` agent is prompted to search for recipes, compare candidates, and answer in Markdown.
- **Tavily web and image search:** The search tool uses `topic="general"`, `max_results=5`, and `include_images=True`. The prompt instructs the agent to use returned image URLs when suitable images are available.
- **Streaming responses:** The backend reads text deltas from `astream_events(version="v3")` and returns a `text/plain` HTTP stream. The frontend reads and displays chunks progressively.
- **Persistent conversation state:** LangGraph's `AsyncPostgresSaver` stores checkpoints in PostgreSQL by `thread_id`; its tables are initialized during backend startup.
- **History controls:** Retrieve user-facing messages from the latest checkpoint or delete the current thread's saved checkpoints.
- **Context summarization:** `SummarizationMiddleware` is enabled with `trigger=("tokens", 4000)` and `keep=("messages", 20)` to summarize older context and retain recent messages.
- **Markdown rendering:** `react-markdown`, `remark-gfm`, and Tailwind Typography render headings, lists, tables, and external images in both streaming and completed responses. Raw HTML is skipped.

The frontend keeps one `thread_id` in `localStorage` and reuses it across page reloads. History is loaded through the **Check history chats** button. The backend filters out tool messages and assistant messages containing tool calls. Because history is read from the latest checkpoint, summarization can replace older exchanges with a summary; this is not a complete conversation archive.

## Tech Stack

| Layer | Technology |
| --- | --- |
| Frontend | Next.js 16, React 19, TypeScript, Tailwind CSS v4 |
| Markdown | `react-markdown`, `remark-gfm`, `@tailwindcss/typography` |
| Backend | Python 3.11+, FastAPI, Pydantic |
| Agent / tools | LangChain `create_agent`, `langchain-openai`, `langchain-tavily` |
| Conversation state | LangGraph PostgreSQL checkpointer, PostgreSQL 17 |
| Local tooling | `uv`, npm, Docker Compose for PostgreSQL |

## Project Structure

Main application paths:

```text
.
├── apps/cook_assistant/frontend/
│   ├── app/                  # Next.js chat page and styles
│   ├── component/            # Text input component
│   └── lib/                  # Fetch and stream helpers
├── src/langchain_cook_assistant/
│   ├── agents/cook_assistant_agent.py  # Streaming and checkpoint-history helpers
│   ├── api/chat.py           # Chat routes
│   ├── middlewares/          # Summarization middleware
│   ├── prompts/              # Agent system prompt
│   ├── schemas/              # Pydantic models
│   ├── tools/                # Tavily search integration
│   └── main.py               # FastAPI lifecycle and agent initialization
├── docs/images/              # README screenshot
├── compose.yaml              # Local PostgreSQL service
├── pyproject.toml            # Python dependencies and package configuration
└── README.md
```

## Run Locally

### Prerequisites

- Python 3.11+ and [uv](https://docs.astral.sh/uv/)
- Node.js 20.9+ and npm (minimum required by the installed Next.js package)
- Docker with Docker Compose
- API access to both models listed below and a Tavily API key

### 1. Configure environment variables

Create `.env` in the repository root:

```dotenv
OPENAI_API_KEY=your_model_api_key
OPENAI_BASE_URL=https://your-provider.example/v1
TAVILY_API_KEY=your_tavily_api_key

# Matches compose.yaml's local development database
DOCKER_SAVER_DB=postgresql://postgres:postgres@localhost:5434/pgsaver_test

# Optional; JSON array, shown with its default value
BACKEND_CORS_ORIGINS=["http://localhost:3000"]
```

The current code fixes the chat model to `openai:qwen3.5-flash` in `main.py` and the summarization model to `openai:qwen3.6-27b` in `middlewares/summarization.py`. Both use the OpenAI-compatible provider configured above. Verify that your provider supports both model IDs, streaming, and tool calling as needed. Model names are not configurable through environment variables in this version. Keep API keys and `.env` out of version control.

### 2. Start PostgreSQL

From the repository root:

```bash
docker compose up -d pgsaver
```

Compose runs PostgreSQL 17 at `localhost:5434`, with data stored in the `pgsaver_data` named volume. Wait for the database to be ready before starting the backend.

### 3. Start the backend

From the repository root:

```bash
uv sync
uv run uvicorn langchain_cook_assistant.main:app --reload --port 8000
```

API documentation: [http://localhost:8000/docs](http://localhost:8000/docs).

### 4. Start the frontend

In a second terminal, from the repository root:

```bash
cd apps/cook_assistant/frontend
npm ci
npm run dev
```

Open [http://localhost:3000](http://localhost:3000). Next.js proxies `/api` and `/api/*` to `http://localhost:8000` by default. To use a different backend address, set `BACKEND_URL` in `apps/cook_assistant/frontend/.env.local` before starting Next.js:

```dotenv
BACKEND_URL=http://localhost:8000
```

## API Overview

| Method | Endpoint | Request / response |
| --- | --- | --- |
| `POST` | `/api` | JSON body: `{ "query": "...", "thread_id": "..." }`; response: streamed plain text containing Markdown |
| `GET` | `/api/{thread_id}` | JSON array: `[{ "role": "human", "message": "..." }, { "role": "ai", "message": "..." }]`; empty array if no saved messages |
| `DELETE` | `/api/{thread_id}` | Delete the thread's checkpoints; response: JSON `null` with the current default status `200` |

The active chat API returns text, not the `CookAnswer` schema defined in the repository; structured output is not enabled.

## Current Limitations

- Input is **text-only**. The system prompt mentions photos, but the UI and request schema do not support image uploads or multimodal messages.
- Recipe images are third-party URLs requested through Tavily and selected by the model. Relevance and successful loading are not guaranteed; there is no image storage or loading fallback yet.
- Recipe scores and nutritional assessments are model-generated suggestions, without independent nutritional calculations or validation.
- The application has no authentication and is intended for local demonstration. Compose starts only PostgreSQL; the root `Dockerfile` is an unused starter template, not a working deployment setup.

## Possible Next Steps

Future work, not implemented in this version:

- OSS / R2 object storage for uploaded images
- Multimodal image input and ingredient recognition
- Online deployment with environment-based configuration
- Image-loading fallbacks, agent/tool evaluations, and UI polish
