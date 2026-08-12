# -*- coding: utf-8 -*-
"""
Created on Tue Aug 11 18:51:00 2026

@author: Анастасия
"""
import unittest
from RatNum import RatNum
from RatPoly import RatPoly

class TestRatPoly(unittest.TestCase):
    
    def test_constructor(self):
        p = RatPoly([RatNum(1,2), RatNum(3,4)])
        self.assertEqual(len(p._coeffs), 2)
    
    def test_degree(self):
        p = RatPoly([RatNum(1,2), RatNum(3,4), RatNum(5,6)])
        self.assertEqual(p.degree(), 2)
        p2 = RatPoly([])
        self.assertEqual(p2.degree(), 0)
    
    def test_get_coeff(self):
        p = RatPoly([RatNum(1,2), RatNum(3,4), RatNum(5,6)])
        self.assertEqual(str(p.get_coeff(0)), "1/2")
        self.assertEqual(str(p.get_coeff(1)), "3/4")
        self.assertEqual(str(p.get_coeff(2)), "5/6")
        self.assertEqual(str(p.get_coeff(3)), "0")  # несуществующий коэффициент
    
    def test_is_nan(self):
        # NaN должен быть НЕ последним коэффициентом!
        p = RatPoly([RatNum(0,0), RatNum(1,2)])  # NaN + 1/2*x
        self.assertTrue(p.is_nan())
        
        p2 = RatPoly([RatNum(1,2), RatNum(3,4)])
        self.assertFalse(p2.is_nan())
        
    def test_scale_coeff(self):
        p = RatPoly([RatNum(1,2), RatNum(3,4)])
        scaled = p.scale_coeff(RatNum(2,1))
        self.assertEqual(str(scaled), "1 + 3/2*x")
    
    def test_neg(self):
        p = RatPoly([RatNum(1,2), RatNum(3,4)])
        p_neg = -p
        self.assertEqual(str(p_neg), "-1/2 + -3/4*x")
    
    def test_add(self):
        p1 = RatPoly([RatNum(1,2), RatNum(3,4)])
        p2 = RatPoly([RatNum(1,3), RatNum(1,3)])
        p3 = p1 + p2
        self.assertEqual(str(p3), "5/6 + 13/12*x")
    
    def test_sub(self):
        p1 = RatPoly([RatNum(1,2), RatNum(3,4)])
        p2 = RatPoly([RatNum(1,3), RatNum(1,3)])
        p3 = p1 - p2
        self.assertEqual(str(p3), "1/6 + 5/12*x")
    
    def test_mul(self):
        p1 = RatPoly([RatNum(1,2), RatNum(1,2)])
        p2 = RatPoly([RatNum(1,3), RatNum(1,3)])
        p3 = p1 * p2
        self.assertEqual(p3.degree(), 2)
    
    def test_div(self):
        # Проверка деления полиномов
        p1 = RatPoly([RatNum(1,1), RatNum(2,1), RatNum(1,1)])  # 1 + 2x + x²
        p2 = RatPoly([RatNum(1,1), RatNum(1,1)])               # 1 + x
        p3 = p1 / p2
        self.assertEqual(str(p3), "1 + 1*x")  # (x+1)² / (x+1) = x+1
    
    def test_eval(self):
        p = RatPoly([RatNum(1,1), RatNum(2,1)])  # 1 + 2x
        x = RatNum(3,1)
        result = p.eval(x)
        self.assertEqual(str(result), "7")
    
    def test_differentiate(self):
        p = RatPoly([RatNum(1,1), RatNum(2,1), RatNum(3,1)])  # 1 + 2x + 3x²
        p_diff = p.differentiate()
        self.assertEqual(str(p_diff), "2 + 6*x")
    
    def test_anti_differentiate(self):
        p = RatPoly([RatNum(1,1), RatNum(2,1), RatNum(3,1)])
        p_anti = p.anti_differentiate()
        self.assertEqual(str(p_anti), "1*x + 1*x^2 + 1*x^3")
    
    def test_integrate(self):
        p = RatPoly([RatNum(1,1), RatNum(2,1)])  # 1 + 2x
        a = RatNum(0,1)
        b = RatNum(1,1)
        result = p.integrate(a, b)  # ∫₀¹ (1 + 2x) dx = [x + x²]₀¹ = 2
        self.assertEqual(str(result), "2")
    
    def test_value_of(self):
        p = RatPoly([RatNum(5,2)])  # только константа
        self.assertEqual(str(p.value_of()), "5/2")
        
        p2 = RatPoly([RatNum(1,2), RatNum(3,4)])
        with self.assertRaises(ValueError):
            p2.value_of()  # степень > 0 → ошибка
        
    def test_str(self):
        p = RatPoly([RatNum(1,2), RatNum(3,4)])
        self.assertEqual(str(p), "1/2 + 3/4*x")
        p2 = RatPoly([])
        self.assertEqual(str(p2), "0")
    
    def test_hash(self):
        p1 = RatPoly([RatNum(1,2), RatNum(3,4)])
        p2 = RatPoly([RatNum(1,2), RatNum(3,4)])
        self.assertEqual(hash(p1), hash(p2))
    
    def test_eq(self):
        p1 = RatPoly([RatNum(1,2), RatNum(3,4)])
        p2 = RatPoly([RatNum(1,2), RatNum(3,4)])
        p3 = RatPoly([RatNum(1,2), RatNum(1,2)])
        self.assertEqual(p1, p2)
        self.assertNotEqual(p1, p3)

if __name__ == "__main__":
    unittest.main()