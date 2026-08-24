# -*- coding: utf-8 -*-
"""
Created on Wed Aug 19 19:53:56 2026

@author: Анастасия
"""
import random


class Ship:
    """Класс корабля."""
    
    def __init__(self):
        self.id = random.randint(1, 1000)
        self.alive_coords = []
        self.hitted_coords = []
        self.field = None

    def set_field(self, field):
        self.field = field

    def add_coordinate(self, coordinate):
        if not self.field._validate_coordinate(coordinate):
            return False
        self.alive_coords.append(coordinate)
        return True

    def hit_coordinate(self, coordinate):
        if not self.field._validate_coordinate(coordinate):
            return False
        if coordinate in self.alive_coords:
            self.alive_coords.remove(coordinate)
            self.hitted_coords.append(coordinate)
            return True
        return False

    def is_alive(self):
        return len(self.alive_coords) > 0

    def get_all_coords(self):
        return self.alive_coords + self.hitted_coords

    def get_id(self):
        return self.id