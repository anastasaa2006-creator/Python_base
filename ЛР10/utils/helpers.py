# -*- coding: utf-8 -*-
"""
Created on Wed Aug 19 20:37:34 2026

@author: Анастасия
"""

# utils/helpers.py

def safe_int_input(prompt):
    """Безопасный ввод целого числа."""
    while True:
        try:
            return int(input(prompt))
        except ValueError:
            print("Ошибка: введите целое число!")


def safe_float_input(prompt):
    """Безопасный ввод числа с плавающей точкой."""
    while True:
        try:
            return float(input(prompt))
        except ValueError:
            print("Ошибка: введите число!")