from PyQt6.QtWidgets import (
    QApplication, QVBoxLayout, QHBoxLayout, QPushButton,
    QDialog, QLabel, QComboBox, QWidget, QGridLayout, QGroupBox, QScrollArea
)
from PyQt6.QtCore import Qt, pyqtSignal
from PyQt6.QtGui import QColor, QFont

class DashboardApp(QDialog):
    def __init__(self, parent=None):

        super(DashboardApp, self).__init__(parent)

        self.setWindowTitle("All Asset Dashboard Final")

        self.setGeometry(100, 100, 1200, 800)  # Set window size and position
        self.setWindowFlags(Qt.WindowType.WindowMinMaxButtonsHint | Qt.WindowType.WindowCloseButtonHint)
        self.setupUI()

    def setupUI(self):
        # Main Layout
        mainLayout = QVBoxLayout(self)

        # Dropdown for asset selection
        self.assetComboBox = QComboBox()
        self.assetComboBox.addItems(["Bitcoin", "Ethereum", "Gold", "All Assets"])
        self.assetComboBox.currentTextChanged.connect(self.updateDashboard)
        mainLayout.addWidget(self.assetComboBox)

        # Asset Details Card
        self.assetDetails = QGroupBox("Asset Details")
        self.assetDetails.setFont(QFont('Arial', 12))
        self.detailsLayout = QVBoxLayout()
        self.assetDetails.setLayout(self.detailsLayout)
        mainLayout.addWidget(self.assetDetails)

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
            # Clear previous asset details and scroll area content
            for i in reversed(range(self.detailsLayout.count())):
                self.detailsLayout.itemAt(i).widget().setParent(None)
            for i in reversed(range(self.scrollLayout.count())):
                self.scrollLayout.itemAt(i).widget().setParent(None)

    def updateStatusView(self):
        # Setup columns for Buy and Sell
        buyLayout = QVBoxLayout()
        sellLayout = QVBoxLayout()

        # Create headers
        buyHeader = QLabel("BUY")
        buyHeader.setStyleSheet("background-color: green; color: white; font-size: 16px; text-align: center;")
        buyLayout.addWidget(buyHeader)
        sellHeader = QLabel("SELL")
        sellHeader.setStyleSheet("background-color: #6f1615; color: white; font-size: 16px;  text-align: center;")
        sellLayout.addWidget(sellHeader)

        # Example data for Buy/Sell status
        assets = ["Bitcoin", "Ethereum", "Gold"]
        buy_data = [75, 90, 80]
        sell_data = [65, 70, 85]

        for i, asset in enumerate(assets):
            buyLabel = QPushButton(f"{asset}: {buy_data[i]}%")
            buyLabel.setStyleSheet("background-color: green; color: white; font-size: 14px; padding: 5px;")
            buyLabel.clicked.connect(lambda _, a=asset: self.showAssetDetails(a))
            buyLayout.addWidget(buyLabel)

            sellLabel = QPushButton(f"{asset}: {sell_data[i]}%")
            sellLabel.setStyleSheet("background-color: red; color: white; font-size: 14px; padding: 5px;")
            sellLabel.clicked.connect(lambda _, a=asset: self.showAssetDetails(a))
            sellLayout.addWidget(sellLabel)

        self.scrollLayout.addLayout(buyLayout)
        self.scrollLayout.addLayout(sellLayout)

    def showAssetDetails(self, asset):
        # Clear previous details
        for i in reversed(range(self.detailsLayout.count())):
            self.detailsLayout.itemAt(i).widget().setParent(None)

        # Example details for the asset
        assetLabel = QLabel(f"Details for {asset}")
        statusLabel = QLabel("Previous Day Status: Right")
        mlPredictionLabel = QLabel("Present Day ML Prediction: Buy")
        supertrendLabel = QLabel("Supertrend Status: Sell")

        # Add to layout
        self.detailsLayout.addWidget(assetLabel)
        self.detailsLayout.addWidget(statusLabel)
        self.detailsLayout.addWidget(mlPredictionLabel)
        self.detailsLayout.addWidget(supertrendLabel)


if __name__ == '__main__':
    import sys
    app = QApplication(sys.argv)
    window = DashboardApp()
    window.show()
    sys.exit(app.exec())
