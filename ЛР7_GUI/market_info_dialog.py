# -*- coding: utf-8 -*-
from PyQt5.QtWidgets import QDialog, QVBoxLayout, QTextEdit, QPushButton

class MarketInfoDialog(QDialog):
    def __init__(self, market, reviews, parent=None):
        super().__init__(parent)
        self.setWindowTitle(f"Информация о рынке: {market.name}")
        self.setMinimumWidth(500)
        self.setMinimumHeight(400)
        
        text = self._build_text(market, reviews)
        
        layout = QVBoxLayout()
        text_edit = QTextEdit()
        text_edit.setPlainText(text)
        text_edit.setReadOnly(True)
        layout.addWidget(text_edit)
        
        btn_close = QPushButton("Закрыть")
        btn_close.clicked.connect(self.accept)
        layout.addWidget(btn_close)
        
        self.setLayout(layout)
    
    def _build_text(self, market, reviews):
        """Формирует текст с информацией о рынке."""
        text = (
            f"FMID: {market.fmid}\n"
            f"Name: {market.name}\n"
            f"Website: {market.website}\n"
            f"Facebook: {market.facebook}\n"
            f"Twitter: {market.twitter}\n"
            f"Youtube: {market.youtube}\n"
            f"OtherMedia: {market.other_media}\n"
            f"Street: {market.street}\n"
            f"City: {market.city}\n"
            f"County: {market.county}\n"
            f"State: {market.state}\n"
            f"ZIP: {market.zip}\n"
            f"Season1Date: {market.season1_date}\n"
            f"Season1Time: {market.season1_time}\n"
            f"Season2Date: {market.season2_date}\n"
            f"Season2Time: {market.season2_time}\n"
            f"Season3Date: {market.season3_date}\n"
            f"Season3Time: {market.season3_time}\n"
            f"Season4Date: {market.season4_date}\n"
            f"Season4Time: {market.season4_time}\n"
            f"Coordinates: ({market.lat}, {market.lon})\n"
            f"Location: {market.location}\n"
            f"Rating: {market.get_rating():.1f} ★\n"
        )
        
        # Категории
        categories = []
        if market.organic == 'Y': categories.append('Organic')
        if market.baked_goods == 'Y': categories.append('Baked Goods')
        if market.cheese == 'Y': categories.append('Cheese')
        if market.crafts == 'Y': categories.append('Crafts')
        if market.flowers == 'Y': categories.append('Flowers')
        if market.eggs == 'Y': categories.append('Eggs')
        if market.seafood == 'Y': categories.append('Seafood')
        if market.herbs == 'Y': categories.append('Herbs')
        if market.vegetables == 'Y': categories.append('Vegetables')
        if market.honey == 'Y': categories.append('Honey')
        if market.jams == 'Y': categories.append('Jams')
        if market.maple == 'Y': categories.append('Maple')
        if market.meat == 'Y': categories.append('Meat')
        if market.nuts == 'Y': categories.append('Nuts')
        if market.plants == 'Y': categories.append('Plants')
        if market.poultry == 'Y': categories.append('Poultry')
        if market.prepared == 'Y': categories.append('Prepared Food')
        if market.soap == 'Y': categories.append('Soap')
        if market.wine == 'Y': categories.append('Wine')
        if market.coffee == 'Y': categories.append('Coffee')
        if market.fruits == 'Y': categories.append('Fruits')
        if market.tofu == 'Y': categories.append('Tofu')
        
        text += f"Categories: {', '.join(categories) if categories else 'Not specified'}\n"
        
        # Отзывы
        if reviews:
            text += f"\nReviews ({len(reviews)}):\n"
            for i, r in enumerate(reviews):
                text += f"  {i+1}. {r.user} - {r.rating} ★: {r.text}\n"
        else:
            text += "\nNo reviews yet"
        
        return text