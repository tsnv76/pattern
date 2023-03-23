from datetime import date
from logging import getLogger

from decors import log
from engine.templator import render
from components.models import Engine

site = Engine()


# Инициализация клиентского логера
LOGGER = getLogger('framework')


# Класс-контроллер - Главная страница
class Index:
    @log
    def __call__(self, request):
        return '200 OK', render('index.html', objects_list=site.categories)


# Класс-контроллер - Страница "О проекте"
class About:
    @log
    def __call__(self, request):
        return '200 OK', render('about.html')


# Класс-контроллер - Страница "Расписания"
class StudyPrograms:
    @log
    def __call__(self, request):
        return '200 OK', render('study-programs.html', data=date.today())


# Класс-контроллер - Страница 404
class NotFound404:
    @log
    def __call__(self, request):
        LOGGER.error(f'Ошибка 404. Страница не найдена')
        return '404 WHAT', '404 PAGE Not Found'


# Класс-контроллер - Страница "Список курсов"
class CoursesList:
    @log
    def __call__(self, request):

        try:
            category = site.find_category_by_id(
                int(request['request_params']['id']))
            LOGGER.info(f'Добавлена категория {category}')
            return '200 OK', render('course_list.html',
                                    objects_list=category.courses,
                                    name=category.name,
                                    id=category.id)
        except KeyError:
            LOGGER.info(f'Нет курса для добавления')
            return '200 OK', 'No courses have been added yet'


# Класс-контроллер - Страница "Создать курс"
class CreateCourse:
    category_id = -1

    @log
    def __call__(self, request):
        if request['method'] == 'POST':

            data = request['data']

            name = data['name']
            name = site.decode_value(name)

            category = None
            if self.category_id != -1:
                category = site.find_category_by_id(int(self.category_id))

                course = site.create_course('record', name, category)
                site.courses.append(course)

            return '200 OK', render('course_list.html',
                                    objects_list=category.courses,
                                    name=category.name,
                                    id=category.id)

        else:
            try:
                self.category_id = int(request['request_params']['id'])
                print(f'ахх {request}')
                LOGGER.info(f'Запрос {request}')
                category = site.find_category_by_id(int(self.category_id))

                return '200 OK', render('create_course.html',
                                        name=category.name,
                                        id=category.id)
            except KeyError:
                LOGGER.info(f'Нет категории для добавления')
                return '200 OK', 'No categories have been added yet'


# Класс-контроллер - Страница "Создать категорию"
class CreateCategory:
    @log
    def __call__(self, request):

        if request['method'] == 'POST':

            print(request)
            LOGGER.info(f'Запрос {request}')
            data = request['data']

            name = data['name']
            name = site.decode_value(name)

            category_id = data.get('category_id')

            category = None
            if category_id:
                category = site.find_category_by_id(int(category_id))

            new_category = site.create_category(name, category)

            site.categories.append(new_category)

            return '200 OK', render('index.html',
                                    objects_list=site.categories)
        else:
            categories = site.categories
            return '200 OK', render('create_category.html',
                                    categories=categories)


# Класс-контроллер - Страница "Список категорий"
class CategoryList:
    @log
    def __call__(self, request):
        return '200 OK', render('category_list.html',
                                objects_list=site.categories)
