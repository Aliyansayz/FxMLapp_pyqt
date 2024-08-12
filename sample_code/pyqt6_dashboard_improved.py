from PyQt6.QtWidgets import (
    QApplication, QVBoxLayout, QHBoxLayout, QPushButton,
    QDialog, QLabel, QComboBox, QWidget, QGridLayout, QGroupBox
)

from PyQt6.QtCharts import QChart, QChartView, QPieSeries, QBarSet, QBarSeries, QBarCategoryAxis, QValueAxis

from PyQt6.QtCore import Qt
from PyQt6.QtGui import QColor, QFont

class DashboardApp(QDialog):
    def __init__(self, parent=None):
        super(DashboardApp, self).__init__(parent)
        self.setWindowTitle("Enhanced Dashboard Interface")
        self.setGeometry(100, 100, 1200, 800)  # Set window size and position
        self.setupUI()

    def setupUI(self):
        # Main Layout
        mainLayout = QGridLayout(self)

        # Dropdown for asset selection
        self.assetComboBox = QComboBox()
        self.assetComboBox.addItems(["Bitcoin", "Ethereum", "Gold"])
        self.assetComboBox.currentTextChanged.connect(self.updateDashboard)
        mainLayout.addWidget(self.assetComboBox, 0, 0, 1, 2)

        # Setup Charts
        self.pieChartView = QChartView()
        self.barChartView = QChartView()
        mainLayout.addWidget(self.createCard(self.pieChartView, "Prediction Outcomes"), 1, 0)
        mainLayout.addWidget(self.createCard(self.barChartView, "Win Accuracy (%)"), 1, 1)

        # Status Information
        self.currentDayStatus = QLabel("Current Day Status: Buy")
        self.currentDayStatus.setFont(QFont('Arial', 14))
        self.previousDayPrediction = QLabel("Previous Day Prediction: Right")
        self.previousDayPrediction.setFont(QFont('Arial', 14))

        mainLayout.addWidget(self.createCard(self.currentDayStatus, "Current Day Status"), 2, 0)
        mainLayout.addWidget(self.createCard(self.previousDayPrediction, "Previous Day Prediction"), 2, 1)

        # Initial update
        self.updateDashboard(self.assetComboBox.currentText())

    def createCard(self, widget, title):
        groupBox = QGroupBox(title)
        groupBox.setFont(QFont('Arial', 12))
        layout = QVBoxLayout()
        layout.addWidget(widget)
        groupBox.setLayout(layout)
        return groupBox

    def updateDashboard(self, asset):
        # This is where you would set up the data specific to the asset
        pieSeries = QPieSeries()
        pieSeries.append("Right", 75)
        pieSeries.append("Wrong", 25)
        pieChart = QChart()
        pieChart.addSeries(pieSeries)
        pieChart.setTitle(f"Most Consecutive Predictions for {asset}")
        self.pieChartView.setChart(pieChart)

        barSet = QBarSet("Accuracy")
        barSet.append([80])
        barSeries = QBarSeries()
        barSeries.append(barSet)
        barChart = QChart()
        barChart.addSeries(barSeries)
        barChart.setTitle("Win Accuracy (%) for " + asset)
        self.barChartView.setChart(barChart)

if __name__ == '__main__':
    import sys
    app = QApplication(sys.argv)
    window = DashboardApp()
    window.show()
    sys.exit(app.exec())
