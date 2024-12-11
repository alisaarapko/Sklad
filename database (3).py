import sqlite3
import sys
from PyQt6.QtWidgets import QApplication, QWidget, QVBoxLayout, QLineEdit, QPushButton, QFormLayout, QLabel, QComboBox

def initialize_database():
    conn = sqlite3.connect('warehouse.db')
    cursor = conn.cursor()

    # Создание таблицы для поставок
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS Deliveries (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            delivery_date TEXT,
            supplier TEXT,
            status TEXT,
            article TEXT,
            name TEXT,
            description TEXT,
            quantity INTEGER,
            storage_area TEXT
        )
    ''')

    # Создание таблицы для отгрузок
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS Shipments (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            shipment_date TEXT,
            customer TEXT,
            status TEXT,
            product_id TEXT,
            quantity INTEGER
        )
    ''')

    # Создание таблицы для отчетов
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS Reports (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            report_date TEXT,
            description TEXT
        )
    ''')

    # Создание таблицы для поставщиков
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS Suppliers (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT,
            contact_info TEXT
        )
    ''')

    # Создание таблицы для складов
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS Warehouses (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            location TEXT,
            capacity REAL
        )
    ''')

    conn.commit()
    conn.close()

class MainApp(QWidget):

    def __init__(self):
        super().__init__()

        self.setWindowTitle("Выбор базы данных")
        self.layout = QVBoxLayout()
        self.setLayout(self.layout)

        self.label = QLabel("Выберите тип базы данных для заполнения:")
        self.layout.addWidget(self.label)

        self.combo_box = QComboBox()
        self.combo_box.addItems(["Поставки", "Отгрузки", "Отчеты", "Поставщики", "Склады"])
        self.layout.addWidget(self.combo_box)

        self.open_button = QPushButton("Открыть")

        self.open_button.clicked.connect(self.open_database_app)
        self.layout.addWidget(self.open_button)

    def open_database_app(self):
        selection = self.combo_box.currentText()
        if selection == "Поставки":
            self.database_app = DatabaseApp()
            self.database_app.show()
        elif selection == "Отгрузки":
            self.database_app = DatabaseApp1()
            self.database_app.show()
        elif selection == "Отчеты":
            self.database_app = ReportsApp()
            self.database_app.show()
        elif selection == "Поставщики":
            self.database_app = SuppliersApp()
            self.database_app.show()
        elif selection == "Склады":
            self.database_app = WarehousesApp()
            self.database_app.show()
        self.close()  # Закрываем окно выбора после открытия приложения

class DatabaseApp(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("База данных поставок")
        self.layout = QVBoxLayout()
        self.setLayout(self.layout)

        self.form_layout = QFormLayout()
        self.layout.addLayout(self.form_layout)

        self.delivery_date_input = QLineEdit()
        self.supplier_input = QLineEdit()
        self.status_input = QLineEdit()
        self.article_input = QLineEdit()
        self.name_input = QLineEdit()
        self.description_input = QLineEdit()
        self.quantity_input = QLineEdit()
        self.storage_area_input = QLineEdit()

        self.form_layout.addRow("Дата поставки", self.delivery_date_input)
        self.form_layout.addRow("Поставщик", self.supplier_input)
        self.form_layout.addRow("Статус", self.status_input)
        self.form_layout.addRow("Артикул", self.article_input)
        self.form_layout.addRow("Название", self.name_input)
        self.form_layout.addRow("Описание", self.description_input)
        self.form_layout.addRow("Количество", self.quantity_input)
        self.form_layout.addRow("Склад", self.storage_area_input)

        self.add_button = QPushButton("Добавить в базу данных")
        self.add_button.clicked.connect(self.add_to_database)
        self.layout.addWidget(self.add_button)

    def add_to_database(self):
        conn = sqlite3.connect('warehouse.db')
        cursor = conn.cursor()

        delivery_date = self.delivery_date_input.text()
        supplier = self.supplier_input.text()
        status = self.status_input.text()
        article = self.article_input.text()
        name = self.name_input.text()
        description = self.description_input.text()
        quantity = self.quantity_input.text()
        storage_area = self.storage_area_input.text()

        cursor.execute('''
            INSERT INTO Deliveries (delivery_date, supplier, status, article, name, description, quantity, storage_area)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        ''', (delivery_date, supplier, status, article, name, description, quantity, storage_area))
        conn.commit()
        conn.close()

        self.delivery_date_input.clear()
        self.supplier_input.clear()
        self.status_input.clear()
        self.article_input.clear()
        self.name_input.clear()
        self.description_input.clear()
        self.quantity_input.clear()
        self.storage_area_input.clear()


class DatabaseApp1(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("База данных отгрузок")
        self.layout = QVBoxLayout()
        self.setLayout(self.layout)

        self.form_layout = QFormLayout()
        self.layout.addLayout(self.form_layout)

        self.shipments_date_input = QLineEdit()
        self.client_input = QLineEdit()
        self.status_input = QLineEdit()
        self.ID_product_input = QLineEdit()
        self.quantity_input = QLineEdit()

        self.form_layout.addRow("Дата отгрузки", self.shipments_date_input)
        self.form_layout.addRow("Клиент", self.client_input)
        self.form_layout.addRow("Статус", self.status_input)
        self.form_layout.addRow("ID товара", self.ID_product_input)
        self.form_layout.addRow("Количество", self.quantity_input)

        self.add_button = QPushButton("Добавить в базу данных")
        self.add_button.clicked.connect(self.add_to_database1)
        self.layout.addWidget(self.add_button)

    def add_to_database1(self):
        conn = sqlite3.connect('warehouse.db')
        cursor = conn.cursor()

        shipments_date = self.shipments_date_input.text()
        client = self.client_input.text()
        status = self.status_input.text()
        ID_product = self.ID_product_input.text()
        quantity = self.quantity_input.text()

        cursor.execute('''
            INSERT INTO Shipments (shipment_date, customer, status, product_id, quantity)
            VALUES (?, ?, ?, ?, ?)
        ''', (shipments_date, client, status, ID_product, quantity))
        conn.commit()
        conn.close()

        self.shipments_date_input.clear()
        self.client_input.clear()
        self.status_input.clear()
        self.ID_product_input.clear()
        self.quantity_input.clear()


class ReportsApp(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("База данных отчетов")
        self.layout = QVBoxLayout()
        self.setLayout(self.layout)

        self.form_layout = QFormLayout()
        self.layout.addLayout(self.form_layout)

        self.report_date_input = QLineEdit()
        self.description_input = QLineEdit()

        self.form_layout.addRow("Дата отчета", self.report_date_input)
        self.form_layout.addRow("Описание", self.description_input)

        self.add_button = QPushButton("Добавить в базу данных")
        self.add_button.clicked.connect(self.add_to_database)
        self.layout.addWidget(self.add_button)

    def add_to_database(self):
        conn = sqlite3.connect('warehouse.db')
        cursor = conn.cursor()

        report_date = self.report_date_input.text()
        description = self.description_input.text()

        cursor.execute('''
            INSERT INTO Reports (report_date, description)
            VALUES (?, ?)
        ''', (report_date, description))
        conn.commit()
        conn.close()

        self.report_date_input.clear()
        self.description_input.clear()


class SuppliersApp(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("База данных поставщиков")
        self.layout = QVBoxLayout()
        self.setLayout(self.layout)

        self.form_layout = QFormLayout()
        self.layout.addLayout(self.form_layout)

        self.name_input = QLineEdit()
        self.contact_info_input = QLineEdit()

        self.form_layout.addRow("Имя", self.name_input)
        self.form_layout.addRow("Контактная информация", self.contact_info_input)

        self.add_button = QPushButton("Добавить в базу данных")
        self.add_button.clicked.connect(self.add_to_database)
        self.layout.addWidget(self.add_button)

    def add_to_database(self):
        conn = sqlite3.connect('warehouse.db')
        cursor = conn.cursor()

        name = self.name_input.text()
        contact_info = self.contact_info_input.text()

        cursor.execute('''
            INSERT INTO Suppliers (name, contact_info)
            VALUES (?, ?)
        ''', (name, contact_info))
        conn.commit()
        conn.close()

        self.name_input.clear()
        self.contact_info_input.clear()


class WarehousesApp(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("База данных складов")
        self.layout = QVBoxLayout()
        self.setLayout(self.layout)

        self.form_layout = QFormLayout()
        self.layout.addLayout(self.form_layout)

        self.location_input = QLineEdit()
        self.capacity_input = QLineEdit()

        self.form_layout.addRow("Локация", self.location_input)
        self.form_layout.addRow("Вместимость (м²)", self.capacity_input)

        self.add_button = QPushButton("Добавить в базу данных")
        self.add_button.clicked.connect(self.add_to_database)
        self.layout.addWidget(self.add_button)

    def add_to_database(self):
        conn = sqlite3.connect('warehouse.db')
        cursor = conn.cursor()

        location = self.location_input.text()
        capacity = self.capacity_input.text()

        cursor.execute('''
            INSERT INTO Warehouses (location, capacity)
            VALUES (?, ?)
        ''', (location, capacity))
        conn.commit()
        conn.close()

        self.location_input.clear()
        self.capacity_input.clear()


if __name__ == "__main__":
    initialize_database()  # Инициализация базы данных и создание таблиц

    app = QApplication(sys.argv)

    main_app = MainApp()
    main_app.show()

    sys.exit(app.exec())

