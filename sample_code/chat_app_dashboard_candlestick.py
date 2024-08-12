from PyQt6.QtCore import Qt
from PyQt6.QtGui import QFont

from PyQt6.QtWidgets import (QApplication, QVBoxLayout, QHBoxLayout, QPushButton, QComboBox,
                             QDialog, QLabel, QTextEdit, QLineEdit, QStackedWidget, QGroupBox,
                             QWidget, QSizePolicy, QStyleFactory, QTableWidget, QTableWidgetItem,
                             QScrollArea, QCheckBox, QGridLayout)
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
import mplfinance as mpf
import pandas as pd


class ChatbotApp(QDialog):
    def __init__(self, parent=None):
        super(ChatbotApp, self).__init__(parent)

        self.setWindowTitle("Enhanced Dashboard Interface")
        self.setGeometry(100, 100, 1200, 800)  # Set window size and position

        self.setWindowFlags(Qt.WindowType.WindowMinMaxButtonsHint | Qt.WindowType.WindowCloseButtonHint)

        # Create the main layout
        mainLayout = QHBoxLayout()

        # topBarLayout = QHBoxLayout()
        # mainLayout.addStretch(1)
        # mainLayout.addWidget(self.fullscreenButton)

        # Create sidebar
        self.sidebar = self.createSidebar()
        mainLayout.addLayout(self.sidebar)

        self.setupUI()

        # Create central view manager
        self.centralWidget = QStackedWidget()  # Main Window

        mainLayout.addWidget(self.centralWidget)

        # Create views
        self.createViews()
        # Create All Asset dashboard view

        self.asset_store()

        self.setLayout(mainLayout)
        self.setWindowTitle("Chatbot Interface")
        self.setGeometry(100, 100, 800, 600)  # Set window size and position

    def createSidebar(self):
        layout = QVBoxLayout()

        # Create buttons and connect them to switch views
        buttons = [
            ("Home", self.showChatbotView),
            ("Settings", self.showSettingsView),
            ("About", self.showAboutView),
            ("Primary Dashboard", self.showPrimaryDashboardView ),
            ("Last 3 Days Table", self.showTab  ),  # Add Table view button
            ("History Table", self.showTableView)
        ]
        for text, handler in buttons:
            btn = QPushButton(text)
            btn.setSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Fixed)
            btn.setStyleSheet("border: none; font-size: 18px;")  # Remove border and increase font size
            btn.clicked.connect(handler)
            layout.addWidget(btn)

        layout.addStretch(1)  # Add stretch to push buttons to the top
        return layout

    def toggleFullscreen(self):
        if self.isFullScreen():
            self.showNormal()
            self.fullscreenButton.setText("Fullscreen")
        else:
            self.showFullScreen()
            self.fullscreenButton.setText("Exit Fullscreen")
    def createViews(self):
        # Chatbot View
        chatbotView = QWidget()
        chatbotLayout = QVBoxLayout(chatbotView)

        chatDisplay = QTextEdit()
        chatDisplay.setReadOnly(True)
        chatDisplay.setPlaceholderText("Chatbot messages will appear here...")

        userInput = QLineEdit()
        userInput.setPlaceholderText("Type your message here...")

        sendButton = QPushButton("Send")
        sendButton.clicked.connect(lambda: self.sendMessage(userInput, chatDisplay))

        inputLayout = QHBoxLayout()
        inputLayout.addWidget(userInput)
        inputLayout.addWidget(sendButton)

        chatbotLayout.addWidget(chatDisplay)
        chatbotLayout.addLayout(inputLayout)

        # Settings View
        settingsView = QWidget()
        settingsLayout = QVBoxLayout(settingsView)
        settingsLabel = QLabel("Settings Page")
        settingsLayout.addWidget(settingsLabel)

        self.fullscreenButton = QPushButton("Fullscreen")
        self.fullscreenButton.setSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Fixed)
        self.fullscreenButton.setStyleSheet("border: none; font-size: 18px;")
        self.fullscreenButton.clicked.connect(self.toggleFullscreen)
        settingsLayout.addWidget(self.fullscreenButton)

        # About View
        aboutView = QWidget()
        aboutLayout = QVBoxLayout(aboutView)
        aboutLabel = QLabel("About Page")
        aboutLayout.addWidget(aboutLabel)

        # Table View
        self.tableView = QWidget()
        tableLayout = QVBoxLayout(self.tableView)

        # Scrollable area for checkboxes
        scrollArea = QScrollArea()
        scrollWidget = QWidget()
        scrollGridLayout = QGridLayout(scrollWidget)




        assets = [
            'AUDCAD', 'AUDCHF', 'AUDJPY', 'AUDNZD', 'AUDUSD',
            'CADCHF', 'CADJPY',
            'CHFJPY',
            'EURAUD', 'EURCAD', 'EURCHF', 'EURGBP', 'EURJPY', 'EURNZD', 'EURUSD',
            'GBPAUD', 'GBPCAD', 'GBPCHF', 'GBPJPY', 'GBPUSD', 'GBPNZD',
            'NZDCAD', 'NZDCHF', 'NZDJPY', 'NZDUSD',
            'USDCHF', 'USDCAD', 'USDJPY'
        ]

        self.checkboxes = {}

        maxPerRow = 5
        maxPerColumn = 3

        # Table View
        self.tableView = QWidget()
        tableLayout = QGridLayout(self.tableView)  # Use QGridLayout

        # Scrollable area for checkboxes
        scrollArea = QScrollArea()
        scrollWidget = QWidget()
        scrollGridLayout = QGridLayout(scrollWidget)  # Use QGridLayout for positioning

        for asset in assets:
            checkbox = QCheckBox(asset)
            checkbox.stateChanged.connect(self.updateTables)
            scrollGridLayout.addWidget(checkbox)
            # scrollLayout.addWidget(checkbox)
            self.checkboxes[asset] = checkbox

        # scrollWidget.setLayout(scrollLayout)
        # scrollArea.setWidget(scrollWidget)
        # scrollArea.setWidgetResizable(True)
        # tableLayout.addWidget(scrollArea, 0 , 1)

        scrollWidget.setLayout(scrollGridLayout)
        scrollArea.setWidget(scrollWidget)
        scrollArea.setWidgetResizable(True)
        tableLayout.addWidget(scrollArea, 0, 1)  # Position checkboxes in the top right corner

        # checkboxesLayout = QVBoxLayout()
        # checkboxesLayout.addWidget(scrollArea)
        # checkboxesLayout.addStretch(1)  # Push checkboxes to the top
        # tableLayout.addLayout(checkboxesLayout, 1)  # Ratio 1 for smaller size

        # ___________________________________________________________
        # for index, asset in enumerate(assets):
        #     checkbox = QCheckBox(asset)
        #     checkbox.stateChanged.connect(self.updateTables)
        #
        #     # Calculate the current row and column based on index
        #     column = (index // maxPerColumn) % maxPerRow
        #     row = (index // (maxPerRow * maxPerColumn)) * maxPerColumn + index % maxPerColumn
        #
        #     scrollGridLayout.addWidget(checkbox, row, column)
        #     self.checkboxes[asset] = checkbox
        #
        # scrollWidget.setLayout(scrollGridLayout)
        # scrollArea.setWidget(scrollWidget)
        # scrollArea.setWidgetResizable(True)
        # tableLayout.addWidget(scrollArea)
        # _________________________________________________________

        # Scrollable area for tables
        # self.tableScrollArea = QScrollArea()
        # self.tablesWidget = QWidget()
        # self.tablesLayout = QVBoxLayout(self.tablesWidget)
        # ______________________________________________________--
        # Position checkboxes in the top right corner
        tableLayout.addWidget(scrollArea, 0, 1, 1, 1)  # Specify row, column, row span, and column span

        # Scrollable area for tables
        self.tableScrollArea = QScrollArea()
        self.tablesWidget = QWidget()
        self.tablesLayout = QVBoxLayout(self.tablesWidget)

        self.tables = {
            "AUDUSD": self.createTableWidget(["AUD/USD", "ML Prediction", "H4 Supertrend Indicator"]),
            "EURUSD": self.createTableWidget(["EUR/USD", "ML Prediction", "H4 Supertrend Indicator"]),
            "NZDUSD": self.createTableWidget(["NZD/USD", "ML Prediction", "H4 Supertrend Indicator"]),
            "AUDNZD": self.createTableWidget(["AUD/NZD", "ML Prediction", "H4 Supertrend Indicator"]),
            "CADJPY": self.createTableWidget(["CAD/JPY", "ML Prediction", "H4 Supertrend Indicator"]),
            "NZDJPY": self.createTableWidget(["NZD/JPY", "ML Prediction", "H4 Supertrend Indicator"]),
            "GBPNZD": self.createTableWidget(["GBP/NZD", "ML Prediction", "H4 Supertrend Indicator"]),
            "GBPUSD": self.createTableWidget(["GBP/USD", "ML Prediction", "H4 Supertrend Indicator"]),
            "GBPJPY": self.createTableWidget(["GBP/JPY", "ML Prediction", "H4 Supertrend Indicator"]),
            "GBPCAD": self.createTableWidget(["GBP/CAD", "ML Prediction", "H4 Supertrend Indicator"]),
            "EURCAD": self.createTableWidget(["EUR/CAD", "ML Prediction", "H4 Supertrend Indicator"]),
            "EURJPY": self.createTableWidget(["EUR/JPY", "ML Prediction", "H4 Supertrend Indicator"]),

        }

        self.tablesWidget.setLayout(self.tablesLayout)
        self.tableScrollArea.setWidget(self.tablesWidget)
        self.tableScrollArea.setWidgetResizable(True)
        tableLayout.addWidget(self.tableScrollArea)

        # Position tables on the left side
        tableLayout.addWidget(self.tableScrollArea, 0, 0, 1, 1)  # Specify row, column, row span, and column span

        # Add views to the stacked widget
        self.centralWidget.addWidget(chatbotView) # 0
        self.centralWidget.addWidget(settingsView) # 1
        self.centralWidget.addWidget(aboutView) # 2

        self.centralWidget.addWidget(self.tableView) # 3  Add table view to central widget
        primary_dashboard_view = self.setupUI(view_active=True)
        #
        self.centralWidget.addWidget(primary_dashboard_view) # 4

    def createCard(self, widget, title):
        groupBox = QGroupBox(title)
        groupBox.setFont(QFont('Arial', 12))
        layout = QVBoxLayout()
        layout.addWidget(widget)
        groupBox.setLayout(layout)
        return groupBox


    def setupUI(self, view_active=None):
        # Main Layout
        primary_dash_view = QWidget()

        mainLayout = QVBoxLayout(primary_dash_view)

        # mainLayout = QVBoxLayout(self)
        scrollArea = QScrollArea()
        scrollArea.setWidgetResizable(True)
        scrollWidget = QWidget()
        scrollLayout = QVBoxLayout(scrollWidget)
        scrollArea.setWidget(scrollWidget)
        mainLayout.addWidget(scrollArea)

        # Dropdown for asset selection
        self.assetComboBox = QComboBox()
        self.assetComboBox.addItems(["Bitcoin", "Ethereum", "Gold", "All Assets"])
        self.assetComboBox.currentTextChanged.connect(self.updateDashboard)
        scrollLayout.addWidget(self.assetComboBox)

        # Scroll Area for asset status
        self.scrollArea = QScrollArea()
        self.scrollArea.setWidgetResizable(True)
        self.scrollWidget = QWidget()
        self.scrollLayout = QHBoxLayout(self.scrollWidget)

        # Asset Details Card
        self.assetDetails = QGroupBox("Asset Details")
        self.assetDetails.setFont(QFont('Arial', 12))
        self.detailsLayout = QVBoxLayout()
        self.assetDetails.setLayout(self.detailsLayout)
        scrollLayout.addWidget(self.assetDetails)

        self.scrollArea.setWidget(self.scrollWidget)
        scrollLayout.addWidget(self.createCard(self.scrollArea, "Assets Status Overview"))

        if  view_active == True :
            return primary_dash_view


    def updateDashboard(self, asset):
        if asset == "All Assets":
            self.updateStatusView()
        else:
            # Clear previous asset details and scroll area content
            for i in reversed(range(self.detailsLayout.count())):
                self.detailsLayout.itemAt(i).widget().setParent(None)
            for i in reversed(range(self.scrollLayout.count())):
                self.scrollLayout.itemAt(i).widget().setParent(None)

            # Show details and candlestick chart for the selected asset
            self.showAssetDetails(asset)

    def updateStatusView(self):
        # Setup columns for Buy and Sell
        buyLayout = QVBoxLayout()
        sellLayout = QVBoxLayout()

        # Create headers
        buyHeader = QLabel("BUY")
        buyHeader.setFixedSize(50, 30)  # Set absolute size for the header
        buyHeader.setStyleSheet(
            "background-color: green; color: white; font-size: 12px; padding: 5px; text-align: center;")
        buyLayout.addWidget(buyHeader)

        sellHeader = QLabel("SELL")
        sellHeader.setFixedSize(50, 30)  # Set absolute size for the header
        sellHeader.setStyleSheet(
            "background-color: red; color: white; font-size: 12px; padding: 5px; text-align: center;")
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

        # Get the asset details from the dictionary
        details = self.asset_data[asset]["details"]

        # Display the asset details
        symbol_name = self.asset_data[asset]["symbol"]
        detailLabel = QLabel(symbol_name)
        self.detailsLayout.addWidget(detailLabel)
        for detail in details:
            detailLabel = QLabel(detail)
            self.detailsLayout.addWidget(detailLabel)

        # Add candlestick chart
        self.addCandlestickChart(asset)

    def addCandlestickChart(self, asset):
        # Retrieve the candlestick data from the dictionary
        data = self.asset_data[asset]["candlestick"]

        # Create custom style with green and red colors
        mc = mpf.make_marketcolors(up='green', down='red', inherit=True)
        s = mpf.make_mpf_style(marketcolors=mc)

        # Create candlestick chart using mplfinance
        fig = Figure(figsize=(5, 3))
        ax = fig.add_subplot(111)
        mpf.plot(data, type='candle', ax=ax, style=s)

        # Add chart to the layout
        canvas = FigureCanvas(fig)

        # Add chart to the layout
        canvas = FigureCanvas(fig)
        self.detailsLayout.addWidget(canvas)

    def createTableWidget(self, pairs):

        tableWidget = QTableWidget(5, len(pairs))

        tableWidget.setHorizontalHeaderLabels(pairs)

        # tableWidget.setItem(0, 0, QTableWidgetItem(f"Date")) # Date first column
        # tableWidget.setItem(0, 1, QTableWidgetItem(f"ML Prediction")) # ML prediction second column
        # tableWidget.setItem(0, 2, QTableWidgetItem(f"H4 Supertrend Indicator")) # Hour 4 Supertrend third column
        # tableWidget.setItem(0, 1, QTableWidgetItem(f""))

        for i in range(0, 5 ):
            tableWidget.setItem(i, 0, QTableWidgetItem(f"{i + 20} July "))  # first column Date

        for i in range(0, 5 ):
            tableWidget.setItem(i, 1, QTableWidgetItem(f"{i}"))  # first column Date

        for i in range(0, 5 ):
            tableWidget.setItem(i, 2, QTableWidgetItem(f"{i}"))  # first column Date


        # Example data for table
        # for i in range(1, 5+1 ):
        #     for j in range(1, len(pairs) ):
        #         tableWidget.setItem(i, j, QTableWidgetItem(f"Data {i + 1}, {pairs[j]}"))


        tableWidget.setSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Fixed)
        tableWidget.setMaximumHeight(150)
        return tableWidget

    def showChatbotView(self):
        self.centralWidget.setCurrentIndex(0)

    def showSettingsView(self):

        self.centralWidget.setCurrentIndex(1)

    def showAboutView(self):
        self.centralWidget.setCurrentIndex(2)

    def showTableView(self):
        self.centralWidget.setCurrentIndex(3)

    def showPrimaryDashboardView(self):

        self.centralWidget.setCurrentIndex(4)


    def showTab(self):
        pass
    def updateTables(self):
        # Clear all tables
        for i in reversed(range(self.tablesLayout.count())):
            widget = self.tablesLayout.itemAt(i).widget()
            if widget is not None:
                widget.setParent(None)

        # Add selected tables
        for asset, checkbox in self.checkboxes.items():
            if checkbox.isChecked():
                self.tablesLayout.addWidget(self.tables[asset])

        self.tablesLayout.addStretch(1)

    def sendMessage(self, userInput, chatDisplay):
        message = userInput.text()
        if message.strip():  # Check if the message is not empty
            chatDisplay.append(f"You: {message}")
            chatDisplay.append(f"Bot: {self.getBotResponse(message)}")
            userInput.clear()  # Clear the input field after sending

    def getBotResponse(self, message):
        # Placeholder function to generate bot responses
        return "This is a response to your message."



    def asset_store(self):
        # Example data dictionary for assets
        self.asset_data = {
            "Bitcoin": {
                "details": ["Previous Day Status: Right", "Present Day ML Prediction: Buy", "Supertrend Status: Sell"
                            ],
                "symbol": "Bitcoin",
                "candlestick": pd.DataFrame({
                    'Date': pd.date_range('2023-08-01', periods=10),
                    'Open': [100, 102, 104, 103, 105, 107, 108, 109, 110, 108],
                    'High': [102, 104, 105, 106, 108, 109, 110, 111, 112, 110],
                    'Low': [98, 100, 103, 102, 104, 106, 107, 107, 109, 107],
                    'Close': [101, 103, 105, 104, 107, 108, 109, 110, 109, 108]
                }).set_index('Date')
            },
            "Ethereum": {
                "details": ["Previous Day Status: Neutral", "Present Day ML Prediction: Sell",
                            "Supertrend Status: Buy"],
                "symbol": "Ethereum",
                "candlestick": pd.DataFrame({
                    'Date': pd.date_range('2023-08-01', periods=10),
                    'Open': [200, 202, 204, 203, 205, 207, 208, 209, 210, 208],
                    'High': [202, 204, 205, 206, 208, 209, 210, 211, 212, 210],
                    'Low': [198, 200, 203, 202, 204, 206, 207, 207, 209, 207],
                    'Close': [201, 203, 205, 204, 207, 208, 209, 210, 209, 208]
                }).set_index('Date')
            },
            "Gold": {
                "details": ["Previous Day Status: Bullish", "Present Day ML Prediction: Hold",
                            "Supertrend Status: Buy"],
                "symbol": "Gold",
                "candlestick": pd.DataFrame({
                    'Date': pd.date_range('2023-08-01', periods=10),
                    'Open': [1800, 1802, 1804, 1803, 1805, 1807, 1808, 1809, 1810, 1808],
                    'High': [1802, 1804, 1805, 1806, 1808, 1809, 1810, 1811, 1812, 1810],
                    'Low': [1798, 1800, 1803, 1802, 1804, 1806, 1807, 1807, 1809, 1807],
                    'Close': [1801, 1803, 1805, 1804, 1807, 1808, 1809, 1810, 1809, 1808]
                }).set_index('Date')
            }
        }


if __name__ == '__main__':
    import sys

    app = QApplication(sys.argv)
    app.setStyle(QStyleFactory.create("Fusion"))  # Set the Fusion style
    chatbotApp = ChatbotApp()
    chatbotApp.show()
    sys.exit(app.exec())
