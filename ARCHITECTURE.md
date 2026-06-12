# Project Structure

## Overview
The COSMOCODE analyzer has been refactored from a single monolithic `server.py` file into a well-organized modular architecture.

## File Structure

```
CosmoCode/
├── server.py              # Main entry point (minimal, imports and runs app)
├── config.py              # Configuration (PORT, WORKSPACE_DIR)
├── run.bat                # Batch script to start server
├── README.md              # Project documentation
│
├── core/                  # Core analysis logic
│   ├── __init__.py       # Package exports
│   ├── parser.py         # CodeParser class - parses code in multiple languages
│   ├── graph_builder.py  # GalaxyGraphBuilder class - builds dependency graphs
│   └── work_iq.py        # WorkIQSimulator class - generates organizational context
│
├── handlers/              # HTTP request handlers
│   ├── __init__.py       # Package exports
│   ├── base.py           # BaseHandler - CORS headers & common functionality
│   ├── demo.py           # DemoDataHandler - /api/demo-data endpoint
│   ├── local.py          # ParseLocalHandler - /api/parse-local endpoint
│   └── github.py         # ParseGithubHandler - /api/parse-github endpoint
│
├── public/                # Frontend static files
│   ├── index.html
│   ├── style.css
│   └── js/
│       ├── app.js
│       ├── galaxy.js
│       ├── mockData.js
│       ├── parser.js
│       └── libs/
│           ├── lucide.min.js
│           ├── OrbitControls.js
│           └── three.min.js
```

## Module Descriptions

### Core Modules (`core/`)

**`parser.py` - CodeParser**
- Parses code files in multiple languages (Python, JavaScript, Java, C#, Go)
- Extracts classes, functions, dependencies, and metrics
- Detects code quality issues and security risks
- Calculates cyclomatic complexity and code coverage

**`graph_builder.py` - GalaxyGraphBuilder**
- Builds galaxy graph structure from parsed code
- Creates nodes (stars, planets, blackholes) and edges (orbits, dependencies)
- Detects circular dependencies
- Calculates dependency depth
- Computes codebase health metrics

**`work_iq.py` - WorkIQSimulator**
- Generates simulated organizational context for nodes
- Creates commit history and team discussion signals
- Adds human context to code analysis

### Handler Modules (`handlers/`)

**`base.py` - BaseHandler**
- Base Tornado request handler
- Provides CORS headers for all endpoints
- Handles HTTP OPTIONS requests

**`demo.py` - DemoDataHandler**
- **Endpoint**: `GET /api/demo-data`
- Returns sample code analysis for demo repositories
- Shows React frontend, FastAPI backend, and other examples

**`local.py` - ParseLocalHandler**
- **Endpoint**: `POST /api/parse-local`
- Accepts uploaded local files as JSON
- Parses and returns dependency graph
- Enriches nodes with WorkIQ signals

**`github.py` - ParseGithubHandler**
- **Endpoint**: `POST /api/parse-github`
- Downloads and analyzes GitHub repositories
- Supports both main and master branches
- Returns graph analysis with WorkIQ context

### Configuration (`config.py`)
- `PORT`: Server port (default 8000)
- `WORKSPACE_DIR`: Root directory for static file serving

### Entry Point (`server.py`)
- Imports all modules
- Creates and configures Tornado application
- Sets up URL routing
- Starts the server

## How It Works

1. **Server Startup**
   - `server.py` creates the Tornado app with routes
   - Routes to appropriate handler for each endpoint
   - Serves static files from `public/` directory

2. **Code Analysis Flow**
   - Handler receives request (demo, local files, or GitHub URL)
   - `CodeParser` analyzes each code file
   - `GalaxyGraphBuilder` constructs graph structure
   - `WorkIQSimulator` adds organizational context
   - Response sent as JSON to frontend

3. **Graph Structure**
   - **Stars**: Classes or files
   - **Planets**: Functions/methods
   - **Black Holes**: Code issues/risks
   - **Orbits**: Function calls and dependencies

## Running the Server

```bash
python server.py
```

Or use the batch script:
```bash
run.bat
```

Server will start on `http://localhost:8000`

## API Endpoints

### GET /api/demo-data
Returns sample code analysis with demo repositories.

```json
{
  "react_galaxy": { ... },
  "python_galaxy": { ... }
}
```

### POST /api/parse-local
Upload local files for analysis.

**Request:**
```json
{
  "files": [
    { "path": "src/app.js", "content": "..." },
    { "path": "src/main.js", "content": "..." }
  ]
}
```

**Response:**
```json
{
  "status": "success",
  "graph": { ... }
}
```

### POST /api/parse-github
Analyze a GitHub repository.

**Request:**
```json
{
  "url": "owner/repo" or "https://github.com/owner/repo"
}
```

**Response:**
```json
{
  "status": "success",
  "repoName": "owner/repo",
  "graph": { ... }
}
```

## Supported Languages

- Python (.py)
- JavaScript (.js, .jsx)
- TypeScript (.ts, .tsx)
- Java (.java)
- C# (.cs)
- Go (.go)

## Benefits of Modularization

✅ **Separation of Concerns** - Each module has a single responsibility
✅ **Easier Testing** - Individual modules can be tested independently
✅ **Better Maintainability** - Changes are localized to specific files
✅ **Code Reusability** - Components can be imported and used elsewhere
✅ **Scalability** - Easy to add new handlers or parsing logic
✅ **Readability** - Smaller, focused files are easier to understand
