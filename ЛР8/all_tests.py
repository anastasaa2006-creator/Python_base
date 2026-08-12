# -*- coding: utf-8 -*-
"""
Created on Wed Aug 12 19:52:13 2026

@author: Анастасия
"""
import unittest

if __name__ == "__main__":
    # Загружаем все тесты из файлов
    loader = unittest.TestLoader()
    suite = unittest.TestSuite()
    
    suite.addTests(loader.loadTestsFromName('test_ratnum'))
    suite.addTests(loader.loadTestsFromName('test_ratpoly'))
    
    runner = unittest.TextTestRunner(verbosity=2)
    runner.run(suite)
