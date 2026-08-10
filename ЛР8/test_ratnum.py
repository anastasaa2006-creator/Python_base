# -*- coding: utf-8 -*-
"""
Created on Mon Aug 10 21:09:41 2026

@author: Анастасия
"""

import unittest
import math
from RatNum import RatNum


class TestRatNum(unittest.TestCase):

    def test_constructor(self):
        a = RatNum(1, 2) #конструктор
        self.assertEqual(a._num, 1)
        self.assertEqual(a._den, 2)
        
        b = RatNum(2, 4)
        self.assertEqual(b._num, 1)
        self.assertEqual(b._den, 2)
        
        c = RatNum(0, 0)
        self.assertTrue(c.is_nan())
    
    def test_constructor_zero_division(self):
        
        with self.assertRaises(ZeroDivisionError): #деление на 0
            RatNum(1, 0)


    def test_is_nan(self):
        a = RatNum(1, 2)
        self.assertFalse(a.is_nan())
        
        b = RatNum(0, 0)
        self.assertTrue(b.is_nan())

    def test_is_negative(self):
        a = RatNum(-1, 2)
        self.assertTrue(a.is_negative())
        
        b = RatNum(1, 2)
        self.assertFalse(b.is_negative())
        
        c = RatNum(0, 0)
        self.assertFalse(c.is_negative())


    def test_is_positive(self):
        a = RatNum(1, 2)
        self.assertTrue(a.is_positive())
        
        b = RatNum(-1, 2)
        self.assertFalse(b.is_positive())
        
        c = RatNum(0, 0)
        self.assertFalse(c.is_positive())

   

    def test_compare_to(self):
        a = RatNum(1, 2)
        b = RatNum(1, 3)
        c = RatNum(1, 2)
        nan = RatNum(0, 0)
        
        self.assertTrue(a.compare_to(b) > 0)
        self.assertTrue(b.compare_to(a) < 0)
        self.assertEqual(a.compare_to(c), 0)
        self.assertTrue(nan.compare_to(a) > 0)
        self.assertEqual(nan.compare_to(nan), 0)




    def test_float_value(self):
        a = RatNum(1, 2)
        self.assertAlmostEqual(a.float_value(), 0.5)
        
        b = RatNum(0, 0)
        self.assertTrue(math.isnan(b.float_value()))


    def test_int_value(self):
        a = RatNum(5, 2)
        self.assertEqual(a.int_value(), 2)
        
        b = RatNum(0, 0)
        self.assertEqual(b.int_value(), 0)


    def test_neg(self):
        a = RatNum(1, 2)
        b = -a
        self.assertEqual(b._num, -1)
        self.assertEqual(b._den, 2)
        
        nan = RatNum(0, 0)
        c = -nan
        self.assertTrue(c.is_nan())



    def test_add(self):
        a = RatNum(1, 2)
        b = RatNum(1, 3)
        c = a + b
        self.assertEqual(str(c), "5/6")
        
        nan = RatNum(0, 0)
        d = a + nan
        self.assertTrue(d.is_nan())



    def test_sub(self):
        a = RatNum(1, 2)
        b = RatNum(1, 3)
        c = a - b
        self.assertEqual(str(c), "1/6")


    def test_mul(self):
        a = RatNum(1, 2)
        b = RatNum(2, 3)
        c = a * b
        self.assertEqual(str(c), "1/3")
        
        nan = RatNum(0, 0)
        d = a * nan
        self.assertTrue(d.is_nan())


    def test_div(self):
        a = RatNum(1, 2)
        b = RatNum(2, 3)
        c = a / b
        self.assertEqual(str(c), "3/4")
        
        zero = RatNum(0, 1)
        d = a / zero
        self.assertTrue(d.is_nan())
        
        nan = RatNum(0, 0)
        e = a / nan
        self.assertTrue(e.is_nan())


    def test_str(self):
        a = RatNum(1, 2)
        self.assertEqual(str(a), "1/2")
        
        b = RatNum(3, 1)
        self.assertEqual(str(b), "3")
        
        c = RatNum(0, 0)
        self.assertEqual(str(c), "NaN")

    def test_hash(self):
        a = RatNum(1, 2)
        b = RatNum(2, 4)
        self.assertEqual(hash(a), hash(b))
        
        c = RatNum(0, 0)
        self.assertEqual(hash(c), 0)



    def test_eq(self):
        a = RatNum(1, 2)
        b = RatNum(2, 4)
        c = RatNum(1, 3)
        
        self.assertEqual(a, b)
        self.assertNotEqual(a, c)
        self.assertEqual(a, a)
        
        nan1 = RatNum(0, 0)
        nan2 = RatNum(0, 0)
        self.assertEqual(nan1, nan2)



    def test_gcd(self):
        self.assertEqual(RatNum.gcd(12, 18), 6)
        self.assertEqual(RatNum.gcd(7, 13), 1)


if __name__ == '__main__':
    unittest.main()