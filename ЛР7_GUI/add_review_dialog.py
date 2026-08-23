# -*- coding: utf-8 -*-
"""
Created on Fri Aug 14 21:07:02 2026

@author: Анастасия
"""

from PyQt5.QtWidgets import QDialog, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit, QPushButton, QSpinBox

class AddReviewDialog(QDialog):
    def __init__(self, market_name, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Добавить отзыв")
        self.setModal(True)
        self.setMinimumWidth(400)
        
        layout = QVBoxLayout()
        
        # Информация о рынке
        layout.addWidget(QLabel(f"Рынок: {market_name}"))
        
        # Поле для имени пользователя
        layout.addWidget(QLabel("Ваше имя:"))
        self.user_input = QLineEdit()
        layout.addWidget(self.user_input)
        
        # Поле для текста отзыва
        layout.addWidget(QLabel("Текст отзыва:"))
        self.text_input = QLineEdit()
        layout.addWidget(self.text_input)
        
        # Поле для рейтинга (1-5)
        layout.addWidget(QLabel("Рейтинг (1-5):"))
        self.rating_input = QSpinBox()
        self.rating_input.setRange(1, 5)
        layout.addWidget(self.rating_input)
        
        # Кнопки
        btn_layout = QHBoxLayout()
        self.btn_ok = QPushButton("Сохранить")
        self.btn_cancel = QPushButton("Отмена")
        self.btn_ok.clicked.connect(self.accept)
        self.btn_cancel.clicked.connect(self.reject)
        btn_layout.addWidget(self.btn_ok)
        btn_layout.addWidget(self.btn_cancel)
        layout.addLayout(btn_layout)
        
        self.setLayout(layout)
    
    def get_review_data(self):
        return {
            'user': self.user_input.text().strip(),
            'text': self.text_input.text().strip(),
            'rating': self.rating_input.value()
        }