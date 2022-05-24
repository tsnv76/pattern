from engine.templator import render


# Класс-контроллер - Главная страница
class Index:
    def __call__(self, request):
        return '200 OK', render('index.html')


# Класс-контроллер - Страница "О проекте"
class About:
    def __call__(self, request):
        return '200 OK', render('about.html')


# Класс-контроллер - Страница "Отчеты"
class Otchets:
    def __call__(self, request):
        return '200 OK', render('otchets.html')


# Класс-контроллер - Страница "Контакты"
class Contacts:
    def __call__(self, request):
        return '200 OK', render('contacts.html')

