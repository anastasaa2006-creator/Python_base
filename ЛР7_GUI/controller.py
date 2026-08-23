# -*- coding: utf-8 -*-
"""
Created on Fri Aug 14 20:40:05 2026

@author: Анастасия
"""
import logging
from managers.market_manager import MarketManager
from managers.review_manager import ReviewManager
from config import settings
from utils.helpers import haversine

class Controller:
    def __init__(self):
        self.market_manager = MarketManager(settings.DATA_FILE)
        self.review_manager = ReviewManager(settings.REVIEWS_FILE)
        
        for market in self.market_manager.get_all():
            if market.fmid in self.review_manager.reviews:
                market.reviews = self.review_manager.reviews[market.fmid]
            else:
                market.reviews = []
    
    def get_all_markets(self):
        return self.market_manager.get_all()
    

    def search_by_city_state(self, city, state):
        """Поиск рынков по городу и штату"""
        city_clean = city.lower().replace(" ", "")
        state_clean = state.lower().replace(" ", "")
        
        result = []
        for market in self.market_manager.get_all():
            market_city = market.city.lower().replace(" ", "")
            market_state = market.state.lower().replace(" ", "")

            if city_clean in market_city and state_clean in market_state:
                result.append(market)
        
        return result
        

    def get_coordinates_by_city_state(self, city, state):
        """Возвращает координаты"""
        city_clean = city.lower().replace(" ", "")
        state_clean = state.lower().replace(" ", "")
        
        lat_sum = 0
        lon_sum = 0
        count = 0
        
        for market in self.market_manager.get_all():
            market_city = market.city.lower().replace(" ", "")
            market_state = market.state.lower().replace(" ", "")
            
            if city_clean in market_city and state_clean in market_state:
                if market.lat != 0 and market.lon != 0:
                    lat_sum += market.lat
                    lon_sum += market.lon
                    count += 1
        
        if count > 0:
            return lat_sum / count, lon_sum / count
        logging.warning(f"Не найдены координаты для {city}, {state}") 
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