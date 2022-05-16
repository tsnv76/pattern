from pprint import pprint

from request import Request


def app(environ, start_response):
    # pprint(environ)
    request = Request(environ)
    print(request.headers)
    print(request.body.read())
    start_response("200 OK", [('Content-Type', 'text/html')])
    return [b'Hello from WSGI application']
