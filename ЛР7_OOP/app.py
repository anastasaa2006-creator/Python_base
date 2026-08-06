import sys
import os

# Добавляем корневую папку в путь поиска модулей
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from config import settings
from managers.market_manager import MarketManager
from managers.review_manager import ReviewManager
from utils.helpers import safe_int_input, safe_float_input


class App:
    def __init__(self):
        self.market_manager = MarketManager(settings.DATA_FILE)
        self.review_manager = ReviewManager(settings.REVIEWS_FILE)
        self.running = True

    def run(self):
        while self.running:
            cmd = input("Command ('list', 'view', 'search', 'zip', 'dist', 'add', 'show', 'del', 'sort', 'end') => ").strip().lower()
            print(cmd)

            if cmd == 'list':
                self.cmd_list()
            elif cmd == 'view':
                self.cmd_view()
            elif cmd == 'search':
                self.cmd_search()
            elif cmd == 'zip':
                self.cmd_zip()
            elif cmd == 'dist':
                self.cmd_dist()
            elif cmd == 'add':
                self.cmd_add()
            elif cmd == 'show':
                self.cmd_show()
            elif cmd == 'del':
                self.cmd_delete()
            elif cmd == 'sort':
                self.cmd_sort()
            elif cmd == 'end':
                self.review_manager.save()
                print("Done")
                self.running = False
            else:
                print("Invalid command, ignoring")

    def cmd_list(self):
        markets = self.market_manager.get_all()
        per_page = 5
        total = len(markets)
        total_pages = (total + per_page - 1) // per_page
        page = 1
    
        while True:
            start = (page - 1) * per_page
            end = min(start + per_page, total)
    
            print(f"\n=== Page {page}/{total_pages} ===")
            for i in range(start, end):
                print(markets[i].display_brief(i + 1))
    
            print()
            if total_pages <= 1:
                break
    
            print("Options: (next) (prev) (page N - enter the page number) (back)")
            choice = input("=> ").strip().lower()
    
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

    def cmd_view(self):
        num = safe_int_input("Enter market number => ")
        if num is None:
            return
        m = self.market_manager.get_by_index(num - 1)
        if m:
            m.display_full()
        else:
            print("Market not found")

    def cmd_search(self):
        city = input("Enter city name => ").strip().lower()
        print(city)
        state = input("Enter state name => ").strip().lower()
        print(state)

        result = self.market_manager.search_by_city_state(city, state)
        if result:
            print(f"Found {len(result)} market(s):")
            for i, m in enumerate(result):
                print(m.display_brief(i + 1))
        else:
            print("No markets found")

    def cmd_zip(self):
        zip_code = input("Enter ZIP Code => ").strip()
        print(zip_code)

        result = self.market_manager.search_by_zip(zip_code)
        if result:
            print(f"Found {len(result)} market(s):")
            for i, m in enumerate(result):
                print(m.display_brief(i + 1))
        else:
            print("No markets found")

    def cmd_dist(self):
        lat = safe_float_input("Enter latitude => ")
        print(lat)
        lon = safe_float_input("Enter longitude => ")
        print(lon)
        radius = safe_float_input("Enter radius (miles) => ")
        print(radius)

        result = self.market_manager.search_by_distance(lat, lon, radius)
        if result:
            print(f"Found {len(result)} market(s):")
            for i, (dist, m) in enumerate(result):
                print(f"{i + 1}. {m.name} - {m.city}, {m.state} ({dist:.1f} miles)")
        else:
            print("No markets found")

    def cmd_add(self):
        self.cmd_list()

        num = safe_int_input("Enter market number => ")
        if num is None:
            return
        m = self.market_manager.get_by_index(num - 1)
        if not m:
            print("Market not found")
            return

        user = input("Enter your name => ")
        print(user)
        text = input("Enter your review text => ").strip()
        print(text)
        rating = safe_int_input("Enter rating (1-5) => ")
        print(rating)

        if rating < 1 or rating > 5:
            print("Rating must be between 1 and 5")
            return

        self.review_manager.add(m, user, text, rating)
        print("Review added successfully!")

    def cmd_show(self):
        num = safe_int_input("Enter market number => ")
        if num is None:
            return
        m = self.market_manager.get_by_index(num - 1)
        if not m:
            print("Market not found")
            return

        reviews = self.review_manager.get(m.fmid)
        if not reviews:
            print("No reviews for this market")
            return

        print(f"\nReviews for {m.name}:")
        for i, r in enumerate(reviews):
            print(f"{i + 1}. User: {r.user}, Rating: {r.rating} ★")
            print(f"   Text: {r.text}")

    def cmd_delete(self):
        self.cmd_list()

        num = safe_int_input("Enter market number => ")
        if num is None:
            return
        m = self.market_manager.get_by_index(num - 1)
        if not m:
            print("Market not found")
            return

        reviews = self.review_manager.get(m.fmid)
        if not reviews:
            print("No reviews for this market")
            return

        for i, r in enumerate(reviews):
            print(f"{i + 1}. User: {r.user}, Rating: {r.rating} ★")
            print(f"   Text: {r.text}")

        review_num = safe_int_input("Enter review number to delete => ")
        if review_num is None:
            return

        if review_num < 1 or review_num > len(reviews):
            print("Review not found")
            return

        user = input("Enter your name to confirm => ").strip()
        print(user)

        if self.review_manager.delete(m, review_num - 1, user):
            print("Review deleted successfully!")
        else:
            print("You can only delete your own reviews")

    def cmd_sort(self):
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

        self.market_manager.sort(key, reverse=(order == 'desc'))
        self.cmd_list()


if __name__ == '__main__':
    app = App()
    app.run()