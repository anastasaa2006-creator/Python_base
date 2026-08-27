# -*- coding: utf-8 -*-
"""
Created on Fri Aug 14 20:40:05 2026

@author: Анастасия
"""

from managers.db_market_manager import DBMarketManager
from managers.review_manager import ReviewManager
from config import settings
from utils.helpers import haversine

class Controller:
    def __init__(self):
        self.market_manager = DBMarketManager()
        self.review_manager = ReviewManager(settings.REVIEWS_FILE)
        
    def get_all_markets(self):
        markets = self.market_manager.get_all()
        print(f"DEBUG: Загружено рынков: {len(markets)}")
        print(f"DEBUG: Отзывов в менеджере: {len(self.review_manager.reviews)}")
        
        for market in markets:
            fmid = market.fmid
            print(f"DEBUG: Рынок {market.name} (fmid={fmid}, тип={type(fmid)})")
            if fmid in self.review_manager.reviews:
                market.reviews = self.review_manager.reviews[fmid]
                print(f"DEBUG: Найдено {len(market.reviews)} отзывов")
            else:
                market.reviews = []
                print(f"DEBUG: Отзывов НЕТ для fmid={fmid}")
        return markets
    
    def search_markets(self, city=None, state=None, zip_code=None, radius=None):
        """
        Универсальный поиск рынков.
        Если указан radius — фильтрует по расстоянию.
        """
        lat, lon = None, None
        results = []

        if city and state:
            lat, lon = self.get_coordinates_by_city_state(city, state)
            if lat is None or lon is None:
                raise ValueError(f"Не найдены координаты для {city}, {state}")
            
            if radius is None:
                results = self.search_by_city_state(city, state)
            else:
                results = self.get_all_markets()

        elif zip_code:
            lat, lon = self.get_coordinates_by_zip(zip_code)
            if lat is None or lon is None:
                raise ValueError(f"Не найдены координаты для ZIP: {zip_code}")
            
            if radius is None:
                results = self.search_by_zip(zip_code)
            else:
                results = self.get_all_markets()

        else:
            raise ValueError("Укажите город+штат или ZIP код!")

        if radius is not None and radius > 0 and lat is not None and lon is not None:
            filtered = []
            for market in results:
                if market.lat == 0 or market.lon == 0:
                    continue
                dist = haversine(lat, lon, market.lat, market.lon)
                if dist <= radius:
                    filtered.append(market)
            results = filtered

        return results
        
    def search_by_city_state(self, city, state):
        """Поиск рынков по городу и штату."""
        city_clean = city.lower().replace(" ", "")
        state_clean = state.lower().replace(" ", "")
        
        result = []
        for market in self.market_manager.get_all():

            if market.city is None or market.state is None:
                continue
            
            market_city = market.city.lower().replace(" ", "")
            market_state = market.state.lower().replace(" ", "")
            
            if city_clean in market_city and state_clean in market_state:
                result.append(market)
        
        return result
        

    def get_coordinates_by_city_state(self, city, state):
        """Возвращает координаты (УДАЛЯЕТ ВСЕ ПРОБЕЛЫ!)."""
        city_clean = city.lower().replace(" ", "")
        state_clean = state.lower().replace(" ", "")
        
        lat_sum = 0
        lon_sum = 0
        count = 0
        
        for market in self.market_manager.get_all():
            if market.city is None or market.state is None:
                continue
            
            market_city = market.city.lower().replace(" ", "")
            market_state = market.state.lower().replace(" ", "")
            
            if city_clean in market_city and state_clean in market_state:
                if market.lat != 0 and market.lon != 0:
                    lat_sum += market.lat
                    lon_sum += market.lon
                    count += 1
        
        if count > 0:
            return lat_sum / count, lon_sum / count
        
        return None, None
    

    def search_by_zip(self, zip_code):
        return self.market_manager.search_by_zip(zip_code)
    
    def add_review(self, market, user, text, rating):
        self.review_manager.add(market, user, text, rating)
    
    def get_reviews(self, fmid):
        return self.review_manager.get(fmid)
    
    def delete_review(self, market, index, user):
        return self.review_manager.delete(market, index, user)
    
    def search_by_distance(self, lat, lon, radius):
        return self.market_manager.search_by_distance(lat, lon, radius)
    
    def get_coordinates_by_zip(self, zip_code):
        for market in self.market_manager.get_all():
            if market.zip == zip_code:
                return market.lat, market.lon
        return None, None