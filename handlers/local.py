import re
import tornado.escape
from core import CodeParser, GalaxyGraphBuilder, WorkIQSimulator
from .base import BaseHandler


class ParseLocalHandler(BaseHandler):
    """Endpoint for parsing folder uploaded from local directory structure."""
    
    def post(self):
        try:
            body = tornado.escape.json_decode(self.request.body)
            files = body.get("files", [])
            if not isinstance(files, list) or not files:
                self.set_status(400)
                self.write({"status": "error", "message": "Request must include a non-empty 'files' array."})
                return

            parsed_files = {}
            for f in files:
                if not isinstance(f, dict):
                    continue
                path = f.get("path", "")
                content = f.get("content", "")
                if not isinstance(path, str) or not isinstance(content, str):
                    continue
                if len(path) > 1024 or '\x00' in path:
                    continue
                normalized_path = path.replace('\\', '/').strip('/')
                if not normalized_path or '..' in normalized_path or normalized_path.startswith('/'):
                    continue
                if not re.search(r'\.(py|js|jsx|ts|tsx|go|java|cs)$', normalized_path, re.IGNORECASE):
                    continue

                parsed_files[normalized_path] = CodeParser.parse_file(normalized_path, content)

            if not parsed_files:
                self.set_status(400)
                self.write({"status": "error", "message": "No parseable source files were provided."})
                return

            graph = GalaxyGraphBuilder.build_graph(parsed_files)
            
            # Enrich nodes with Work IQ
            for node in graph["nodes"]:
                if node["type"] in ["star", "planet"]:
                    node["workSignals"] = WorkIQSimulator.get_signals(node["name"], node["id"])

            self.write({
                "status": "success",
                "graph": graph
            })
        except tornado.web.HTTPError as e:
            self.set_status(e.status_code)
            self.write({"status": "error", "message": e.reason})
        except Exception as e:
            self.set_status(500)
            self.write({"status": "error", "message": "Internal server error while parsing local files."})
