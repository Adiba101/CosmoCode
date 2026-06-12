import tornado.escape
from core import CodeParser, GalaxyGraphBuilder, WorkIQSimulator
from .base import BaseHandler


class DemoDataHandler(BaseHandler):
    """Endpoint for loading standard mock repo instantly."""
    
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
