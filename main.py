import tkinter as tk
from src.GUI import GUI
from src.WalletKeeper import WalletKeeper

if __name__ == '__main__':
    """
    Финальное создание объектов классов.
    """
    app = WalletKeeper()
    root = tk.Tk()
    gui = GUI(root, app)
    root.mainloop()
