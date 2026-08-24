# -*- coding: utf-8 -*-
"""
Created on Wed Aug 19 19:54:20 2026

@author: Анастасия
"""
from models.ship import Ship
import random


class Field:
    """Игровое поле."""
    
    ROWS = {'a': 0, 'b': 1, 'c': 2, 'd': 3, 'e': 4,
            'f': 5, 'g': 6, 'h': 7, 'i': 8, 'j': 9}
    COLS = {'1': 0, '2': 1, '3': 2, '4': 3, '5': 4,
            '6': 5, '7': 6, '8': 7, '9': 8, '10': 9}
    ROW_LETTERS = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j']
    FLEET_LENGTHS = [4, 3, 3, 2, 2, 2, 1, 1, 1, 1]
    
    SHOT_MISS = 'Blunder'
    SHOT_HIT = 'Hit'
    SHOT_KILL = 'Target destroyed'
    SHOT_ERROR = 'Invalid shot'

    def __init__(self):
        self.grid = [[' ' for _ in range(10)] for _ in range(10)]
        self.ships = []
        self.forbidden = set()

    def _validate_coordinate(self, coord):
        if len(coord) < 2 or len(coord) >= 4:
            return False
        if coord[0] not in self.ROW_LETTERS:
            return False
        try:
            if int(coord[1:]) not in range(1, 11):
                return False
        except ValueError:
            return False
        return True

    def _coord_to_index(self, coord):
        return self.ROWS[coord[0]], self.COLS[coord[1:]]

    def _index_to_coord(self, x, y):
        for letter, idx in self.ROWS.items():
            if idx == x:
                for num, idx2 in self.COLS.items():
                    if idx2 == y:
                        return letter + num
        return None

    def _get_cell_status(self, coord):
        if not self._validate_coordinate(coord):
            return 'error'
        x, y = self._coord_to_index(coord)
        val = self.grid[x][y]
        return {' ': 'clear', 'x': 'hitted', 'X': 'destroyed', '1': 'ship', '.': 'was beaten'}.get(val, 'unknown')

    def _create_buffer(self, coord_line):
        coords = coord_line.split('-')
        buffer_set = set()
        for coord in coords:
            x, y = self._coord_to_index(coord)
            for dx in (-1, 0, 1):
                for dy in (-1, 0, 1):
                    nx, ny = x + dx, y + dy
                    if 0 <= nx < 10 and 0 <= ny < 10:
                        buffer_set.add(self._index_to_coord(nx, ny))
        return buffer_set - set(coords)

    def can_place_ship(self, coord_line, length):
        coords = coord_line.split('-')
        if length != len(coords):
            return False
        
        for coord in coords:
            if coord in self.forbidden or not self._validate_coordinate(coord):
                return False
        
        for coord in self._create_buffer(coord_line):
            if coord in self.forbidden:
                return False
        return True

    def place_ship(self, coord_line, length):
        coords = coord_line.split('-')
        if length != len(coords):
            return False
        
        ship = Ship()
        ship.set_field(self)
        placed = []
        
        for coord in coords:
            if coord in self.forbidden:
                for c in placed:
                    x, y = self._coord_to_index(c)
                    self.grid[x][y] = ' '
                    self.forbidden.remove(c)
                return False
            
            if ship.add_coordinate(coord):
                x, y = self._coord_to_index(coord)
                self.grid[x][y] = '1'
                self.forbidden.add(coord)
                placed.append(coord)
        
        for coord in self._create_buffer(coord_line):
            if coord:
                self.forbidden.add(coord)
        
        self.ships.append(ship)
        return True

    def _generate_horizontal(self, length):
        row = random.choice(self.ROW_LETTERS)
        start = random.randint(1, 11 - length)
        return '-'.join([f"{row}{start + i}" for i in range(length)])

    def _generate_vertical(self, length):
        start = random.randint(0, 10 - length)
        num = random.randint(1, 10)
        return '-'.join([f"{self.ROW_LETTERS[start + i]}{num}" for i in range(length)])

    def random_placing(self):
        self._reset()
        lengths = self.FLEET_LENGTHS.copy()
        
        for length in lengths:
            placed = False
            for _ in range(500):
                coord_line = self._generate_horizontal(length) if random.choice([True, False]) else self._generate_vertical(length)
                if self.can_place_ship(coord_line, length):
                    self.place_ship(coord_line, length)
                    placed = True
                    break
            if not placed:
                return self.random_placing()
        return True

    def _reset(self):
        self.grid = [[' ' for _ in range(10)] for _ in range(10)]
        self.ships = []
        self.forbidden = set()

    def shot(self, coord):
        if not self._validate_coordinate(coord):
            return self.SHOT_ERROR
        
        status = self._get_cell_status(coord)
        x, y = self._coord_to_index(coord)
        
        if status == 'clear':
            self.grid[x][y] = '.'
            return self.SHOT_MISS
        
        if status == 'ship':
            for ship in self.ships:
                if coord in ship.alive_coords:
                    ship.hit_coordinate(coord)
                    if not ship.is_alive():
                        for c in ship.get_all_coords():
                            cx, cy = self._coord_to_index(c)
                            self.grid[cx][cy] = 'X'
                        self._mark_around_ship(ship)
                        self.ships.remove(ship)
                        return self.SHOT_KILL
                    self.grid[x][y] = 'x'
                    return self.SHOT_HIT
        
        return self.SHOT_ERROR

    def _mark_around_ship(self, ship):
        for coord in ship.get_all_coords():
            x, y = self._coord_to_index(coord)
            for dx in (-1, 0, 1):
                for dy in (-1, 0, 1):
                    nx, ny = x + dx, y + dy
                    if 0 <= nx < 10 and 0 <= ny < 10 and self.grid[nx][ny] == ' ':
                        self.grid[nx][ny] = '.'

    def has_ships(self):
        return len(self.ships) > 0

    def get_all_ship_coords(self):
        result = []
        for ship in self.ships:
            result.extend(ship.get_all_coords())
        return result

    def get_damaged_cells(self):
        damaged = []
        for x in range(10):
            for y in range(10):
                if self.grid[x][y] == 'x':
                    coord = self._index_to_coord(x, y)
                    if coord:
                        damaged.append(coord)
        return damaged