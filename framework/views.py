# Класс-контроллер - Главная страница
class Index:
    def __call__(self, request):
        return '200 OK', render('index.html')


# Класс-контроллер - Страница "О проекте"
class About:
    def __call__(self, request):
        return '200 OK', render('about.html')