import sys
import pywinstyles
from PyQt5.QtWidgets import QApplication, QMainWindow, QTextEdit, QPushButton, QVBoxLayout, QWidget, QHBoxLayout, QSizePolicy
from PyQt5.QtWidgets import QLabel, QFrame
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont
from message_handler import process_response
from conversation_manager import conversation_manager
from theme import theme_manager
from placeholder_text import PlaceholderText
from hover_button import HoverButton

# Mock model for standalone testing
if __name__ == "__main__":
    class MockModel:
        conversation_history = []
    model = MockModel()
else:
    import model

# Create application
app = QApplication(sys.argv)

# Create main window
window = QMainWindow()
window.setGeometry(0, 0, 800, 600)
window.setWindowTitle("Chatbot")
pywinstyles.apply_style(window, "dark")


# Central widget and main layout
central_widget = QWidget()
window.setCentralWidget(central_widget)
central_widget.setStyleSheet(f"background-color: {theme_manager.WINDOW_BG};")
main_layout = QHBoxLayout(central_widget)
main_layout.setSpacing(10)

# Sidebar for conversations (left side)
sidebar_widget = QWidget()
sidebar_widget.setFixedWidth(200)
sidebar_widget.setStyleSheet(
    f"background-color: {theme_manager.TEXT_BG}; border: none; border-radius: 10px; padding: 5px;" 
)
sidebar_layout = QVBoxLayout(sidebar_widget)
sidebar_layout.setContentsMargins(5, 5, 5, 5)
sidebar_layout.setSpacing(0)
sidebar_layout.setAlignment(Qt.AlignTop)
main_layout.addWidget(sidebar_widget)

# Chatbot Name Label
chatbot_name_label = QLabel("Chatbot")
chatbot_name_label.setStyleSheet(f"color: {theme_manager.TEXT_COLOR};")
chatbot_name_label.setFont(QFont("Arial", 28, QFont.Bold))
sidebar_layout.addWidget(chatbot_name_label)

# New Chat button
new_chat_button = HoverButton("+ New Chat")
new_chat_button.setFont(QFont("Arial", 12))
sidebar_layout.addWidget(new_chat_button)

# Add a divider between new chat button and the conversation buttons
divider = QFrame()
divider.setFrameShape(QFrame.HLine)
divider.setStyleSheet(f"background-color: {theme_manager.TEXT_COLOR}; margin: 0px 20px")
divider.setFixedHeight(2)
sidebar_layout.addSpacing(10)
sidebar_layout.addWidget(divider)
sidebar_layout.addSpacing(10)

# Chat area container (right side)
chat_area_widget = QWidget()
chat_area_layout = QVBoxLayout(chat_area_widget)
chat_area_layout.setContentsMargins(0, 0, 0, 0)
chat_area_layout.setSpacing(10)

# Response area
response_area_textbox = QTextEdit()
response_area_textbox.setReadOnly(True)
response_area_textbox.setStyleSheet(
    f"background-color: {theme_manager.TEXT_BG}; color: {theme_manager.TEXT_COLOR}; border: none; border-radius: 10px;"
    f"padding: 5px;")
response_area_textbox.setFont(QFont("Arial", 12))
chat_area_layout.addWidget(response_area_textbox, stretch=1)

# Add conversation buttons
for buttons in conversation_manager.get_conversation_buttons(response_area_textbox, sidebar_layout):
    sidebar_layout.addWidget(buttons)

# Input area
input_widget = QWidget()
input_widget.setStyleSheet(f"background-color: {theme_manager.WINDOW_BG};")
input_layout = QVBoxLayout(input_widget)
input_layout.setContentsMargins(0, 0, 0, 0)
input_layout.setSpacing(0)

# Text box
user_input_textbox = PlaceholderText("Ask me anything")
user_input_textbox.setMinimumHeight(30)
user_input_textbox.setMaximumHeight(30)
user_input_textbox.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
user_input_textbox.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
user_input_textbox.document().documentLayout().documentSizeChanged.connect(
    lambda: user_input_textbox.setMaximumHeight(int(user_input_textbox.document().size().height() + 10)))
user_input_textbox.setStyleSheet(
    f"background-color: {theme_manager.TEXT_BG}; color: {theme_manager.PLACEHOLDER_COLOR}; border: none;"
    f"border-top-left-radius: 10px; border-top-right-radius: 10px;"
    f"padding: 5px;")
user_input_textbox.setFont(QFont("Arial", 12))
input_layout.addWidget(user_input_textbox)

# Extention box
extension_box = QWidget()
extension_box.setStyleSheet(
    f"background-color: {theme_manager.TEXT_BG};"
    f"border-bottom-left-radius: 10px; border-bottom-right-radius: 10px;")
extension_layout = QHBoxLayout(extension_box)
extension_layout.setContentsMargins(0, 0, 10, 10)
extension_layout.addStretch()
send_button = QPushButton("Send")
send_button.setFixedSize(70, 30)
send_button.setFont(QFont("Arial", 12))
send_button.setStyleSheet(
    f"QPushButton {{ background-color: {theme_manager.BUTTON_BG}; color: {theme_manager.TEXT_COLOR}; border: none; border-radius: 5px;}}"
    f"QPushButton:pressed {{ background-color: {theme_manager.BUTTON_PRESSED_BG}; border-radius: 5px;}}")
extension_layout.addWidget(send_button)
extension_box.setFixedHeight(40)
input_layout.addWidget(extension_box)

chat_area_layout.addWidget(input_widget)
main_layout.addWidget(chat_area_widget)

# Send button functionality
def send_message(get_response_func=None):
    # Get user input
    prompt = user_input_textbox.toPlainText().strip()
    if not prompt: # Skip if empty
        return    
    
    # Reset input box
    user_input_textbox.clear()
    user_input_textbox.setMaximumHeight(30)

    process_response(response_area_textbox, prompt, get_response_func, sidebar_layout)

send_button.clicked.connect(lambda: send_message)

# New Chat button function. resets the conversation and clears the window
def reset_chat():
    response_area_textbox.clear()
    model.conversation_history = []
    conversation_manager.reset_conversation_state()

new_chat_button.clicked.connect(reset_chat)

def add_conversation_button(button):
    sidebar_layout.addWidget(button)

conversation_manager.signals.button_created.connect(add_conversation_button)

# Show window and start event loop (for testing)
if __name__ == "__main__":
    window.show()
    sys.exit(app.exec_())