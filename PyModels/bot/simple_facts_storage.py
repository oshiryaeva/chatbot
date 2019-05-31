# -*- coding: utf-8 -*-

from bot.base_facts_storage import BaseFactsStorage

import datetime
import itertools


class SimpleFactsStorage(BaseFactsStorage):
    """
    Базовый класс хранилища фактов с добавленной функциональностью:
    1) метод enumerate_smalltalk_replicas возвращает пустой список, а не
       бросает исключение.
    2) факты о текущем времени и дне недели добавляются в список, возвращаемый
       методом enumerate_facts.
    """

    def __init__(self, text_utils):
        """
        :param text_utils: экземпляр класса TextUtils
        """
        super(SimpleFactsStorage, self).__init__()
        self.text_utils = text_utils

    def enumerate_facts(self, interlocutor):
        memory_phrases = []

        # Добавляем текущие факты
        # День недели
        dw = [u'понедельник', u'вторник', u'среда', u'четверг',
              u'пятница', u'суббота', u'воскресенье'][datetime.datetime.today().weekday()]
        memory_phrases.append((u'сегодня ' + dw, '3', 'current_day of week'))

        # Время года
        cur_month = datetime.datetime.now().month
        season = {12: u'зима', 11: u'зима', 2: u'зима',
                  3: u'весна', 4: u'весна', 5: u'весна',
                  6: u'лето', 7: u'лето', 8: u'лето',
                  9: u'осень', 10: u'осень', 11: u'осень'}[cur_month]
        memory_phrases.append((u'сейчас ' + season, '3', 'current_season'))

        # Текущий месяц
        month = {1: u'январь', 2: u'февраль', 3: u'март',
                 4: u'апрель', 5: u'май', 6: u'июнь', 7: u'июль',
                 8: u'август', 9: u'сентябрь', 10: u'октябрь', 11: u'ноябрь', 12: u'декабрь'}[cur_month]
        memory_phrases.append((u'сейчас ' + month, '3', 'current_month'))

        # Добавляем текущее время с точностью до минуты
        current_minute = datetime.datetime.now().minute
        current_hour = datetime.datetime.now().hour
        current_time = u'Сейчас ' + str(current_hour)
        if 20 >= current_hour >= 5:
            current_time += u' часов '
        elif current_hour in [1, 21]:
            current_time += u' час '
        elif (current_hour % 10) in [2, 3, 4]:
            current_time += u' часа '
        else:
            current_time += u' часов '

        current_time += str(current_minute)
        if current_minute == 1:
            current_time += u' минута '  # 1 минута
        elif current_minute <= 4 and (current_minute % 10) in [2, 3, 4]:
            current_time += u' минуты '  # 2 минуты, 3 минуты, 4 минуты
        elif current_time > 20 and (current_minute % 10) == 1:
            current_time += u' минута '  # 21 минута, 31 минута, etc.
        elif current_time > 20 and (current_minute % 10) in [2, 3, 4]:
            current_time += u' минуты '  # 22 минуты, 23 минуты, etc.
        else:
            current_time += u' минут '  # 6 минут, 27 минут etc

        memory_phrases.append((current_time, '3', 'current_time'))

        # возвращаем список фактов (потом надо переделать на выдачу по мере чтения из файла и
        # генерации через yield).
        for f in itertools.chain(self.new_facts, memory_phrases):
            yield f

    def store_new_fact(self, interlocutor, fact):
        pass
