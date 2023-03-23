import os
from datetime import date
from logging import getLogger

from components.cbv import ListView, CreateView
from components.decors import Logger, debug, AppRoute
from engine.framework_requests import GetRequests
from engine.main import Framework
from engine.templator import render
from components.models import Engine

site = Engine()

# Инициализация логера
LOGGER = getLogger('framework')
routes = {}


# Класс-контроллер - Главная страница
@AppRoute(routes=routes, url='/')
class Index:
    @debug
    def __call__(self, request):
        return '200 OK', render('index.html', objects_list=site.categories)


# Класс-контроллер - Страница "О проекте"
@AppRoute(routes=routes, url='/about/')
class About:
    @debug
    def __call__(self, request):
        return '200 OK', render('about.html')


# Класс-контроллер - Страница "Расписания"
@AppRoute(routes=routes, url='/study_programs/')
class StudyPrograms:
    @debug
    def __call__(self, request):
        return '200 OK', render('study-programs.html', data=date.today())


# Класс-контроллер - Страница 404
class NotFound404:
    @debug
    def __call__(self, request):
        LOGGER.error(f'Ошибка 404. Страница не найдена')
        return '404 WHAT', '404 PAGE Not Found'


# Класс-контроллер - Страница "Список курсов"
class CoursesList:
    @debug
    def __call__(self, request):

        try:
            category = site.find_category_by_id(
                int(request['request_params']['id']))
            return '200 OK', render('course_list.html',
                                    objects_list=category.courses,
                                    name=category.name,
                                    id=category.id)
        except KeyError:
            LOGGER.error(f'Курсы еще не добавлены')
            return '200 OK', 'No courses have been added yet'


# Класс-контроллер - Страница "Создать курс"
@AppRoute(routes=routes, url='/create-course/')
class CreateCourse:
    category_id = -1

    @debug
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
                LOGGER.info(f'Добавлен курс {name}')

            return '200 OK', render('course_list.html',
                                    objects_list=category.courses,
                                    name=category.name,
                                    id=category.id)

        else:
            try:
                self.category_id = int(request['request_params']['id'])
                category = site.find_category_by_id(int(self.category_id))

                return '200 OK', render('create_course.html',
                                        name=category.name,
                                        id=category.id)
            except KeyError:
                LOGGER.error(f'Категория еще не добавлена')
                return '200 OK', 'No categories have been added yet'


# Класс-контроллер - Страница "Создать категорию"
@AppRoute(routes=routes, url='/create-category/')
class CategoryCreateView(CreateView):
    template_name = 'create_category.html'

    def create_obj(self, data: dict):
        name = data['name']
        name = site.decode_value(name)
        new_obj = site.create_category(name)
        site.categories.append(new_obj)
        LOGGER.info(f'Добавлена категория {name}')


# Класс-контроллер - Страница "Список категорий"
@AppRoute(routes=routes, url='/category-list/')
class CategoryListView(ListView):
    queryset = site.categories
    template_name = 'category_list.html'


# Класс-контроллер - Страница "Список студентов"
@AppRoute(routes=routes, url='/student-list/')
class StudentListView(ListView):
    queryset = site.students
    template_name = 'student_list.html'


# Класс-контроллер - Страница "Создать студента"
@AppRoute(routes=routes, url='/create-student/')
class StudentCreateView(CreateView):
    template_name = 'create_student.html'

    def create_obj(self, data: dict):
        name = data['name']
        name = site.decode_value(name)
        new_obj = site.create_user('student', name)
        site.students.append(new_obj)
        LOGGER.info(f'Добавлен студент {name}')


# Класс-контроллер - Страница "Добавить студента на курс"
@AppRoute(routes=routes, url='/add-student/')
class AddStudentByCourseCreateView(CreateView):
    template_name = 'add_student.html'

    def get_context_data(self):
        context = super().get_context_data()
        context['courses'] = site.courses
        context['students'] = site.students
        return context

    def create_obj(self, data: dict):
        course_name = data['course_name']
        course_name = site.decode_value(course_name)
        course = site.get_course(course_name)
        student_name = data['student_name']
        student_name = site.decode_value(student_name)
        student = site.get_student(student_name)
        course.add_student(student)
        LOGGER.info(f'Студент {student_name} записан на курс {course_name}')
