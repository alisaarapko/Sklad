import sys
import sqlite3
import hashlib
from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QVBoxLayout, QWidget, QPushButton,
    QLineEdit, QLabel, QMessageBox, QTableWidget, QHBoxLayout, QTableWidgetItem
)

from database import MainApp  # Импортируем класс MainApp из файла db.py

def create_connection():
    try:
        conn = sqlite3.connect('warehouse.db')
        return conn
    except sqlite3.Error as e:
        print(f"Ошибка при подключении к базе данных: {e}")
        return None

def create_tables():
    conn = create_connection()
    if conn is None:
        return

    cursor = conn.cursor()

    # Создание таблиц
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL
        )
    ''')

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS Products (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            price REAL NOT NULL,
            quantity INTEGER NOT NULL
        )
    ''')

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS Deliveries (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            delivery_date TEXT NOT NULL,
            supplier TEXT NOT NULL,
            status TEXT NOT NULL,
            article TEXT NOT NULL,
            name TEXT NOT NULL,
            description TEXT NOT NULL,
            quantity INTEGER NOT NULL,
            storage_area TEXT NOT NULL
        )
    ''')

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS Shipments (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            shipment_date TEXT NOT NULL,
            customer TEXT NOT NULL,
            status TEXT NOT NULL,
            product_id INTEGER,
            quantity INTEGER NOT NULL,
            FOREIGN KEY (product_id) REFERENCES Products (id)
        )
    ''')

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS Reports (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            report_date TEXT NOT NULL,
            description TEXT NOT NULL
        )
    ''')

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS Suppliers (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            contact_info TEXT NOT NULL
        )
    ''')

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS Warehouses (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            location TEXT NOT NULL,
            capacity INTEGER NOT NULL
        )
    ''')

    conn.commit()
    conn.close()

class LoginWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Вход в систему")
        self.setFixedSize(300, 200)

        self.layout = QVBoxLayout()
        self.label_username = QLabel("Логин:")
        self.layout.addWidget(self.label_username)

        self.input_username = QLineEdit()
        self.layout.addWidget(self.input_username)

        self.label_password = QLabel("Пароль:")
        self.layout.addWidget(self.label_password)

        self.input_password = QLineEdit()
        self.input_password.setEchoMode(QLineEdit.EchoMode.Password)
        self.layout.addWidget(self.input_password)

        button_layout = QHBoxLayout()
        self.button_login = QPushButton("Войти")
        self.button_login.setStyleSheet("background-color: #badbad;")
        self.button_login.clicked.connect(self.login)
        button_layout.addWidget(self.button_login)

        self.button_register = QPushButton("Регистрация")
        self.button_register.setStyleSheet("background-color: #badbad;")
        self.button_register.clicked.connect(self.register)
        button_layout.addWidget(self.button_register)

        self.layout.addLayout(button_layout)
        container = QWidget()
        container.setLayout(self.layout)
        self.setCentralWidget(container)

    def hash_password(self, password):
        return hashlib.sha256(password.encode()).hexdigest()

    def login(self):
        username = self.input_username.text()
        password = self.input_password.text()

        conn = create_connection()
        if conn is None:
            QMessageBox.critical(self, "Ошибка", "Не удалось подключиться к базе данных.")
            return

        cursor = conn.cursor()
        cursor.execute("SELECT * FROM users WHERE username=? AND password=?", (username, self.hash_password(password)))
        user = cursor.fetchone()
        conn.close()

        if user:
            self.open_main_window()
        else:
            QMessageBox.warning(self, "Ошибка", "Неверный логин или пароль.")

    def open_main_window(self):
        self.main_window = MainWindow()
        self.main_window.show()
        self.close()

    def register(self):
        username = self.input_username.text()
        password = self.input_password.text()

        if len(password) < 8:
            QMessageBox.warning(self, "Ошибка", "Пароль должен содержать не менее 8 символов.")
            return

        conn = create_connection()
        if conn is None:
            QMessageBox.critical(self, "Ошибка", "Не удалось подключиться к базе данных.")
            return

        cursor = conn.cursor()
        try:
            cursor.execute("INSERT INTO users (username, password) VALUES (?, ?)",
                           (username, self.hash_password(password)))
            conn.commit()
            QMessageBox.information(self, "Успех", "Регистрация прошла успешно!")
        except sqlite3.IntegrityError:
            QMessageBox.warning(self, "Ошибка", "Пользователь с таким именем уже существует.")
        finally:
            conn.close()

class MainWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Склад")
        self.setFixedSize(700, 500)

        button_layout = QHBoxLayout()

        self.button_add = QPushButton(" + Добавить")
        self.button_add.setStyleSheet("background-color: #d6ced5; font-size: 14px;")
        self.button_add.clicked.connect(self.open_database_selection)
        button_layout.addWidget(self.button_add)


        self.button_deliveries = QPushButton("Поставки")
        self.button_deliveries.setStyleSheet("background-color: #badbad; font-size: 14px;")
        self.button_deliveries.clicked.connect(self.show_deliveries)
        button_layout.addWidget(self.button_deliveries)

        self.button_shipments = QPushButton("Отгрузки")
        self.button_shipments.setStyleSheet("background-color: #badbad; font-size: 14px;")
        self.button_shipments.clicked.connect(self.show_shipments)
        button_layout.addWidget(self.button_shipments)

        self.button_reports = QPushButton("Отчеты")
        self.button_reports.setStyleSheet("background-color: #badbad; font-size: 14px;")
        self.button_reports.clicked.connect(self.show_reports)
        button_layout.addWidget(self.button_reports)

        self.button_suppliers = QPushButton("Поставщики")
        self.button_suppliers.setStyleSheet("background-color: #badbad; font-size: 14px;")
        self.button_suppliers.clicked.connect(self.show_suppliers)
        button_layout.addWidget(self.button_suppliers)

        self.button_warehouses = QPushButton("Склады")
        self.button_warehouses.setStyleSheet("background-color: #badbad; font-size: 14px;")
        self.button_warehouses.clicked.connect(self.show_warehouses)
        button_layout.addWidget(self.button_warehouses)


        self.main_layout = QVBoxLayout()
        self.main_layout.addLayout(button_layout)

        self.content_area = QVBoxLayout()
        self.main_layout.addLayout(self.content_area)

        self.setLayout(self.main_layout)

    def open_database_selection(self):
        self.database_selection_window = MainApp()
        self.database_selection_window.show()

    def clear_content(self):
        for i in reversed(range(self.content_area.count())):
            widget = self.content_area.itemAt(i).widget()
            if widget is not None:
                widget.deleteLater()

    def show_deliveries(self):
        self.clear_content()
        title_label = QLabel('Поставки')
        title_label.setStyleSheet("font-size: 32px; font-weight: bold;")
        self.content_area.addWidget(title_label)

        self.deliveries_table = QTableWidget(self)
        self.deliveries_table.setColumnCount(9)
        self.deliveries_table.setHorizontalHeaderLabels(
            ["ID", "Дата поставки", "Поставщик", "Статус", "Артикул", "Название", "Описание", "Количество", "Зона хранения"])
        self.content_area.addWidget(self.deliveries_table)

        self.load_deliveries()

        back_button = QPushButton("Назад")
        back_button.setStyleSheet("background-color: #d6ced5; font-size: 14px;")
        back_button.clicked.connect(self.clear_content)
        self.content_area.addWidget(back_button)

    def load_deliveries(self):
        conn = create_connection()
        if conn is None:
            QMessageBox.critical(self, "Ошибка", "Не удалось подключиться к базе данных.")
            return

        cursor = conn.cursor()
        cursor.execute("SELECT * FROM Deliveries")
        deliveries = cursor.fetchall()
        conn.close()

        self.deliveries_table.setRowCount(len(deliveries))
        for row_index, row_data in enumerate(deliveries):
            for column_index, value in enumerate(row_data):
                self.deliveries_table.setItem(row_index, column_index, QTableWidgetItem(str(value)))

    def show_shipments(self):
        self.clear_content()
        title_label = QLabel('Отгрузки')
        title_label.setStyleSheet("font-size: 32px; font-weight: bold;")
        self.content_area.addWidget(title_label)

        self.shipments_table = QTableWidget(self)
        self.shipments_table.setColumnCount(6)
        self.shipments_table.setHorizontalHeaderLabels(
            ["ID", "Дата отгрузки", "Клиент", "Статус", "ID продукта", "Количество"])
        self.content_area.addWidget(self.shipments_table)

        self.load_shipments()

        back_button = QPushButton("Назад")
        back_button.setStyleSheet("background-color: #d6ced5; font-size: 14px;")
        back_button.clicked.connect(self.clear_content)
        self.content_area.addWidget(back_button)

    def load_shipments(self):
        conn = create_connection()
        if conn is None:
            QMessageBox.critical(self, "Ошибка", "Не удалось подключиться к базе данных.")
            return

        cursor = conn.cursor()
        cursor.execute("SELECT * FROM Shipments")
        shipments = cursor.fetchall()
        conn.close()

        self.shipments_table.setRowCount(len(shipments))
        for row_index, row_data in enumerate(shipments):
            for column_index, value in enumerate(row_data):
                self.shipments_table.setItem(row_index, column_index, QTableWidgetItem(str(value)))

    def show_reports(self):
        self.clear_content()
        title_label = QLabel('Отчеты')
        title_label.setStyleSheet("font-size: 32px; font-weight: bold;")
        self.content_area.addWidget(title_label)

        self.reports_table = QTableWidget(self)
        self.reports_table.setColumnCount(3)
        self.reports_table.setHorizontalHeaderLabels(
            ["ID", "Дата отчета", "Описание"])
        self.content_area.addWidget(self.reports_table)

        self.load_reports()

        back_button = QPushButton("Назад")
        back_button.setStyleSheet("background-color: #d6ced5; font-size: 14px;")
        back_button.clicked.connect(self.clear_content)
        self.content_area.addWidget(back_button)

    def load_reports(self):
        conn = create_connection()
        if conn is None:
            QMessageBox.critical(self, "Ошибка", "Не удалось подключиться к базе данных.")
            return

        cursor = conn.cursor()
        cursor.execute("SELECT * FROM Reports")
        reports = cursor.fetchall()
        conn.close()

        self.reports_table.setRowCount(len(reports))
        for row_index, row_data in enumerate(reports):
            for column_index, value in enumerate(row_data):
                self.reports_table.setItem(row_index, column_index, QTableWidgetItem(str(value)))

    def show_suppliers(self):
        self.clear_content()
        title_label = QLabel('Поставщики')
        title_label.setStyleSheet("font-size: 32px; font-weight: bold;")
        self.content_area.addWidget(title_label)

        self.suppliers_table = QTableWidget(self)
        self.suppliers_table.setColumnCount(3)
        self.suppliers_table.setHorizontalHeaderLabels(
            ["ID", "Имя", "Контактная информация"])
        self.content_area.addWidget(self.suppliers_table)

        self.load_suppliers()

        back_button = QPushButton("Назад")
        back_button.setStyleSheet("background-color: #d6ced5; font-size: 14px;")
        back_button.clicked.connect(self.clear_content)
        self.content_area.addWidget(back_button)

    def load_suppliers(self):
        conn = create_connection()
        if conn is None:
            QMessageBox.critical(self, "Ошибка", "Не удалось подключиться к базе данных.")
            return

        cursor = conn.cursor()
        cursor.execute("SELECT * FROM Suppliers")
        suppliers = cursor.fetchall()
        conn.close()

        self.suppliers_table.setRowCount(len(suppliers))
        for row_index, row_data in enumerate(suppliers):
            for column_index, value in enumerate(row_data):
                self.suppliers_table.setItem(row_index, column_index, QTableWidgetItem(str(value)))

    def show_warehouses(self):
        self.clear_content()
        title_label = QLabel('Склады')
        title_label.setStyleSheet("font-size: 32px; font-weight: bold;")
        self.content_area.addWidget(title_label)

        self.warehouses_table = QTableWidget(self)
        self.warehouses_table.setColumnCount(3)
        self.warehouses_table.setHorizontalHeaderLabels(
            ["ID", "Локация", "Вместимость"])
        self.content_area.addWidget(self.warehouses_table)

        self.load_warehouses()

        back_button = QPushButton("Назад")
        back_button.setStyleSheet("background-color: #d6ced5; font-size: 14px;")
        back_button.clicked.connect(self.clear_content)
        self.content_area.addWidget(back_button)

    def load_warehouses(self):
        conn = create_connection()
        if conn is None:
            QMessageBox.critical(self, "Ошибка", "Не удалось подключиться к базе данных.")
            return

        cursor = conn.cursor()
        cursor.execute("SELECT * FROM Warehouses")
        warehouses = cursor.fetchall()
        conn.close()

        self.warehouses_table.setRowCount(len(warehouses))
        for row_index, row_data in enumerate(warehouses):
            for column_index, value in enumerate(row_data):
                self.warehouses_table.setItem(row_index, column_index, QTableWidgetItem(str(value)))

if __name__ == "__main__":
    create_tables()
    app = QApplication(sys.argv)
    window = LoginWindow()
    window.show()
    sys.exit(app.exec())