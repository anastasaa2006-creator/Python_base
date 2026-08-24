# -*- coding: utf-8 -*-
"""
Created on Wed Aug 19 19:56:06 2026

@author: Анастасия
"""
# -*- coding: utf-8 -*-
import tkinter as tk
from tkinter import ttk, messagebox
import json
import os


class ScoreWindow:
    def __init__(self, parent):
        self.parent = parent
        self.window = tk.Toplevel(parent)
        self.window.title("Статистика")
        self.window.geometry("400x350")
        self.window.resizable(False, False)
        self.window.transient(parent)
        self.window.grab_set()

        self._create_widgets()
        self._load_scores()

    def _create_widgets(self):
        main = ttk.Frame(self.window, padding=15)
        main.pack(fill=tk.BOTH, expand=True)

        ttk.Label(main, text="Таблица рекордов", font=('Arial', 14, 'bold')).pack(pady=(0, 10))

        columns = ('#', 'Имя', 'Победы', 'Поражения')
        self.tree = ttk.Treeview(main, columns=columns, show='headings', height=10)
        self.tree.heading('#', text='#')
        self.tree.heading('Имя', text='Имя')
        self.tree.heading('Победы', text='Победы')
        self.tree.heading('Поражения', text='Поражения')
        self.tree.column('#', width=40)
        self.tree.column('Имя', width=150)
        self.tree.column('Победы', width=80)
        self.tree.column('Поражения', width=80)

        scroll = ttk.Scrollbar(main, orient='vertical', command=self.tree.yview)
        self.tree.configure(yscrollcommand=scroll.set)
        self.tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scroll.pack(side=tk.RIGHT, fill=tk.Y)

        btn_frame = ttk.Frame(main)
        btn_frame.pack(fill=tk.X, pady=10)
        ttk.Button(btn_frame, text="Обновить", command=self._load_scores).pack(side=tk.LEFT, padx=5)
        ttk.Button(btn_frame, text="Очистить", command=self.clear_scores).pack(side=tk.LEFT, padx=5)
        ttk.Button(btn_frame, text="Закрыть", command=self.window.destroy).pack(side=tk.RIGHT, padx=5)

    def _load_scores(self):
        for row in self.tree.get_children():
            self.tree.delete(row)

        try:
            with open('scores.json', 'r', encoding='utf-8') as f:
                scores = json.load(f)
        except FileNotFoundError:
            self.tree.insert('', 'end', values=('', 'Нет данных', '', ''))
            return

        if not scores:
            self.tree.insert('', 'end', values=('', 'Нет данных', '', ''))
            return

        scores.sort(key=lambda x: x.get('wins', 0), reverse=True)
        for i, score in enumerate(scores, 1):
            self.tree.insert('', 'end', values=(i, score.get('name', 'Unknown'), score.get('wins', 0), score.get('losses', 0)))

    def clear_scores(self):
        if messagebox.askyesno("Подтверждение", "Очистить историю?"):
            if os.path.exists('scores.json'):
                os.remove('scores.json')
            self._load_scores()