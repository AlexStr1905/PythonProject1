import re
import os
import copy
import json
import datetime
import tkinter as tk
import matplotlib.pyplot as plt

"""
Базовые форматы для json - файла и даты
"""

INITIAL_HISTORY = {"income":{},"consumption":{}}

DATE_FORMAT = '%d-%m-%y'

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

    self.show_diagramm_consumption_button = tk.Button(root, text="Посмотреть диаграмму расходов", command=show_consumption)
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

class WalletKeeper:
  """
  Ядро приложения: класс обработки запросов и сохранения статистики
  """
  def __init__(self, history_fname:dict = 'history.json'):
    self.history_fname = history_fname
    self.history = self.load_histroy()


  def new_transaction(self, action:str = 'undefined', amount:int = 0, category:str = 'undefined', date:str = None):
    """
    Создание новой транзакции и добавление её в историю
    action может быть произвольным, обычно используется `income` и `consumption`
    """

    if date is None:
      date = datetime.datetime.now().strftime(DATE_FORMAT)

    _action = {'amount':amount, 'date':date}
    if category not in self.history[action]:
      self.history[action][category] = [_action]
    else:
      self.history[action][category].append(_action)

    self.save_history()


  def get_action_history(self, action:str, max_size:int = 10, month:str = None) -> list[tuple[str, int, str]]:
    """
    Получить историю действий в формате ("название", "количество", "% от всех операций в этой категории")
    В случае если категорий больше, чем max_size, то будут выведены max_size - 1 категорий, а остальные
    помечены others
    """

    if month is None:
      month = str(datetime.datetime.now().month)

    actions = []
    overall = 0
    for category, transactions in self.history[action].items():
      total = sum([tr['amount'] for tr in transactions if re.findall(r'\d+', tr['date'])[1] == month])
      overall += total
      actions.append([category, total, ''])

    for i in range(len(actions)):
      actions[i][2] = f'{100 * actions[i][1]/overall:.1f}'

    actions.sort(key=lambda x: x[1])
    if len(actions) > max_size:
      others_total = sum([actions[i][1] for i in range(max_size, len(actions))])
      return actions[:max_size] + [('others', others_total, f'{100*others_total/overall:1.f}')]

    return actions


  def load_histroy(self) -> None:
    """
    Загрузка истории из json файла
    """
    if self.history_fname not in os.listdir():
      return copy.deepcopy(INITIAL_HISTORY)

    with open(self.history_fname, 'r', encoding='utf-8') as f:
      return json.load(f)


  def save_history(self) -> None:
    """
    Сохранение истории в json файл
    """
    with open(self.history_fname, 'w', encoding='utf-8') as f:
      json.dump(self.history, f)


  def delete_history(self) -> None:
    """
    Очистка истории
    """
    self.history = copy.deepcopy(INITIAL_HISTORY)
    self.save_history()

if __name__ == '__main__':
  """
  Финальное создание объектов классов.
  """
  app = WalletKeeper()
  root = tk.Tk()
  gui = GUI(root, app)
  root.mainloop()