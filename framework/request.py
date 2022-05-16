class Request:

    def __init__(self, environ):
        self.headers = self._get_http_headers(environ)
        self.method = None
        self.body = environ.get('wsgi.input')
        self.query_params = 0
        self.path = 0

    @staticmethod
    def _get_http_headers(environ):
        headers = {}
        for k, v in environ.items():
            if k.startswith('HTTP_'):
                headers[k[5:].lower()] = v
        return headers
