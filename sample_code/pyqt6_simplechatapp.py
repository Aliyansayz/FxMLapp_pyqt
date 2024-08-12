from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import (QApplication, QVBoxLayout, QHBoxLayout, QPushButton,
                             QDialog, QLabel, QTextEdit, QLineEdit, QStackedWidget,
                             QWidget, QSizePolicy, QStyleFactory)


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
        self.setGeometry(100, 100, 800, 600)  # Set window size and position

    def createSidebar(self):
        layout = QVBoxLayout()

        # Create buttons and connect them to switch views
        buttons = [
            ("Home", self.showChatbotView),
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

        # Add views to the stacked widget
        self.centralWidget.addWidget(chatbotView)
        self.centralWidget.addWidget(settingsView)
        self.centralWidget.addWidget(aboutView)

    def showChatbotView(self):
        self.centralWidget.setCurrentIndex(0)

    def showSettingsView(self):
        self.centralWidget.setCurrentIndex(1)

    def showAboutView(self):
        self.centralWidget.setCurrentIndex(2)

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
