# -*- coding: utf-8 -*-
"""
Created on Wed Aug 19 19:56:18 2026

@author: Анастасия
"""

import sys
import os

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import tkinter as tk
from gui.main_window import MainWindow


def main():
    root = tk.Tk()
    app = MainWindow(root)
    root.mainloop()


if __name__ == '__main__':
    main()