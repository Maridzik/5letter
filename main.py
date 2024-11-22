import sys

from PyQt6.QtWidgets import QApplication, QPushButton, QVBoxLayout, QWidget, QLabel, QHBoxLayout, QLineEdit
from PyQt6.QtGui import QFont
from PyQt6.QtCore import QRect
from random import choice

import sqlite3


class win(QWidget):
    def __init__(self, word: str, text: str, attempts: int = 5):
        super().__init__()

        self.setWindowTitle("Окончание Игры")
        self.resize(400, 200)

        font = QFont("Arial", 24, QFont.Weight.Bold)
        font2 = QFont("Arial", 16)

        self.main_layout = QVBoxLayout()
        self.label1 = QLabel()
        self.label2 = QLabel()
        self.label3 = QLabel()

        # Отображение текста результата
        self.label1.setText(text)
        self.label1.setFont(font)

        if text == "Вы победили":
            self.label1.setStyleSheet("color: green;")
        if text == "Вы проиграли":
            self.label1.setStyleSheet("color: red;")

        self.label2.setText(f"Загаданное слово было: {word}")
        self.label2.setFont(font)

        self.label3.setText(f"попыток: {attempts}")
        self.label3.setFont(font2)

        self.main_layout.addWidget(self.label1)
        self.main_layout.addWidget(self.label2)
        self.main_layout.addWidget(self.label3)

        self.setLayout(self.main_layout)


class WordleGame(QWidget):
    def __init__(self):
        super().__init__()
        self.attempts = 0
        self.res_word = ""
        self.setFixedSize(600, 600)
        self.setWindowTitle("Угадай слово")
        self.init_ui()

    def init_ui(self):
        self.main_layout = QVBoxLayout(self)
        self.layouts = [QHBoxLayout() for _ in range(5)]

        # Создание ячеек для ввода букв слова
        for i in range(25):
            label = QLabel(self)
            label.setGeometry(QRect(80, 20, 61, 61))
            label.setStyleSheet("border: 1px solid black; font-size: 32px;")
            label.setText("")
            label.setObjectName(f"label_{i+1}")
            self.layouts[i // 5].addWidget(label)

        for layout in self.layouts:
            self.main_layout.addLayout(layout)

        self.set_res_word()

        self.pushButton = QPushButton("Enter")
        self.pushButton.setFixedSize(600, 100)
        self.pushButton.clicked.connect(self.set_word)

        self.lineEdit = QLineEdit()

        self.main_layout.addWidget(self.lineEdit)
        self.main_layout.addWidget(self.pushButton)
        self.setLayout(self.main_layout)

    # Установка загаданного слова из базы данных
    def set_res_word(self):
        con = sqlite3.connect("words.sqlite")
        cursor = con.cursor()
        self.words = cursor.execute('''SELECT word from words''').fetchall()
        self.words = [word[0] for word in self.words]
        self.res_word = choice(self.words)
        print(self.res_word)

    # Обработка ввода слова пользователем
    def set_word(self):
        if self.attempts < 5:
            self.word = self.lineEdit.text().lower()
            layout = self.layouts[int(self.attempts)]
            self.attempts += 1
            self.check_word(layout)

    # Проверка введенного слова
    def check_word(self, layout):
        res_word_copy = list(self.res_word)

        for i in range(layout.count()):
            item = layout.itemAt(i).widget()
            if item is not None:
                item.setText(self.word[i])
                if self.word[i] == self.res_word[i]:
                    # Если буква на правильном месте, меняем цвет фона на зелёный
                    item.setStyleSheet("border: 1px solid black; font-size: 32px; background-color: green;")
                    res_word_copy[i] = None  # если буква есть ставим None

        for i in range(layout.count()):
            item = layout.itemAt(i).widget()
            if item is not None and self.word[i] != self.res_word[i]:
                if self.word[i] in res_word_copy:
                    # Если буква есть в загаданном слове, но на другой позиции, меняем цвет фона на жёлтый
                    item.setStyleSheet("border: 1px solid black; font-size: 32px; background-color: yellow;")
                    res_word_copy[res_word_copy.index(self.word[i])] = None  


        if self.word == self.res_word:
            self.hide()
            self.win_window = win(self.res_word, "Вы победили", self.attempts)
            self.win_window.show()

        elif self.attempts == 5:
            self.hide()
            self.win_window = win(self.res_word, "Вы проиграли")
            self.win_window.show()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    game = WordleGame()
    game.show()
    sys.exit(app.exec())
