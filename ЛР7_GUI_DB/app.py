# -*- coding: utf-8 -*-
"""
Created on Wed Aug 12 21:39:14 2026

@author: Анастасия
"""
import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QMessageBox, QListWidgetItem, QDialog, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit, QPushButton
from PyQt5.QtCore import Qt
from main_window import Ui_MainWindow
from controller import Controller
from add_review_dialog import AddReviewDialog
from utils.helpers import haversine

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        
        # === ЗАПОЛНЯЕМ ВЫПАДАЮЩИЙ СПИСОК ДЛЯ СОРТИРОВКИ ===
        self.ui.comboSort.addItem("По умолчанию")
        self.ui.comboSort.addItem("По названию (А-Я)")
        self.ui.comboSort.addItem("По названию (Я-А)")
        self.ui.comboSort.addItem("По городу (А-Я)")
        self.ui.comboSort.addItem("По штату (А-Я)")
        self.ui.comboSort.addItem("По рейтингу (сначала высокие)")
        self.ui.comboSort.addItem("По рейтингу (сначала низкие)")
        
        self.controller = Controller()
        self.all_markets = []
        self.current_page = 0
        self.per_page = 10
        self.total_pages = 1
        self.last_coordinates = None
        
        # === ПОДКЛЮЧАЕМ КНОПКИ НАВИГАЦИИ ===
        self.ui.btnFirst.clicked.connect(self.first_page)
        self.ui.btnPrev.clicked.connect(self.prev_page)
        self.ui.btnNext.clicked.connect(self.next_page)
        self.ui.btnLast.clicked.connect(self.last_page)
        self.ui.btnGoTo.clicked.connect(self.go_to_page)
        
        # === ПОДКЛЮЧАЕМ КНОПКИ ДЕЙСТВИЙ ===
        self.ui.btnSearch.clicked.connect(self.search_markets)
        self.ui.btnAdd.clicked.connect(self.add_review)
        self.ui.btnShowReviews.clicked.connect(self.show_reviews)
        self.ui.btnDeleteReview.clicked.connect(self.delete_review)
        self.ui.btnRefresh.clicked.connect(self.load_markets)
        self.ui.btnExit.clicked.connect(self.close)
        
        # === ВЫБИРАЕМ ПО УМОЛЧАНИЮ ПЕРВУЮ РАДИО-КНОПКУ ===
        self.ui.radioNameState.setChecked(True)
        
        # === ДВОЙНОЙ КЛИК ДЛЯ ПРОСМОТРА ПОЛНОЙ ИНФЫ ===
        self.ui.listWidget.itemDoubleClicked.connect(self.show_full_info)
        
        # === ЗАГРУЖАЕМ ДАННЫЕ ===
        self.load_markets()
    
        self.ui.comboSort.currentIndexChanged.connect(self.on_sort_changed)

    def on_sort_changed(self, index):
        criteria = self.ui.comboSort.currentText()
        sort_map = {
            "По умолчанию": None,
            "По названию (А-Я)": "name_asc",
            "По названию (Я-А)": "name_desc",
            "По городу (А-Я)": "city_asc",
            "По штату (А-Я)": "state_asc",
            "По рейтингу (сначала высокие)": "rating_desc",
            "По рейтингу (сначала низкие)": "rating_asc",
        }
        key = sort_map.get(criteria)
        if key:
            self.sort_markets(key)
        
    def load_markets(self):
        self.all_markets = self.controller.get_all_markets()  # ← ЭТО ДОЛЖНО БЫТЬ!
        self.total_pages = max(1, (len(self.all_markets) + self.per_page - 1) // self.per_page)
        self.current_page = 0
        self.update_page_info()
        self.display_markets()
    
    def display_markets(self):
        start = self.current_page * self.per_page
        end = min(start + self.per_page, len(self.all_markets))
        page_markets = self.all_markets[start:end]
        
        self.ui.listWidget.clear()
        for i, market in enumerate(page_markets):
            rating = market.get_rating()
            text = f"{start + i + 1}. {market.name} - {market.city}, {market.state} ({rating:.1f} ★)"
            print(f"DEBUG display_markets: {text}")
            item = QListWidgetItem(text)
            self.ui.listWidget.addItem(item)
        
        self.update_page_info()
    
    def update_page_info(self):
        """Обновляет информацию о странице."""
        self.ui.lblCurrentPage.setText(str(self.current_page + 1))
        self.ui.lblTotalPages.setText(str(self.total_pages))
    
    def first_page(self):
        self.current_page = 0
        self.display_markets()
    
    def last_page(self):
        self.current_page = self.total_pages - 1
        self.display_markets()
    
    def next_page(self):
        if self.current_page < self.total_pages - 1:
            self.current_page += 1
            self.display_markets()
    
    def prev_page(self):
        if self.current_page > 0:
            self.current_page -= 1
            self.display_markets()
    
    def go_to_page(self):
        try:
            page = int(self.ui.lineEditPage.text()) - 1
            if 0 <= page < self.total_pages:
                self.current_page = page
                self.display_markets()
            else:
                QMessageBox.warning(self, "Ошибка", f"Введите номер от 1 до {self.total_pages}")
        except ValueError:
            QMessageBox.warning(self, "Ошибка", "Введите число!")
    
    def search_markets(self):
        try:
            city = self.ui.lineEditCity.text().strip()
            state = self.ui.lineEditState.text().strip()
            zip_code = self.ui.lineEditZip.text().strip()
            radius = None
            
            if self.ui.chkDistance.isChecked():
                radius = float(self.ui.lineEditRadius.text().strip())
            
            if self.ui.radioNameState.isChecked():
                if not city or not state:
                    QMessageBox.warning(self, "Ошибка", "Введите город и штат!")
                    return
                self.all_markets = self.controller.search_markets(city=city, state=state, radius=radius)
            
            elif self.ui.radioZip.isChecked():
                if not zip_code:
                    QMessageBox.warning(self, "Ошибка", "Введите ZIP код!")
                    return
                self.all_markets = self.controller.search_markets(zip_code=zip_code, radius=radius)
            
            else:
                QMessageBox.warning(self, "Ошибка", "Выберите режим поиска!")
                return
            
            self.total_pages = max(1, (len(self.all_markets) + self.per_page - 1) // self.per_page)
            self.current_page = 0
            self.display_markets()
            
            if not self.all_markets:
                QMessageBox.information(self, "Результат", "Рынки не найдены")
                
        except ValueError as e:
            QMessageBox.warning(self, "Ошибка", str(e))
    
    
    def show_reviews(self):
        """Показывает отзывы о выбранном рынке."""
        selected = self.ui.listWidget.currentRow()
        if selected < 0:
            QMessageBox.warning(self, "Ошибка", "Выберите рынок из списка!")
            return
        
        start = self.current_page * self.per_page
        index = start + selected
        if index >= len(self.all_markets):
            return
        market = self.all_markets[index]
        
        reviews = self.controller.get_reviews(market.fmid)
        if not reviews:
            QMessageBox.information(self, "Отзывы", f"Нет отзывов для рынка:\n{market.name}")
            return
        
        text = f" Отзывы для: {market.name}\n\n"
        for i, r in enumerate(reviews):
            text += f"{i+1}. {r.user} - {r.rating} ★\n"
            text += f"   {r.text}\n\n"
        
        QMessageBox.information(self, "Отзывы", text)
        
    def show_full_info(self, item):
        """Показывает полную информацию о рынке в отдельном окне с прокруткой."""
        row = self.ui.listWidget.currentRow()
        if row < 0:
            return
        
        start = self.current_page * self.per_page
        index = start + row
        if index >= len(self.all_markets):
            return
        
        market = self.all_markets[index]
        
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
        
        reviews = self.controller.get_reviews(market.fmid)
        if reviews:
            text += f"\nReviews ({len(reviews)}):\n"
            for i, r in enumerate(reviews):
                text += f"  {i+1}. {r.user} - {r.rating} ★: {r.text}\n"
        else:
            text += "\nNo reviews yet"
        
        from PyQt5.QtWidgets import QTextEdit, QPushButton, QVBoxLayout, QDialog
        
        dialog = QDialog(self)
        dialog.setWindowTitle(f"Информация о рынке: {market.name}")
        dialog.setMinimumWidth(500)
        dialog.setMinimumHeight(400)
        
        layout = QVBoxLayout()
        text_edit = QTextEdit()
        text_edit.setPlainText(text)
        text_edit.setReadOnly(True)
        layout.addWidget(text_edit)
        
        btn_close = QPushButton("Закрыть")
        btn_close.clicked.connect(dialog.accept)
        layout.addWidget(btn_close)
        
        dialog.setLayout(layout)
        dialog.exec_()
    
    def add_review(self):
        """Открывает окно добавления отзыва."""
        selected = self.ui.listWidget.currentRow()
        if selected < 0:
            QMessageBox.warning(self, "Ошибка", "Выберите рынок из списка!")
            return
        
        start = self.current_page * self.per_page
        index = start + selected
        if index >= len(self.all_markets):
            return
        market = self.all_markets[index]
        
        dialog = AddReviewDialog(market.name, self)
        if dialog.exec_():
            data = dialog.get_review_data()
            if not data['user'] or not data['text']:
                QMessageBox.warning(self, "Ошибка", "Заполните все поля!")
                return
            
            self.controller.add_review(market, data['user'], data['text'], data['rating'])
            QMessageBox.information(self, "Успех", "Отзыв добавлен!")
            self.load_markets()

    def delete_review(self):
        """Удаляет выбранный отзыв."""
        selected = self.ui.listWidget.currentRow()
        if selected < 0:
            QMessageBox.warning(self, "Ошибка", "Выберите рынок из списка!")
            return
        
        start = self.current_page * self.per_page
        index = start + selected
        if index >= len(self.all_markets):
            return
        market = self.all_markets[index]
        
        reviews = self.controller.get_reviews(market.fmid)
        if not reviews:
            QMessageBox.information(self, "Отзывы", f"Нет отзывов для рынка:\n{market.name}")
            return
        
        text = f"Выберите отзыв для удаления:\n\n"
        for i, r in enumerate(reviews):
            text += f"{i+1}. {r.user} - {r.rating} ★\n"
            text += f"   {r.text}\n\n"
        
        from PyQt5.QtWidgets import QInputDialog
        num, ok = QInputDialog.getInt(self, "Удаление отзыва", 
                                       text + "\nВведите номер отзыва для удаления:", 
                                       1, 1, len(reviews))
        if not ok:
            return
        
        review_index = num - 1
        review = reviews[review_index]
        
        name, ok = QInputDialog.getText(self, "Подтверждение", 
                                         "Введите ваше имя для подтверждения:")
        if not ok or name.strip() != review.user:
            QMessageBox.warning(self, "Ошибка", "Имена не совпадают! Удаление отменено.")
            return
        
        if self.controller.delete_review(market, review_index, name.strip()):
            QMessageBox.information(self, "Успех", "Отзыв удален!")
            self.load_markets()
        else:
            QMessageBox.warning(self, "Ошибка", "Не удалось удалить отзыв.")
            
    def sort_markets(self, criteria):
        """Сортирует рынки по выбранному критерию."""
        if criteria == "name_asc":
            self.all_markets.sort(key=lambda m: m.name.lower())
        elif criteria == "name_desc":
            self.all_markets.sort(key=lambda m: m.name.lower(), reverse=True)
        elif criteria == "city_asc":
            self.all_markets.sort(key=lambda m: m.city.lower())
        elif criteria == "state_asc":
            self.all_markets.sort(key=lambda m: m.state.lower())
        elif criteria == "rating_desc":
            self.all_markets.sort(key=lambda m: m.get_rating(), reverse=True)
        elif criteria == "rating_asc":
            self.all_markets.sort(key=lambda m: m.get_rating())
        
        self.current_page = 0
        self.display_markets()
        
if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())