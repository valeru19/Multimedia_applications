import sys  # Импорт модуля sys для работы с системными функциями (например, завершение программы).
import math  # Импорт модуля math для математических операций (sin, cos, sqrt и т.д.).
from PySide6.QtWidgets import (QApplication, QMainWindow, QVBoxLayout,
                               QWidget, QLineEdit, QPushButton, QLabel, QHBoxLayout)
from PySide6.QtGui import QPainter, QPen, QColor  # Импорт классов для рисования и работы с цветами.
from PySide6.QtCore import Qt, QPointF  # Импорт базовых классов (флаги, точки и т.д.).

# Предопределённая палитра цветов для графиков
COLOR_PALETTE = [
    QColor("blue"),  # Синий
    QColor("orange"),  # Оранжевый
    QColor("green"),  # Зелёный
    QColor("red"),  # Красный
    QColor("purple"),  # Фиолетовый
    QColor("brown"),  # Коричневый
    QColor("magenta"),  # Пурпурный
    QColor("darken")  # Темно-циановый
]


class PlotWidget(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)  # Инициализация родительского класса QWidget.
        self.functions = []  # Список для хранения функций, их цветов и меток.
        self.color_index = 0  # Индекс для перебора цветов из палитры.

    def paintEvent(self, event):
        # Метод, вызываемый при перерисовке виджета.
        painter = QPainter(self)  # Создание объекта QPainter для рисования.
        painter.setRenderHint(QPainter.Antialiasing)  # Включение сглаживания для плавных линий.

        self.draw_grid(painter)  # Рисует сетку.
        self.draw_axes(painter)  # Рисует оси координат.

        for func, color, label in self.functions:  # Перебор всех функций.
            self.draw_curve(painter, func, color, label)  # Рисует график функции.

        self.draw_legend(painter)  # Рисует легенду.

    def draw_axes(self, painter):
        # Рисует оси координат и подписи к ним.
        width, height = self.width(), self.height()  # Получаем размеры виджета.
        center_x, center_y = width // 2, height // 2  # Вычисляем центр виджета.
        scale_x, scale_y = 20, 20  # Масштаб для осей (1 единица = 20 пикселей).

        # Рисуем оси
        painter.setPen(QPen(Qt.white, 2))  # Устанавливаем черный цвет и толщину линии.
        painter.drawLine(0, center_y, width, center_y)  # Ось X.
        painter.drawLine(center_x, 0, center_x, height)  # Ось Y.

        # Подписи осей
        painter.drawText(width - 20, center_y - 5, "X")  # Подпись оси X.
        painter.drawText(center_x + 5, 20, "Y")  # Подпись оси Y.

        # Подписи масштаба для оси X
        for x in range(-10, 11, 2):  # Перебор значений по оси X.
            px = center_x + x * scale_x  # Вычисление координаты X.
            painter.drawText(px - 10, center_y + 20, f"{x}")  # Подпись значения.

        # Подписи масштаба для оси Y
        for y in range(-10, 11, 2):  # Перебор значений по оси Y.
            py = center_y - y * scale_y  # Вычисление координаты Y.
            painter.drawText(center_x + 10, py + 5, f"{y}")  # Подпись значения.

    def draw_grid(self, painter):
        # Рисует сетку на виджете.
        width, height = self.width(), self.height()  # Получаем размеры виджета.
        center_x, center_y = width // 2, height // 2  # Вычисляем центр виджета.
        scale_x, scale_y = 20, 20  # Масштаб для сетки.

        # Устанавливаем серый цвет и стиль линии (пунктирная).
        painter.setPen(QPen(QColor(200, 200, 200), 1.5, Qt.DotLine))

        # Вертикальные линии
        for x in range(-10, 11):  # Перебор значений по оси X.
            px = center_x + x * scale_x  # Вычисление координаты X.
            painter.drawLine(px, 0, px, height)  # Рисуем вертикальную линию.

        # Горизонтальные линии
        for y in range(-10, 11):  # Перебор значений по оси Y.
            py = center_y - y * scale_y  # Вычисление координаты Y.
            painter.drawLine(0, py, width, py)  # Рисуем горизонтальную линию.

    def draw_curve(self, painter, func, color, label):
        # Рисует график функции.
        width, height = self.width(), self.height()  # Получаем размеры виджета.
        center_x, center_y = width // 2, height // 2  # Вычисляем центр виджета.
        scale_x, scale_y = 20, 20  # Масштаб для осей.

        painter.setPen(QPen(color, 2))  # Устанавливаем цвет и толщину линии.
        points = []  # Список для хранения точек графика.

        for x in range(-100, 101):  # Перебор значений X с шагом 0.1.
            try:
                x_val = x / 10  # Преобразуем X в дробное значение.
                y = func(x_val)  # Вычисляем Y для текущего X.
                px = center_x + x_val * scale_x  # Вычисляем координату X на виджете.
                py = center_y - y * scale_y  # Вычисляем координату Y на виджете.
                points.append(QPointF(px, py))  # Добавляем точку в список.
            except:
                continue  # Пропускаем ошибки (например, деление на ноль).

        # Рисуем линию по точкам
        for i in range(len(points) - 1):  # Перебор точек.
            painter.drawLine(points[i], points[i + 1])  # Рисуем линию между точками.

    def draw_legend(self, painter):
        # Рисует легенду с описанием функций.
        painter.setPen(QPen(Qt.white, 1))  # Устанавливаем белый цвет для текста.
        painter.drawText(20, 30, "Легенда:")  # Заголовок легенды.
        y_offset = 50  # Начальное смещение по Y.

        for func, color, label in self.functions:  # Перебор всех функций.
            painter.setPen(QPen(color, 2))  # Устанавливаем цвет функции.
            painter.drawText(20, y_offset, label)  # Рисуем метку функции.
            y_offset += 20  # Увеличиваем смещение для следующей метки.

    def add_function(self, func, color, label):
        # Добавляет функцию в список для отрисовки.
        self.functions.append((func, color, label))  # Добавляем кортеж (функция, цвет, метка).
        self.update()  # Обновляем виджет для перерисовки.

    def clear_functions(self):
        # Очищает список функций.
        self.functions.clear()  # Очищаем список.
        self.color_index = 0  # Сбрасываем индекс цвета.
        self.update()  # Обновляем виджет.

    def get_next_color(self):
        # Возвращает следующий цвет из палитры.
        color = COLOR_PALETTE[self.color_index % len(COLOR_PALETTE)]  # Получаем цвет по индексу.
        self.color_index += 1  # Увеличиваем индекс.
        return color  # Возвращаем цвет.


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()  # Инициализация родительского класса QMainWindow.
        self.setWindowTitle("Графический анализатор")  # Устанавливаем заголовок окна.
        self.setMinimumSize(800, 600)  # Устанавливаем минимальный размер окна.

        central_widget = QWidget()  # Создаем центральный виджет.
        self.setCentralWidget(central_widget)  # Устанавливаем его как центральный.
        layout = QVBoxLayout()  # Создаем вертикальный компоновщик.
        central_widget.setLayout(layout)  # Устанавливаем компоновщик для центрального виджета.

        # Виджет для рисования
        self.plot_widget = PlotWidget()  # Создаем виджет для рисования графиков.
        layout.addWidget(self.plot_widget)  # Добавляем его в компоновщик.

        # Панель управления
        control_layout = QHBoxLayout()  # Создаем горизонтальный компоновщик для панели управления.

        self.func_input = QLineEdit()  # Создаем поле ввода для функций.
        self.func_input.setPlaceholderText("Введите функцию (например: math.sin(x)*2)")  # Устанавливаем подсказку.
        control_layout.addWidget(self.func_input)  # Добавляем поле ввода в компоновщик.

        btn_add = QPushButton("Добавить")  # Создаем кнопку "Добавить".
        btn_add.clicked.connect(self.add_function)  # Подключаем метод add_function к кнопке.
        control_layout.addWidget(btn_add)  # Добавляем кнопку в компоновщик.

        btn_clear = QPushButton("Очистить")  # Создаем кнопку "Очистить".
        btn_clear.clicked.connect(self.plot_widget.clear_functions)  # Подключаем метод clear_functions к кнопке.
        control_layout.addWidget(btn_clear)  # Добавляем кнопку в компоновщик.

        layout.addLayout(control_layout)  # Добавляем панель управления в вертикальный компоновщик.

        # Подсказка
        info = QLabel("Доступные функции: math.sin(x), math.cos(x), math.tan(x), math.sqrt(x), etc.")
        layout.addWidget(info)  # Добавляем метку в компоновщик.

    def add_function(self):
        # Добавляет функцию в виджет для отрисовки.
        try:
            expr = self.func_input.text()  # Получаем текст из поля ввода.
            func = lambda x, e=expr: eval(e, {"math": math, "x": x})  # Создаем лямбда-функцию.
            color = self.plot_widget.get_next_color()  # Получаем следующий цвет.
            self.plot_widget.add_function(func, color, f"y = {expr}")  # Добавляем функцию в виджет.
            self.func_input.clear()  # Очищаем поле ввода.
        except Exception as e:
            print(f"Ошибка: {e}")  # Выводим ошибку в консоль.


if __name__ == "__main__":
    app = QApplication(sys.argv)  # Создаем экземпляр приложения.
    window = MainWindow()  # Создаем экземпляр главного окна.
    window.show()  # Отображаем окно.
    sys.exit(app.exec())  # Запускаем главный цикл обработки событий.
