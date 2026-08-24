# -*- coding: utf-8 -*-
"""
Created on Wed Aug 19 19:54:57 2026

@author: Анастасия
"""
from models.field import Field
import random


class Game:
    def __init__(self, ai_skill=1):
        self.player_field = Field()
        self.ai_field = Field()
        self.current_player = 'player'
        self.is_over = False
        self.winner = None
        self.ai_skill = ai_skill
        
        # AI состояние - НИЧЕГО НЕ СБРАСЫВАЕМ!
        self.ai_shots_history = set()  # Все выстрелы
        self.ai_hits = []  # Все попадания
        self.ai_ship_hits = []  # Попадания по текущему кораблю
        self.ai_ship_direction = None  # Направление текущего корабля
        self.ai_targets = []  # Очередь целей для добивания
        self.ai_destroyed_ships = []  # Потопленные корабли
        self.ai_processing_ship = False  # Флаг - добиваем корабль

    def setup(self):
        self.player_field.random_placing()
        self.ai_field.random_placing()
        self.current_player = 'player'
        self.is_over = False
        self.winner = None
        
        # Сбрасываем только когда новая игра
        self.ai_shots_history = set()
        self.ai_hits = []
        self.ai_ship_hits = []
        self.ai_ship_direction = None
        self.ai_targets = []
        self.ai_destroyed_ships = []
        self.ai_processing_ship = False

    def make_shot(self, x, y):
        if self.is_over:
            return 'game_over'

        coord = Field.ROW_LETTERS[x] + str(y + 1)
        field = self.ai_field if self.current_player == 'player' else self.player_field
        result = field.shot(coord)

        if result == Field.SHOT_ERROR:
            return 'invalid'
        
        if result == Field.SHOT_MISS:
            if self.current_player == 'ai':
                self.ai_shots_history.add((x, y))
            self.current_player = 'ai' if self.current_player == 'player' else 'player'
            
            # ЕСЛИ МЫ ДОБИВАЛИ КОРАБЛЬ И ПРОМАХНУЛИСЬ - НЕ СБРАСЫВАЕМ!
            # Просто переключаем ход, но цели сохраняем
            return 'miss'
        
        if result == Field.SHOT_HIT:
            if self.current_player == 'ai':
                self.ai_shots_history.add((x, y))
                self.ai_hits.append((x, y))
                self.ai_ship_hits.append((x, y))
                self.ai_processing_ship = True
                
                # Определяем направление если есть 2 попадания
                if len(self.ai_ship_hits) >= 2:
                    self._determine_direction()
                
                # Добавляем цели для добивания
                self._add_targets(x, y)
            return 'hit'
        
        if result == Field.SHOT_KILL:
            if self.current_player == 'ai':
                # Корабль потоплен!
                self.ai_destroyed_ships.append(self.ai_ship_hits.copy())
                
                # Отмечаем все клетки вокруг
                for hx, hy in self.ai_ship_hits:
                    for dx in [-1, 0, 1]:
                        for dy in [-1, 0, 1]:
                            nx, ny = hx + dx, hy + dy
                            if 0 <= nx < 10 and 0 <= ny < 10:
                                self.ai_shots_history.add((nx, ny))
                
                # Сбрасываем текущий корабль
                self.ai_ship_hits = []
                self.ai_ship_direction = None
                self.ai_targets = []
                self.ai_processing_ship = False
                
                # Проверяем, есть ли еще подбитые корабли
                damaged = self.player_field.get_damaged_cells()
                if damaged:
                    # Есть еще подбитые - начинаем их добивать
                    coord = damaged[0]
                    x = Field.ROW_LETTERS.index(coord[0])
                    y = int(coord[1:]) - 1
                    self.ai_ship_hits.append((x, y))
                    self.ai_processing_ship = True
                    self._add_targets(x, y)
            
            if self.current_player == 'player':
                if not self.ai_field.has_ships():
                    self.is_over = True
                    self.winner = 'player'
                    return 'win'
            else:
                if not self.player_field.has_ships():
                    self.is_over = True
                    self.winner = 'ai'
                    return 'win'
            return 'kill'
        
        return 'invalid'

    def _determine_direction(self):
        """Определяет направление корабля по попаданиям"""
        if len(self.ai_ship_hits) < 2:
            return
        
        hits = sorted(self.ai_ship_hits)
        # Проверяем горизонталь
        if all(y == hits[0][1] for x, y in hits):
            self.ai_ship_direction = 'horizontal'
        # Проверяем вертикаль
        elif all(x == hits[0][0] for x, y in hits):
            self.ai_ship_direction = 'vertical'

    def _add_targets(self, x, y):
        """Добавляет цели для добивания"""
        # Очищаем старые цели
        self.ai_targets = []
        
        if self.ai_ship_direction == 'horizontal':
            # Бьем только влево и вправо
            hits_sorted = sorted(self.ai_ship_hits, key=lambda p: p[1])
            left_x, left_y = hits_sorted[0]
            right_x, right_y = hits_sorted[-1]
            
            # Влево от самой левой
            if left_y - 1 >= 0:
                coord = Field.ROW_LETTERS[left_x] + str(left_y)
                if self.player_field._get_cell_status(coord) in ('clear', 'ship'):
                    if (left_x, left_y - 1) not in self.ai_shots_history:
                        self.ai_targets.append((left_x, left_y - 1))
            
            # Вправо от самой правой
            if right_y + 1 < 10:
                coord = Field.ROW_LETTERS[right_x] + str(right_y + 2)
                if self.player_field._get_cell_status(coord) in ('clear', 'ship'):
                    if (right_x, right_y + 1) not in self.ai_shots_history:
                        self.ai_targets.append((right_x, right_y + 1))
        
        elif self.ai_ship_direction == 'vertical':
            # Бьем только вверх и вниз
            hits_sorted = sorted(self.ai_ship_hits, key=lambda p: p[0])
            top_x, top_y = hits_sorted[0]
            bottom_x, bottom_y = hits_sorted[-1]
            
            # Вверх от самой верхней
            if top_x - 1 >= 0:
                coord = Field.ROW_LETTERS[top_x - 1] + str(top_y + 1)
                if self.player_field._get_cell_status(coord) in ('clear', 'ship'):
                    if (top_x - 1, top_y) not in self.ai_shots_history:
                        self.ai_targets.append((top_x - 1, top_y))
            
            # Вниз от самой нижней
            if bottom_x + 1 < 10:
                coord = Field.ROW_LETTERS[bottom_x + 1] + str(bottom_y + 1)
                if self.player_field._get_cell_status(coord) in ('clear', 'ship'):
                    if (bottom_x + 1, bottom_y) not in self.ai_shots_history:
                        self.ai_targets.append((bottom_x + 1, bottom_y))
        
        else:
            # Направление не определено - бьем по всем сторонам
            for dx, dy in [(1, 0), (-1, 0), (0, 1), (0, -1)]:
                nx, ny = x + dx, y + dy
                if 0 <= nx < 10 and 0 <= ny < 10:
                    coord = Field.ROW_LETTERS[nx] + str(ny + 1)
                    if self.player_field._get_cell_status(coord) in ('clear', 'ship'):
                        if (nx, ny) not in self.ai_shots_history:
                            self.ai_targets.append((nx, ny))

    def _get_random_target(self):
        """Получает случайную цель для поиска"""
        # Шахматный порядок для эффективного поиска
        empty = []
        for x in range(10):
            for y in range(10):
                coord = Field.ROW_LETTERS[x] + str(y + 1)
                status = self.player_field._get_cell_status(coord)
                if status in ('clear', 'ship'):
                    if (x, y) not in self.ai_shots_history:
                        # Приоритет клеткам через одну
                        if (x + y) % 2 == 0:
                            empty.append((x, y))
        
        if not empty:
            # Если нет шахматных - берем любые
            for x in range(10):
                for y in range(10):
                    coord = Field.ROW_LETTERS[x] + str(y + 1)
                    status = self.player_field._get_cell_status(coord)
                    if status in ('clear', 'ship'):
                        if (x, y) not in self.ai_shots_history:
                            empty.append((x, y))
        
        if empty:
            return random.choice(empty)
        return None

    def ai_turn(self):
        if self.is_over:
            return 'game_over'

        # СЛОЖНЫЙ AI (уровень 3)
        if self.ai_skill == 3:
            # ЕСЛИ ЕСТЬ ЦЕЛИ - БЬЕМ ПО НИМ!
            if self.ai_targets:
                # Берем первую цель
                x, y = self.ai_targets.pop(0)
                coord = Field.ROW_LETTERS[x] + str(y + 1)
                status = self.player_field._get_cell_status(coord)
                if status in ('clear', 'ship'):
                    if (x, y) not in self.ai_shots_history:
                        return self.make_shot(x, y)
                # Если цель неактуальна - берем следующую
                return self.ai_turn()
            
            # Если добиваем корабль и нет целей - ищем вокруг попаданий
            if self.ai_processing_ship and self.ai_ship_hits:
                # Бьем по ближайшим необстрелянным клеткам
                for hx, hy in self.ai_ship_hits:
                    for dx, dy in [(1, 0), (-1, 0), (0, 1), (0, -1)]:
                        nx, ny = hx + dx, hy + dy
                        if 0 <= nx < 10 and 0 <= ny < 10:
                            coord = Field.ROW_LETTERS[nx] + str(ny + 1)
                            status = self.player_field._get_cell_status(coord)
                            if status in ('clear', 'ship'):
                                if (nx, ny) not in self.ai_shots_history:
                                    return self.make_shot(nx, ny)
            
            # НЕТ ЦЕЛЕЙ - ИЩЕМ НОВЫЙ КОРАБЛЬ
            target = self._get_random_target()
            if target:
                x, y = target
                return self.make_shot(x, y)
            
            return 'miss'

        # СРЕДНИЙ AI (уровень 2)
        if self.ai_skill == 2:
            # Добиваем подбитые
            damaged = self.player_field.get_damaged_cells()
            if damaged:
                coord = damaged[0]
                x = Field.ROW_LETTERS.index(coord[0])
                y = int(coord[1:]) - 1
                
                directions = [(1, 0), (-1, 0), (0, 1), (0, -1)]
                random.shuffle(directions)
                for dx, dy in directions:
                    nx, ny = x + dx, y + dy
                    if 0 <= nx < 10 and 0 <= ny < 10:
                        coord_check = Field.ROW_LETTERS[nx] + str(ny + 1)
                        if self.player_field._get_cell_status(coord_check) in ('clear', 'ship'):
                            return self.make_shot(nx, ny)
            
            # Случайный выстрел
            empty = []
            for x in range(10):
                for y in range(10):
                    coord = Field.ROW_LETTERS[x] + str(y + 1)
                    if self.player_field._get_cell_status(coord) in ('clear', 'ship'):
                        if (x, y) not in self.ai_shots_history:
                            empty.append((x, y))
            
            if empty:
                x, y = random.choice(empty)
                return self.make_shot(x, y)

        # ЛЕГКИЙ AI (уровень 1)
        empty = []
        for x in range(10):
            for y in range(10):
                coord = Field.ROW_LETTERS[x] + str(y + 1)
                if self.player_field._get_cell_status(coord) in ('clear', 'ship'):
                    if (x, y) not in self.ai_shots_history:
                        empty.append((x, y))

        if empty:
            x, y = random.choice(empty)
            return self.make_shot(x, y)
        
        return 'miss'