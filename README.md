# Gamenator

## 🚀 Overview

**Gamenator** is an experimental AI-driven engine that generates playable WebGL games from natural language prompts. By leveraging **Retrieval-Augmented Generation (RAG)**, this system goes beyond simple code completion; it understands game design patterns, physics logic, and shader implementations to construct robust, interactive 3D experiences on the fly.

This project demonstrates the practical application of Large Language Models (LLMs) in software engineering, specifically focusing on the challenges of generating complex, state-dependent systems like game loops.

## 🧠 RAG Architecture & AI Implementation

The core of Gamenator is a specialized RAG pipeline designed to minimize hallucinations in code generation.

1.  **Knowledge Base**: A vector database indexed with high-quality WebGL/Three.js snippets, game logic patterns (ECS), and shader libraries.
2.  **Semantic Retrieval**: When a user prompts "Create a space shooter," the system retrieves relevant context—such as flight controls, projectile logic, and starfield shaders—before querying the LLM.
3.  **Context-Aware Generation**: The LLM receives the user prompt enriched with these retrieved technical constraints, ensuring the generated code is syntactically correct and logically sound.

## 🛠️ Tech Stack

### AI & Backend
*   **Python**: Core logic and API handling.
*   **Google Gemini**: Advanced LLM for code generation and reasoning.
*   **PostgreSQL + pgvector**: Vector database for semantic search and RAG.
*   **FastAPI**: High-performance async REST API to serve the generator.
*   **TextEmbedding**: Custom embedding generation for context retrieval.

### Frontend & Rendering
*   **Jinja2**: Server-side templating for the UI.
*   **Three.js / WebGL**: The rendering engine used for the generated output.
*   **Vanilla JavaScript**: Lightweight client-side logic without heavy frameworks.

## 📦 Installation & Setup

Follow these steps to set up the development environment.

### Prerequisites
*   Python (v3.10+)
*   PostgreSQL (with pgvector extension enabled)

### 1. Clone the Repository
```bash
git clone https://github.com/yourusername/gamenator.git
cd gamenator
```

### 2. Backend Setup
Navigate to the server directory and install dependencies.

```bash
cd server
python -m venv venv
source venv/bin/activate  # or `venv\Scripts\activate` on Windows
pip install -r requirements.txt
```

Create a `.env` file in the `server` directory:
```env
AI_API_KEY=

DB_HOST=
DB_PORT=
DB_USER=
DB_PASSWORD=
DB_NAME=gamenator
```

### 3. Database Setup
Execute the following SQL script to initialize the project table and vector indexes.

```sql
-- ----------------------------
-- Table structure for project
-- ----------------------------
DROP TABLE IF EXISTS "public"."project";
CREATE TABLE "public"."project" (
  "id" char(64) COLLATE "pg_catalog"."default" NOT NULL,
  "game_id" char(64) COLLATE "pg_catalog"."default" NOT NULL,
  "content" text COLLATE "pg_catalog"."default" NOT NULL,
  "description" text COLLATE "pg_catalog"."default",
  "embedding" vector(1024),
  "section" varchar(50) COLLATE "pg_catalog"."default",
  "created_at" timestamptz(6) DEFAULT CURRENT_TIMESTAMP,
  "updated_at" timestamptz(6) DEFAULT CURRENT_TIMESTAMP
)
;

-- ----------------------------
-- Indexes structure for table project
-- ----------------------------
CREATE INDEX "project_embedding_idx" ON "public"."project" USING hnsw (
  "embedding" "public"."vector_cosine_ops"
);

-- ----------------------------
-- Primary Key structure for table project
-- ----------------------------
ALTER TABLE "public"."project" ADD CONSTRAINT "project_pkey" PRIMARY KEY ("id");
```

### 4. Running the Application
Start the backend API:
```bash
# In terminal 1 (server)
uvicorn main:app --reload
```

Start the frontend development server:
```bash
# In terminal 2 (client)
npm run dev
```

## 🌟 Usage

1.  Open your browser to `http://localhost:5173`.
2.  Enter a prompt in the input field (e.g., *"A 3D maze game where the player collects glowing orbs"*).
3.  Watch the RAG pipeline retrieve relevant assets and generate the game code.
4.  Play the result immediately in the WebGL canvas.

## 🔮 Future Improvements

*   **Multi-Agent System**: Implementing a "Critic" agent to review code before rendering.
*   **Asset Generation**: Integrating Stable Diffusion for texture generation alongside code generation.
*   **Local LLM Support**: Adding support for Llama 3 for offline generation.
