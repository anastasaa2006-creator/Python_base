# -*- coding: utf-8 -*-
"""
Created on Wed Aug 19 19:55:07 2026

@author: Анастасия
"""
import json


class ConfigManager:
    DEFAULT_CONFIG = {
        'window_width': 1100,
        'window_height': 750,
        'ai_skill': 1,
        'theme': 'Морская',
        'font_size': 10,
        'cell_size': 35
    }

    def __init__(self, filename='config.json'):
        self.filename = filename
        self.config = self.DEFAULT_CONFIG.copy()
        self.load()

    def load(self):
        try:
            with open(self.filename, 'r', encoding='utf-8') as f:
                data = json.load(f)
                for key, value in data.items():
                    if key in self.config:
                        self.config[key] = value
        except FileNotFoundError:
            self.save()

    def save(self):
        with open(self.filename, 'w', encoding='utf-8') as f:
            json.dump(self.config, f, indent=2, ensure_ascii=False)

    def get(self, key):
        return self.config.get(key, self.DEFAULT_CONFIG.get(key))

    def set(self, key, value):
        self.config[key] = value
        self.save()