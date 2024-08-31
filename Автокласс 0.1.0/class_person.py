# переписать этот гавнакод в синглтон
import os

class Person:
    lus_task = dict()
    count_win = 0
    count_los = 0

    def __init__(self, name=None, task=None):
        self.name = name
        self.update_task(task)

    def update_task(self, task):
        """Обновляет текущую задачу"""
        self.quest = task[0]
        self.solution = task[1]
        self.current_solution = task[2]
        self.picture = task[3]
        self.comment = task[4]

    def score_report(self, user_solution):
        """счетчик ответов"""
        user_solution = user_solution.strip('"\'')
        if user_solution == self.current_solution:
            Person.count_win += 1
        elif user_solution != self.current_solution:
            Person.count_los += 1
            Person.lus_task[self.quest] = (self.current_solution, user_solution, self.comment)

    def get_task(self) -> list:
        return [self.quest, self.solution, self.current_solution, self.picture]

    @classmethod
    def get_result(cls):
        """сохронение результата на рабочий стол"""
        home_dir = os.path.expanduser('~')
        with open(home_dir + r'\Desktop/'+'test.txt', 'w', encoding='utf-8') as f:
            result = f'количество правильных ответов {cls.count_win}\nколичество не правильных ответов {cls.count_los}\n'
            f.write(result)
            for k, v in cls.lus_task.items():
                parser_lus_task = f'\nвопрос: {k}\nправильный ответ - {v[0]}\nваш ответ - {v[1]}\nкоментарий:\n{v[2]}\n\n'
                f.write(parser_lus_task)

