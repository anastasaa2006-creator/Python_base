# -*- coding: utf-8 -*-
"""
Created on Tue Aug 11 18:25:09 2026

@author: Анастасия
"""
import math
from RatNum import RatNum


class RatPoly:
    """
    Полином с рациональными коэффициентами.
    
    Поля представления:
        - self._coeffs: list[RatNum] — коэффициенты от младшей степени к старшей
          Например: [a0, a1, a2, ...] → a0 + a1*x + a2*x^2 + ...
    
    Инвариант представления:
        - Все коэффициенты — RatNum
        - Старший коэффициент не равен нулю (кроме полинома 0)
        - Пустой список обозначает полином 0
    
    Функция абстракции:
        - Полином представляется как сумма coeff[i] * x^i
    """
    
    def __init__(self, coeffs=None):
        """
        создает полином с коэффициентами coeffs
        
        @requires: coeffs — список RatNum или чисел (int, float) или None
        @modifies: nothing
        @effects: создает новый полином
        @throws: TypeError если coeffs не список
        @returns: RatPoly
        """
        if coeffs is None:
            self._coeffs = []
            return
        
        if not isinstance(coeffs, list):
            raise TypeError("coeffs должен быть списком")
        
        rat_coeffs = []
        for c in coeffs:
            if isinstance(c, RatNum):
                rat_coeffs.append(c)
            elif isinstance(c, (int, float)):
                rat_coeffs.append(RatNum(int(c), 1) if isinstance(c, int) else RatNum(int(c), 1))
            else:
                raise TypeError(f"Неподдерживаемый тип коэффициента: {type(c)}")
        
        # Удаляем ведущие нули
        while rat_coeffs and (rat_coeffs[-1].is_nan() or (not rat_coeffs[-1].is_nan() and rat_coeffs[-1]._num == 0)):
            rat_coeffs.pop()
        
        self._coeffs = rat_coeffs
    
    def degree(self):
        """
        возвращает степень полинома
        
        @requires: none
        @modifies: nothing
        @effects: возвращает степень полинома (0 для полинома 0)
        @throws: none
        @returns: int
        """
        if not self._coeffs:
            return 0
        return len(self._coeffs) - 1
    
    def get_coeff(self, degree):
        """
        возвращает коэффициент при x^degree
        
        @requires: degree >= 0
        @modifies: nothing
        @effects: возвращает коэффициент при x^degree
        @throws: ValueError если degree < 0
        @returns: RatNum
        """
        if degree < 0:
            raise ValueError("Степень не может быть отрицательной")
        
        if degree >= len(self._coeffs):
            return RatNum(0, 1)
        
        return self._coeffs[degree]

    def is_nan(self):
        """
        проверяет является ли полином NaN
        
        @requires: none
        @modifies: nothing
        @effects: возвращает True если хотя бы один коэффициент NaN
        @throws: none
        @returns: bool
        """
        for c in self._coeffs:
            if c.is_nan():
                return True
        return False
    
    def scale_coeff(self, scale):
        """
        все коэффициенты полинома умножаем на число - scale.
        
        @requires: scale — RatNum
        @modifies: nothing
        @effects: возвращает новый полином с коэффициентами, умноженными на scale
        @throws: TypeError если scale не RatNum
        @returns: RatPoly
        """
        if not isinstance(scale, RatNum):
            raise TypeError("scale должен быть RatNum")
        
        new_coeffs = [c * scale for c in self._coeffs]
        return RatPoly(new_coeffs)

    def __neg__(self):
        """
        унарный - (аддитивная инверсия)
        
        @requires: none
        @modifies: nothing
        @effects: возвращает -self
        @throws: none
        @returns: RatPoly
        """
        new_coeffs = [-c for c in self._coeffs]
        return RatPoly(new_coeffs)  
        
    def __add__(self, other):
        """
        сложение полиномов
        
        @requires: other — RatPoly
        @modifies: nothing
        @effects: возвращает self + other
        @throws: TypeError если other не RatPoly
        @returns: RatPoly
        """
        if not isinstance(other, RatPoly):
            raise TypeError("other должен быть RatPoly")
        
        max_len = max(len(self._coeffs), len(other._coeffs))
        result_coeffs = [RatNum(0, 1) for _ in range(max_len)]
        
        for i in range(max_len):
            if i < len(self._coeffs):
                result_coeffs[i] = result_coeffs[i] + self._coeffs[i]
            if i < len(other._coeffs):
                result_coeffs[i] = result_coeffs[i] + other._coeffs[i]
        
        return RatPoly(result_coeffs)
    
    def __sub__(self, other):
        """
        вычитание полиномов
        
        @requires: other — RatPoly
        @modifies: nothing
        @effects: возвращает self - other
        @throws: TypeError если other не RatPoly
        @returns: RatPoly
        """
        if not isinstance(other, RatPoly):
            raise TypeError("other должен быть RatPoly")
        return self + (-other)    
        
    def __mul__(self, other):
        """
        умножение полиномов
        
        @requires: other — RatPoly
        @modifies: nothing
        @effects: возвращает self * other
        @throws: TypeError если other не RatPoly
        @returns: RatPoly
        """
        if not isinstance(other, RatPoly):
            raise TypeError("other должен быть RatPoly")
        
        if not self._coeffs or not other._coeffs:
            return RatPoly([])
        
        result_len = len(self._coeffs) + len(other._coeffs) - 1
        result_coeffs = [RatNum(0, 1) for _ in range(result_len)]
        
        for i, c1 in enumerate(self._coeffs):
            for j, c2 in enumerate(other._coeffs):
                result_coeffs[i + j] = result_coeffs[i + j] + (c1 * c2)
        
        return RatPoly(result_coeffs)
    
    def __truediv__(self, other):
        """
        деление полиномов
        
        @requires: other — RatPoly (не нулевой)
        @modifies: nothing
        @effects: возвращает self / other
        @throws: TypeError если other не RatPoly
        @returns: RatPoly
        """
        if not isinstance(other, RatPoly):
            raise TypeError("other должен быть RatPoly")
        
        if not other._coeffs:
            return RatPoly([RatNum(0, 0)])
        
        if not self._coeffs:
            return RatPoly([])
        
        dividend = self._coeffs.copy()
        divisor = other._coeffs.copy()
        result = []
        
        while len(dividend) >= len(divisor):
            coeff = dividend[-1] / divisor[-1]
            result.append(coeff)
            
            for i in range(len(divisor)):
                dividend[len(dividend) - 1 - i] = dividend[len(dividend) - 1 - i] - (coeff * divisor[len(divisor) - 1 - i])
            
            dividend.pop()
            
            while dividend and dividend[-1]._num == 0:
                dividend.pop()
        
        result.reverse()
        return RatPoly(result)
    
    def eval(self, x):
        """
        вычисляет значение полинома в конкретной точке x
        
        @requires: x — RatNum
        @modifies: nothing
        @effects: возвращает значение полинома в точке x
        @throws: TypeError если x не RatNum
        @returns: RatNum
        """
        if not isinstance(x, RatNum):
            raise TypeError("x должен быть RatNum")
        
        if not self._coeffs:
            return RatNum(0, 1)
        
        result = RatNum(0, 1)
        power = RatNum(1, 1)
        
        for c in self._coeffs:
            result = result + (c * power)
            power = power * x
        
        return result
    
    def differentiate(self):
        """
        производная полинома
        
        @requires: none
        @modifies: nothing
        @effects: возвращает производную полинома
        @throws: none
        @returns: RatPoly
        """
        if len(self._coeffs) <= 1:
            return RatPoly([])
        
        result = []
        for i in range(1, len(self._coeffs)):
            result.append(self._coeffs[i] * RatNum(i, 1))
        
        return RatPoly(result)
    
    def anti_differentiate(self):
        """
        первообразная полинома (с константой 0).
        
        @requires: none
        @modifies: nothing
        @effects: возвращает первообразную полинома
        @throws: none
        @returns: RatPoly
        """
        result = [RatNum(0, 1)]
        for i, c in enumerate(self._coeffs):
            result.append(c / RatNum(i + 1, 1))
        
        return RatPoly(result)
    
    def integrate(self, a, b):
        """
        определенный интеграл от a до b.
        
        @requires: a, b — RatNum
        @modifies: nothing
        @effects: возвращает определенный интеграл от a до b
        @throws: TypeError если a или b не RatNum
        @returns: RatNum
        """
        if not isinstance(a, RatNum) or not isinstance(b, RatNum):
            raise TypeError("a и b должны быть RatNum")
        
        poly = self.anti_differentiate()
        return poly.eval(b) - poly.eval(a)
    
    def value_of(self):
        """
        возвращает значение полинома как RatNum (если степень 0).
        
        @requires: degree() == 0
        @modifies: nothing
        @effects: возвращает единственный коэффициент
        @throws: ValueError если степень > 0
        @returns: RatNum
        """
        if self.degree() > 0:
            raise ValueError("value_of() можно вызывать только для полинома степени 0")
        
        if not self._coeffs:
            return RatNum(0, 1)
        
        return self._coeffs[0]
    
    def __str__(self):
        """
        строковое красивое представление полинома
        
        @requires: none
        @modifies: nothing
        @effects: возвращает строку вида "a0 + a1*x + a2*x^2 + ..."
        @throws: none
        @returns: str
        """
        if not self._coeffs:
            return "0"
        
        if self.is_nan():
            return "NaN"
        
        result = []
        for i, c in enumerate(self._coeffs):
            if c._num == 0:
                continue
            
            if i == 0:
                result.append(str(c))
            elif i == 1:
                result.append(f"{c}*x")
            else:
                result.append(f"{c}*x^{i}")
        
        return " + ".join(result) if result else "0"
    
    def __hash__(self):
        """
        хэш-код !полинома!
        
        @requires: none
        @modifies: nothing
        @effects: возвращает хэш-код
        @throws: none
        @returns: int
        """
        if self.is_nan():
            return 0
        return hash(tuple(self._coeffs))
    
    def __eq__(self, other):
        """
        проверяет равны ли два полинома 
        
        @requires: other — RatPoly
        @modifies: nothing
        @effects: возвращает True если полиномы равны
        @throws: none
        @returns: bool
        """
        if not isinstance(other, RatPoly):
            return False
        
        if self.is_nan() and other.is_nan():
            return True
        
        if len(self._coeffs) != len(other._coeffs):
            return False
        
        for i in range(len(self._coeffs)):
            if self._coeffs[i] != other._coeffs[i]:
                return False
        
        return True
        