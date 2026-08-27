from models.review import Review

class Market:
    """Класс для хранения данных об одном рынке."""
    def __init__(self, data):
        self.fmid = data.get('FMID', '')
        self.name = data.get('MarketName', '')
        self.website = data.get('Website', '')
        self.facebook = data.get('Facebook', '')
        self.twitter = data.get('Twitter', '')
        self.youtube = data.get('Youtube', '')
        self.other_media = data.get('OtherMedia', '')
        self.street = data.get('street', '')
        self.city = data.get('city', '')
        self.county = data.get('County', '')
        self.state = data.get('State', '')
        self.zip = data.get('zip', '')
        self.season1_date = data.get('Season1Date', '')
        self.season1_time = data.get('Season1Time', '')
        self.season2_date = data.get('Season2Date', '')
        self.season2_time = data.get('Season2Time', '')
        self.season3_date = data.get('Season3Date', '')
        self.season3_time = data.get('Season3Time', '')
        self.season4_date = data.get('Season4Date', '')
        self.season4_time = data.get('Season4Time', '')
        self.lat = float(data.get('y', 0)) if data.get('y', '') else 0
        self.lon = float(data.get('x', 0)) if data.get('x', '') else 0
        self.location = data.get('Location', '')
        self.credit = data.get('Credit', '')
        self.wic = data.get('WIC', '')
        self.wic_cash = data.get('WICcash', '')
        self.sfmnp = data.get('SFMNP', '')
        self.snap = data.get('SNAP', '')
        self.organic = data.get('Organic', '')
        self.baked_goods = data.get('Bakedgoods', '')
        self.cheese = data.get('Cheese', '')
        self.crafts = data.get('Crafts', '')
        self.flowers = data.get('Flowers', '')
        self.eggs = data.get('Eggs', '')
        self.seafood = data.get('Seafood', '')
        self.herbs = data.get('Herbs', '')
        self.vegetables = data.get('Vegetables', '')
        self.honey = data.get('Honey', '')
        self.jams = data.get('Jams', '')
        self.maple = data.get('Maple', '')
        self.meat = data.get('Meat', '')
        self.nursery = data.get('Nursery', '')
        self.nuts = data.get('Nuts', '')
        self.plants = data.get('Plants', '')
        self.poultry = data.get('Poultry', '')
        self.prepared = data.get('Prepared', '')
        self.soap = data.get('Soap', '')
        self.trees = data.get('Trees', '')
        self.wine = data.get('Wine', '')
        self.coffee = data.get('Coffee', '')
        self.beans = data.get('Beans', '')
        self.fruits = data.get('Fruits', '')
        self.grains = data.get('Grains', '')
        self.juices = data.get('Juices', '')
        self.mushrooms = data.get('Mushrooms', '')
        self.pet_food = data.get('PetFood', '')
        self.tofu = data.get('Tofu', '')
        self.wild_harvested = data.get('WildHarvested', '')
        self.update_time = data.get('updateTime', '')
        self.reviews = []

    def get_rating(self):
        if not self.reviews:
            return 0
        total = sum(r.rating for r in self.reviews)
        rating = total / len(self.reviews)
        print(f"DEBUG get_rating: {self.name} → {rating}")  # ← ДОБАВЬ!
        return rating

    def display_brief(self, index):
        rating = self.get_rating()
        rating_str = f" ({rating:.1f} ★)" if rating > 0 else ""
        return f"{index}. {self.name} - {self.city}, {self.state}{rating_str}"
        
    def __str__(self):
        return f"Market(name='{self.name}', city='{self.city}', state='{self.state}')"

    def display_full(self):
        print("\n" + "=" * 50)
        print(f"FMID: {self.fmid}")
        print(f"Name: {self.name}")
        print(f"Website: {self.website}")
        print(f"Facebook: {self.facebook}")
        print(f"Twitter: {self.twitter}")
        print(f"Youtube: {self.youtube}")
        print(f"Other Media: {self.other_media}")
        print(f"Street: {self.street}")
        print(f"City: {self.city}")
        print(f"County: {self.county}")
        print(f"State: {self.state}")
        print(f"ZIP: {self.zip}")
        print(f"Season 1: {self.season1_date} - {self.season1_time}")
        print(f"Season 2: {self.season2_date} - {self.season2_time}")
        print(f"Season 3: {self.season3_date} - {self.season3_time}")
        print(f"Season 4: {self.season4_date} - {self.season4_time}")
        print(f"Coordinates: ({self.lat}, {self.lon})")
        print(f"Location: {self.location}")
        
        print("\nPayment Methods:")
        methods = []
        if self.credit == 'Y': methods.append('Credit Card')
        if self.wic == 'Y': methods.append('WIC')
        if self.wic_cash == 'Y': methods.append('WIC Cash')
        if self.sfmnp == 'Y': methods.append('SFMNP')
        if self.snap == 'Y': methods.append('SNAP')
        print(f"  {', '.join(methods) if methods else 'Not specified'}")
        
        print("\nCategories:")
        categories = []
        if self.organic == 'Y': categories.append('Organic')
        if self.baked_goods == 'Y': categories.append('Baked Goods')
        if self.cheese == 'Y': categories.append('Cheese')
        if self.crafts == 'Y': categories.append('Crafts')
        if self.flowers == 'Y': categories.append('Flowers')
        if self.eggs == 'Y': categories.append('Eggs')
        if self.seafood == 'Y': categories.append('Seafood')
        if self.herbs == 'Y': categories.append('Herbs')
        if self.vegetables == 'Y': categories.append('Vegetables')
        if self.honey == 'Y': categories.append('Honey')
        if self.jams == 'Y': categories.append('Jams')
        if self.maple == 'Y': categories.append('Maple')
        if self.meat == 'Y': categories.append('Meat')
        if self.nuts == 'Y': categories.append('Nuts')
        if self.plants == 'Y': categories.append('Plants')
        if self.poultry == 'Y': categories.append('Poultry')
        if self.prepared == 'Y': categories.append('Prepared Food')
        if self.soap == 'Y': categories.append('Soap')
        if self.wine == 'Y': categories.append('Wine')
        if self.coffee == 'Y': categories.append('Coffee')
        if self.fruits == 'Y': categories.append('Fruits')
        if self.tofu == 'Y': categories.append('Tofu')
        print(f"  {', '.join(categories) if categories else 'Not specified'}")
        
        rating = self.get_rating()
        print(f"\nRating: {rating:.1f} ★" if rating > 0 else "\nNo reviews yet")
        
        if self.reviews:
            print("\nReviews:")
            for i, r in enumerate(self.reviews):
                print(f"  {i+1}. {r.user} - {r.rating} ★: {r.text}")
        print("=" * 50)