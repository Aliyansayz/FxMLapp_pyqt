from PyQt6.QtCore import Qt
from PyQt6.QtGui import QIcon
from PyQt6.QtWidgets import (
    QApplication, QVBoxLayout, QHBoxLayout, QPushButton,
    QDialog, QLabel, QStackedWidget, QWidget, QSizePolicy,
    QComboBox, QStyleFactory
)

from PyQt6.QtCharts import QChart, QChartView, QPieSeries, QBarSet, QBarSeries, QBarCategoryAxis, QValueAxis


class DashboardApp(QDialog):
    def __init__(self, parent=None):
        super(DashboardApp, self).__init__(parent)

        # Create the main layout
        mainLayout = QHBoxLayout()

        # Create sidebar
        self.sidebar = self.createSidebar()
        mainLayout.addLayout(self.sidebar)

        # Create central view manager
        self.centralWidget = QStackedWidget()
        mainLayout.addWidget(self.centralWidget)

        # Create views
        self.createViews()

        self.setLayout(mainLayout)
        self.setWindowTitle("Dashboard Interface")
        self.setGeometry(100, 100, 1200, 800)  # Set window size and position
        self.setWindowIcon(QIcon("icon.png"))  # Optional: Set window icon
        self.setWindowFlags(Qt.WindowType.WindowMinMaxButtonsHint | Qt.WindowType.WindowCloseButtonHint)

    def createSidebar(self):
        layout = QVBoxLayout()

        # Create buttons and connect them to switch views
        buttons = [
            ("Dashboard", self.showDashboardView),
            ("Settings", self.showSettingsView),
            ("About", self.showAboutView)
        ]

        for text, handler in buttons:
            btn = QPushButton(text)
            btn.setSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Fixed)
            btn.setStyleSheet("border: none; font-size: 18px;")  # Remove border and increase font size
            btn.clicked.connect(handler)
            layout.addWidget(btn)

        layout.addStretch(1)  # Add stretch to push buttons to the top
        return layout

    def createViews(self):
        # Dashboard View
        dashboardView = QWidget()
        dashboardLayout = QVBoxLayout(dashboardView)

        # Dropdown to select element
        self.elementDropdown = QComboBox()
        self.elementDropdown.addItems(["Bitcoin", "Ethereum", "Gold"])
        self.elementDropdown.currentTextChanged.connect(self.updateDashboard)
        dashboardLayout.addWidget(self.elementDropdown)

        # Create chart views
        self.pieChartView = QChartView()
        self.barChartView = QChartView()

        # Add charts to the dashboard layout
        dashboardLayout.addWidget(self.pieChartView)
        dashboardLayout.addWidget(self.barChartView)

        # Current Day Status
        self.currentDayStatus = QLabel("Current Day Status: Buy")
        self.currentDayStatus.setStyleSheet("color: #6f1615; font-family: 'Raleway'; font-size: 16pt;")
        dashboardLayout.addWidget(self.currentDayStatus)

        # Previous Day Prediction
        self.previousDayPrediction = QLabel("Previous Day Prediction: Right")
        self.previousDayPrediction.setStyleSheet("color: green; font-family: 'Raleway'; font-size: 16pt;")
        dashboardLayout.addWidget(self.previousDayPrediction)

        # Settings View
        settingsView = QWidget()
        settingsLayout = QVBoxLayout(settingsView)
        settingsLabel = QLabel("Settings Page")
        settingsLayout.addWidget(settingsLabel)

        # About View
        aboutView = QWidget()
        aboutLayout = QVBoxLayout(aboutView)
        aboutLabel = QLabel("About Page")
        aboutLayout.addWidget(aboutLabel)

        # Add views to the stacked widget
        self.centralWidget.addWidget(dashboardView)
        self.centralWidget.addWidget(settingsView)
        self.centralWidget.addWidget(aboutView)

        # Initialize dashboard with the first element
        self.updateDashboard(self.elementDropdown.currentText())

    def showDashboardView(self):
        self.centralWidget.setCurrentIndex(0)

    def showSettingsView(self):
        self.centralWidget.setCurrentIndex(1)

    def showAboutView(self):
        self.centralWidget.setCurrentIndex(2)

    def updateDashboard(self, element):
        # Example data based on the element selection
        if element == "Bitcoin":
            right_predictions = 70
            wrong_predictions = 30
            win_accuracy = 85
        elif element == "Ethereum":
            right_predictions = 60
            wrong_predictions = 40
            win_accuracy = 75
        elif element == "Gold":
            right_predictions = 80
            wrong_predictions = 20
            win_accuracy = 90

        # Update pie chart
        pieSeries = QPieSeries()
        pieSeries.append("Most Consecutive Right", right_predictions)
        pieSeries.append("Most Consecutive Wrong", wrong_predictions)
        pieSeries.slices()[0].setBrush(Qt.GlobalColor.red)
        pieSeries.slices()[1].setBrush(Qt.GlobalColor.green)

        pieChart = QChart()
        pieChart.addSeries(pieSeries)
        pieChart.setTitle(f"Most Consecutive Predictions for {element}")
        self.pieChartView.setChart(pieChart)

        # Update horizontal bar chart
        barSet = QBarSet(f"Win Accuracy for {element}")
        barSet.append([win_accuracy])

        barSeries = QBarSeries()
        barSeries.append(barSet)

        barChart = QChart()
        barChart.addSeries(barSeries)
        barChart.setTitle("Win Accuracy (%)")

        axisX = QBarCategoryAxis()
        axisX.append(["Accuracy"])
        barChart.addAxis(axisX, Qt.AlignmentFlag.AlignBottom)
        barSeries.attachAxis(axisX)

        axisY = QValueAxis()
        axisY.setRange(0, 100)
        barChart.addAxis(axisY, Qt.AlignmentFlag.AlignLeft)
        barSeries.attachAxis(axisY)

        self.barChartView.setChart(barChart)


if __name__ == '__main__':
    import sys

    app = QApplication(sys.argv)
    app.setStyle(QStyleFactory.create("Fusion"))  # Set the Fusion style
    dashboardApp = DashboardApp()
    dashboardApp.show()
    sys.exit(app.exec())
