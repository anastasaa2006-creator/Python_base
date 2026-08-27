# -*- coding: utf-8 -*-
"""
Created on Mon Aug 17 19:54:30 2026

@author: Анастасия
"""
import os
import psycopg2
from dotenv import load_dotenv
from models.market import Market

load_dotenv()

class DBMarketManager:
    def __init__(self):
        try:
            self.conn = psycopg2.connect(
                host=os.getenv('DB_HOST', 'localhost'),
                database=os.getenv('DB_NAME', 'farmers_markets_new'),
                user=os.getenv('DB_USER', 'postgres'),
                password=os.getenv('DB_PASSWORD'),
                port=os.getenv('DB_PORT', '5432')
            )
        except Exception as e:
            raise Exception(f"Не удалось подключиться к БД: {e}")
    
    def get_all(self):
        cur = self.conn.cursor()
        cur.execute("SELECT * FROM markets")
        rows = cur.fetchall()
        cur.close()

        cur = self.conn.cursor()
        cur.execute("SELECT * FROM markets LIMIT 0")
        col_names = [desc[0] for desc in cur.description]
        cur.close()
        
        markets = []
        for row in rows:
            data = dict(zip(col_names, row))
            market_data = {}
            for key, value in data.items():
                if key == 'fmid': market_data['FMID'] = value
                elif key == 'marketname': market_data['MarketName'] = value
                elif key == 'city': market_data['city'] = value
                elif key == 'state': market_data['State'] = value
                elif key == 'zip': market_data['zip'] = value
                elif key == 'y': market_data['y'] = value
                elif key == 'x': market_data['x'] = value
                else: market_data[key.capitalize()] = value
            
            market = Market(market_data)
            
            
            cur = self.conn.cursor()
            cur.execute("SELECT season_number, season_date, season_time FROM market_seasons WHERE fmid = %s", (market.fmid,))
            seasons = cur.fetchall()
            cur.close()
            
            for season_num, season_date, season_time in seasons:
                setattr(market, f'season{season_num}_date', season_date)
                setattr(market, f'season{season_num}_time', season_time)
            

            cur = self.conn.cursor()
            cur.execute("SELECT payment_type FROM market_payments WHERE fmid = %s", (market.fmid,))
            payments = cur.fetchall()
            cur.close()
            
            for payment_type in payments:
                setattr(market, payment_type[0].lower(), 'Y')
              
            cur = self.conn.cursor()
            cur.execute("SELECT category FROM market_categories WHERE fmid = %s", (market.fmid,))
            categories = cur.fetchall()
            cur.close()
            
            for category in categories:
                setattr(market, category[0].lower(), 'Y')
            
            markets.append(market)
        
        return markets
    
    def search_by_city_state(self, city, state):
        cur = self.conn.cursor()
        cur.execute(
            "SELECT * FROM markets WHERE LOWER(city) LIKE %s AND LOWER(state) LIKE %s",
            (f"%{city.lower()}%", f"%{state.lower()}%")
        )
        rows = cur.fetchall()
        cur.close()
        return self._rows_to_markets(rows)
    
    def search_by_zip(self, zip_code):
        cur = self.conn.cursor()
        cur.execute("SELECT * FROM markets WHERE zip = %s", (zip_code,))
        rows = cur.fetchall()
        cur.close()
        return self._rows_to_markets(rows)
    
    def search_by_distance(self, lat, lon, radius):
        cur = self.conn.cursor()
        cur.execute("""
            SELECT *, 
            3959 * acos(cos(radians(%s)) * cos(radians(CAST(y AS FLOAT))) * 
            cos(radians(CAST(x AS FLOAT)) - radians(%s)) + sin(radians(%s)) * sin(radians(CAST(y AS FLOAT)))) AS distance
            FROM markets
            WHERE y IS NOT NULL AND x IS NOT NULL AND y != '' AND x != ''
            HAVING distance < %s
            ORDER BY distance
        """, (lat, lon, lat, radius))
        rows = cur.fetchall()
        cur.close()
        return self._rows_to_markets(rows)
    
    def _rows_to_markets(self, rows):
        if not rows:
            return []
        cur = self.conn.cursor()
        cur.execute("SELECT * FROM markets LIMIT 0")
        col_names = [desc[0] for desc in cur.description]
        cur.close()
        
        markets = []
        for row in rows:
            data = dict(zip(col_names, row))
            market_data = {}
            for key, value in data.items():
                if key == 'fmid': market_data['FMID'] = value
                elif key == 'marketname': market_data['MarketName'] = value
                elif key == 'city': market_data['city'] = value
                elif key == 'state': market_data['State'] = value
                elif key == 'zip': market_data['zip'] = value
                elif key == 'y': market_data['y'] = value
                elif key == 'x': market_data['x'] = value
                elif key == 'website': market_data['Website'] = value
                elif key == 'facebook': market_data['Facebook'] = value
                elif key == 'twitter': market_data['Twitter'] = value
                elif key == 'youtube': market_data['Youtube'] = value
                elif key == 'othermedia': market_data['OtherMedia'] = value
                elif key == 'street': market_data['street'] = value
                elif key == 'county': market_data['County'] = value
                elif key == 'location': market_data['Location'] = value
                elif key == 'updatetime': market_data['updateTime'] = value
            markets.append(Market(market_data))
        return markets