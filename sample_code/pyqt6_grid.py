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

        # Create sidebar
        self.sidebar = self.createSidebar()
        mainLayout.addLayout(self.sidebar)

        # Create central view manager
        self.centralWidget = QStackedWidget()
        mainLayout.addWidget(self.centralWidget)

        # Create views
        self.createViews()

        self.setLayout(mainLayout)
        self.setWindowTitle("Chatbot Interface")
        self.setGeometry(100, 100, 1000, 600)  # Set window size and position

    def createSidebar(self):
        layout = QVBoxLayout()

        # Create buttons and connect them to switch views
        buttons = [
            ("Home", self.showChatbotView),
            ("Settings", self.showSettingsView),
            ("About", self.showAboutView),
            ("Table", self.showTableView)  # Add Table view button
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

        # About View
        aboutView = QWidget()
        aboutLayout = QVBoxLayout(aboutView)
        aboutLabel = QLabel("About Page")
        aboutLayout.addWidget(aboutLabel)

        # Table View
        self.tableView = QWidget()
        tableLayout = QGridLayout(self.tableView)  # Use QGridLayout

        # Scrollable area for checkboxes
        scrollArea = QScrollArea()
        scrollWidget = QWidget()
        scrollGridLayout = QGridLayout(scrollWidget)  # Use QGridLayout for positioning

        # Add "All symbols" checkbox
        self.allSymbolsCheckbox = QCheckBox("All symbols")
        self.allSymbolsCheckbox.stateChanged.connect(self.toggleAllCheckboxes)
        scrollGridLayout.addWidget(self.allSymbolsCheckbox, 0, 0)

        # Add checkboxes for assets
        assets = ["Bitcoin", "Ethereum", "Solana", "Binance", "Ripple",
                  "Cardano", "Polkadot", "Litecoin", "Stellar", "Chainlink"]

        self.checkboxes = {}

        maxPerRow = 2  # Define maximum checkboxes per row

        for index, asset in enumerate(assets):
            checkbox = QCheckBox(asset)
            checkbox.stateChanged.connect(self.updateTables)

            # Calculate the current row and column based on index
            row = index // maxPerRow + 1  # Start from the second row
            column = index % maxPerRow

            scrollGridLayout.addWidget(checkbox, row, column)
            self.checkboxes[asset] = checkbox

        scrollWidget.setLayout(scrollGridLayout)
        scrollArea.setWidget(scrollWidget)
        scrollArea.setWidgetResizable(True)

        # Position checkboxes in the top right corner
        tableLayout.addWidget(scrollArea, 0, 1, 1, 1)  # Specify row, column, row span, and column span

        # Scrollable area for tables
        self.tableScrollArea = QScrollArea()
        self.tablesWidget = QWidget()
        self.tablesLayout = QVBoxLayout(self.tablesWidget)

        self.tables = {
            "Bitcoin": self.createTableWidget(["BTC/USD", "BTC/EUR"]),
            "Ethereum": self.createTableWidget(["ETH/USD", "ETH/EUR"]),
            "Solana": self.createTableWidget(["SOL/USD", "SOL/EUR"]),
            "Binance": self.createTableWidget(["BNB/USD", "BNB/EUR"]),
            "Ripple": self.createTableWidget(["XRP/USD", "XRP/EUR"]),
            "Cardano": self.createTableWidget(["ADA/USD", "ADA/EUR"]),
            "Polkadot": self.createTableWidget(["DOT/USD", "DOT/EUR"]),
            "Litecoin": self.createTableWidget(["LTC/USD", "LTC/EUR"]),
            "Stellar": self.createTableWidget(["XLM/USD", "XLM/EUR"]),
            "Chainlink": self.createTableWidget(["LINK/USD", "LINK/EUR"]),
        }

        self.tablesWidget.setLayout(self.tablesLayout)
        self.tableScrollArea.setWidget(self.tablesWidget)
        self.tableScrollArea.setWidgetResizable(True)

        # Position tables on the left side
        tableLayout.addWidget(self.tableScrollArea, 0, 0, 1, 1)  # Specify row, column, row span, and column span

        # Add views to the stacked widget
        self.centralWidget.addWidget(chatbotView)
        self.centralWidget.addWidget(settingsView)
        self.centralWidget.addWidget(aboutView)
        self.centralWidget.addWidget(self.tableView)  # Add table view to central widget

    def createTableWidget(self, pairs):
        tableWidget = QTableWidget(5, len(pairs))
        tableWidget.setHorizontalHeaderLabels(pairs)

        # Example data for table
        for i in range(5):
            for j, pair in enumerate(pairs):
                tableWidget.setItem(i, j, QTableWidgetItem(f"Data {i + 1}, {pair}"))

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

    def toggleAllCheckboxes(self, state):
        checked = (state == Qt.CheckState.Checked)
        for checkbox in self.checkboxes.values():
            checkbox.setChecked(checked)

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
