import tornado.web


class BaseHandler(tornado.web.RequestHandler):
    """Base handler providing CORS headers and request validation."""

    MAX_REQUEST_BODY = 5 * 1024 * 1024  # 5 MB
    ALLOWED_METHODS = ['GET', 'POST', 'OPTIONS']

    def set_default_headers(self):
        self.set_header("Access-Control-Allow-Origin", "*")
        self.set_header("Access-Control-Allow-Headers", "x-requested-with, content-type")
        self.set_header("Access-Control-Allow-Methods", ", ".join(self.ALLOWED_METHODS))

    def prepare(self):
        content_length = int(self.request.headers.get("Content-Length", 0) or 0)
        if content_length > self.MAX_REQUEST_BODY:
            raise tornado.web.HTTPError(413, reason="Request payload too large")

    def options(self):
        self.set_status(204)
        self.finish()
