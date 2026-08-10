# -*- coding: utf-8 -*-
"""
Created on Mon Aug 10 19:12:23 2026

@author: Анастасия
"""
import math
class RatNum:
    
    def __init__(self, num, den=1):

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
        return self._num == 0 and self._den == 0
        
        
    def is_negative(self):
        if self.is_nan():
            return False
        return self._num < 0
        
    def is_positive(self):
       if self.is_nan():
           return False
       return self._num > 0
        
    def compare_to(self, other):
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
        if self.is_nan():
           return float('nan')
        return self._num / self._den
        
    def int_value(self):
        if self.is_nan():
           return 0
        return self._num // self._den
        
    def __neg__(self):
        if self.is_nan():
            return RatNum(0, 0)
        return RatNum(-self._num,self._den)
   
    def __add__(self, other):  #сложение
        if not isinstance(other, RatNum):
            raise TypeError("other должен быть RatNum")
        if self.is_nan() or other.is_nan():
            return RatNum(0, 0)  # NaN
        
        num = self._num * other._den + other._num * self._den
        den = self._den * other._den
        return RatNum(num, den)
    
    def __sub__(self, other):
        if not isinstance(other, RatNum): #Вычитание
            raise TypeError("other должен быть RatNum")
        return self.__add__(-other)
    
    def __mul__(self, other):
        if not isinstance(other, RatNum): #Умножение
            raise TypeError("other должен быть RatNum")
        if self.is_nan() or other.is_nan():
            return RatNum(0, 0)  # NaN
        
        num = self._num * other._num
        den = self._den * other._den
        return RatNum(num, den)
        
    def __truediv__(self, other):
       if not isinstance(other, RatNum): #Деление
           raise TypeError("other должен быть RatNum")
       if other.is_nan():
           return RatNum(0, 0)  # NaN
       if other._num == 0:
           return RatNum(0, 0)  # деление на 0
       if self.is_nan():
           return self
       
       return self.__mul__(RatNum(other._den, other._num))    
    
    @staticmethod 
    def gcd(a, b):
        return math.gcd(abs(a), abs(b))
    
    def __str__(self):
        if self.is_nan():
             return "NaN"
        if self._den == 1:
             return str(self._num)
        return f"{self._num}/{self._den}"
   
    def __hash__(self):
        if self.is_nan():
            return 0
        return hash((self._num, self._den))
        
        
    def __eq__(self, other):
        if not isinstance(other, RatNum):
            return False
        return self.compare_to(other) == 0    
        
        
        
        
        
        
        
        
        
        
        