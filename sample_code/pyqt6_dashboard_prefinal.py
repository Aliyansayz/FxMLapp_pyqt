from PyQt6.QtCore import Qt
from PyQt6.QtGui import QIcon
from PyQt6.QtWidgets import (
    QApplication, QVBoxLayout, QHBoxLayout, QPushButton,
    QDialog, QLabel, QStackedWidget, QWidget, QSizePolicy,
    QComboBox, QStyleFactory, QMenu
)
from PyQt6.QtCharts import QChart, QChartView, QPieSeries, QBarSet, QBarSeries, QBarCategoryAxis, QValueAxis


class DashboardApp(QDialog):
    def __init__(self, parent=None):
        super(DashboardApp, self).__init__(parent)
        self.current_view_index = 0

        # Create the main layout
        mainLayout = QHBoxLayout()

        # Create sidebar
        self.sidebar = self.createSidebar()
        mainLayout.addLayout(self.sidebar)

        # Sidebar visibility toggle
        self.sidebar_visible = True
        self.toggle_sidebar_action = QAction("Toggle Sidebar", self)
        self.toggle_sidebar_action.triggered.connect(self.toggle_sidebar_visibility)

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
        self.buttons = [
            ("Dashboard", self.showDashboardView, 0),
            ("Settings", self.showSettingsView, 1),
            ("About", self.showAboutView, 2)
        ]

        self.button_widgets = []
        for text, handler, index in self.buttons:
            btn = QPushButton(text)
            btn.setSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Fixed)
            btn.setStyleSheet("border: none; font-size: 18px;")
            btn.clicked.connect(handler)
            layout.addWidget(btn)
            self.button_widgets.append(btn)

        layout.addStretch(1)  # Add stretch to push buttons to the top
        return layout

    def createViews(self):
        # Code for views (same as your previous message)
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

    def showView(self, index):
        if self.centralWidget.currentIndex() != index:
            self.centralWidget.setCurrentIndex(index)
            self.update_button_styles(index)
            self.current_view_index = index

    def showDashboardView(self):
        self.showView(0)

    def showSettingsView(self):
        self.showView(1)

    def showAboutView(self):
        self.showView(2)

    def update_button_styles(self, active_index):
        for i, btn in enumerate(self.button_widgets):
            if i == active_index:
                btn.setStyleSheet("background-color: lightblue; border: none; font-size: 18px;")
            else:
                btn.setStyleSheet("background-color: None; border: none; font-size: 18px;")

    def toggle_sidebar_visibility(self):
        self.sidebar_visible = not self.sidebar_visible
        for btn in self.button_widgets:
            btn.setVisible(self.sidebar_visible)

if __name__ == '__main__':
    import sys

    app = QApplication(sys.argv)
    app.setStyle(QStyleFactory.create("Fusion"))  # Set the Fusion style
    dashboardApp = DashboardApp()
    dashboardApp.show()
    sys.exit(app.exec())
