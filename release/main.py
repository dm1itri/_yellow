import sys

from PyQt5.QtWidgets import QWidget, QApplication, QPushButton, QTableWidgetItem, QTableWidget, QDialog
from sqlite3 import connect
from addEditCoffeeForm import Ui_Dialog


class MyWidget(QDialog, Ui_Dialog):
    def __init__(self, parent=None):
        super().__init__()
        self.setupUi(self)  # Загружаем дизайн
        self.pushButton.clicked.connect(self.run)
        # Обратите внимание: имя элемента такое же как в QTDesigner

    def run(self):
        try:
            data1 = self.tableWidget.item(0, 0).text()
            data2 = self.tableWidget.item(0, 1).text()
            data3 = self.tableWidget.item(0, 2).text()
            data4 = self.tableWidget.item(0, 3).text()
            data5 = self.tableWidget.item(0, 4).text()
            data6 = self.tableWidget.item(0, 5).text()
            data7 = self.tableWidget.item(0, 6).text()

            with connect('data/coffee.sqlite') as conn:
                cur = conn.cursor()
                cur.execute('SELECT * from coff where ID = ?', (data1,)).fetchone()
                if cur.execute('SELECT * from coff where ID = ?', (data1,)).fetchone():
                    cur.execute('''UPDATE coff SET (name, degree_of_roasting, ground_in_grains, taste_description, price, packing_volume) = 
                    (?, ?, ?, ?, ?, ?)  WHERE ID = ?''',
                                (data2, data3, data4, data5, data6, data7, data1))
                else:
                    cur.execute('''INSERT INTO coff VALUES (?, ?, ?, ?, ?, ?, ?)''',
                                (data1, data2, data3, data4, data5, data6, data7))
                    conn.commit()
            self.close()
        except Exception as e:
            print(e)


class Example(QWidget):
    def __init__(self):
        super().__init__()
        self.i()

    def i(self):
        self.resize(650, 500)
        self.setWindowTitle('Капучино')

        # Получим результат запроса,
        # который ввели в текстовое поле
        res = connect(
            'data/coffee.sqlite').cursor().execute('SELECT * from coff').fetchall()
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
            res = connect(
                'data/coffee.sqlite').cursor().execute('SELECT * from coff').fetchall()
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