from wsgiref.simple_server import make_server
from engine.main import Framework
from urls import routes

# Создаем объект WSGI-приложения
application = Framework(routes)

with make_server('', 8081, application) as httpd:
    print("Запуск на порту 8081...")
    httpd.serve_forever()
