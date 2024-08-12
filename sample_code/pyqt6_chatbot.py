from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import (QApplication, QVBoxLayout, QHBoxLayout, QPushButton,
                             QDialog, QLabel, QTextEdit, QLineEdit, QStackedWidget,
                             QWidget, QSizePolicy, QStyleFactory, QTableWidget, QTableWidgetItem,
                             QScrollArea, QCheckBox, QGridLayout)


class ChatbotApp(QDialog):
    def __init__(self, parent=None):
        super(ChatbotApp, self).__init__(parent)

        # Create the main layout
        mainLayout = QHBoxLayout()



        # topBarLayout = QHBoxLayout()
        # mainLayout.addStretch(1)
        # mainLayout.addWidget(self.fullscreenButton)



        # Create sidebar
        self.sidebar = self.createSidebar()
        mainLayout.addLayout(self.sidebar)

        # Create central view manager
        self.centralWidget = QStackedWidget()  # Main Window

        mainLayout.addWidget(self.centralWidget)


        # Create views
        self.createViews()

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



        # Add checkboxes for assets
        # assets = ["AUDUSD", "EURUSD", "NZDUSD", "AUDNZD", "CADJPY","NZDJPY", "GBPNZD",
        #           "GBPUSD", "GBPJPY", "GBPCAD", "EURCAD", "EURJPY","AUDCAD", "EURNZD", "USDCAD", "USDJPY"
        #           "NZDUSD", "AUDJPY", ""]

        assets = [
            'AUDCAD', 'AUDCHF', 'AUDJPY', 'AUDNZD', 'AUDUSD',
            'CADCHF', 'CADJPY',
            'CHFJPY',  # 'CHFSGD=X', 'EURSGD=X',  'EURTRY=X', 'SGDUSD=X', , 'AUDSGD=X'
            'EURAUD', 'EURCAD', 'EURCHF', 'EURGBP', 'EURJPY', 'EURNZD', 'EURUSD',
            'GBPAUD', 'GBPCAD', 'GBPCHF', 'GBPJPY', 'GBPUSD', 'GBPNZD',  # 'GBPSGD=X'
            'NZDCAD', 'NZDCHF', 'NZDJPY', 'NZDUSD',  # 'NZDSGD=X',
            'USDCHF', 'USDCAD', 'USDJPY'  # , 'USDTRY=X'
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
        self.centralWidget.addWidget(aboutView) # 3
        self.centralWidget.addWidget(self.tableView)  # Add table view to central widget

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


if __name__ == '__main__':
    import sys

    app = QApplication(sys.argv)
    app.setStyle(QStyleFactory.create("Fusion"))  # Set the Fusion style
    chatbotApp = ChatbotApp()
    chatbotApp.show()
    sys.exit(app.exec())
