from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import (QApplication, QVBoxLayout, QHBoxLayout, QPushButton,
                             QDialog, QLabel, QLineEdit, QStackedWidget,
                             QWidget, QSizePolicy, QStyleFactory, QScrollArea)


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

        # Create a scroll area for chat display
        chatScroll = QScrollArea()
        chatScroll.setWidgetResizable(True)

        # Create a widget to hold chat messages
        chatContainer = QWidget()
        self.chatLayout = QVBoxLayout(chatContainer)
        self.chatLayout.setAlignment(Qt.AlignmentFlag.AlignTop)

        chatScroll.setWidget(chatContainer)

        userInput = QLineEdit()
        userInput.setPlaceholderText("Type your message here...")

        # Connect the returnPressed signal to the sendMessage function
        userInput.returnPressed.connect(lambda: self.sendMessage(userInput))

        sendButton = QPushButton("Send")
        sendButton.clicked.connect(lambda: self.sendMessage(userInput))

        inputLayout = QHBoxLayout()
        inputLayout.addWidget(userInput)
        inputLayout.addWidget(sendButton)

        chatbotLayout.addWidget(chatScroll)
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

    def sendMessage(self, userInput):
        message = userInput.text()
        if message.strip():  # Check if the message is not empty
            self.addMessage("You", message, Qt.AlignmentFlag.AlignRight, user=True)
            bot_response = self.getBotResponse(message)
            self.addMessage("Bot", bot_response, Qt.AlignmentFlag.AlignLeft, user=False)
            userInput.clear()  # Clear the input field after sending

    def addMessage(self, sender, message, alignment, user):
        # Create a label for the message
        messageLabel = QLabel(f"{sender}: {message}")
        messageLabel.setWordWrap(True)  # Enable word wrap
        messageLabel.setTextInteractionFlags(Qt.TextInteractionFlag.TextSelectableByMouse)  # Make text selectable

        # Apply different styles for user and bot messages
        if user:
            messageLabel.setStyleSheet("""
                background-color: #008000; /* Emerald Green */
                border-radius: 15px;
                padding: 10px;
                color: white;
                """)
        else:
            messageLabel.setStyleSheet("""
                background-color: #808080; /* Gray */
                border-radius: 15px;
                padding: 10px;
                color: white;
                """)

        # Set size policy to expand and take available width, but not exceed it
        messageLabel.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Maximum)

        # Create a container for the message with proper alignment
        container = QWidget()
        containerLayout = QHBoxLayout(container)
        containerLayout.setContentsMargins(0, 0, 0, 0)  # Remove margins for a tighter fit
        containerLayout.addWidget(messageLabel)
        containerLayout.setAlignment(alignment)  # Align the message based on the sender

        # Ensure the container itself is expanding horizontally
        container.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Maximum)

        # Add the container to the chat layout
        self.chatLayout.addWidget(container)

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
