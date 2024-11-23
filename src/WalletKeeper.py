from src.Const import *
import datetime
import os
import json
import copy
import re


class WalletKeeper:
    """
    Ядро приложения: класс обработки запросов и сохранения статистики
    """

    def __init__(self, history_fname: dict = 'history.json'):
        self.history_fname = history_fname
        self.history = self.load_histroy()

    def new_transaction(self, action: str = 'undefined', amount: int = 0, category: str = 'undefined',
                        date: str = None):
        """
        Создание новой транзакции и добавление её в историю
        action может быть произвольным, обычно используется `income` и `consumption`
        """

        if date is None:
            date = datetime.datetime.now().strftime(DATE_FORMAT)

        _action = {'amount': amount, 'date': date}
        if category not in self.history[action]:
            self.history[action][category] = [_action]
        else:
            self.history[action][category].append(_action)

        self.save_history()

    def get_action_history(self, action: str, max_size: int = 10, month: str = None) -> list[tuple[str, int, str]]:
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
            actions[i][2] = f'{100 * actions[i][1] / overall:.1f}'

        actions.sort(key=lambda x: x[1])
        if len(actions) > max_size:
            others_total = sum([actions[i][1] for i in range(max_size, len(actions))])
            return actions[:max_size] + [('others', others_total, f'{100 * others_total / overall:1.f}')]

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
