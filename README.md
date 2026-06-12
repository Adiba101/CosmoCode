# 🌌 COSMOCODE
### AI-Powered Galaxy Codebase Visualizer
*Agents League Hackathon • Microsoft Track • Creative Apps*

COSMOCODE transforms any software codebase into an interactive, navigable 3D galaxy. Classes are stars, functions are planets, dependencies are orbital paths, and risk zones are black holes. Developers explore their entire project as a living universe, grasping architecture and risk without reading lines of code.

---

## 🛠️ File Structure & Access Map

Here is the directory structure. You can click on any file below to open it directly:

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

---

## ☄️ Celestial Visual Mappings

When viewing your codebase in the 3D galaxy:
- ⭐ **Stars (Classes/Modules)**: Size = Lines of Code (LOC); Brightness = Test Coverage %; Color = Programming Language.
- 🪐 **Planets (Functions/Methods)**: Orbit radius = parameter count; Speed = complexity.
- 🌌 **Orbital Paths (Dependencies)**: Neon curves connecting stars; Thickness = dependency strength.
- 🕳️ **Black Holes (Bugs/Risks)**: Dark core with red/orange accretion rings. Size scales with vulnerability severity (e.g. secret keys in code, unsafe `eval` execution).

---

## ⚡ Quick Start
1. Go to the root directory `c:\Users\dell\OneDrive\Desktop\CosmoCode\`.
4. Install the Python dependency:

    pip install -r requirements.txt

5. Double-click the **[run.bat](file:///c:/Users/dell/OneDrive/Desktop/CosmoCode/run.bat)** file or run `python server.py`.
6. Your browser will automatically open to `http://localhost:8000/`.
7. The system will auto-load a mock React Frontend galaxy on start so you can see the orbiting planets and black holes immediately.
8. Click **Load New Repo** at the top right to drag-and-drop a local folder or parse a GitHub URL.

## Tests

Run the built-in unit tests with:

    python -m unittest discover tests

Or on Windows:

    run_tests.bat
