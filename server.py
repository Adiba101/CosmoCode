import os
import re
import sys
import json
import urllib.request
import zipfile
import io
import math
import hashlib
import tornado.ioloop
import tornado.web
import tornado.escape

PORT = 8000
WORKSPACE_DIR = os.getcwd()

# Robust multi-language code parser
class CodeParser:
    @staticmethod
    def calculate_complexity(content):
        # Cyclomatic complexity approximation: count branch points
        branch_points = len(re.findall(r'\b(if|for|while|elif|else|catch|case|&&|\|\|)\b', content))
        return max(1, branch_points + 1)

    @staticmethod
    def detect_bugs_risks(content, file_path):
        risks = []
        # 1. Security check: hardcoded credentials
        creds_pattern = r'\b(secret|password|passwd|token|api_key|private_key)\s*=\s*[\'"][^\'"]{4,}[\'"]'
        for match in re.finditer(creds_pattern, content, re.IGNORECASE):
            line_no = content[:match.start()].count('\n') + 1
            risks.append({
                "category": "SECURITY",
                "severity": "CRITICAL",
                "message": "Potential hardcoded credential or secret key detected.",
                "line": line_no,
                "snippet": match.group(0),
                "owaspRef": "OWASP A02:2021-Cryptographic Failures"
            })
            
        # 2. Security check: dangerous functions
        eval_pattern = r'\b(eval|exec|unsafe|dangerouslySetInnerHTML)\b'
        for match in re.finditer(eval_pattern, content):
            line_no = content[:match.start()].count('\n') + 1
            risks.append({
                "category": "SECURITY",
                "severity": "HIGH",
                "message": f"Dangerous operation '{match.group(0)}' used, exposing risk of injection.",
                "line": line_no,
                "snippet": content.split('\n')[line_no-1].strip(),
                "owaspRef": "OWASP A03:2021-Injection"
            })

        # 3. Architectural check: God functions (length > 100 LOC)
        lines = content.split('\n')
        if len(lines) > 250:
            risks.append({
                "category": "ARCH",
                "severity": "MEDIUM",
                "message": f"God File Smell: File contains {len(lines)} lines, which violates modularity principles.",
                "line": 1,
                "snippet": lines[0],
                "owaspRef": "Clean Code: Single Responsibility Principle"
            })

        # 4. Error handling: empty catch/except blocks
        empty_except = r'(except\b.*:|catch\s*\(.*\)\s*\{)\s*(\bpass\b|\bcontinue\b|\{\}|\s*\}|\s*//\s*.*)'
        for match in re.finditer(empty_except, content, re.MULTILINE):
            line_no = content[:match.start()].count('\n') + 1
            risks.append({
                "category": "PERF",
                "severity": "HIGH",
                "message": "Silent Failure: Empty catch/except block swallows errors and blocks debugging.",
                "line": line_no,
                "snippet": match.group(0).strip().replace('\n', ' '),
                "owaspRef": "OWASP A09:2021-Security Logging and Monitoring Failures"
            })

        return risks

    @classmethod
    def parse_file(cls, file_path, content):
        _, ext = os.path.splitext(file_path.lower())
        
        # Initialize default metrics
        metrics = {
            "classes": [],
            "functions": [],
            "dependencies": [],
            "bugs": [],
            "loc": len(content.splitlines()),
            "complexity": cls.calculate_complexity(content),
            "coverage": 0,
            "language": "Text"
        }

        # Deterministic coverage simulation (based on hash)
        if "test" in file_path.lower():
            metrics["coverage"] = 100
        else:
            h = int(hashlib.md5(content.encode('utf-8')).hexdigest()[:4], 16)
            metrics["coverage"] = 20 + (h % 76)  # 20% to 95%

        # Detect risks
        metrics["bugs"] = cls.detect_bugs_risks(content, file_path)

        # Parse based on language
        if ext == '.py':
            metrics["language"] = "Python"
            # Classes
            class_matches = re.finditer(r'^\s*class\s+(\w+)(?:\s*\((.*?)\))?\s*:', content, re.MULTILINE)
            for m in class_matches:
                metrics["classes"].append({
                    "name": m.group(1),
                    "line": content[:m.start()].count('\n') + 1,
                    "inherits": [x.strip() for x in m.group(2).split(',')] if m.group(2) else []
                })
            # Functions
            func_matches = re.finditer(r'^\s*def\s+(\w+)\s*\((.*?)\)\s*(?:->\s*.*?)?:', content, re.MULTILINE)
            for m in func_matches:
                param_count = len(m.group(2).split(',')) if m.group(2).strip() else 0
                metrics["functions"].append({
                    "name": m.group(1),
                    "line": content[:m.start()].count('\n') + 1,
                    "paramCount": param_count,
                    "isPublic": not m.group(1).startswith('_')
                })
            # Dependencies
            dep_matches = re.finditer(r'^\s*(?:import\s+(\w+)|from\s+(\w+)\s+import)', content, re.MULTILINE)
            for m in dep_matches:
                dep_name = m.group(1) or m.group(2)
                if dep_name:
                    metrics["dependencies"].append(dep_name)

        elif ext in ['.js', '.jsx', '.ts', '.tsx']:
            metrics["language"] = "JavaScript" if ext in ['.js', '.jsx'] else "TypeScript"
            # Classes
            class_matches = re.finditer(r'\bclass\s+(\w+)(?:\s+extends\s+(\w+))?', content)
            for m in class_matches:
                metrics["classes"].append({
                    "name": m.group(1),
                    "line": content[:m.start()].count('\n') + 1,
                    "inherits": [m.group(2)] if m.group(2) else []
                })
            # Functions
            func_matches = re.finditer(r'\b(?:function\s+(\w+)|const\s+(\w+)\s*=\s*(?:\(.*?\)|[^=\n]+)\s*=>|(\w+)\s*\((.*?)\)\s*\{)', content)
            for m in func_matches:
                name = m.group(1) or m.group(2) or m.group(3)
                if name and name not in ['if', 'for', 'while', 'switch', 'catch']:
                    params_text = m.group(4) or ""
                    param_count = len(params_text.split(',')) if params_text.strip() else 0
                    metrics["functions"].append({
                        "name": name,
                        "line": content[:m.start()].count('\n') + 1,
                        "paramCount": param_count,
                        "isPublic": True
                    })
            # Dependencies
            dep_matches = re.finditer(r'\b(?:import\s+.*?\s+from\s+[\'"](.*?)[\'"]|require\s*\(\s*[\'"](.*?)[\'"]\s*\))', content)
            for m in dep_matches:
                dep_path = m.group(1) or m.group(2)
                if dep_path:
                    # extract end component of path
                    dep_name = dep_path.split('/')[-1]
                    metrics["dependencies"].append(dep_name)

        elif ext == '.go':
            metrics["language"] = "Go"
            # Classes (Structs count as classes in Go context)
            struct_matches = re.finditer(r'\btype\s+(\w+)\s+struct\b', content)
            for m in struct_matches:
                metrics["classes"].append({
                    "name": m.group(1),
                    "line": content[:m.start()].count('\n') + 1,
                    "inherits": []
                })
            # Functions
            func_matches = re.finditer(r'\bfunc\s+(?:\((.*?)\)\s*)?(\w+)\s*\((.*?)\)', content)
            for m in func_matches:
                name = m.group(2)
                params_text = m.group(3) or ""
                param_count = len(params_text.split(',')) if params_text.strip() else 0
                metrics["functions"].append({
                    "name": name,
                    "line": content[:m.start()].count('\n') + 1,
                    "paramCount": param_count,
                    "isPublic": name[0].isupper() if name else False
                })
            # Dependencies
            dep_matches = re.finditer(r'\bimport\s+\((.*?)\)|\bimport\s+[\'"](.*?)[\'"]', content, re.DOTALL)
            for m in dep_matches:
                if m.group(1):
                    # Multi-line import block
                    paths = re.findall(r'[\'"](.*?)[\'"]', m.group(1))
                    metrics["dependencies"].extend([p.split('/')[-1] for p in paths])
                elif m.group(2):
                    metrics["dependencies"].append(m.group(2).split('/')[-1])

        elif ext == '.java':
            metrics["language"] = "Java"
            # Classes
            class_matches = re.finditer(r'\b(?:class|interface|enum)\s+(\w+)', content)
            for m in class_matches:
                metrics["classes"].append({
                    "name": m.group(1),
                    "line": content[:m.start()].count('\n') + 1,
                    "inherits": []
                })
            # Functions
            func_matches = re.finditer(r'\b(?:public|protected|private|static|\s)+\s+[\w<>]+\s+(\w+)\s*\((.*?)\)\s*(?:throws\s+.*?)?\{', content)
            for m in func_matches:
                name = m.group(1)
                if name not in ['if', 'for', 'while', 'switch', 'catch', 'synchronized']:
                    params_text = m.group(2) or ""
                    param_count = len(params_text.split(',')) if params_text.strip() else 0
                    metrics["functions"].append({
                        "name": name,
                        "line": content[:m.start()].count('\n') + 1,
                        "paramCount": param_count,
                        "isPublic": "public" in m.group(0)
                    })
            # Dependencies
            dep_matches = re.finditer(r'^\s*import\s+(.*?);', content, re.MULTILINE)
            for m in dep_matches:
                dep_name = m.group(1).split('.')[-1]
                metrics["dependencies"].append(dep_name)

        elif ext == '.cs':
            metrics["language"] = "C#"
            # Classes
            class_matches = re.finditer(r'\b(?:class|interface|struct|enum)\s+(\w+)', content)
            for m in class_matches:
                metrics["classes"].append({
                    "name": m.group(1),
                    "line": content[:m.start()].count('\n') + 1,
                    "inherits": []
                })
            # Functions
            func_matches = re.finditer(r'\b(?:public|protected|private|static|internal|\s)+\s+[\w<>]+\s+(\w+)\s*\((.*?)\)\s*\{', content)
            for m in func_matches:
                name = m.group(1)
                if name not in ['if', 'for', 'while', 'switch', 'catch', 'using', 'lock']:
                    params_text = m.group(2) or ""
                    param_count = len(params_text.split(',')) if params_text.strip() else 0
                    metrics["functions"].append({
                        "name": name,
                        "line": content[:m.start()].count('\n') + 1,
                        "paramCount": param_count,
                        "isPublic": "public" in m.group(0)
                    })
            # Dependencies
            dep_matches = re.finditer(r'^\s*using\s+(.*?);', content, re.MULTILINE)
            for m in dep_matches:
                dep_name = m.group(1).split('.')[-1]
                metrics["dependencies"].append(dep_name)

        return metrics

# Process repo analysis outputs into Galaxy JSON
class GalaxyGraphBuilder:
    @staticmethod
    def detect_circular_dependencies(edges):
        """Detect circular dependencies using DFS with colors.
        Returns count of circular dependencies found."""
        # Build adjacency list for dependency edges only
        graph = {}
        for edge in edges:
            if edge["type"] == "dependency":
                source = edge["source"]
                target = edge["target"]
                if source not in graph:
                    graph[source] = []
                graph[source].append(target)
        
        # Track visited states: 0 = unvisited, 1 = visiting, 2 = visited
        states = {}
        cycles_found = 0
        
        def has_cycle(node, path):
            nonlocal cycles_found
            if node in states:
                if states[node] == 1:  # Back edge found - cycle detected
                    cycles_found += 1
                    return True
                return False
            
            states[node] = 1  # Mark as visiting
            
            for neighbor in graph.get(node, []):
                if has_cycle(neighbor, path + [node]):
                    pass
            
            states[node] = 2  # Mark as visited
            return False
        
        # Check all nodes for cycles
        for node in graph:
            if node not in states:
                has_cycle(node, [])
        
        return min(cycles_found, 10)  # Cap at 10 to avoid huge numbers
    
    @staticmethod
    def calculate_dependency_depth(edges, nodes):
        """Calculate maximum dependency depth (longest dependency chain).
        Returns the depth as a float. Handles circular dependencies gracefully."""
        # Build adjacency list for dependencies
        graph = {}
        in_degree = {}
        
        for node in nodes:
            node_id = node["id"]
            in_degree[node_id] = 0
            graph[node_id] = []
        
        for edge in edges:
            if edge["type"] == "dependency":
                source = edge["source"]
                target = edge["target"]
                if source not in graph:
                    graph[source] = []
                if target not in in_degree:
                    in_degree[target] = 0
                graph[source].append(target)
                in_degree[target] += 1
        
        # Find root nodes (no incoming dependencies)
        roots = [node_id for node_id in graph if in_degree.get(node_id, 0) == 0]
        
        # If no roots (circular dependency), compute depth from all unvisited nodes
        if not roots:
            roots = list(graph.keys())
        
        if not roots:
            return 0.0
        
        # DFS to find maximum depth from each root, with cycle detection
        max_depth = 0
        global_visited = set()
        
        def dfs_depth(node, current_depth, path_visited):
            nonlocal max_depth
            max_depth = max(max_depth, current_depth)
            
            for neighbor in graph.get(node, []):
                # Skip if we've hit a cycle in this path
                if neighbor in path_visited:
                    continue
                # Mark as visited for this path
                path_visited.add(neighbor)
                dfs_depth(neighbor, current_depth + 1, path_visited)
                path_visited.discard(neighbor)
        
        for root in roots:
            if root not in global_visited:
                global_visited.add(root)
                path_visited = {root}
                dfs_depth(root, 1, path_visited)
        
        return float(max_depth)

    @staticmethod
    def build_graph(files_data):
        nodes = []
        edges = []
        
        # Summaries for Counts
        summary = {
            "stars": 0,       # Classes
            "planets": 0,     # Functions
            "orbits": 0,      # Dependencies
            "blackholes": 0,  # Bugs
            "loc": 0,
            "avgCoverage": 0,
            "avgComplexity": 0
        }
        
        node_map = {}
        total_coverage = 0
        total_complexity = 0
        valid_files_count = 0
        
        # First Pass: Register all file nodes (Stars)
        for filepath, data in files_data.items():
            valid_files_count += 1
            summary["loc"] += data["loc"]
            total_coverage += data["coverage"]
            total_complexity += data["complexity"]
            
            # Group classes as stars
            if data["classes"]:
                for cls in data["classes"]:
                    summary["stars"] += 1
                    node_id = f"class:{filepath}:{cls['name']}"
                    node = {
                        "id": node_id,
                        "name": cls["name"],
                        "type": "star",
                        "filepath": filepath,
                        "language": data["language"],
                        "loc": data["loc"],
                        "coverage": data["coverage"],
                        "complexity": data["complexity"],
                        "line": cls["line"],
                        "bugsCount": len(data["bugs"]),
                        "workSignalsCount": int(hashlib.md5(cls["name"].encode()).hexdigest()[:1], 16) % 4
                    }
                    nodes.append(node)
                    node_map[cls["name"]] = node_id
            else:
                # File itself counts as a star if no classes defined
                summary["stars"] += 1
                base_name = os.path.basename(filepath)
                node_id = f"file:{filepath}:{base_name}"
                node = {
                    "id": node_id,
                    "name": base_name,
                    "type": "star",
                    "filepath": filepath,
                    "language": data["language"],
                    "loc": data["loc"],
                    "coverage": data["coverage"],
                    "complexity": data["complexity"],
                    "line": 1,
                    "bugsCount": len(data["bugs"]),
                    "workSignalsCount": int(hashlib.md5(base_name.encode()).hexdigest()[:1], 16) % 4
                }
                nodes.append(node)
                node_map[base_name] = node_id

            # Functions as planets orbiting their file's classes
            for func in data["functions"]:
                summary["planets"] += 1
                func_id = f"func:{filepath}:{func['name']}"
                # Parent star is the first class in the file, or the file star itself
                parent_id = f"class:{filepath}:{data['classes'][0]['name']}" if data["classes"] else f"file:{filepath}:{os.path.basename(filepath)}"
                
                node = {
                    "id": func_id,
                    "name": func["name"],
                    "type": "planet",
                    "filepath": filepath,
                    "language": data["language"],
                    "parentStar": parent_id,
                    "paramCount": func["paramCount"],
                    "isPublic": func["isPublic"],
                    "complexity": max(1, data["complexity"] // (len(data["functions"]) or 1)),
                    "line": func["line"]
                }
                nodes.append(node)
                # Link planet to parent star
                edges.append({
                    "source": parent_id,
                    "target": func_id,
                    "type": "orbit"
                })

            # Bugs as Black Holes
            for bug in data["bugs"]:
                summary["blackholes"] += 1
                bug_id = f"bug:{filepath}:{bug['category']}:{bug['line']}"
                parent_id = f"class:{filepath}:{data['classes'][0]['name']}" if data["classes"] else f"file:{filepath}:{os.path.basename(filepath)}"
                
                node = {
                    "id": bug_id,
                    "name": f"{bug['category']}: L{bug['line']}",
                    "type": "blackhole",
                    "filepath": filepath,
                    "category": bug["category"],
                    "severity": bug["severity"],
                    "message": bug["message"],
                    "line": bug["line"],
                    "owaspRef": bug["owaspRef"],
                    "snippet": bug["snippet"],
                    "parentStar": parent_id
                }
                nodes.append(node)
                # Link blackhole to parent star
                edges.append({
                    "source": parent_id,
                    "target": bug_id,
                    "type": "gravitational_pull"
                })

        # Second Pass: Resolve dependencies (Orbit Paths)
        for filepath, data in files_data.items():
            parent_id = f"class:{filepath}:{data['classes'][0]['name']}" if data["classes"] else f"file:{filepath}:{os.path.basename(filepath)}"
            for dep in data["dependencies"]:
                # Look for matching target star in code
                if dep in node_map:
                    summary["orbits"] += 1
                    edges.append({
                        "source": parent_id,
                        "target": node_map[dep],
                        "type": "dependency",
                        "strength": 2 + (data["complexity"] % 4)
                    })

        if valid_files_count > 0:
            summary["avgCoverage"] = round(total_coverage / valid_files_count, 1)
            summary["avgComplexity"] = round(total_complexity / valid_files_count, 1)
        
        # Calculate dependency metrics
        summary["dependencyDepth"] = GalaxyGraphBuilder.calculate_dependency_depth(edges, nodes)
        summary["circularImports"] = GalaxyGraphBuilder.detect_circular_dependencies(edges)
        
        # Calculate codebase health score (same formula as frontend)
        # Base 100, minus penalties for complexity and bugs, plus coverage bonus
        bug_penalty = summary["blackholes"] * 12
        complexity_penalty = summary["avgComplexity"] * 1.5
        coverage_bonus = (summary["avgCoverage"] - 50) * 0.1
        summary["codebaseHealth"] = max(0, min(100, round(100 - bug_penalty - complexity_penalty + coverage_bonus)))
            
        return {
            "summary": summary,
            "nodes": nodes,
            "edges": edges
        }

# Simulated Work IQ Organizational Context Generator
class WorkIQSimulator:
    DEVELOPERS = ["Sarah Chen", "Marcus Vance", "Elena Rostova", "Alex Mercer"]
    MESSAGES = [
        "Hey team, this module has been failing on prod occasionally. I think there is a concurrency leak in the connection pool.",
        "Refactoring this class today to fit the new Auth spec. Ping me if you hit any import breaks.",
        "Let's add test coverage for this function before the sprint review. Fabric IQ shows it has 0% coverage currently.",
        "OWASP scan flagged this section for weak hashing. We should migrate this to PBKDF2 as soon as possible.",
        "This is deprecated code from v1. Please don't write any new imports pointing to this module.",
        "We discussed this file in the standup meeting on June 8th. The plan is to split it into microservices next sprint."
    ]

    @classmethod
    def get_signals(cls, node_name, seed_str):
        h = int(hashlib.md5(seed_str.encode()).hexdigest()[:4], 16)
        
        # Commit context
        author = cls.DEVELOPERS[h % len(cls.DEVELOPERS)]
        commits_count = 3 + (h % 20)
        days_ago = h % 30
        
        # Teams context
        msg_count = 1 + (h % 3)
        teams_msgs = []
        for i in range(msg_count):
            msg_idx = (h + i) % len(cls.MESSAGES)
            teams_msgs.append({
                "sender": cls.DEVELOPERS[(h + i + 1) % len(cls.DEVELOPERS)],
                "timestamp": f"{days_ago + i} days ago",
                "message": cls.MESSAGES[msg_idx]
            })

        return {
            "author": author,
            "commitsCount": commits_count,
            "lastModified": f"{days_ago} days ago",
            "teamsDiscussions": teams_msgs,
            "prComment": f"Resolved PR review comment: 'Refactor {node_name} to prevent cyclic dependencies.'"
        }

# Base handler providing CORS headers
class BaseHandler(tornado.web.RequestHandler):
    def set_default_headers(self):
        self.set_header("Access-Control-Allow-Origin", "*")
        self.set_header("Access-Control-Allow-Headers", "x-requested-with, content-type")
        self.set_header("Access-Control-Allow-Methods", "POST, GET, OPTIONS")

    def options(self):
        self.set_status(204)
        self.finish()

# Endpoint for loading standard mock repo instantly
class DemoDataHandler(BaseHandler):
    def get(self):
        # Build three demo repositories: React App, Python Backend, Go Microservice
        demo_repos = {
            "react_galaxy": {
                "name": "React Portal Frontend",
                "summary": "Core user web application dashboard.",
                "files": {
                    "src/components/AuthCard.tsx": """import React, { useState } from 'react';
import { useAuth } from '../context/AuthContext';
import { securityLogger } from '../utils/logger';

export class AuthCard extends React.Component {
    constructor(props) {
        super(props);
        this.state = { username: '', password: '' };
    }

    handleLogin = async () => {
        const { username, password } = this.state;
        // SECURITY RISK: Weak security logging of parameters
        securityLogger.info("Attempting login for user: " + username);
        
        if(password === "123456" || password === "admin") {
            // SECURITY CRITICAL BUG
            alert("Warning: Weak credentials used!");
        }

        try {
            await this.props.auth.login(username, password);
        } catch (e) {
            // SILENT FAILURE BUG
            console.log("error"); 
        }
    }
}
""",
                    "src/context/AuthContext.tsx": """import { createContext, useContext } from 'react';
import { api } from '../services/api';

export class AuthProvider {
    login(u, p) {
        return api.post('/auth/login', { u, p });
    }
    logout() {
        return api.post('/auth/logout');
    }
}
""",
                    "src/services/api.ts": """export const api = {
    post: (url, body) => fetch(url, { method: 'POST', body: JSON.stringify(body) }),
    get: (url) => fetch(url)
};
"""
                }
            },
            "python_galaxy": {
                "name": "FastAPI AI Orchestrator",
                "summary": "Core AI model routing and pipeline server.",
                "files": {
                    "app/main.py": """from fastapi import FastAPI, Depends
from app.services.model_router import ModelRouter
from app.auth.security import get_current_user

app = FastAPI()

class ApiServer:
    def __init__(self):
        self.router = ModelRouter()

    def get_health(self):
        return {"status": "ok"}

@app.get("/predict")
def predict(prompt: str, user = Depends(get_current_user)):
    router = ModelRouter()
    return router.route_prompt(prompt)
""",
                    "app/services/model_router.py": """from app.services.llm_service import LlmService
import eval  # smell

class ModelRouter:
    def __init__(self):
        self.llm = LlmService()
        self.api_key = "sk-live-prod-secret-992384a82b13" # CRITICAL SECRET BUG

    def route_prompt(self, prompt):
        # GOD METHOD smelling code
        if not prompt:
            return {"error": "empty prompt"}
        if "generate" in prompt:
            return self.llm.generate(prompt)
        elif "analyze" in prompt:
            return self.llm.analyze(prompt)
        else:
            # Dangerous evaluation code injection risk
            return eval(prompt) 
""",
                    "app/services/llm_service.py": """class LlmService:
    def generate(self, p):
        return {"result": f"Generated text for {p}"}
    def analyze(self, p):
        return {"result": f"Analyzed text for {p}"}
""",
                    "app/auth/security.py": """def get_current_user(token: str):
    try:
        # verify token logic
        return {"user": "developer"}
    except Exception:
        pass # SILENT FAILURE BUG
"""
                }
            }
        }

        # Build galaxy data for both and return
        response_data = {}
        for key, repo in demo_repos.items():
            parsed_files = {}
            for filepath, content in repo["files"].items():
                parsed_files[filepath] = CodeParser.parse_file(filepath, content)
            
            graph = GalaxyGraphBuilder.build_graph(parsed_files)
            
            # Enrich nodes with Work IQ
            for node in graph["nodes"]:
                if node["type"] in ["star", "planet"]:
                    node["workSignals"] = WorkIQSimulator.get_signals(node["name"], node["id"])
                    
            response_data[key] = {
                "name": repo["name"],
                "summary": repo["summary"],
                "graph": graph
            }

        self.write(response_data)

# Endpoint for parsing folder uploaded from local directory structure
class ParseLocalHandler(BaseHandler):
    def post(self):
        try:
            body = tornado.escape.json_decode(self.request.body)
            # Support folders payload: array of {path: 'src/app.js', content: '...'}
            files = body.get("files", [])
            
            parsed_files = {}
            for f in files:
                path = f.get("path", "")
                content = f.get("content", "")
                parsed_files[path] = CodeParser.parse_file(path, content)
                
            graph = GalaxyGraphBuilder.build_graph(parsed_files)
            
            # Enrich nodes with Work IQ
            for node in graph["nodes"]:
                if node["type"] in ["star", "planet"]:
                    node["workSignals"] = WorkIQSimulator.get_signals(node["name"], node["id"])

            self.write({
                "status": "success",
                "graph": graph
            })
        except Exception as e:
            self.set_status(500)
            self.write({"status": "error", "message": str(e)})

# Endpoint for downloading and parsing a GitHub repository ZIP
class ParseGithubHandler(BaseHandler):
    def post(self):
        try:
            body = tornado.escape.json_decode(self.request.body)
            repo_url = body.get("url", "").strip()
            
            if not repo_url:
                self.set_status(400)
                self.write({"status": "error", "message": "Repository URL is required"})
                return

            # Clean github URL to extract owner/repo
            # Pattern matches: https://github.com/owner/repo or owner/repo
            github_pattern = r'(?:https?://github\.com/)?([^/]+)/([^/]+?)(?:\.git|/)?$'
            match = re.search(github_pattern, repo_url)
            if not match:
                self.set_status(400)
                self.write({"status": "error", "message": "Invalid GitHub repository URL format"})
                return
            
            owner = match.group(1)
            repo = match.group(2)
            
            # Use zip ball download API
            zip_url = f"https://api.github.com/repos/{owner}/{repo}/zipball/main"
            
            headers = {
                "User-Agent": "Code-Constellation-Visualizer-Agent"
            }
            
            # Fetch zip file
            import ssl
            ssl_context = ssl._create_unverified_context()
            req = urllib.request.Request(zip_url, headers=headers)
            try:
                with urllib.request.urlopen(req, context=ssl_context) as response:
                    zip_data = response.read()
            except Exception as e:
                # Try master branch if main branch failed
                zip_url_master = f"https://api.github.com/repos/{owner}/{repo}/zipball/master"
                req_master = urllib.request.Request(zip_url_master, headers=headers)
                with urllib.request.urlopen(req_master, context=ssl_context) as response:
                    zip_data = response.read()
            
            # Extract and parse in-memory
            parsed_files = {}
            with zipfile.ZipFile(io.BytesIO(zip_data)) as z:
                for filename in z.namelist():
                    # Skip directories, system files, and binary assets
                    if filename.endswith('/') or any(x in filename.lower() for x in ['.png', '.jpg', '.jpeg', '.gif', '.pdf', '.node', '.dll', '.exe', 'node_modules/','.git/']):
                        continue
                    
                    try:
                        # Extract file content
                        with z.open(filename) as f:
                            content = f.read().decode('utf-8', errors='ignore')
                            
                        # Clean prefix repo-folder name
                        clean_path = '/'.join(filename.split('/')[1:])
                        if clean_path:
                            parsed_files[clean_path] = CodeParser.parse_file(clean_path, content)
                    except Exception:
                        continue # Skip unparseable files
            
            if not parsed_files:
                self.set_status(404)
                self.write({"status": "error", "message": "No parseable code files found in the repository."})
                return

            graph = GalaxyGraphBuilder.build_graph(parsed_files)
            
            # Enrich nodes with Work IQ
            for node in graph["nodes"]:
                if node["type"] in ["star", "planet"]:
                    node["workSignals"] = WorkIQSimulator.get_signals(node["name"], node["id"])

            self.write({
                "status": "success",
                "repoName": f"{owner}/{repo}",
                "graph": graph
            })
            
        except Exception as e:
            self.set_status(500)
            self.write({"status": "error", "message": str(e)})

def make_app():
    return tornado.web.Application([
        (r"/api/demo-data", DemoDataHandler),
        (r"/api/parse-local", ParseLocalHandler),
        (r"/api/parse-github", ParseGithubHandler),
        (r"/(.*)", tornado.web.StaticFileHandler, {"path": os.path.join(WORKSPACE_DIR, "public"), "default_filename": "index.html"}),
    ], debug=True)

if __name__ == "__main__":
    app = make_app()
    print(f"Code Constellation Server starting on http://localhost:{PORT}")
    app.listen(PORT)
    try:
        tornado.ioloop.IOLoop.current().start()
    except KeyboardInterrupt:
        print("\nShutting down Code Constellation Server...")
        sys.exit(0)
