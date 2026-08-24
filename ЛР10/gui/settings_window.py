# -*- coding: utf-8 -*-
"""
Created on Wed Aug 19 19:55:52 2026

@author: Анастасия
"""
import tkinter as tk
from tkinter import ttk, messagebox


class SettingsWindow:
    def __init__(self, parent, config, main_window):
        self.parent = parent
        self.config = config
        self.main_window = main_window

        self.window = tk.Toplevel(parent)
        self.window.title("Настройки игры")
        self.window.geometry("400x400")
        self.window.resizable(False, False)
        self.window.transient(parent)
        self.window.grab_set()

        self.window.update_idletasks()
        x = (self.window.winfo_screenwidth() - 400) // 2
        y = (self.window.winfo_screenheight() - 400) // 2
        self.window.geometry(f"400x400+{x}+{y}")

        self._create_widgets()
        self._load_config()

    def _create_widgets(self):
        main = ttk.Frame(self.window, padding=20)
        main.pack(fill=tk.BOTH, expand=True)

        # Сложность AI
        ttk.Label(main, text="Сложность", font=('Segoe UI', 11, 'bold')).grid(row=0, column=0, columnspan=2, sticky='w', pady=(0, 5))
        
        ai_frame = ttk.Frame(main)
        ai_frame.grid(row=1, column=0, columnspan=2, sticky='w', pady=(0, 15))
        self.ai_skill = tk.IntVar(value=1)
        for text, val in [("Лёгкий", 1), ("Средний", 2), ("Сложный", 3)]:
            ttk.Radiobutton(ai_frame, text=text, variable=self.ai_skill, value=val).pack(side=tk.LEFT, padx=5)

        # Цветовая тема
        ttk.Label(main, text="Цветовая тема", font=('Segoe UI', 11, 'bold')).grid(row=2, column=0, columnspan=2, sticky='w', pady=(0, 5))
        
        theme_frame = ttk.Frame(main)
        theme_frame.grid(row=3, column=0, columnspan=2, sticky='w', pady=(0, 15))
        self.theme = tk.StringVar(value="Морская")
        for text in ["Морская", "Фиолетовая", "Оранжевая", "Зеленая"]:
            ttk.Radiobutton(theme_frame, text=text, variable=self.theme, value=text).pack(anchor='w', pady=1)

        # Размеры
        ttk.Label(main, text="Размеры", font=('Segoe UI', 11, 'bold')).grid(row=4, column=0, columnspan=2, sticky='w', pady=(0, 5))
        
        size2 = ttk.Frame(main)
        size2.grid(row=5, column=0, columnspan=2, sticky='w', pady=(0, 15))
        ttk.Label(size2, text="Шрифт:").pack(side=tk.LEFT)
        self.font_size = tk.IntVar(value=10)
        ttk.Spinbox(size2, from_=8, to=20, textvariable=self.font_size, width=6).pack(side=tk.LEFT, padx=5)
        ttk.Label(size2, text="Клетка:").pack(side=tk.LEFT, padx=(15, 0))
        self.cell_size = tk.IntVar(value=35)
        ttk.Spinbox(size2, from_=25, to=60, textvariable=self.cell_size, width=6).pack(side=tk.LEFT, padx=5)

        # Кнопки
        btn_frame = ttk.Frame(main)
        btn_frame.grid(row=6, column=0, columnspan=2, pady=(20, 0))
        
        ttk.Button(btn_frame, text="Сохранить", command=self.save_and_restart).pack(side=tk.LEFT, padx=5)
        ttk.Button(btn_frame, text="Отмена", command=self.window.destroy).pack(side=tk.LEFT, padx=5)

        # Растягиваем последнюю строку
        main.grid_rowconfigure(7, weight=1)

    def _load_config(self):
        self.ai_skill.set(self.config.get('ai_skill'))
        self.theme.set(self.config.get('theme'))
        self.font_size.set(self.config.get('font_size'))
        self.cell_size.set(self.config.get('cell_size'))

    def save_and_restart(self):
        self.config.set('ai_skill', self.ai_skill.get())
        self.config.set('theme', self.theme.get())
        self.config.set('font_size', self.font_size.get())
        self.config.set('cell_size', self.cell_size.get())
        self.config.save()

        self.window.destroy()
        self.main_window.apply_settings()
        messagebox.showinfo("Настройки", "Настройки сохранены")