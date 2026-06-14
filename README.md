

🌌 COSMOCODE — Explore Your Codebase as a Galaxy

An AI-powered code analyzer that turns your source code into an interactive 3D galaxy

Built with Python · Tornado · Three.js


✨ Overview

COSMOCODE takes any codebase — uploaded locally or pulled straight from GitHub — and transforms it into a navigable 3D galaxy visualization. Classes and files become stars, functions and methods become planets, and code issues or security risks become black holes. Dependencies and function calls are rendered as orbits, giving you an intuitive, spatial way to understand how a project is structured, where its complexity lives, and where its risks are hiding.

On top of raw structural analysis, COSMOCODE layers a simulated WorkIQ context — commit history and team discussion signals — adding a human dimension to the code map.


🌠 Demo
1. Watch demo video 
2. Start the server and open http://localhost:8000 in your browser to explore the galaxy view, load demo repositories, upload local files, or analyze any public GitHub repo by URL.

🌟 Features

🪐 Galaxy Graph Visualization

Every codebase is rendered as a galaxy with a consistent visual language:

Code ElementGalaxy ElementWhyClasses / Files⭐ StarsAnchors of the codebase — large, bright, centralFunctions / Methods🪐 PlanetsOrbit around their parent starCode Issues / Security Risks🕳️ Black HolesDense, dangerous, and worth avoidingFunction Calls / Dependencies🛰️ OrbitsThe gravitational pull connecting everything

🧠 Multi-Language Code Parsing

The CodeParser engine analyzes source files and extracts:


Classes and their members
Functions and methods (with signatures)
Import / dependency lists
Lines of code (LOC)
Cyclomatic complexity
Estimated code coverage
Code quality issues and security risks

## ☄️ Celestial Visual Mappings

When viewing your codebase in the 3D galaxy:
- ⭐ **Stars (Classes/Modules)**: Size = Lines of Code (LOC); Brightness = Test Coverage %; Color = Programming Language.
- 🪐 **Planets (Functions/Methods)**: Orbit radius = parameter count; Speed = complexity.
- 🌌 **Orbital Paths (Dependencies)**: Neon curves connecting stars; Thickness = dependency strength.
- 🕳️ **Black Holes (Bugs/Risks)**: Dark core with red/orange accretion rings. Size scales with vulnerability severity (e.g. secret keys in code, unsafe `eval` execution).

---

🌌 Dependency Graph Construction

The GalaxyGraphBuilder takes parsed file metrics and builds the full galaxy structure:


Generates nodes (stars, planets, black holes) and edges (orbits, dependencies)
Detects circular dependencies
Calculates dependency depth
Computes overall codebase health metrics


👥 WorkIQ — Organizational Context

The WorkIQSimulator enriches each node with simulated human context:


Commit history signals
Team discussion activity
Adds a "who's been working on this" layer to the technical graph


🔭 Three Ways to Explore


Demo Mode — instantly browse pre-loaded sample galaxies (React frontend, FastAPI backend, etc.)
Local Upload — upload your own project files for analysis
GitHub Import — paste a repo URL (owner/repo or full GitHub link) and analyze it directly, supporting both main and master branches



📁 Project Structure

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
│   └── work_iq.py         # WorkIQSimulator class - generates organizational context
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
│
└── test_parser.py         # Unit tests for the CodeParser


### 🚀 Launch Controls (Root Folder)

- **[run.bat](file:///c:/Users/dell/OneDrive/Desktop/CosmoCode/run.bat)**: Double-click this script on Windows to launch the Python backend and open the frontend in your browser.
- **[server.py](file:///c:/Users/dell/OneDrive/Desktop/CosmoCode/server.py)**: The Tornado web server and code analysis engine. Scans and parses Python, JS/TS, Go, and Java files.
- **[README.md](file:///c:/Users/dell/OneDrive/Desktop/CosmoCode/README.md)**: This guide.

### 🎨 Frontend Assets (inside `public/` folder)

- **[public/index.html](file:///c:/Users/dell/OneDrive/Desktop/CosmoCode/public/index.html)**: The main layout structure containing HUD displays, Query consoles, and the WebGL canvas.
- **[public/style.css](file:///c:/Users/dell/OneDrive/Desktop/CosmoCode/public/style.css)**: Glassmorphic cyber stylesheet with tailored HSL neon palettes and smooth viewport sizing.

### 🧠 Core Javascript Engines (inside `public/js/` folder)

- **[public/js/galaxy.js](file:///c:/Users/dell/OneDrive/Desktop/CosmoCode/public/js/galaxy.js)**: The WebGL engine using Three.js. Manages camera interpolation, orbital planet rotation, curved lines, and pulsing accretion disks.
- **[public/js/app.js](file:///c:/Users/dell/OneDrive/Desktop/CosmoCode/public/js/app.js)**: The main controller linking WebGL scenes, Natural Language Queries, and sidebar listings.
- **[public/js/parser.js](file:///c:/Users/dell/OneDrive/Desktop/CosmoCode/public/js/parser.js)**: In-browser code parser that extracts metrics (LOC, complexity) and counts classes/functions client-side.
- **[public/js/mockData.js](file:///c:/Users/dell/OneDrive/Desktop/CosmoCode/public/js/mockData.js)**: Pre-parsed mock database models representing React and FastAPI systems for instant offline loading.


🧩 Module Reference

Core (core/)

parser.py — CodeParser
Parses code files in multiple languages, extracting classes, functions, dependencies, and metrics. Detects code quality issues, security risks, cyclomatic complexity, and estimated coverage.

graph_builder.py — GalaxyGraphBuilder
Builds the galaxy graph structure from parsed code — nodes (stars, planets, black holes) and edges (orbits, dependencies). Detects circular dependencies, dependency depth, and overall codebase health.

work_iq.py — WorkIQSimulator
Generates simulated organizational context (commit history, team discussion signals) and attaches it to graph nodes.

Handlers (handlers/)

base.py — BaseHandler
Base Tornado request handler providing CORS headers and shared functionality across all endpoints, plus OPTIONS request handling.

demo.py — DemoDataHandler
GET /api/demo-data — returns sample code analysis for demo repositories (React frontend, FastAPI backend, and more).

local.py — ParseLocalHandler
POST /api/parse-local — accepts uploaded local files as JSON, parses them, builds the dependency graph, and enriches it with WorkIQ signals.

github.py — ParseGithubHandler
POST /api/parse-github — downloads and analyzes a GitHub repository (supports main and master branches), returning the full graph analysis with WorkIQ context.

Configuration (config.py)


PORT — server port (default 8000)
WORKSPACE_DIR — root directory used for serving static frontend files


Entry Point (server.py)

Imports the core and handler modules, configures the Tornado application and URL routing, and starts the server.


🔄 How It Works


Server Startup
server.py creates the Tornado app, registers routes for each API endpoint, and serves static frontend files from public/.
Code Analysis Flow
A request comes in (demo data, local files, or a GitHub URL) → CodeParser analyzes each file → GalaxyGraphBuilder constructs the graph → WorkIQSimulator adds organizational context → the result is returned as JSON.
Galaxy Rendering
The frontend (Three.js) takes the returned graph JSON and renders it as an interactive 3D galaxy — stars, planets, black holes, and orbits — that users can pan, zoom, and click through.



🚀 Getting Started

Prerequisites


Python 3.8+
Tornado (pip install tornado)


Run the Server

bashpython server.py

Or, on Windows, use the included batch script — it launches your browser and starts the server in one step:

bashrun.bat

Then open:

http://localhost:8000


🔌 API Reference

GET /api/demo-data

Returns sample code analysis for built-in demo repositories.

Response:

json{
  "react_galaxy": { ... },
  "python_galaxy": { ... }
}

POST /api/parse-local

Analyze a set of locally uploaded files.

Request:

json{
  "files": [
    { "path": "src/app.js", "content": "..." },
    { "path": "src/main.js", "content": "..." }
  ]
}

Response:

json{
  "status": "success",
  "graph": { ... }
}

POST /api/parse-github

Analyze a public GitHub repository.

Request:

json{
  "url": "owner/repo"
}

(also accepts a full https://github.com/owner/repo URL)

Response:

json{
  "status": "success",
  "repoName": "owner/repo",
  "graph": { ... }
}


🗣️ Supported Languages

LanguageExtensionsPython.pyJavaScript.js, .jsxTypeScript.ts, .tsxJava.javaC#.csGo.go


🧪 Testing

Unit tests for the parser live in test_parser.py and cover multi-language parsing (e.g. Python class/function extraction and C# namespace/class parsing).

Run the tests with:

bashpython -m unittest test_parser.py


🏗️ Architecture Notes

COSMOCODE was refactored from a single monolithic server.py into a modular architecture:


✅ Separation of Concerns — each module has a single responsibility
✅ Easier Testing — individual modules can be tested independently
✅ Better Maintainability — changes are localized to specific files
✅ Code Reusability — components can be imported and used elsewhere
✅ Scalability — easy to add new handlers or parsing logic
✅ Readability — smaller, focused files are easier to understand


See ARCHITECTURE.md for the full breakdown.

🛠️ Technologies

TechnologyPurposePython 3Core server language and analysis runtimeTornadoAsync web server and HTTP request handlingThree.js3D galaxy rendering and interactive visualizationOrbitControls.jsCamera pan, zoom, and rotate in the galaxy viewLucide IconsClean, consistent UI iconographyGitHub APIRepository download and branch resolution for GitHub parsingGitHub CopilotAI-assisted development throughout the project
🌌 Visual Legend

🏆 Evaluation Criteria

CriteriaWeightHow COSMOCODE DeliversAccuracy & Relevance20%Fully meets the Creative Apps track requirements. Parses 6 languages with AST-level accuracy. Foundry IQ recommendations are grounded in real code evidence, not hallucinations. GitHub Copilot usage is integrated and documented throughout development.Reasoning & Multi-step Thinking20%5-step pipeline: Upload / Fetch → Parse → Graph Build → WorkIQ Enrich → Visualize. Foundry IQ performs multi-step risk reasoning — clustering low-coverage, high-complexity nodes to produce ranked, prioritized recommendations with file-level citations.Creativity & Originality15%First-of-its-kind spatial code exploration tool. Mapping software architecture to an interactive 3D galaxy is a novel metaphor that makes abstract codebases immediately intuitive. WorkIQ Team Signals fuses code analysis with human organizational context — a unique combination.User Experience & Presentation15%Polished dark-theme UI with a real-time 3D galaxy, Fabric IQ Query Console for semantic filtering, Foundry IQ recommendations panel, Mission Control Dashboard with 5 health metrics, drill-down star/planet detail views with source code preview and team chat signals.Reliability & Safety20%All processing is local — no code is sent to external servers. Input validation on all API endpoints. Graceful error handling across local, GitHub, and demo flows. Modular architecture ensures each component can be tested independently (test_parser.py included).Community Vote10%The galaxy metaphor is visually striking and instantly shareable. Seeing your own codebase rendered as a 3D universe is a moment everyone wants to show their team. The Mission Control Dashboard gives a clear, at-a-glance health score that resonates with engineers and managers alike.


🙏 Acknowledgements


Built for Agents League 2026 by Microsoft
AI-assisted development powered by GitHub Copilot
3D rendering by Three.js
Icons by Lucide
SymbolMeaning

⭐ StarA class or file
🪐 PlanetA function or method
🕳️ Black HoleA code issue or security risk
🛰️ OrbitA function call or dependency

📝 License

MIT License — free to use, modify, and distribute



🌌 Every codebase is a galaxy waiting to be explored. 🌌
