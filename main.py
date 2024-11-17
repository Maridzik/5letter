import sys

from PyQt6.QtWidgets import QApplication, QWidget, QVBoxLayout, QHBoxLayout, QLineEdit,QTableWidgetItem, QComboBox, QLabel, QPushButton, QTableWidget

import sqlite3

class  MyWidget(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        hlayout = QHBoxLayout()
        vlayout1 = QVBoxLayout()

        self.combobox = QComboBox()
        self.pushbutton = QPushButton("пуск")
        self.pushbutton.clicked.connect(self.find_films)

        self.tablewidget = QTableWidget()

        vlayout1.addWidget(self.combobox)
        vlayout1.addWidget(self.pushbutton)
        hlayout.addLayout(vlayout1)
        hlayout.addWidget(self.tablewidget)

        self.setLayout(hlayout)
        self.genres_set()

    def genres_set(self):
        con = sqlite3.connect("genre_filter/films_db.sqlite")
        cursor = con.cursor()
        genres = cursor.execute('''SELECT title from genres''').fetchall()
        for g in genres:
            self.combobox.addItem(g[0])
        con.close()

    def find_films(self):
        con = sqlite3.connect("genre_filter/films_db.sqlite")
        cursor = con.cursor()
        genre = cursor.execute('''SELECT id from genres WHERE title = ? ''', (self.combobox.currentText(),)).fetchone()
        genre_id = genre[0]

        films = cursor.execute('''SELECT title, genre, year from films WHERE genre = ? ''', (genre_id,)).fetchall()

        self.tablewidget.setColumnCount(len(films[0]))
        self.tablewidget.setRowCount(len(films))
        self.tablewidget.setHorizontalHeaderLabels(['Название', 'Жанр', 'Год'])
        for i, row in enumerate(films):
            for j, elem in enumerate(row):
                self.tablewidget.setItem(i, j, QTableWidgetItem(str(elem)))        
            



def main():
    app = QApplication(sys.argv)
    ex = MyWidget()
    ex.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()