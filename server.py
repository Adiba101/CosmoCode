import os
import sys
import tornado.ioloop
import tornado.web

from config import PORT, WORKSPACE_DIR
from handlers import DemoDataHandler, ParseLocalHandler, ParseGithubHandler


def make_app():
    """Create and configure the Tornado application."""
    return tornado.web.Application([
        (r"/api/demo-data", DemoDataHandler),
        (r"/api/parse-local", ParseLocalHandler),
        (r"/api/parse-github", ParseGithubHandler),
        (r"/(.*)", tornado.web.StaticFileHandler, {"path": os.path.join(WORKSPACE_DIR, "public"), "default_filename": "index.html"}),
    ], debug=True)


if __name__ == "__main__":
    app = make_app()
    print(f"COSMOCODE Server starting on http://localhost:{PORT}")
    app.listen(PORT)
    try:
        tornado.ioloop.IOLoop.current().start()
    except KeyboardInterrupt:
        print("\nShutting down COSMOCODE Server...")
        sys.exit(0)
# Modularized server - see config.py, core/, and handlers/ for implementation
