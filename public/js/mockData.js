/**
 * Static Mock Datasets for offline-fallback demo usage.
 */
const MOCK_REPOS = {
  "react_galaxy": {
    "name": "React Portal Frontend",
    "summary": "Core user web application dashboard.",
    "graph": {
      "summary": {
        "stars": 3,
        "planets": 8,
        "orbits": 3,
        "blackholes": 2,
        "loc": 320,
        "avgCoverage": 65.5,
        "avgComplexity": 4.8
      },
      "nodes": [
        // Star 1
        {
          "id": "class:src/components/AuthCard.tsx:AuthCard",
          "name": "AuthCard",
          "type": "star",
          "filepath": "src/components/AuthCard.tsx",
          "language": "TypeScript",
          "loc": 120,
          "coverage": 45,
          "complexity": 8,
          "line": 5,
          "bugsCount": 2,
          "workSignalsCount": 3
        },
        // Star 2
        {
          "id": "class:src/context/AuthContext.tsx:AuthProvider",
          "name": "AuthProvider",
          "type": "star",
          "filepath": "src/context/AuthContext.tsx",
          "language": "TypeScript",
          "loc": 90,
          "coverage": 85,
          "complexity": 3,
          "line": 4,
          "bugsCount": 0,
          "workSignalsCount": 1
        },
        // Star 3
        {
          "id": "file:src/services/api.ts:api",
          "name": "api",
          "type": "star",
          "filepath": "src/services/api.ts",
          "language": "TypeScript",
          "loc": 110,
          "coverage": 90,
          "complexity": 2,
          "line": 1,
          "bugsCount": 0,
          "workSignalsCount": 2
        },
        
        // Planets for AuthCard
        {
          "id": "func:src/components/AuthCard.tsx:constructor",
          "name": "constructor",
          "type": "planet",
          "filepath": "src/components/AuthCard.tsx",
          "language": "TypeScript",
          "parentStar": "class:src/components/AuthCard.tsx:AuthCard",
          "paramCount": 1,
          "isPublic": true,
          "complexity": 1,
          "line": 6
        },
        {
          "id": "func:src/components/AuthCard.tsx:handleLogin",
          "name": "handleLogin",
          "type": "planet",
          "filepath": "src/components/AuthCard.tsx",
          "language": "TypeScript",
          "parentStar": "class:src/components/AuthCard.tsx:AuthCard",
          "paramCount": 0,
          "isPublic": true,
          "complexity": 6,
          "line": 11
        },
        {
          "id": "func:src/components/AuthCard.tsx:render",
          "name": "render",
          "type": "planet",
          "filepath": "src/components/AuthCard.tsx",
          "language": "TypeScript",
          "parentStar": "class:src/components/AuthCard.tsx:AuthCard",
          "paramCount": 0,
          "isPublic": true,
          "complexity": 2,
          "line": 28
        },

        // Planets for AuthProvider
        {
          "id": "func:src/context/AuthContext.tsx:login",
          "name": "login",
          "type": "planet",
          "filepath": "src/context/AuthContext.tsx",
          "language": "TypeScript",
          "parentStar": "class:src/context/AuthContext.tsx:AuthProvider",
          "paramCount": 2,
          "isPublic": true,
          "complexity": 2,
          "line": 5
        },
        {
          "id": "func:src/context/AuthContext.tsx:logout",
          "name": "logout",
          "type": "planet",
          "filepath": "src/context/AuthContext.tsx",
          "language": "TypeScript",
          "parentStar": "class:src/context/AuthContext.tsx:AuthProvider",
          "paramCount": 0,
          "isPublic": true,
          "complexity": 1,
          "line": 8
        },

        // Planets for Api
        {
          "id": "func:src/services/api.ts:post",
          "name": "post",
          "type": "planet",
          "filepath": "src/services/api.ts",
          "language": "TypeScript",
          "parentStar": "file:src/services/api.ts:api",
          "paramCount": 2,
          "isPublic": true,
          "complexity": 1,
          "line": 2
        },
        {
          "id": "func:src/services/api.ts:get",
          "name": "get",
          "type": "planet",
          "filepath": "src/services/api.ts",
          "language": "TypeScript",
          "parentStar": "file:src/services/api.ts:api",
          "paramCount": 1,
          "isPublic": true,
          "complexity": 1,
          "line": 3
        },
        {
          "id": "func:src/services/api.ts:delete",
          "name": "delete",
          "type": "planet",
          "filepath": "src/services/api.ts",
          "language": "TypeScript",
          "parentStar": "file:src/services/api.ts:api",
          "paramCount": 1,
          "isPublic": true,
          "complexity": 1,
          "line": 4
        },

        // Blackholes (Bugs) for AuthCard
        {
          "id": "bug:src/components/AuthCard.tsx:SECURITY:12",
          "name": "SECURITY: L12",
          "type": "blackhole",
          "filepath": "src/components/AuthCard.tsx",
          "category": "SECURITY",
          "severity": "CRITICAL",
          "message": "Weak authentication credentials check ('123456' / 'admin') bypassing server.",
          "line": 12,
          "owaspRef": "OWASP A02:2021-Cryptographic Failures",
          "snippet": "if(password === '123456' || password === 'admin')",
          "parentStar": "class:src/components/AuthCard.tsx:AuthCard"
        },
        {
          "id": "bug:src/components/AuthCard.tsx:PERF:22",
          "name": "PERF: L22",
          "type": "blackhole",
          "filepath": "src/components/AuthCard.tsx",
          "category": "PERF",
          "severity": "HIGH",
          "message": "Silent Failure: Empty catch block swallows runtime errors, making debugging impossible.",
          "line": 22,
          "owaspRef": "OWASP A09:2021-Security Logging failures",
          "snippet": "catch (e) { console.log('error'); }",
          "parentStar": "class:src/components/AuthCard.tsx:AuthCard"
        }
      ],
      "edges": [
        // Orbit links (Classes -> Planets)
        { "source": "class:src/components/AuthCard.tsx:AuthCard", "target": "func:src/components/AuthCard.tsx:constructor", "type": "orbit" },
        { "source": "class:src/components/AuthCard.tsx:AuthCard", "target": "func:src/components/AuthCard.tsx:handleLogin", "type": "orbit" },
        { "source": "class:src/components/AuthCard.tsx:AuthCard", "target": "func:src/components/AuthCard.tsx:render", "type": "orbit" },
        
        { "source": "class:src/context/AuthContext.tsx:AuthProvider", "target": "func:src/context/AuthContext.tsx:login", "type": "orbit" },
        { "source": "class:src/context/AuthContext.tsx:AuthProvider", "target": "func:src/context/AuthContext.tsx:logout", "type": "orbit" },
        
        { "source": "file:src/services/api.ts:api", "target": "func:src/services/api.ts:post", "type": "orbit" },
        { "source": "file:src/services/api.ts:api", "target": "func:src/services/api.ts:get", "type": "orbit" },
        { "source": "file:src/services/api.ts:api", "target": "func:src/services/api.ts:delete", "type": "orbit" },

        // Gravitational links (Classes -> Blackholes)
        { "source": "class:src/components/AuthCard.tsx:AuthCard", "target": "bug:src/components/AuthCard.tsx:SECURITY:12", "type": "gravitational_pull" },
        { "source": "class:src/components/AuthCard.tsx:AuthCard", "target": "bug:src/components/AuthCard.tsx:PERF:22", "type": "gravitational_pull" },

        // Dependency links (Stars -> Stars)
        {
          "source": "class:src/components/AuthCard.tsx:AuthCard",
          "target": "class:src/context/AuthContext.tsx:AuthProvider",
          "type": "dependency",
          "strength": 4
        },
        {
          "source": "class:src/context/AuthContext.tsx:AuthProvider",
          "target": "file:src/services/api.ts:api",
          "type": "dependency",
          "strength": 3
        },
        {
          "source": "class:src/components/AuthCard.tsx:AuthCard",
          "target": "file:src/services/api.ts:api",
          "type": "dependency",
          "strength": 2
        }
      ]
    }
  },

  "python_galaxy": {
    "name": "FastAPI AI Orchestrator",
    "summary": "Core AI model routing and pipeline server.",
    "graph": {
      "summary": {
        "stars": 4,
        "planets": 6,
        "orbits": 3,
        "blackholes": 3,
        "loc": 410,
        "avgCoverage": 71.2,
        "avgComplexity": 6.5
      },
      "nodes": [
        // Star 1
        {
          "id": "file:app/main.py:ApiServer",
          "name": "ApiServer",
          "type": "star",
          "filepath": "app/main.py",
          "language": "Python",
          "loc": 85,
          "coverage": 95,
          "complexity": 2,
          "line": 8,
          "bugsCount": 0,
          "workSignalsCount": 1
        },
        // Star 2
        {
          "id": "class:app/services/model_router.py:ModelRouter",
          "name": "ModelRouter",
          "type": "star",
          "filepath": "app/services/model_router.py",
          "language": "Python",
          "loc": 150,
          "coverage": 40,
          "complexity": 12,
          "line": 4,
          "bugsCount": 2,
          "workSignalsCount": 3
        },
        // Star 3
        {
          "id": "class:app/services/llm_service.py:LlmService",
          "name": "LlmService",
          "type": "star",
          "filepath": "app/services/llm_service.py",
          "language": "Python",
          "loc": 95,
          "coverage": 80,
          "complexity": 3,
          "line": 1,
          "bugsCount": 0,
          "workSignalsCount": 0
        },
        // Star 4
        {
          "id": "file:app/auth/security.py:security",
          "name": "security",
          "type": "star",
          "filepath": "app/auth/security.py",
          "language": "Python",
          "loc": 80,
          "coverage": 70,
          "complexity": 5,
          "line": 1,
          "bugsCount": 1,
          "workSignalsCount": 2
        },

        // Planets for ApiServer
        {
          "id": "func:app/main.py:get_health",
          "name": "get_health",
          "type": "planet",
          "filepath": "app/main.py",
          "language": "Python",
          "parentStar": "file:app/main.py:ApiServer",
          "paramCount": 0,
          "isPublic": true,
          "complexity": 1,
          "line": 12
        },
        {
          "id": "func:app/main.py:predict",
          "name": "predict",
          "type": "planet",
          "filepath": "app/main.py",
          "language": "Python",
          "parentStar": "file:app/main.py:ApiServer",
          "paramCount": 2,
          "isPublic": true,
          "complexity": 2,
          "line": 16
        },

        // Planets for ModelRouter
        {
          "id": "func:app/services/model_router.py:__init__",
          "name": "__init__",
          "type": "planet",
          "filepath": "app/services/model_router.py",
          "language": "Python",
          "parentStar": "class:app/services/model_router.py:ModelRouter",
          "paramCount": 0,
          "isPublic": true,
          "complexity": 2,
          "line": 5
        },
        {
          "id": "func:app/services/model_router.py:route_prompt",
          "name": "route_prompt",
          "type": "planet",
          "filepath": "app/services/model_router.py",
          "language": "Python",
          "parentStar": "class:app/services/model_router.py:ModelRouter",
          "paramCount": 1,
          "isPublic": true,
          "complexity": 9,
          "line": 9
        },

        // Planets for LlmService
        {
          "id": "func:app/services/llm_service.py:generate",
          "name": "generate",
          "type": "planet",
          "filepath": "app/services/llm_service.py",
          "language": "Python",
          "parentStar": "class:app/services/llm_service.py:LlmService",
          "paramCount": 1,
          "isPublic": true,
          "complexity": 1,
          "line": 2
        },
        {
          "id": "func:app/services/llm_service.py:analyze",
          "name": "analyze",
          "type": "planet",
          "filepath": "app/services/llm_service.py",
          "language": "Python",
          "parentStar": "class:app/services/llm_service.py:LlmService",
          "paramCount": 1,
          "isPublic": true,
          "complexity": 1,
          "line": 4
        },

        // Blackholes (Bugs)
        {
          "id": "bug:app/services/model_router.py:SECURITY:7",
          "name": "SECURITY: L7",
          "type": "blackhole",
          "filepath": "app/services/model_router.py",
          "category": "SECURITY",
          "severity": "CRITICAL",
          "message": "Hardcoded OpenAI credentials stored in API route module key string.",
          "line": 7,
          "owaspRef": "OWASP A02:2021-Cryptographic Failures",
          "snippet": "self.api_key = 'sk-live-prod-secret-992384a82b13'",
          "parentStar": "class:app/services/model_router.py:ModelRouter"
        },
        {
          "id": "bug:app/services/model_router.py:SECURITY:18",
          "name": "SECURITY: L18",
          "type": "blackhole",
          "filepath": "app/services/model_router.py",
          "category": "SECURITY",
          "severity": "HIGH",
          "message": "Code injection vulnerability: executing arbitrary prompts via eval().",
          "line": 18,
          "owaspRef": "OWASP A03:2021-Injection",
          "snippet": "return eval(prompt)",
          "parentStar": "class:app/services/model_router.py:ModelRouter"
        },
        {
          "id": "bug:app/auth/security.py:PERF:7",
          "name": "PERF: L7",
          "type": "blackhole",
          "filepath": "app/auth/security.py",
          "category": "PERF",
          "severity": "HIGH",
          "message": "Silent Exception Smell: Empty 'except' statement suppresses authentication verification failure.",
          "line": 7,
          "owaspRef": "OWASP A09:2021-Security Logging failures",
          "snippet": "except Exception: pass",
          "parentStar": "file:app/auth/security.py:security"
        }
      ],
      "edges": [
        // Orbits
        { "source": "file:app/main.py:ApiServer", "target": "func:app/main.py:get_health", "type": "orbit" },
        { "source": "file:app/main.py:ApiServer", "target": "func:app/main.py:predict", "type": "orbit" },
        
        { "source": "class:app/services/model_router.py:ModelRouter", "target": "func:app/services/model_router.py:__init__", "type": "orbit" },
        { "source": "class:app/services/model_router.py:ModelRouter", "target": "func:app/services/model_router.py:route_prompt", "type": "orbit" },
        
        { "source": "class:app/services/llm_service.py:LlmService", "target": "func:app/services/llm_service.py:generate", "type": "orbit" },
        { "source": "class:app/services/llm_service.py:LlmService", "target": "func:app/services/llm_service.py:analyze", "type": "orbit" },

        // Gravitational pulls
        { "source": "class:app/services/model_router.py:ModelRouter", "target": "bug:app/services/model_router.py:SECURITY:7", "type": "gravitational_pull" },
        { "source": "class:app/services/model_router.py:ModelRouter", "target": "bug:app/services/model_router.py:SECURITY:18", "type": "gravitational_pull" },
        { "source": "file:app/auth/security.py:security", "target": "bug:app/auth/security.py:PERF:7", "type": "gravitational_pull" },

        // Dependencies
        {
          "source": "file:app/main.py:ApiServer",
          "target": "class:app/services/model_router.py:ModelRouter",
          "type": "dependency",
          "strength": 5
        },
        {
          "source": "class:app/services/model_router.py:ModelRouter",
          "target": "class:app/services/llm_service.py:LlmService",
          "type": "dependency",
          "strength": 4
        },
        {
          "source": "file:app/main.py:ApiServer",
          "target": "file:app/auth/security.py:security",
          "type": "dependency",
          "strength": 2
        }
      ]
    }
  }
};
