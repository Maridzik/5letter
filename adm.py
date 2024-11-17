import sys
from PyQt6.QtWidgets import(
    QApplication, QPushButton, QVBoxLayout, QWidget, QTableWidget, QTableWidgetItem, QLineEdit, QComboBox
)

import sqlite3


class WordleGame(QWidget):
    def __init__(self):
        super().__init__()

        self.main_layout = QVBoxLayout()

        self.table_widget = QTableWidget()

        self.line_edit = QLineEdit()
        self.line_edit.setText("Введите слово")

        self.combobox = QComboBox()
        self.combobox.addItems(["Удалить", "Добавить"])

        self.pushbutton = QPushButton("Выполнить")
        self.pushbutton.clicked.connect(self.do)

        self.setup_bd()
        
        self.main_layout.addWidget(self.combobox)
        self.main_layout.addWidget(self.line_edit)
        self.main_layout.addWidget(self.pushbutton)
        self.main_layout.addWidget(self.table_widget)
        self.setLayout(self.main_layout)


    def setup_bd(self) -> list:
        con = sqlite3.connect("words.sqlite")

        cursor = con.cursor()

        self.words = cursor.execute('''SELECT word from words ''').fetchall()

        con.close()

        self.setup_table()

    def setup_table(self):
        for i, row in enumerate(self.words):
            self.table_widget.setRowCount(len(self.words))
            self.table_widget.setColumnCount(len(row))
            for j, col in enumerate(row):
                    self.table_widget.setItem(i, j, QTableWidgetItem(str(col)))

    def do(self):
        word = self.line_edit.text()

        con = sqlite3.connect("words.sqlite")

        cursor = con.cursor()

        if self.combobox.currentText() == "Удалить":
            cursor.execute('''DELETE from words WHERE word = ?''', (word,)).fetchall()
        elif self.combobox.currentText() == "Добавить":
            if len(word) == 5:
                cursor.execute("INSERT INTO words (word) VALUES (?)", (word,))
                print(f"{word} добавлено")

        cursor.execute('''UPDATE words SET id = rowid''')
            

        con.commit()
        con.close()

        self.setup_bd()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    game = WordleGame()
    game.show()
    sys.exit(app.exec())
