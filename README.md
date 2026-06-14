

---

# 🌌 COSMOCODE — Explore Your Codebase as a Galaxy

> **An AI-powered code analyzer that transforms source code into an interactive 3D galaxy visualization.**

**Built with:** Python • Tornado • Three.js • GitHub Copilot

---

# ✨ Overview

COSMOCODE takes any codebase — uploaded locally or pulled directly from GitHub — and transforms it into a navigable **3D galaxy visualization**.

Classes and files become **Stars**, functions become **Planets**, code issues become **Black Holes**, and dependencies become **Orbits**.

This allows developers to:

* Understand architecture instantly
* Identify complexity hotspots
* Discover risky code
* Visualize dependencies
* Explore repositories interactively

Additionally, COSMOCODE introduces **WorkIQ**, a layer that simulates team activity and commit intelligence to add organizational context to the visualization.

---

# 🌠 Demo

### Option 1: Watch Demo Video

(Add your demo video link here)

### Option 2: Run Locally

```bash
python server.py
```

Open:

```text
http://localhost:8000
```

---

# 🌟 Features

## 🪐 Galaxy Graph Visualization

| Code Element        | Galaxy Element  | Meaning                      |
| ------------------- | --------------- | ---------------------------- |
| Classes / Files     | ⭐ Stars         | Main structural components   |
| Functions / Methods | 🪐 Planets      | Orbit around parent stars    |
| Dependencies        | 🛰️ Orbits      | Connections between modules  |
| Issues / Risks      | 🕳️ Black Holes | Security or quality concerns |

---

## 🧠 Multi-Language Parsing

COSMOCODE analyzes:

* Classes
* Functions
* Methods
* Dependencies
* Imports
* Lines of Code (LOC)
* Cyclomatic Complexity
* Test Coverage Estimates
* Security Risks
* Code Quality Issues

Supported Languages:

| Language   | Extensions    |
| ---------- | ------------- |
| Python     | `.py`         |
| JavaScript | `.js`, `.jsx` |
| TypeScript | `.ts`, `.tsx` |
| Java       | `.java`       |
| C#         | `.cs`         |
| Go         | `.go`         |

---

# ☄️ Celestial Visual Mapping

| Visual Element  | Mapping                                               |
| --------------- | ----------------------------------------------------- |
| ⭐ Stars         | Size = LOC, Brightness = Coverage %, Color = Language |
| 🪐 Planets      | Orbit Radius = Parameter Count                        |
| 🌌 Orbits       | Thickness = Dependency Strength                       |
| 🕳️ Black Holes | Size = Risk Severity                                  |

---

# 🌌 Dependency Graph Construction

The **GalaxyGraphBuilder**:

* Generates Stars, Planets, and Black Holes
* Creates dependency relationships
* Detects circular dependencies
* Measures dependency depth
* Calculates code health metrics

---

# 👥 WorkIQ — Organizational Context

WorkIQ enriches the galaxy with:

* Commit history signals
* Team activity indicators
* Collaboration insights
* Ownership hints

This provides a human perspective on the codebase.

---

# 🔭 Three Ways to Explore

### 🎮 Demo Mode

Explore preloaded sample repositories instantly.

### 📂 Local Upload

Upload your own project files for analysis.

### 🐙 GitHub Import

Paste a repository URL and analyze it instantly.

Supports:

* `owner/repo`
* Full GitHub URLs
* `main` branch
* `master` branch

---

# 📁 Project Structure

```text
CosmoCode/
│
├── server.py
├── config.py
├── run.bat
├── README.md
│
├── core/
│   ├── __init__.py
│   ├── parser.py
│   ├── graph_builder.py
│   └── work_iq.py
│
├── handlers/
│   ├── __init__.py
│   ├── base.py
│   ├── demo.py
│   ├── local.py
│   └── github.py
│
├── public/
│   ├── index.html
│   ├── style.css
│   │
│   └── js/
│       ├── app.js
│       ├── galaxy.js
│       ├── parser.js
│       ├── mockData.js
│       │
│       └── libs/
│           ├── three.min.js
│           ├── OrbitControls.js
│           └── lucide.min.js
│
└── test_parser.py
```

---

# 🚀 Launch Controls

## server.py

Main Tornado application.

Responsibilities:

* API routing
* Static file serving
* Backend startup
* Analysis orchestration

## run.bat

One-click launcher for Windows.

Starts:

* Backend server
* Browser session

## config.py

Stores application settings:

```python
PORT = 8000
WORKSPACE_DIR = "public"
```

---

# 🎨 Frontend Components

## index.html

Main application layout.

Contains:

* Galaxy canvas
* Dashboard panels
* Query console
* Information overlays

## style.css

Provides:

* Dark space-themed UI
* Glassmorphism
* Responsive design
* Animations

---

# 🧠 Core JavaScript Engines

## galaxy.js

Three.js rendering engine.

Features:

* Galaxy generation
* Camera controls
* Animations
* Orbit rendering

## app.js

Application controller.

Handles:

* UI interactions
* API communication
* State management

## parser.js

Browser-side parser.

Extracts:

* LOC
* Functions
* Classes
* Complexity metrics

## mockData.js

Provides sample repositories for Demo Mode.

---

# 🧩 Module Reference

## parser.py — CodeParser

Responsible for:

* Multi-language parsing
* Function extraction
* Class extraction
* Dependency detection
* Risk identification

---

## graph_builder.py — GalaxyGraphBuilder

Responsible for:

* Graph construction
* Dependency mapping
* Circular dependency detection
* Health metrics

---

## work_iq.py — WorkIQSimulator

Responsible for:

* Commit activity simulation
* Team signal generation
* Ownership insights

---

# 🔄 How It Works

```text
Upload / GitHub Repo
          │
          ▼
     CodeParser
          │
          ▼
 GalaxyGraphBuilder
          │
          ▼
    WorkIQSimulator
          │
          ▼
      JSON Graph
          │
          ▼
    Three.js Galaxy
```

---

# 🚀 Getting Started

## Prerequisites

* Python 3.8+
* Tornado

Install dependencies:

```bash
pip install tornado
```

---

## Start the Server

```bash
python server.py
```

Or:

```bash
run.bat
```

Visit:

```text
http://localhost:8000
```

---

# 🔌 API Reference

## GET /api/demo-data

Returns demo repositories.

### Response

```json
{
  "react_galaxy": {},
  "python_galaxy": {}
}
```

---

## POST /api/parse-local

Analyze local files.

### Request

```json
{
  "files": [
    {
      "path": "src/app.js",
      "content": "..."
    }
  ]
}
```

---

## POST /api/parse-github

Analyze a GitHub repository.

### Request

```json
{
  "url": "owner/repo"
}
```

### Response

```json
{
  "status": "success",
  "repoName": "owner/repo",
  "graph": {}
}
```

---

# 🧪 Testing

Run unit tests:

```bash
python -m unittest test_parser.py
```

Tests cover:

* Python parsing
* JavaScript parsing
* C# parsing
* Dependency extraction

---

# 🏗️ Architecture Benefits

✅ Separation of Concerns

✅ Modular Design

✅ Easier Testing

✅ Improved Maintainability

✅ Better Scalability

✅ Higher Reusability

---

# 🛠️ Technologies Used

| Technology     | Purpose                 |
| -------------- | ----------------------- |
| Python 3       | Backend Runtime         |
| Tornado        | Web Server              |
| Three.js       | 3D Visualization        |
| OrbitControls  | Camera Navigation       |
| Lucide Icons   | UI Icons                |
| GitHub API     | Repository Import       |
| GitHub Copilot | AI-Assisted Development |

---

# 🌌 Visual Legend

| Symbol | Meaning               |
| ------ | --------------------- |
| ⭐      | Class / File          |
| 🪐     | Function / Method     |
| 🛰️    | Dependency            |
| 🕳️    | Issue / Security Risk |

---

# 🏆 Hackathon Evaluation Alignment

| Criteria             | Weight | COSMOCODE Advantage                                |
| -------------------- | ------ | -------------------------------------------------- |
| Accuracy & Relevance | 20%    | Multi-language parsing and evidence-based insights |
| Reasoning            | 20%    | Multi-stage analysis pipeline                      |
| Creativity           | 15%    | Galaxy-based code exploration                      |
| User Experience      | 15%    | Interactive 3D visualization                       |
| Reliability & Safety | 20%    | Local processing and validation                    |
| Community Vote       | 10%    | Highly visual and shareable experience             |

---

# 🙏 Acknowledgements

* Built for **Agents League 2026**
* Developed with **GitHub Copilot**
* Visualization powered by **Three.js**
* Icons by **Lucide**

---

# 📝 License

MIT License

Free to use, modify, and distribute.

---

#🌌 Every codebase is a galaxy waiting to be explored.🌌


