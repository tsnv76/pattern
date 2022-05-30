from wsgiref.simple_server import make_server
from engine.main import Framework, DebugApplication, FakeApplication
from views import routes

# Создаем объект WSGI-приложения
application = Framework(routes)
# application = DebugApplication(routes)
# application = FakeApplication(routes)


with make_server('', 8081, application) as httpd:
    print("Запуск на порту 8081...")
    httpd.serve_forever()
