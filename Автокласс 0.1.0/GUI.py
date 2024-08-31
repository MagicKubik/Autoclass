from tkinter import *
from tkinter import ttk
import re
from class_person import Person
from class_quest import Quest

class TitlePage:

    def __init__(self):
        self.title_page = Tk()
        self.title_page.geometry('600x300')
        self.title_page.title('ПДД тест')

        self.USER_NAME = ''
        self.USER_TASKS = ()
        self.check = (self.title_page.register(self.is_valid), "%P")
        self.errmsg = StringVar()

        # Widgets
        self.create_widgets()

    def create_widgets(self):
        # Label for name
        self.label_title = ttk.Label(text='Ваше имя ->', font=("Arial", 14))
        self.label_title.place(x=50, y=50)

        # Entry for name
        self.entry_name = ttk.Entry()
        self.entry_name.place(x=200, y=50)

        # Label for task range
        self.label_task_range = ttk.Label(text='Выберите вопросы С 1 - ПО 800', font=("Arial", 14))
        self.label_task_range.place(x=50, y=100)

        # Entries for task range
        self.entry_start = ttk.Entry(width=5, validate="key", validatecommand=self.check)
        self.entry_start.place(x=350, y=100)

        self.entry_end = ttk.Entry(width=5, validate="key", validatecommand=self.check)
        self.entry_end.place(x=400, y=100)

        # Submit button
        self.btn_submit = ttk.Button(text='Отправить', command=self.get_start)
        self.btn_submit.place(x=200, y=200)

        # Label for errors
        self.error_label = ttk.Label(foreground="red", textvariable=self.errmsg, wraplength=250)
        self.error_label.place(x=300, y=130)

    def start(self):
        self.title_page.mainloop()

    def is_valid(self,*args):
        """валидация на номер заданий"""
        pattern = r"^(?:[1-9]?[0-9]?[0-9]|[1-7][0-9][0-9]|800])$"
        result = re.match(pattern, *args) is not None
        if not result and int(result) is not int:
            self.errmsg.set("выберите билет от 1 до 800")
        else:
            self.errmsg.set('')
        return result

    def get_start(self):
        """создание стартового окна"""
        self.USER_NAME = self.entry_name.get()
        start_task = self.entry_start.get()
        end_task = self.entry_end.get()

        if not start_task or not end_task:
            self.errmsg.set("Пожалуйста, введите диапазон задач")
            return

        self.USER_TASKS = (int(start_task), int(end_task))

        self.title_page.destroy()
        self.open_test_page()

    def open_test_page(self):
        person = Person(self.USER_NAME, Quest().get_task(self.USER_TASKS[0]))
        TestPage(person, Quest().get_task(self.USER_TASKS[0]), self.USER_TASKS).start()




class TestPage(TitlePage):

    def __init__(self, user, task, num_task):
        # вроде как тут не нужно наследование мы передаем обьект класса как аргумент...
        # наследуем экземпляр класса Person
        super(TitlePage).__init__()
        self.person = user

        self.task = task
        self.num_task = num_task
        self.current_task_index = self.num_task[0]

        self.window = Tk()
        self.window.geometry('700x600')
        self.window.title(f'Тестирование: {self.person.name}')

        # Переменная для хранения выбранного ответа
        self.selected_answer = StringVar(value=None)

        self.load_task()

    def load_task(self):
        """формирует новое задание"""
        self.quest = self.task[0]
        self.solution = self.task[1]
        self.picture = self.task[3]

        self.person.update_task(self.task)

        try:
            self.test_page_path = PhotoImage(file=self.picture)
        except Exception:
            print(f'путь {self.picture} не найден!')

        self.img = ttk.Label(self.window, image=self.test_page_path)
        self.img.place(x=50, y=20)

        self.test_quest = ttk.Label(self.window, text=self.quest, font=("Arial", 12))
        self.test_quest.place(x=60, y=250)

        self.btn = ttk.Button(self.window, text="подтвердить", command=self.next_task)
        self.btn.place(x=300, y=500)

        self.test_quest.config(text=self.quest)
        self.selected_answer.set('')
        self.test_solution_radiobutton()

    def test_solution_radiobutton(self):
        '''если решение очень огромное то фильтруем его чере \n '''
        validated_solutions = []
        for num_solution in self.solution:
            words = num_solution.split()
            strings = ''
            current_line = ''
            word_count = 0
            for word in words:
                if word_count + 1 > 16 or len(current_line) + len(word) + 1 > 118:
                    strings += current_line.strip() + '\n'
                    current_line = ''
                    word_count = 0

                current_line += word + ' '
                word_count += 1
            strings += current_line.strip()
            validated_solutions.append(strings)

        # Удаляем старые радиокнопки
        for widget in self.window.winfo_children():
            if isinstance(widget, ttk.Radiobutton):
                widget.destroy()
        self.window.update_idletasks()

        # Создаем новые радиокнопки
        y_position = 300
        for solution in validated_solutions:
            if solution.strip():
                radiobutton = ttk.Radiobutton(self.window, text=solution, value=solution, variable=self.selected_answer)
                radiobutton.place(width=550, x=90, y=y_position, relwidth=1)
                y_position += 35


    def next_task(self):
        """подгружает новое задание"""
        # Возвращаем результат в Person
        selection_user = self.selected_answer.get()
        self.person.score_report(selection_user)

        # Переход к следующему вопросу
        self.current_task_index += 1
        if self.current_task_index <= self.num_task[1]:
            for widget in self.window.winfo_children():
                widget.destroy()
            self.task = Quest().get_task(self.current_task_index)
            self.load_task()
        else:
            for widget in self.window.winfo_children():
                widget.destroy()
            self.window.update_idletasks()
            self.final_message = 'отчет по тесту лежит на рабочем столе\n\t\tTEST.TXT\n\n\t\tദ്ദി(˵ •̀ ᴗ - ˵ ) ✧'
            self.test_quest = ttk.Label(self.window, text=self.final_message, font=("Arial", 12))
            self.test_quest.place(x=180, y=250)
            self.person.get_result()
            self.window.after(50000, self.window.destroy)

    def start(self):
        self.window.mainloop()