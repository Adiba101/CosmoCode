import os
import re
import json
import urllib.request
import zipfile
import io
import tornado.escape
from urllib.error import HTTPError, URLError
from core import CodeParser, GalaxyGraphBuilder, WorkIQSimulator
from .base import BaseHandler


class ParseGithubHandler(BaseHandler):
    """Endpoint for downloading and parsing a GitHub repository ZIP."""
    
    def post(self):
        try:
            body = tornado.escape.json_decode(self.request.body)
            repo_url = body.get("url", "").strip()
            
            if not repo_url:
                self.set_status(400)
                self.write({"status": "error", "message": "Repository URL is required."})
                return

            github_pattern = r'^(?:https?://github\.com/)?([^/]+)/([^/]+?)(?:\.git|/)?$'
            match = re.search(github_pattern, repo_url)
            if not match:
                self.set_status(400)
                self.write({"status": "error", "message": "Invalid GitHub repository URL format."})
                return
            
            owner = match.group(1)
            repo = match.group(2)
            headers = {
                "User-Agent": "COSMOCODE-Visualizer-Agent"
            }
            github_token = os.environ.get("GITHUB_TOKEN")
            if github_token:
                headers["Authorization"] = f"token {github_token}"

            default_branch = None
            repo_api_url = f"https://api.github.com/repos/{owner}/{repo}"
            try:
                with urllib.request.urlopen(urllib.request.Request(repo_api_url, headers=headers)) as response:
                    repo_info = json.loads(response.read().decode('utf-8', errors='ignore'))
                    default_branch = repo_info.get('default_branch')
            except HTTPError as e:
                if e.code == 403:
                    self.set_status(429)
                    self.write({"status": "error", "message": "GitHub API rate limited or access denied. Try again later or set GITHUB_TOKEN."})
                    return
                # fallback to default branch guesses if the repo info endpoint is unavailable
            except URLError:
                pass

            if not default_branch:
                default_branch = 'main'

            zip_urls = [
                f"https://api.github.com/repos/{owner}/{repo}/zipball/{default_branch}",
                f"https://api.github.com/repos/{owner}/{repo}/zipball/master"
            ]
            
            zip_data = None
            for zip_url in zip_urls:
                req = urllib.request.Request(zip_url, headers=headers)
                try:
                    with urllib.request.urlopen(req) as response:
                        zip_data = response.read()
                    break
                except HTTPError as e:
                    if e.code == 404:
                        continue
                    if e.code == 403:
                        self.set_status(429)
                        self.write({"status": "error", "message": "GitHub API rate limited or access denied. Try again later or set GITHUB_TOKEN."})
                        return
                except URLError as e:
                    self.set_status(502)
                    self.write({"status": "error", "message": "Network error contacting GitHub. Please try again later."})
                    return

            if zip_data is None:
                self.set_status(404)
                self.write({"status": "error", "message": "Repository not found or repository archive unavailable."})
                return
            
            parsed_files = {}
            with zipfile.ZipFile(io.BytesIO(zip_data)) as z:
                for filename in z.namelist():
                    if filename.endswith('/') or any(x in filename.lower() for x in ['.png', '.jpg', '.jpeg', '.gif', '.pdf', '.node', '.dll', '.exe', 'node_modules/', '.git/']):
                        continue
                    try:
                        with z.open(filename) as f:
                            content = f.read().decode('utf-8', errors='ignore')
                        clean_path = '/'.join(filename.split('/')[1:])
                        if clean_path and re.search(r'\.(py|js|jsx|ts|tsx|go|java|cs)$', clean_path, re.IGNORECASE):
                            parsed_files[clean_path] = CodeParser.parse_file(clean_path, content)
                    except Exception:
                        continue

            if not parsed_files:
                self.set_status(404)
                self.write({"status": "error", "message": "No parseable source files found in the repository."})
                return

            graph = GalaxyGraphBuilder.build_graph(parsed_files)
            
            for node in graph["nodes"]:
                if node["type"] in ["star", "planet"]:
                    node["workSignals"] = WorkIQSimulator.get_signals(node["name"], node["id"])

            self.write({
                "status": "success",
                "repoName": f"{owner}/{repo}",
                "graph": graph
            })
        except tornado.web.HTTPError as e:
            self.set_status(e.status_code)
            self.write({"status": "error", "message": e.reason})
        except Exception:
            self.set_status(500)
            self.write({"status": "error", "message": "Internal server error while parsing GitHub repository."})
