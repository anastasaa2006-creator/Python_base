# -*- coding: utf-8 -*-
"""
Created on Wed Aug 19 19:55:35 2026

@author: Анастасия
"""
import tkinter as tk
from tkinter import ttk, messagebox
from models.game import Game
from models.field import Field
from managers.config_manager import ConfigManager
from gui.settings_window import SettingsWindow
from gui.score_window import ScoreWindow
import json
import os


class MainWindow:
    def __init__(self, root):
        self.root = root
        self.root.title("Морской бой")
        self.config = ConfigManager()

        # Устанавливаем размер окна из конфига
        width = self.config.get('window_width')
        height = self.config.get('window_height')
        self.root.geometry(f"{width}x{height}")
        self.root.minsize(900, 650)

        self.font_size = self.config.get('font_size')
        self.cell_size = self.config.get('cell_size')
        self.game = None
        self.waiting_ai = False
        self.game_over_handled = False

        self._create_menu()
        self._create_main_frame()
        self._apply_theme()
        self.start_new_game()

    def apply_settings(self):
        """Применяет настройки без перезапуска"""
        # Обновляем размеры
        self.font_size = self.config.get('font_size')
        self.cell_size = self.config.get('cell_size')
        
        # Обновляем тему
        self._apply_theme()
        
        # Перерисовываем поля
        self._update_ui()

    def _create_menu(self):
        menubar = tk.Menu(self.root)
        self.root.config(menu=menubar)

        game_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Игра", menu=game_menu)
        game_menu.add_command(label="Новая игра", command=self.start_new_game)
        game_menu.add_separator()
        game_menu.add_command(label="Выход", command=self.root.quit)

        menubar.add_cascade(label="Настройки", command=self.open_settings)
        menubar.add_cascade(label="Статистика", command=self.open_scores)

    def _create_main_frame(self):
        main_frame = ttk.Frame(self.root)
        main_frame.pack(fill=tk.BOTH, expand=True, padx=15, pady=15)

        info_frame = ttk.Frame(main_frame)
        info_frame.pack(fill=tk.X, pady=(0, 15))

        self.label_turn = ttk.Label(info_frame, text="Ваш ход: ", font=('Arial', self.font_size))
        self.label_turn.pack(side=tk.LEFT)

        self.label_status = ttk.Label(info_frame, text="", font=('Arial', self.font_size, 'bold'))
        self.label_status.pack(side=tk.RIGHT)

        fields_frame = ttk.Frame(main_frame)
        fields_frame.pack(fill=tk.BOTH, expand=True)

        left = ttk.LabelFrame(fields_frame, text="Ваше поле", padding=10)
        left.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=10)
        self.canvas_my = tk.Canvas(left, bg='lightblue')
        self.canvas_my.pack(fill=tk.BOTH, expand=True)

        right = ttk.LabelFrame(fields_frame, text="Поле противника", padding=10)
        right.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=10)
        self.canvas_enemy = tk.Canvas(right, bg='lightblue')
        self.canvas_enemy.pack(fill=tk.BOTH, expand=True)
        self.canvas_enemy.bind('<Button-1>', self.on_canvas_click)

    def _apply_theme(self):
        themes = {
            'Морская': {'bg': '#e8f4f8', 'ship': '#4a9aaa', 'hit': '#f5d742', 'destroy': '#e8555a', 'miss': '#6ba8c8'},
            'Фиолетовая': {'bg': '#f5edf7', 'ship': '#a07ab0', 'hit': '#f5d742', 'destroy': '#e8555a', 'miss': '#c8a8d8'},
            'Оранжевая': {'bg': '#fef5ed', 'ship': '#d48a6a', 'hit': '#f5d742', 'destroy': '#e8555a', 'miss': '#e8b898'},
            'Зеленая': {'bg': '#edf7f0', 'ship': '#5aaa7a', 'hit': '#f5d742', 'destroy': '#e8555a', 'miss': '#90c8a8'}
        }
        self.colors = themes.get(self.config.get('theme'), themes['Морская'])
        self.canvas_my.config(bg=self.colors['bg'])
        self.canvas_enemy.config(bg=self.colors['bg'])

    def start_new_game(self):
        # Передаем сложность AI в игру
        ai_skill = self.config.get('ai_skill')
        self.game = Game(ai_skill=ai_skill)
        self.game.setup()
        self.waiting_ai = False
        self.game_over_handled = False
        
        # Обновляем размеры из настроек
        self.font_size = self.config.get('font_size')
        self.cell_size = self.config.get('cell_size')
        
        self._apply_theme()
        self._update_ui()
        
        # Добавляем сообщение о сложности
        difficulty_names = {1: "Лёгкий", 2: "Средний", 3: "Сложный"}
        self.label_status.config(text=f"Сложность: {difficulty_names.get(ai_skill, 'Лёгкий')}")

    def _update_ui(self):
        self._draw_field(self.canvas_my, self.game.player_field, show_ships=True)
        self._draw_field(self.canvas_enemy, self.game.ai_field, show_ships=False)

        current = "Игрок" if self.game.current_player == 'player' else "Компьютер"
        self.label_turn.config(text=f"Ход: {current}")

        if self.game.is_over and not self.game_over_handled:
            self.game_over_handled = True
            winner = "Игрок" if self.game.winner == 'player' else "Компьютер"
            self.label_status.config(text=f"Игра окончена! Победил: {winner}")
            self._save_score("Игрок", 1 if self.game.winner == 'player' else 0, 0 if self.game.winner == 'player' else 1)
            messagebox.showinfo("Игра окончена", f"Победил: {winner}!")

        self.root.update_idletasks()

    def _save_score(self, name, wins, losses):
        try:
            with open('scores.json', 'r', encoding='utf-8') as f:
                scores = json.load(f)
        except FileNotFoundError:
            scores = []

        for score in scores:
            if score['name'] == name:
                score['wins'] += wins
                score['losses'] += losses
                break
        else:
            scores.append({'name': name, 'wins': wins, 'losses': losses})

        with open('scores.json', 'w', encoding='utf-8') as f:
            json.dump(scores, f, indent=2, ensure_ascii=False)

    def _draw_field(self, canvas, field, show_ships):
        canvas.delete("all")
        size = 10
        
        w = canvas.winfo_width()
        h = canvas.winfo_height()
        if w <= 1 or h <= 1:
            w, h = 400, 400

        margin = 25
        available_w = w - margin * 2
        available_h = h - margin * 2
        
        cell = min(available_w, available_h) // size
        cell = min(cell, self.cell_size)
        if cell < 20:
            cell = 20

        offset_x = margin + (available_w - cell * size) // 2
        offset_y = margin + (available_h - cell * size) // 2

        letters = 'ABCDEFGHIJ'
        font = ('Arial', max(8, self.font_size))
        for i in range(size):
            canvas.create_text(offset_x - 12, offset_y + i * cell + cell/2, 
                              text=letters[i], font=font, anchor='e')
            canvas.create_text(offset_x + i * cell + cell/2, offset_y - 12, 
                              text=str(i+1), font=font, anchor='s')

        for i in range(size + 1):
            canvas.create_line(offset_x + i * cell, offset_y, 
                              offset_x + i * cell, offset_y + size * cell, fill='black')
            canvas.create_line(offset_x, offset_y + i * cell, 
                              offset_x + size * cell, offset_y + i * cell, fill='black')

        for x in range(size):
            for y in range(size):
                x1, y1 = offset_x + x * cell, offset_y + y * cell
                x2, y2 = x1 + cell, y1 + cell
                val = field.grid[x][y]

                if val == '1' and show_ships:
                    canvas.create_rectangle(x1, y1, x2, y2, 
                                          fill=self.colors['ship'], outline='black')
                elif val == 'x':
                    canvas.create_rectangle(x1, y1, x2, y2, 
                                          fill=self.colors['hit'], outline='black')
                    canvas.create_line(x1, y1, x2, y2, fill='red', width=2)
                    canvas.create_line(x2, y1, x1, y2, fill='red', width=2)
                elif val == 'X':
                    canvas.create_rectangle(x1, y1, x2, y2, 
                                          fill=self.colors['destroy'], outline='black')
                    canvas.create_line(x1, y1, x2, y2, fill='black', width=2)
                    canvas.create_line(x2, y1, x1, y2, fill='black', width=2)
                elif val == '.':
                    canvas.create_oval(x1 + cell*0.3, y1 + cell*0.3,
                                      x2 - cell*0.3, y2 - cell*0.3,
                                      fill=self.colors['miss'], outline='blue')

    def on_canvas_click(self, event):
        if self.game.is_over or self.game.current_player != 'player' or self.waiting_ai:
            return

        canvas = event.widget
        if canvas != self.canvas_enemy:
            return

        size = 10
        w = canvas.winfo_width()
        h = canvas.winfo_height()
        if w <= 1 or h <= 1:
            w, h = 400, 400

        margin = 25
        available_w = w - margin * 2
        available_h = h - margin * 2
        
        cell = min(available_w, available_h) // size
        cell = min(cell, self.cell_size)
        if cell < 20:
            cell = 20

        offset_x = margin + (available_w - cell * size) // 2
        offset_y = margin + (available_h - cell * size) // 2

        x = int((event.x - offset_x) / cell)
        y = int((event.y - offset_y) / cell)

        if x < 0 or x >= size or y < 0 or y >= size:
            return

        result = self.game.make_shot(x, y)
        if result == 'invalid':
            return

        self._update_ui()

        if not self.game.is_over and self.game.current_player == 'ai':
            self.waiting_ai = True
            self.root.after(500, self._ai_turn)

    def _ai_turn(self):
        if self.game.is_over:
            self.waiting_ai = False
            return

        if self.game.current_player != 'ai':
            self.waiting_ai = False
            return

        self.game.ai_turn()
        self._update_ui()

        if not self.game.is_over and self.game.current_player == 'ai':
            self.root.after(500, self._ai_turn)
        else:
            self.waiting_ai = False

    def open_settings(self):
        SettingsWindow(self.root, self.config, self)

    def open_scores(self):
        ScoreWindow(self.root)