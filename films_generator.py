from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QApplication, QMainWindow
from PyQt5.QtSql import QSqlDatabase, QSqlQuery, QSqlTableModel
import sqlite3
import sys

if hasattr(QtCore.Qt, 'AA_EnableHighDpiScaling'):
    QtWidgets.QApplication.setAttribute(QtCore.Qt.AA_EnableHighDpiScaling, True)

if hasattr(QtCore.Qt, 'AA_UseHighDpiPixmaps'):
    QtWidgets.QApplication.setAttribute(QtCore.Qt.AA_UseHighDpiPixmaps, True)


class Ui_MainWindow(QMainWindow):
    def setupUi(self, MainWindow):
        super().__init__()
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(511, 331)
        font = QtGui.QFont()
        font.setPointSize(7)
        MainWindow.setFont(font)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.finding = QtWidgets.QTextEdit(self.centralwidget)
        self.finding.setGeometry(QtCore.QRect(10, 10, 171, 41))
        self.finding.setObjectName("finding")
        self.go = QtWidgets.QPushButton(self.centralwidget)
        self.go.setGeometry(QtCore.QRect(200, 30, 81, 21))
        self.go.setObjectName("go")
        self.update_row = QtWidgets.QPushButton(self.centralwidget)
        self.update_row.setGeometry(QtCore.QRect(290, 30, 81, 21))
        self.update_row.setObjectName("update_row")
        self.table = QtWidgets.QTableView(self.centralwidget)
        self.table.setGeometry(QtCore.QRect(10, 60, 491, 251))
        self.table.setObjectName("table")
        MainWindow.setCentralWidget(self.centralwidget)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "Генерация фильмов"))
        self.go.setText(_translate("MainWindow", "Запуск"))
        self.update_row.setText(_translate("MainWindow", "Изменить"))


class Generator(Ui_MainWindow):
    def __init__(self):
        super(Generator, self).setupUi(self)
        con = sqlite3.connect('films_db.sqlite')
        self.cur = con.cursor()
        self.db = QSqlDatabase.addDatabase('QSQLITE')
        self.db.setDatabaseName('films_db.sqlite')
        self.model_films = QSqlTableModel(self)
        self.model_films.select()
        self.table.setModel(self.model_films)
        self.table.setEditTriggers(QtWidgets.QAbstractItemView.EditTrigger.NoEditTriggers)
        self.table.setSelectionMode(QtWidgets.QAbstractItemView.SelectionMode.SingleSelection)
        self.go.clicked.connect(self.going)
        self.update_row.clicked.connect(self.updating)

    def going(self):
        if self.finding.toPlainText():
            self.statusbar.showMessage('')
            sql = QSqlQuery(f'''select * from films where {self.finding.toPlainText()}''', self.db)
            self.model_films.setQuery(sql)
        else:
            self.statusbar.showMessage('Неверное условие поиска')

    def updating(self):
        id_r = self.table.currentIndex().siblingAtColumn(0).data()
        if id_r:
            res = self.cur.execute(f'select * from films where id = {id_r}').fetchall()[0]
            sql = f'''update films set title = "{res[1][::-1]}", year = {res[2] + 1000},
            duration = {res[4] * 2}'''
            self.up = QSqlQuery()
            self.up.exec(sql)
            self.going()


if __name__ == '__main__':
    app = QApplication([])
    form = Generator()
    form.show()
    sys.exit(app.exec())
