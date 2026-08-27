# -*- coding: utf-8 -*-
"""
Created on Sun Aug 16 21:42:25 2026

@author: Анастасия
"""

import unittest
from controller import Controller

class TestController(unittest.TestCase):
    
    def setUp(self):
        self.controller = Controller()
    
    def test_get_all_markets(self):
        """Проверяет, что список рынков загружается."""
        markets = self.controller.get_all_markets()
        self.assertTrue(len(markets) > 0)
        print(f" Загружено рынков: {len(markets)}")
    
    def test_search_by_city_state(self):
        """Проверяет поиск по городу и штату (ищет любой существующий)."""
        markets = self.controller.get_all_markets()
        if not markets:
            self.skipTest("Нет данных для теста")
        
        # Берем первый рынок из базы
        first = markets[0]
        city = first.city
        state = first.state
        
        result = self.controller.search_by_city_state(city, state)
        self.assertTrue(len(result) > 0)
        print(f"Поиск по городу '{city}' и штату '{state}' дал {len(result)} результатов")
    
    def test_search_by_zip(self):
        """Проверяет поиск по ZIP (ищет любой существующий)."""
        markets = self.controller.get_all_markets()
        if not markets:
            self.skipTest("Нет данных для теста")
        
        # Берем первый рынок с ZIP
        for market in markets:
            if market.zip:
                zip_code = market.zip
                result = self.controller.search_by_zip(zip_code)
                self.assertTrue(len(result) > 0)
                print(f" Поиск по ZIP '{zip_code}' дал {len(result)} результатов")
                return
        
        self.skipTest("Нет рынков с ZIP в базе")
    
    def test_add_review(self):
        """Проверяет добавление отзыва."""
        markets = self.controller.get_all_markets()
        if not markets:
            self.skipTest("Нет данных для теста")
        
        market = markets[0]
        self.controller.add_review(market, "TestUser", "Test review", 5)
        reviews = self.controller.get_reviews(market.fmid)
        
        found = False
        for r in reviews:
            if r.user == "TestUser":
                found = True
                break
        
        self.assertTrue(found)
        print(f"Отзыв добавлен для рынка {market.name}")
        
        # Чистим за собой
        for i, r in enumerate(reviews):
            if r.user == "TestUser":
                self.controller.delete_review(market, i, "TestUser")
                break

if __name__ == "__main__":
    unittest.main()