class Request:

    def __init__(self, environ: dict):
        self.method = environ['REQUEST_METHOD'].lower()
        self.query_params = self._get_query_params(environ)
        print(self.query_params)
        self.path = environ['PATH_INFO']
        self.headers = self._get_headers(environ)

    @staticmethod
    def _get_headers(environ):
        headers = {}
        for k, v in environ.items():
            if k.startswith('HTTP'):
                headers[k[5:].lower()] = v
        return headers

    @staticmethod
    def _get_query_params(environ: dict):
        result = environ['QUERY_STRING']
        query_param = {}
        if result:
            data = result.split('&')
            for item in data:
                k, v = item.split('=')
                if query_param.get(k):
                    query_param[k].append(v)
                else:
                    query_param[k] = [v]
        return query_param
