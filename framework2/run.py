from wsgiref.simple_server import make_server
from engine.main import Framework
from urls import routes

# Создаем объект WSGI-приложения
application = Framework(routes)

with make_server('127.0.0.1', 8000, application) as httpd:
    print("Запуск на порту 8000...")
    httpd.serve_forever()
