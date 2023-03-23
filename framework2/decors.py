"""Декоратор"""
import logging
import time
from datetime import datetime

from pattern.singlton import SingletonByName


def log(func_to_log):
    """Функция-декоратор"""
    def log_saver(*args, **kwargs):
        logger_name = 'framework'
        LOGGER = logging.getLogger(logger_name)

        ret = func_to_log(*args, **kwargs)
        LOGGER.debug(f'Была вызвана функция {func_to_log.__name__} c параметрами {args}, {kwargs}. '
                     f'Вызов из модуля {func_to_log.__module__}')
        return ret
    return log_saver


class Logger(metaclass=SingletonByName):

    def __init__(self, name):
        self.name = name

    def log(self, text):
        print('log--->', text, datetime())


def debug(func):
    def inner(*args, **kwargs):
        start = time.time()
        result = func(*args, **kwargs)
        end = time.time()
        print(f'Была вызвана функция {func.__name__} c параметрами {args}, {kwargs}.'
              f'Вызов из модуля {func.__module__}. Время выполения {end - start}')
        return result

    return inner


# Декоратор для реализации маршрутизации
class AppRoute:
    def __init__(self, routes, url):
        """
        Сохраняем значение переданного параметра
        """
        self.routes = routes
        self.url = url

    def __call__(self, cls):
        """
        Сам декоратор
        """
        self.routes[self.url] = cls()
