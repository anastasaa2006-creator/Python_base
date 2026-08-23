import math

def haversine(lat1, lon1, lat2, lon2):
    """Вычисляет расстояние между двумя точками в милях."""
    lat1, lon1, lat2, lon2 = map(math.radians, [lat1, lon1, lat2, lon2])
    dlat = lat2 - lat1
    dlon = lon2 - lon1
    a = math.sin(dlat / 2) ** 2 + math.cos(lat1) * math.cos(lat2) * math.sin(dlon / 2) ** 2
    return 3959.0 * 2 * math.asin(math.sqrt(a))
