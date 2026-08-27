class Review:
    """Класс для хранения одного отзыва."""
    def __init__(self, user, text, rating):
        self.user = user
        self.text = text
        self.rating = rating

    def to_dict(self):
        return {'user': self.user, 'text': self.text, 'rating': self.rating}

    def __str__(self):
        return f"Review(user='{self.user}', rating={self.rating}, text='{self.text[:20]}...')"