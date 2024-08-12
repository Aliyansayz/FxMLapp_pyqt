from PyQt6.QtWidgets import (
    QApplication, QVBoxLayout, QHBoxLayout, QPushButton,
    QDialog, QLabel, QComboBox, QWidget, QGridLayout, QGroupBox, QScrollArea
)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QColor, QFont

class DashboardApp(QDialog):
    def __init__(self, parent=None):
        super(DashboardApp, self).__init__(parent)
        self.setWindowTitle("All Asset Dashboard Interface")
        self.setGeometry(100, 100, 1200, 800)  # Set window size and position
        self.setWindowFlags(Qt.WindowType.WindowMinMaxButtonsHint | Qt.WindowType.WindowCloseButtonHint)  # Enable minimize, maximize and close buttons
        self.setupUI()

    def setupUI(self):
        # Main Layout
        mainLayout = QVBoxLayout(self)

        # Dropdown for asset selection
        self.assetComboBox = QComboBox()
        self.assetComboBox.addItems(["Bitcoin", "Ethereum", "Gold", "All Assets"])
        self.assetComboBox.currentTextChanged.connect(self.updateDashboard)
        mainLayout.addWidget(self.assetComboBox)

        # Scroll Area for asset status
        self.scrollArea = QScrollArea()
        self.scrollArea.setWidgetResizable(True)
        self.scrollWidget = QWidget()
        self.scrollLayout = QHBoxLayout(self.scrollWidget)
        self.scrollArea.setWidget(self.scrollWidget)
        mainLayout.addWidget(self.createCard(self.scrollArea, "Assets Status Overview"))

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
        if asset == "All Assets":
            self.updateStatusView()
        else:
            # Clear the scroll area when selecting specific assets
            for i in reversed(range(self.scrollLayout.count())):
                self.scrollLayout.itemAt(i).widget().setParent(None)

    def updateStatusView(self):
        # Setup columns for Buy and Sell
        buyLayout = QVBoxLayout()
        sellLayout = QVBoxLayout()

        buyHeader = QLabel("BUY")
        buyHeader.setStyleSheet("background-color: green; color: white; font-size: 16px; padding: 5px; text-align: center;")
        buyLayout.addWidget(buyHeader)

        sellHeader = QLabel("SELL")
        sellHeader.setStyleSheet("background-color: red; color: white; font-size: 16px; padding: 5px; text-align: center;")
        sellLayout.addWidget(sellHeader)

        # Example data for Buy/Sell status
        assets = ["Bitcoin", "Ethereum", "Gold"]
        buy_data = [75, 90, 80]
        sell_data = [65, 70, 85]

        # Create Buy and Sell bars
        for i, asset in enumerate(assets):
            buyLabel = QLabel(f"{asset}: {buy_data[i]}%")
            buyLabel.setStyleSheet("background-color: green; color: white; font-size: 14px; padding: 5px;")
            buyLayout.addWidget(buyLabel)

            sellLabel = QLabel(f"{asset}: {sell_data[i]}%")
            sellLabel.setStyleSheet("background-color: red; color: white; font-size: 14px; padding: 5px;")
            sellLayout.addWidget(sellLabel)

        self.scrollLayout.addLayout(buyLayout)
        self.scrollLayout.addLayout(sellLayout)

if __name__ == '__main__':
    import sys
    app = QApplication(sys.argv)
    window = DashboardApp()
    window.show()
    sys.exit(app.exec())
