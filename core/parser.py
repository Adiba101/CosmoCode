import ast
import os
import re
import hashlib


class CodeParser:
    """Robust multi-language code parser with complexity and risk analysis."""
    
    @staticmethod
    def calculate_complexity(content, ext=""):
        """Estimate cyclomatic complexity, using AST for Python when available."""
        if ext == '.py':
            try:
                tree = ast.parse(content)
            except SyntaxError:
                branch_points = len(re.findall(r'\b(if|for|while|elif|else|catch|case|&&|\|\||try|with|assert)\b', content))
                return max(1, branch_points + 1)
            branch_nodes = 0
            for node in ast.walk(tree):
                if isinstance(node, (ast.If, ast.For, ast.While, ast.Try, ast.With, ast.Match, ast.Assert, ast.BoolOp, ast.ExceptHandler)):
                    branch_nodes += 1
            return max(1, branch_nodes + 1)

        branch_points = len(re.findall(r'\b(if|for|while|elif|else|catch|case|&&|\|\||switch|assert)\b', content))
        return max(1, branch_points + 1)

    @staticmethod
    def detect_bugs_risks(content, file_path):
        """Detect security, architectural, and error handling risks in code."""
        risks = []
        lines = content.split('\n')
        
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
                "owaspRef": "OWASP A02:2021-Cryptographic Failures",
                "remediation": "Remove hardcoded secrets and load sensitive values from secure configuration or environment variables."
            })
            
        # 2. Security check: dangerous functions
        dangerous_pattern = r'\b(eval|exec|new Function|Function\(|unsafe|dangerouslySetInnerHTML)\b'
        for match in re.finditer(dangerous_pattern, content):
            line_no = content[:match.start()].count('\n') + 1
            snippet = lines[line_no-1].strip() if 0 <= line_no-1 < len(lines) else match.group(0)
            risks.append({
                "category": "SECURITY",
                "severity": "HIGH",
                "message": f"Dangerous operation '{match.group(1)}' used, exposing risk of injection.",
                "line": line_no,
                "snippet": snippet,
                "owaspRef": "OWASP A03:2021-Injection",
                "remediation": "Avoid dynamic code execution and use safe, explicit APIs instead."
            })

        # 3. Architectural check: God functions (length > 250 LOC)
        if len(lines) > 250:
            risks.append({
                "category": "ARCH",
                "severity": "MEDIUM",
                "message": f"God File Smell: File contains {len(lines)} lines, which violates modularity principles.",
                "line": 1,
                "snippet": lines[0],
                "owaspRef": "Clean Code: Single Responsibility Principle",
                "remediation": "Split large files into smaller modules with focused responsibilities."
            })

        # 4. Security check: possible injection via command or query concatenation
        injection_pattern = r'\b(exec|query|execute|system|popen)\b.*[+\-\|]\s*[\'\"]'
        for match in re.finditer(injection_pattern, content, re.IGNORECASE):
            line_no = content[:match.start()].count('\n') + 1
            snippet = lines[line_no - 1].strip() if 0 <= line_no - 1 < len(lines) else match.group(0)
            risks.append({
                "category": "SECURITY",
                "severity": "HIGH",
                "message": "Possible injection risk from string concatenation in command or query execution.",
                "line": line_no,
                "snippet": snippet,
                "owaspRef": "OWASP A03:2021-Injection",
                "remediation": "Use parameterized queries or sanitized APIs instead of constructing commands from raw strings."
            })

        # 5. Security check: path traversal and unsafe file access
        traversal_pattern = r'\b(open|read|write|load|save|mkdir|rmdir|remove|unlink)\b\s*\([^\)]*(\.\.|/\.|\\\.\\)[^\)]*\)'
        for match in re.finditer(traversal_pattern, content, re.IGNORECASE):
            line_no = content[:match.start()].count('\n') + 1
            snippet = lines[line_no - 1].strip() if 0 <= line_no - 1 < len(lines) else match.group(0)
            risks.append({
                "category": "SECURITY",
                "severity": "MEDIUM",
                "message": "Potential path traversal or unsafe file access detected.",
                "line": line_no,
                "snippet": snippet,
                "owaspRef": "OWASP A01:2021-Broken Access Control",
                "remediation": "Validate and sanitize file paths before opening or writing files. Avoid unchecked relative path fragments."
            })

        # 6. Error handling: empty catch/except blocks
        empty_except = r'(except\b.*:|catch\s*\(.*\)\s*\{)\s*(\bpass\b|\bcontinue\b|\{\}|\s*\}|\s*//\s*.*)'
        for match in re.finditer(empty_except, content, re.MULTILINE):
            line_no = content[:match.start()].count('\n') + 1
            risks.append({
                "category": "PERF",
                "severity": "HIGH",
                "message": "Silent Failure: Empty catch/except block swallows errors and blocks debugging.",
                "line": line_no,
                "snippet": match.group(0).strip().replace('\n', ' '),
                "owaspRef": "OWASP A09:2021-Security Logging and Monitoring Failures",
                "remediation": "Handle exceptions explicitly or log errors before swallowing them."
            })

        return risks

    @classmethod
    def parse_file(cls, file_path, content):
        """Parse a code file and extract metrics based on language."""
        _, ext = os.path.splitext(file_path.lower())
        
        # Initialize default metrics
        metrics = {
            "classes": [],
            "functions": [],
            "dependencies": [],
            "bugs": [],
            "loc": len(content.splitlines()),
            "complexity": cls.calculate_complexity(content, ext),
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
            try:
                tree = ast.parse(content)
                for node in ast.walk(tree):
                    if isinstance(node, ast.ClassDef):
                        metrics["classes"].append({
                            "name": node.name,
                            "line": node.lineno,
                            "inherits": [base.id for base in node.bases if isinstance(base, ast.Name)]
                        })
                    elif isinstance(node, ast.FunctionDef):
                        param_count = len([arg for arg in node.args.args if arg.arg != 'self'])
                        metrics["functions"].append({
                            "name": node.name,
                            "line": node.lineno,
                            "paramCount": param_count,
                            "isPublic": not node.name.startswith('_')
                        })
                    elif isinstance(node, ast.Import):
                        for alias in node.names:
                            metrics["dependencies"].append(alias.name.split('.')[0])
                    elif isinstance(node, ast.ImportFrom):
                        if node.module:
                            metrics["dependencies"].append(node.module.split('.')[0])
            except SyntaxError:
                # Fallback for invalid Python syntax
                class_matches = re.finditer(r'^\s*class\s+(\w+)(?:\s*\((.*?)\))?\s*:', content, re.MULTILINE)
                for m in class_matches:
                    metrics["classes"].append({
                        "name": m.group(1),
                        "line": content[:m.start()].count('\n') + 1,
                        "inherits": [x.strip() for x in m.group(2).split(',')] if m.group(2) else []
                    })
                func_matches = re.finditer(r'^\s*def\s+(\w+)\s*\((.*?)\)\s*(?:->\s*.*?)?:', content, re.MULTILINE)
                for m in func_matches:
                    param_count = len(m.group(2).split(',')) if m.group(2).strip() else 0
                    metrics["functions"].append({
                        "name": m.group(1),
                        "line": content[:m.start()].count('\n') + 1,
                        "paramCount": param_count,
                        "isPublic": not m.group(1).startswith('_')
                    })
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
