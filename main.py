import sys

from PyQt5.QtWidgets import QWidget, QApplication, QPushButton, QTableWidgetItem, QTableWidget
from dialog import MyWidget
from sqlite3 import connect


class Example(QWidget):
    def __init__(self):
        super().__init__()
        self.i()

    def i(self):
        self.resize(650, 500)
        self.setWindowTitle('Капучино')

        # Получим результат запроса,
        # который ввели в текстовое поле
        res = connect('coffee.sqlite').cursor().execute('SELECT * from coff').fetchall()
        # Заполним размеры таблицы
        self.tableWidget = QTableWidget(self)
        self.tableWidget.setColumnCount(7)
        self.tableWidget.setRowCount(len(res))
        self.tableWidget.resize(650, 400)
        self.tableWidget.setHorizontalHeaderLabels(['ID', 'name', 'degree_of_roasting', 'ground_in_grains', 'taste_description', 'price', 'packing_volume'])

        for i, row in enumerate(res):
            for j, elem in enumerate(row):
                self.tableWidget.setItem(i, j, QTableWidgetItem(str(elem)))

        self.pushButton = QPushButton(self)
        self.pushButton.setText('Изменение/Добавление')
        self.pushButton.move(500, 450)
        self.pushButton.clicked.connect(self.run_dialog)

    def run_dialog(self):
        a = MyWidget(parent=self)
        try:
            a.show()
            a.exec_()
            res = connect('coffee.sqlite').cursor().execute('SELECT * from coff').fetchall()
            self.tableWidget.setRowCount(len(res))
            for i, row in enumerate(res):
                for j, elem in enumerate(row):
                    self.tableWidget.setItem(i, j, QTableWidgetItem(str(elem)))
        except Exception as e:
            print(e)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = Example()
    ex.show()
    sys.exit(app.exec())