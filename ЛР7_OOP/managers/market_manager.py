import csv
from models.market import Market
from utils.helpers import haversine

class MarketManager:
    def __init__(self, filename='Export.csv'):
        self.filename = filename
        self.markets = []
        self.load()

    def load(self):
        try:
            with open(self.filename, 'r') as f:
                reader = csv.DictReader(f)
                for row in reader:
                    self.markets.append(Market(row))
        except FileNotFoundError:
            print(f"Ошибка: файл {self.filename} не найден!")
            self.markets = []
        
        except Exception as e:
            print(f"Ошибка при загрузке: {e}")
            self.markets = []
   
    def get_all(self):
        return self.markets

    def get_by_index(self, index):
        if 0 <= index < len(self.markets):
            return self.markets[index]
        return None

    def search_by_city_state(self, city, state):
        return [m for m in self.markets if m.city.lower() == city.lower() and m.state.lower() == state.lower()]

    def search_by_zip(self, zip_code):
        return [m for m in self.markets if m.zip == zip_code]

    def search_by_distance(self, lat, lon, radius):
        result = []
        for m in self.markets:
            if m.lat == 0 or m.lon == 0:
                continue
            dist = haversine(lat, lon, m.lat, m.lon)
            if dist <= radius:
                result.append((dist, m))
        result.sort(key=lambda x: x[0])
        return result

    def sort(self, key, reverse=False):
        if key == 'name':
            self.markets.sort(key=lambda m: m.name.lower(), reverse=reverse)
        elif key == 'city':
            self.markets.sort(key=lambda m: m.city.lower(), reverse=reverse)
        elif key == 'state':
            self.markets.sort(key=lambda m: m.state.lower(), reverse=reverse)
        elif key == 'rating':
            self.markets.sort(key=lambda m: m.get_rating(), reverse=reverse)