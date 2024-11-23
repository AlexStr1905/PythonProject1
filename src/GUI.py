from matplotlib import pyplot as plt
import tkinter as tk


class GUI:
    """
    Графический интерфейс: класс графического представления приложения.
    Создание полей рабочего окна, текстовых вводов, кнопок.
    """

    def __init__(self, root, app):
        self.root = root
        self.root.title("Бюджетный калькулятор")

        def show_diagramm(app, action='undefined'):
            """
            Получить диаграмму действий (action) по json файлу.
            Аргумент action определяет по каким операциям строить диаграмму.
            """
            categorys = []
            data = []
            for elem in app.get_action_history(action):
                categorys.append(elem[0])
                data.append(elem[1])
            plt.pie(data, labels=data, autopct='%1.1f', shadow=True, radius=1)
            plt.legend(labels=categorys)
            plt.show()

        self.income_label = tk.Label(root, text="Введите сумму дохода")
        self.income_label.pack()

        self.income_entry = tk.Entry(root)
        self.income_entry.pack()

        self.category_income_label = tk.Label(root, text="Введите категорию дохода")
        self.category_income_label.pack()

        self.category_income_entry = tk.Entry(root)
        self.category_income_entry.pack()

        def show_income():
            """
            Получить диаграмму действий доходов (income) по json файлу.
            """
            show_diagramm(app, 'income')

        self.show_diagramm_income_button = tk.Button(root, text="Посмотреть диаграмму доходов", command=show_income)
        self.show_diagramm_income_button.pack()

        def append_income():
            """
            Создать новую запись с доходом и вывести актуальную диаграмму.
            """
            app.new_transaction('income', int(self.income_entry.get()), self.category_income_entry.get())
            show_diagramm(app, 'income')

        self.calculate_income_button = tk.Button(root, text="Добавить доход", command=append_income)
        self.calculate_income_button.pack()

        self.consumption_label = tk.Label(root, text="Введите сумму расхода")
        self.consumption_label.pack()

        self.consumption_entry = tk.Entry(root)
        self.consumption_entry.pack()

        self.category_consumption_label = tk.Label(root, text="Введите категорию расхода")
        self.category_consumption_label.pack()

        self.category_consumption_entry = tk.Entry(root)
        self.category_consumption_entry.pack()

        def show_consumption():
            """
            Получить диаграмму действий расходов (consumption) по json файлу.
            """
            show_diagramm(app, 'consumption')

        self.show_diagramm_consumption_button = tk.Button(root, text="Посмотреть диаграмму расходов",
                                                          command=show_consumption)
        self.show_diagramm_consumption_button.pack()

        def append_consumption():
            """
            Создать новую запись с доходом и вывести актуальную диаграмму.
            """
            app.new_transaction('consumption', int(self.consumption_entry.get()), self.category_consumption_entry.get())
            show_diagramm(app, 'consumption')

        self.calculate_consumption_button = tk.Button(root, text="Добавить расход", command=append_consumption)
        self.calculate_consumption_button.pack()

        def clear_json():
            """
            Очистить json файл.
            """
            app.delete_history()

        self.clear_json_button = tk.Button(root, text="Очистить историю", command=clear_json)
        self.clear_json_button.pack()
