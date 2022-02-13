import sys
from PyQt5 import uic  # Импортируем uic
from PyQt5.QtWidgets import QApplication, QDialog
from sqlite3 import connect


class MyWidget(QDialog):
    def __init__(self, parent=None):
        super().__init__()
        uic.loadUi('addEditCoffeeForm.ui', self)  # Загружаем дизайн
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

            with connect('coffee.sqlite') as conn:
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
            # Имя элемента совпадает с objectName в QTDesigner


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = MyWidget()
    ex.show()
    sys.exit(app.exec_())