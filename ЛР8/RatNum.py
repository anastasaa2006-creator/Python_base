# -*- coding: utf-8 -*-
"""
Created on Mon Aug 10 19:12:23 2026

@author: Анастасия
"""
import math
class RatNum:
    """
    Неизменяемое рациональное число.
    
    Поля представления:
        - self._num: int (числитель)
        - self._den: int (знаменатель, > 0)
    
    Инвариант представления:
        - self._den > 0
        - числитель и знаменатель не имеют общих делителей (кроме 1)
        - NaN: _num = 0, _den = 0
    
    Функция абстракции:
        - Обычное число: _num / _den
        - NaN: специальное значение (0/0)
    """
    
    def __init__(self, num, den=1):
        """
        создает рац. число num/den.
        
        @requires: den != 0 (если num != 0)
        @modifies: nothing
        @effects: создает новое RatNum
        @throws: ZeroDivisionError если den == 0 и num != 0
        @returns: RatNum
        """
        if num == 0 and den == 0:
            self._num = 0           # NaN
            self._den = 0
            return
       
        if den == 0:
            raise ZeroDivisionError("Знаменатель не может быть 0")
       
        if den < 0:
            num = -num
            den = -den
       
        g = math.gcd(abs(num), den)
        self._num = num // g
        self._den = den // g
       
    def is_nan(self):
        """
        проверяет является ли число NaN.
        
        @requires: none
        @modifies: nothing
        @effects: возвращает True если число NaN
        @returns: bool
        """
        return self._num == 0 and self._den == 0
        
    def is_negative(self):
        """
        проверяет отрицательное ли число
        
        @requires: none
        @modifies: nothing
        @effects: возвращает True если число < 0
        @returns: bool
        """
        if self.is_nan():
            return False
        return self._num < 0
        
    def is_positive(self):
        """
        проверяет положительное ли число
        
        @requires: none
        @modifies: nothing
        @effects: возвращает True если число > 0
        @returns: bool
        """
        if self.is_nan():
            return False
        return self._num > 0
        
    def compare_to(self, other):
        """
        сравнивает два рациональных числа.
        
        @requires: other is RatNum
        @modifies: nothing
        @effects: 
            - 0, если числа равны
            - положительное, если self > other
            - отрицательное, если self < other
            - 0, если оба NaN
            - 1, если self NaN
            - -1, если other NaN
        @throws: TypeError если other не RatNum
        @returns: int
        """
        if not isinstance(other, RatNum):
            raise TypeError("other должен быть RatNum")
        
        if self.is_nan() and other.is_nan():
            return 0
        
        if self.is_nan():
            return 1
        if other.is_nan():
            return -1
        
        left = self._num * other._den
        right = other._num * self._den
        return left - right
         
    def float_value(self):
        """
        преобразует рациональное в с плавающей точкой
        
        @requires: none
        @modifies: nothing
        @effects: возвращает число с плавающей точкой
        @returns: float
        """
        if self.is_nan():
            return float('nan')
        return self._num / self._den
        
    def int_value(self):
        """
        возвращает целую часть числа
        
        @requires: none
        @modifies: nothing
        @effects: возвращает целую часть числа
        @returns: int
        """
        if self.is_nan():
            return 0
        return self._num // self._den
        
    def __neg__(self):
        """
        унарный - (аддитивная инверсия)
        
        @requires: none
        @modifies: nothing
        @effects: возвращает -self
        @returns: RatNum
        """
        if self.is_nan():
            return RatNum(0, 0)
        return RatNum(-self._num, self._den)
   
    def __add__(self, other):
        """
        сложение двух чисел
        
        @requires: other is RatNum
        @modifies: nothing
        @effects: возвращает self + other
        @throws: TypeError если other не RatNum
        @returns: RatNum
        """
        if not isinstance(other, RatNum):
            raise TypeError("other должен быть RatNum")
        if self.is_nan() or other.is_nan():
            return RatNum(0, 0)  # NaN
        
        num = self._num * other._den + other._num * self._den
        den = self._den * other._den
        return RatNum(num, den)
    
    def __sub__(self, other):
        """
        вычитание двух чисел
        
        @requires: other is RatNum
        @modifies: nothing
        @effects: возвращает self - other
        @throws: TypeError если other не RatNum
        @returns: RatNum
        """
        if not isinstance(other, RatNum):
            raise TypeError("other должен быть RatNum")
        return self.__add__(-other)
    
    def __mul__(self, other):
        """
        умножение двух чисел
        
        @requires: other is RatNum
        @modifies: nothing
        @effects: возвращает self * other
        @throws: TypeError если other не RatNum
        @returns: RatNum
        """
        if not isinstance(other, RatNum):
            raise TypeError("other должен быть RatNum")
        if self.is_nan() or other.is_nan():
            return RatNum(0, 0)  
        
        num = self._num * other._num
        den = self._den * other._den
        return RatNum(num, den)
        
    def __truediv__(self, other):
        """
        деление двух чисел
        
        @requires: other is RatNum, other != 0
        @modifies: nothing
        @effects: возвращает self / other
        @throws: TypeError если other не RatNum
        @returns: RatNum (NaN если деление на 0)
        """
        if not isinstance(other, RatNum):
            raise TypeError("other должен быть RatNum")
        if other.is_nan():
            return RatNum(0, 0)  
        if other._num == 0:
            return RatNum(0, 0) 
        if self.is_nan():
            return self
       
        return self.__mul__(RatNum(other._den, other._num))
    
    @staticmethod 
    def gcd(a, b):
        """
        находит наибольший общий делитель двух чисел
        
        @requires: a, b — целые числа
        @modifies: nothing
        @effects: возвращает НОД(a, b)
        @returns: int
        """
        return math.gcd(abs(a), abs(b))
    
    def __str__(self):
        """
        строковое красивое представление числа
        
        @requires: none
        @modifies: nothing
        @effects: возвращает строку "num/den" или "NaN"
        @returns: str
        """
        if self.is_nan():
            return "NaN"
        if self._den == 1:
            return str(self._num)
        return f"{self._num}/{self._den}"
   
    def __hash__(self):
        """
        хэш-код !числа!
        
        @requires: none
        @modifies: nothing
        @effects: возвращает хэш-код
        @returns: int
        """
        if self.is_nan():
            return 0
        return hash((self._num, self._den))
        
    def __eq__(self, other):
        """
        проверяет равны ли два рациональных числа
        
        @requires: other is RatNum
        @modifies: nothing
        @effects: возвращает True если числа равны
        @returns: bool
        """
        if not isinstance(other, RatNum):
            return False
        return self.compare_to(other) == 0 
        
        
        
        
        
        
        
        
        
        
        