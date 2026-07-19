import csv
import math
import json

def load_reviews():
    try:
        with open('reviews.json', 'r') as f:
            return json.load(f)
    except FileNotFoundError:
        return {}

def save_reviews(reviews):
    with open('reviews.json', 'w') as f:
        json.dump(reviews, f, indent=2, ensure_ascii=False)
        
        
def read_init(filename):
    with open(filename, 'r') as f:
        reader = csv.DictReader(f)
        markets = []
        for row in reader:
            markets.append(row)
    return markets


def list_markets(markets, reviews):
    per_page = 5
    total = len(markets)
    total_pages = (total + per_page - 1) // per_page
    page = 1
    
    while True:
        start = (page - 1) * per_page
        end = min(start + per_page, total)
        
        print(f"\n=== Page {page}/{total_pages} ===")
        for i in range(start, end):
            m = markets[i]
            fmid = m['FMID']
            
            if fmid in reviews and reviews[fmid]:
                total_rating = 0
                for r in reviews[fmid]:
                    total_rating += r['rating']
                avg = total_rating / len(reviews[fmid])
                rating_str = f" ({avg:.1f} ★)"
            else:
                rating_str = ""
            
            print(f"{i+1}. {m['MarketName']} - {m['city']}, {m['State']}{rating_str}")
        print()
        
        if total_pages <= 1:
            break
        
        print("Options: (next) (prev) (page N - enter the page number) (back)")
        choice = input("=> ").strip().lower()
        print(choice)
        
        if choice == 'next':
            if page < total_pages:
                page += 1
        elif choice == 'prev':
            if page > 1:
                page -= 1
        elif choice.isdigit():
            num = int(choice)
            if 1 <= num <= total_pages:
                page = num
        elif choice == 'back':
            break
        else:
            print("Invalid option")
    

def view_markets(markets):
    num = int(input("Enter market number => "))
    print(num)
    if not (1 <= num <= len(markets)):
        print("Market not found")
        return
    
    m = markets[num - 1]
    
    print("\n" + "=" * 50)
    print(f"FMID: {m.get('FMID', '')}")
    print(f"Name: {m.get('MarketName', '')}")
    print(f"Website: {m.get('Website', '')}")
    print(f"Facebook: {m.get('Facebook', '')}")
    print(f"Twitter: {m.get('Twitter', '')}")
    print(f"Youtube: {m.get('Youtube', '')}")
    print(f"OtherMedia: {m.get('OtherMedia', '')}")
    print(f"Street: {m.get('street', '')}")
    print(f"City: {m.get('city', '')}")
    print(f"County: {m.get('County', '')}")
    print(f"State: {m.get('State', '')}")
    print(f"ZIP: {m.get('zip', '')}")
    print(f"Season1Date: {m.get('Season1Date', '')}")
    print(f"Season1Time: {m.get('Season1Time', '')}")
    print(f"Season2Date: {m.get('Season2Date', '')}")
    print(f"Season2Time: {m.get('Season2Time', '')}")
    print(f"Season3Date: {m.get('Season3Date', '')}")
    print(f"Season3Time: {m.get('Season3Time', '')}")
    print(f"Season4Date: {m.get('Season4Date', '')}")
    print(f"Season4Time: {m.get('Season4Time', '')}")
    print(f"Coordinates: ({m.get('y', '')}, {m.get('x', '')})")
    print(f"Location: {m.get('Location', '')}")
    print(f"Credit: {m.get('Credit', '')}")
    print(f"WIC: {m.get('WIC', '')}")
    print(f"WICcash: {m.get('WICcash', '')}")
    print(f"SFMNP: {m.get('SFMNP', '')}")
    print(f"SNAP: {m.get('SNAP', '')}")
    print(f"Organic: {m.get('Organic', '')}")
    print(f"Bakedgoods: {m.get('Bakedgoods', '')}")
    print(f"Cheese: {m.get('Cheese', '')}")
    print(f"Crafts: {m.get('Crafts', '')}")
    print(f"Flowers: {m.get('Flowers', '')}")
    print(f"Eggs: {m.get('Eggs', '')}")
    print(f"Seafood: {m.get('Seafood', '')}")
    print(f"Herbs: {m.get('Herbs', '')}")
    print(f"Vegetables: {m.get('Vegetables', '')}")
    print(f"Honey: {m.get('Honey', '')}")
    print(f"Jams: {m.get('Jams', '')}")
    print(f"Maple: {m.get('Maple', '')}")
    print(f"Meat: {m.get('Meat', '')}")
    print(f"Nursery: {m.get('Nursery', '')}")
    print(f"Nuts: {m.get('Nuts', '')}")
    print(f"Plants: {m.get('Plants', '')}")
    print(f"Poultry: {m.get('Poultry', '')}")
    print(f"Prepared: {m.get('Prepared', '')}")
    print(f"Soap: {m.get('Soap', '')}")
    print(f"Trees: {m.get('Trees', '')}")
    print(f"Wine: {m.get('Wine', '')}")
    print(f"Coffee: {m.get('Coffee', '')}")
    print(f"Beans: {m.get('Beans', '')}")
    print(f"Fruits: {m.get('Fruits', '')}")
    print(f"Grains: {m.get('Grains', '')}")
    print(f"Juices: {m.get('Juices', '')}")
    print(f"Mushrooms: {m.get('Mushrooms', '')}")
    print(f"PetFood: {m.get('PetFood', '')}")
    print(f"Tofu: {m.get('Tofu', '')}")
    print(f"WildHarvested: {m.get('WildHarvested', '')}")
    print(f"updateTime: {m.get('updateTime', '')}")
    print("=" * 50)
        
def search_markets(markets, reviews):
    city = input("Enter city name => ").strip().lower()
    print(city)
    state = input("Enter state name => ").strip().lower()
    print(state)

    result = []
    for i in range(len(markets)):
        city_data = markets[i]['city'].lower().strip()
        state_data = markets[i]['State'].lower().strip()
        if city_data == city and state_data == state:
            result.append(markets[i])
            
    if result:
        print(f"Found {len(result)} market(s):")
        for i in range(len(result)):
            m = result[i]
            fmid = m['FMID']
            
            # Считаем средний рейтинг
            if fmid in reviews and reviews[fmid]:
                total = 0
                for r in reviews[fmid]:
                    total += r['rating']
                avg = total / len(reviews[fmid])
                rating_str = f" (Rating: {avg:.1f})"
            else:
                rating_str = ""
            
            print(f"{i+1}. {m['MarketName']} - {m['city']}, {m['State']}{rating_str}")
    else:
        print("Market not found")
        
def search_zip(markets, reviews):
    zipp = input("Enter ZIP Code => ")
    print(zipp)

    result = []
    for i in range(len(markets)):
        if markets[i]['zip'] == zipp:
            result.append(markets[i])
             
    if result:
        print(f"Found {len(result)} market(s):")
        for i in range(len(result)):
            m = result[i]
            fmid = m['FMID']
            
            if fmid in reviews and reviews[fmid]:
                total = 0
                for r in reviews[fmid]:
                    total += r['rating']
                avg = total / len(reviews[fmid])
                rating_str = f" ({avg:.1f} ★)"
            else:
                rating_str = ""
            
            print(f"{i+1}. {m['MarketName']} - {m['city']}, {m['State']}{rating_str}")
    else:
        print("No markets found")

def calc(lat1, lat2, long1, long2):
    lat1 = lat1 * math.pi / 180
    long1 = long1 * math.pi / 180
    lat2 = lat2 * math.pi / 180
    long2 = long2 * math.pi / 180

    dif_lat = lat2 - lat1
    dif_long = long2 - long1

    a = math.sin(dif_lat / 2) ** 2 + math.cos(lat1) * math.cos(lat2) * math.sin(dif_long / 2) ** 2
    c = 2 * math.asin(math.sqrt(a))

    result = 3959.0 * c

    return result
    
def search_dist(markets, reviews):
    lat = float(input("Enter latitude => "))
    print(lat)
    long = float(input("Enter longitude => "))
    print(long)
    r = float(input("Enter radius (miles) => "))
    print(r)
    
    result = []
    for i in range(len(markets)):
        m = markets[i]

        if m['y'] == '' or m['x'] == '':
            continue
        
        lat_market = float(m['y'])
        long_market = float(m['x'])
        dist = calc(lat, lat_market, long, long_market)
        
        if dist <= r:
            result.append((dist, m))
             
    if result:
        result.sort(key=lambda x: x[0])
        print(f"Found {len(result)} market(s):")
        for i in range(len(result)):
            dist, m = result[i]
            fmid = m['FMID']
            
            if fmid in reviews and reviews[fmid]:
                total = 0
                for rev in reviews[fmid]:
                    total += rev['rating']
                avg = total / len(reviews[fmid])
                rating_str = f" ({avg:.1f} ★)"
            else:
                rating_str = ""
            
            print(f"{i+1}. {m['MarketName']} - {m['city']}, {m['State']} ({dist:.1f} miles){rating_str}")
    else:
        print("No markets found")

def add_review(markets, reviews):
    
    list_markets(markets, reviews)
    
    num = int(input("Enter market number => "))
    print(num)
    if not(1 <= num <= len(markets)):
        print("No markets found")
        return
        
    market = markets[num - 1]
    fmid = market['FMID']
    
    user = input("Enter your name => ")
    print(user)
    text = input("Enter your review text => ").strip()
    print(text)
    rating = int(input("Enter rating (1-5) => "))
    print(rating)
        
    if (rating < 1 or rating > 5):
        print("Rating must be between 1 and 5")
        return
       
    review = {
        'user': user,
        'text': text,
        'rating': rating,
    }
      
    if fmid not in reviews:
        reviews[fmid] = []
    reviews[fmid].append(review)
    
    if 'reviews' not in market:
        market['reviews'] = []
    market['reviews'].append(review)
    
    save_reviews(reviews)
    print("Review added successfully!")
    
def show_review(markets, reviews):
    num = int(input("Enter market number => "))
    print(num)
    if not (1 <= num <= len(markets)):
        print("No markets found")
        return
    
    market = markets[num - 1]
    fmid = market['FMID']
    
    if fmid not in reviews or not reviews[fmid]:
        print("No reviews for this market")
        return
    
    print(f"\nReviews for {market['MarketName']}:")
    for i, r in enumerate(reviews[fmid]):
        print(f"{i+1}. User: {r['user']}, Rating: {r['rating']}")
        print(f"   Text: {r['text']}")
                
def sort_markets(markets, reviews):
    print("Sort by: 'name', 'city', 'state', 'rating'")
    key = input("Enter sort key => ").strip().lower()
    print(key)   
    
    if key not in ['name', 'city', 'state', 'rating']:
        print("Invalid sort key")
        return
    
    print("Order: 'asc' (ascending) or 'desc' (descending)")
    order = input("Enter order => ").strip().lower()
    print(order)
    
    if order not in ['asc', 'desc']:
        print("Invalid order")
        return
        
    reverse_order = (order == 'desc')    
    sorted_markets = markets.copy()
    
    if key == 'name':
        sorted_markets.sort(key=lambda m: m['MarketName'].lower(), reverse=reverse_order)
    elif key == 'city':
        sorted_markets.sort(key=lambda m: m['city'].lower(), reverse=reverse_order)
    elif key == 'state':
        sorted_markets.sort(key=lambda m: m['State'].lower(), reverse=reverse_order) 
    elif key == 'rating':
        def avg_rating(m):
            fmid = m['FMID']
            if fmid not in reviews or not reviews[fmid]:
                return 0
            total = 0
            for r in reviews[fmid]:
                total += r['rating']
            return total / len(reviews[fmid])
        sorted_markets.sort(key=avg_rating, reverse=reverse_order)
        
    print(f"\nSorted by {key} ({order}):")
    for i in range(len(sorted_markets)):
        m = sorted_markets[i]
        fmid = m['FMID']
        
        if fmid in reviews and reviews[fmid]:
            total = 0
            for r in reviews[fmid]:
                total += r['rating']
            avg = total / len(reviews[fmid])
            rating_str = f" (avg: {avg:.1f})"
        else:
            rating_str = " (no ratings)"
        
        print(f"{i+1}. {m['MarketName']} - {m['city']}, {m['State']}{rating_str}")       
     
def delete_review(markets, reviews):
    list_markets(markets, reviews)
    
    num = int(input("Enter market number => "))
    print(num)
    if not(1 <= num <= len(markets)):
        print("No markets found")
        return
        
    market = markets[num - 1]
    fmid = market['FMID']
    
    if fmid not in reviews or not reviews[fmid]:
        print("No reviews for this market")
        return 
        
    for i in range(len(reviews[fmid])):
        r = reviews[fmid][i]
        print(f"{i+1}. User: {r['user']}, Rating: {r['rating']} ")
        print(f"Text: {r['text']}")
    
    review_num = int(input("Enter review number to delete => "))
    print(review_num)
    
    if not (1 <= review_num <= len(reviews[fmid])):
        print("Review not found")
        return
    
    review = reviews[fmid][review_num - 1]
    
    user = input("Enter your name to confirm => ").strip()
    print(user)
    
    if review['user'].lower() != user.lower():
        print("You can only delete your own reviews")
        return
    
    del reviews[fmid][review_num - 1]
    if fmid in reviews and reviews[fmid]:
        market['reviews'] = reviews[fmid]
    else:
        market['reviews'] = []
    
    save_reviews(reviews)    
    print("Review deleted successfully!")
        
def main():
    markets = read_init('Export.csv')
    reviews = load_reviews()
    for market in markets:
        fmid = market['FMID']
        if fmid in reviews:
            market['reviews'] = reviews[fmid]
            
    while True:
        comm = input("Command ('list', 'view', 'search', 'zip', 'dist', 'add', 'show', 'del', 'sort', 'end') => ")
        comm = comm.strip().lower()
        print(comm)
        if comm == 'list':
            list_markets(markets,reviews)
        elif comm == 'view':
            view_markets(markets)
        elif comm == 'search':
            search_markets(markets, reviews)
        elif comm == 'zip':
            search_zip(markets, reviews)
        elif comm == 'dist':
            search_dist(markets, reviews)
        elif comm == 'add':
            add_review(markets, reviews)
        elif comm == 'show':
            show_review(markets, reviews)
        elif comm == 'sort':
            sort_markets(markets, reviews)
        elif comm == 'del':
            delete_review(markets, reviews)
        elif comm == 'end':
            save_reviews(reviews)
            print("Done")
            break
        else:
            print("Invalid command, ignoring")
            
if __name__ == '__main__':
    test_markets = read_init('Export.csv')
    assert len(test_markets) > 0
    print(f"Загружено {len(test_markets)} рынков")
    
    test_reviews = load_reviews()
    assert len(test_reviews) >= 0
    print(f"Загружено {len(test_reviews)} рынков с отзывами")
    
    assert 'FMID' in test_markets[0]
    assert 'MarketName' in test_markets[0]
    print("Все поля на месте")

    main()