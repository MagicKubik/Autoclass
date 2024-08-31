import csv
import os
import re
import sys

#переписать на патерн синглтон
class Quest:

    __path_to_quests = r'data_source\test.csv'
    __path_to_picture = r'data_source\picture/'

    def __init__(self):
        self.__nam_guest = 1
        """чтоние файла CSV"""
        with open(self.resource_path(Quest.__path_to_quests), 'r', encoding='utf-8') as data:
            read_csv = csv.reader(data, delimiter=';')
            for row in read_csv:
                # специальная обработка для элемента solution!
                joined_data = ''.join(row[1])
                pattern = r"'.*?'"
                matches = re.findall(pattern, joined_data)
                cleaned_results = [match.strip() for match in matches]

                setattr(self, 'quest_' + self.__secondary_name(), row[0])
                setattr(self, 'solution_' + self.__secondary_name(), cleaned_results)
                setattr(self, 'current_solution_' + self.__secondary_name(), row[2])
                setattr(self, 'comment_' + self.__secondary_name(), row[3])
                """здесь лежит путь к картинке"""
                if os.path.exists(self.__full_path_to_picture()):
                    setattr(self, 'picture_' + self.__secondary_name(),
                            str(self.__full_path_to_picture()))
                else:
                    setattr(self, 'picture_' + self.__secondary_name(), self.resource_path(self.__path_to_picture + '0.PNG'))
                self.__nam_guest += 1

    def __secondary_name(self) -> str:
        # возвращает номер задания
        return str(self.__nam_guest)

    def __full_path_to_picture(self) -> str:
        return self.resource_path(Quest.__path_to_picture + str(self.__nam_guest) + '.png')

    def get_task(self, num_task: int) -> list:
        quest = getattr(self, 'quest_' + str(num_task))
        solution = getattr(self, 'solution_' + str(num_task))
        current_solution = getattr(self, 'current_solution_' + str(num_task))
        picture = getattr(self, 'picture_' + str(num_task))
        comment = getattr(self, 'comment_' + str(num_task))
        return [quest, solution, current_solution, picture, comment]

    @staticmethod
    def resource_path(relative_path):
        """Получить абсолютный путь к ресурсу"""
        try:
            base_path = sys._MEIPASS
        except Exception:
            base_path = os.path.abspath(".")

        return os.path.join(str(base_path), str(relative_path))




# q = Quest()
# data = q.get_task(1)[1]
# print(data)

# joined_data = ' '.join(data)
#
# pattern = r"'.*?'"
# matches = re.findall(pattern, joined_data)
#
# cleaned_results = [match.strip() for match in matches]
#
# print(cleaned_results)