import csv
import math

markets = [
    {
        'FMID': '1018261',
        'MarketName': 'Caledonia Farmers Market',
        'city': 'Danville',
        'State': 'Vermont',
        'zip': '05828',
        'x': -72.140337,
        'y': 44.411036
    },
    {
        'FMID': '1009994',
        'MarketName': "18th Street Farmer's Market",
        'city': 'Scottsbluff',
        'State': 'Nebraska',
        'zip': '69361',
        'x': -103.662538,
        'y': 41.864268
    },
    {
        'FMID': '1000709',
        'MarketName': "26th Annual Highlands Business Partnership's Farmers Market",
        'city': 'Highlands',
        'State': 'New Jersey',
        'zip': '07732',
        'x': -73.994358,
        'y': 40.404837
    }
]

# def read_init(filename):
    # with open(filename, 'r') as f:
        # lines = f.readlines()
    
    # headers = lines[0].strip().split(',')
    # markets = []

    # for line in lines[1:]:
        # if not line.strip():
            # continue
         
        # values = line.strip().split(',')
        
        
        # market = {}
        # for i in range(len(headers)):
            # market[headers[i]] = values[i]
        # markets.append(market)
            
    # return markets


def list_markets(markets):
    for i in range(len(markets)):
        m = markets[i]
        print(f"{i+1}. {m['MarketName']} - {m['city']}, {m['State']}")
    print()
    

def view_markets(markets):
    num = int(input("Enter market number => "))
    print(num)
    if (1 <= num <= len(markets)):
        m = markets[num-1]
        print(f"FMID: {m['FMID']}")
        print(f"Name: {m['MarketName']}")
        print(f"City: {m['city']}")
        print(f"State: {m['State']}")
        print(f"ZIP: {m['zip']}")
        print(f"Coordinates: ({m['y']}, {m['x']})")
    else:
        print("Market not found")
        
def search_markets(markets):
    city = input("Enter city name => ").strip().lower()
    print(city)
    state = input("Enter state name => ").strip().lower()
    print(state)

    result = []
    for i in range(len(markets)):
        if (markets[i]['city'].lower() == city and markets[i]['State'].lower() == state):
            result.append(markets[i])
            
            
    if (result):
        print(f"Found {len(result)} market(s):")
        for i in range(len(result)):
            m = result[i]
            print(f"{i+1}. {m['MarketName']} - {m['city']}, {m['State']}")
        
    else:
        print("Market not found")
        
def search_zip(markets):
    zipp = input("Enter ZIP Code => ")
    print(zipp)

    result = []
    for i in range(len(markets)):
        if (markets[i]['zip'] == zipp):
            result.append(markets[i])
             
    if (result):
        print(f"Found {len(result)} market(s):")
        for i in range(len(result)):
            m = result[i]
            print(f"{i+1}. {m['MarketName']} - {m['city']}, {m['State']}")
        
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
    
def search_dist(markets):
    lat = float(input("Enter latitude => "))
    print(lat)
    long = float(input("Enter longitude => "))
    print(long)
    r = float(input("Enter radius (miles) => "))
    print(r)
    
    result = []
    for i in range(len(markets)):
        m = markets[i]
        dist = calc(lat,m['y'],long,m['x'])
        if dist <= r:
            result.append((dist,m))
             
    if (result):
        print(f"Found {len(result)} market(s):")
        for i in range(len(result)):
            dist, m = result[i]
            print(f"{i+1}. {m['MarketName']} - {m['city']}, {m['State']} ({dist:.1f} miles)")
        
    else:
        print("No markets found")    

def add_review(markets):
    
    list_markets(markets)
    
    num = int(input("Enter market number => "))
    print(num)
    if not(1 <= num <= len(markets)):
        print("No markets found")
        return
        
    market = markets[num - 1]
    
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
    
    if 'review' not in markets:
        markets['review'] = []
        
    markets['review'].append(review)
    print("Review added successfully!")
    
def show_review(markets):
    num = int(input("Enter market number => "))
    print(num)
    if not(1 <= num <= len(markets)):
        print("No markets found")
        return
        
    market = markets[num - 1]
    
    if 'reviews' not in market or not market['reviews']:
        print("No reviews for this market")
        return   
        
    for i in range(len(markets['reviews'])):
        r = market['reviews'][i]
        print(f"{i+1}. User: {r['user']}, Rating: {r['rating']}")
        print(f"   Text: {r['text']}")
        
def sort_markets(markets):
        # print("Sort by: 'name', 'city', 'state', 'rating'")
        # key = input("Enter sort key => ").strip().lower()
        # print(key)   
        
        # if key not in ['name', 'city', 'state', 'rating']:
        # print("Invalid sort key")
        # return
        
        # print("Order: 'asc' (ascending) or 'desc' (descending)")
        # order = input("Enter order => ").strip().lower()
        # print(order)
        
        # if order not in ['asc', 'desc']:
            # print("Invalid order")
            # return
        pass
        
        
def main():
    #markets = read_init('input_7.txt')
    while True:
        comm = input("Command ('list', 'view', 'search', 'zip', 'dist', 'add', 'show', 'sort', 'end') => ")
        comm = comm.strip().lower()
        print(comm)
        match comm:
            case 'list':
                list_markets(markets)
            case 'view':
                view_markets(markets)
            case 'search':
                search_markets(markets)
            case 'zip':
                search_zip(markets)
            case 'dist':
                search_dist(markets)
            case 'add':
                add_review(markets)
            case 'show':
                show_review(markets)
            case 'sort':
                sort_markets(markets)
            case 'end':
                print("Done")
                break
            case _ :
                print("Invalid command, ignoring")
            
if __name__ == '__main__':
    main()