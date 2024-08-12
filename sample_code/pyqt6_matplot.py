import sys
from PyQt6.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QHBoxLayout, QWidget, QLabel, QTabWidget
from matplotlib.backends.backend_qtagg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
import numpy as np


class MplCanvas(FigureCanvas):
    def __init__(self, parent=None, width=5, height=4, dpi=100):
        fig = Figure(figsize=(width, height), dpi=dpi)
        super().__init__(fig)
        self.setParent(parent)

    def plot_doughnut(self, labels, sizes, colors):
        self.figure.clear()
        ax = self.figure.add_subplot(111)
        wedges, texts, autotexts = ax.pie(
            sizes, labels=labels, colors=colors, startangle=90, wedgeprops=dict(width=0.3), autopct='%1.1f%%'
        )
        for text in texts + autotexts:
            text.set_fontsize(12)
        ax.set_aspect('equal')
        self.draw()

    def plot_bar(self, labels, values):
        self.figure.clear()
        ax = self.figure.add_subplot(111)
        bars = ax.bar(labels, values, color=['darkviolet', 'green'])
        ax.set_ylim(0, 100)
        ax.set_ylabel('Win Accuracy (%)')
        ax.set_title('Last Month Win Accuracy')
        for bar in bars:
            yval = bar.get_height()
            ax.text(bar.get_x() + bar.get_width() / 2, yval, f'{yval}%', va='bottom', ha='center')
        self.draw()


class Dashboard(QMainWindow):
    def __init__(self):
        super().__init__()

        # Central widget
        widget = QWidget()
        self.setCentralWidget(widget)

        # Layouts
        main_layout = QVBoxLayout()
        widget.setLayout(main_layout)

        # Doughnut Chart
        doughnut_canvas = MplCanvas(self, width=4, height=3, dpi=100)
        doughnut_labels = ['Most Consecutive Right', 'Most Consecutive Wrong']
        doughnut_sizes = [70, 30]  # Example data
        doughnut_colors = ['darkviolet', 'green']
        doughnut_canvas.plot_doughnut(doughnut_labels, doughnut_sizes, doughnut_colors)
        main_layout.addWidget(doughnut_canvas)

        # Tab Widget for Current Day Status and Previous Day Prediction
        tab_widget = QTabWidget()
        main_layout.addWidget(tab_widget)

        # Current Day Status Tab
        current_day_tab = QWidget()
        tab_widget.addTab(current_day_tab, "Current Day Status")
        current_day_layout = QVBoxLayout()
        current_day_tab.setLayout(current_day_layout)

        buy_sell_label = QLabel("Current Day Status: Buy")
        buy_sell_label.setStyleSheet("color: darkviolet; font-family: 'Raleway'; font-size: 16pt;")
        current_day_layout.addWidget(buy_sell_label)

        # Previous Day Prediction Tab
        previous_day_tab = QWidget()
        tab_widget.addTab(previous_day_tab, "Previous Day Prediction")
        previous_day_layout = QVBoxLayout()
        previous_day_tab.setLayout(previous_day_layout)

        prediction_label = QLabel("Previous Day Prediction: Right")
        prediction_label.setStyleSheet("color: green; font-family: 'Raleway'; font-size: 16pt;")
        previous_day_layout.addWidget(prediction_label)

        # Win Accuracy Bar Chart
        bar_chart_canvas = MplCanvas(self, width=4, height=3, dpi=100)
        bar_labels = ['Accuracy']
        bar_values = [85]  # Example data: win accuracy percentage
        bar_chart_canvas.plot_bar(bar_labels, bar_values)
        main_layout.addWidget(bar_chart_canvas)

        # Window settings
        self.setWindowTitle("Trading Dashboard")
        self.setGeometry(100, 100, 800, 600)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    dashboard = Dashboard()
    dashboard.show()
    sys.exit(app.exec())
