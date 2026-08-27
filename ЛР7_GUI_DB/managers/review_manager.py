import json
from models.review import Review

class ReviewManager:
    def __init__(self, filename='reviews.json'):
        self.filename = filename
        self.reviews = {}
        self.load()

    def load(self):
        try:
            with open(self.filename, 'r', encoding='utf-8') as f:
                data = json.load(f)
                for fmid, revs in data.items():
                    self.reviews[int(fmid)] = [Review(r['user'], r['text'], r['rating']) for r in revs]
        except FileNotFoundError:
            self.reviews = {}

    def save(self):
        data = {}
        for fmid, revs in self.reviews.items():
            data[fmid] = [r.to_dict() for r in revs]
        with open(self.filename, 'w') as f:
            json.dump(data, f, indent=2, ensure_ascii=False)

    def add(self, market, user, text, rating):
        if market.fmid not in self.reviews:
            self.reviews[market.fmid] = []
        review = Review(user, text, rating)
        self.reviews[market.fmid].append(review)
        market.reviews = self.reviews[market.fmid]
        self.save()

    def get(self, fmid):
        return self.reviews.get(fmid, [])

    def delete(self, market, index, user):
        if market.fmid not in self.reviews:
            return False
        if index < 0 or index >= len(self.reviews[market.fmid]):
            return False
        if self.reviews[market.fmid][index].user.lower() != user.lower():
            return False
        del self.reviews[market.fmid][index]
        market.reviews = self.reviews.get(market.fmid, [])
        self.save()
        return True