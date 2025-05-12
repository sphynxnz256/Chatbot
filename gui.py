from message_handler import process_response
import sys
import pywinstyles
from PyQt5.QtWidgets import QApplication, QMainWindow, QTextEdit, QPushButton, QVBoxLayout, QWidget, QHBoxLayout, QSizePolicy
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont
from theme import theme_manager
from placeholder_text_edit import PlaceholderTextEdit

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
    f"background-color: {theme_manager.TEXT_BG}; border: none; border-radius: 10px;" 
)
sidebar_layout = QVBoxLayout(sidebar_widget)
sidebar_layout.setContentsMargins(5, 5, 5, 5)
sidebar_layout.setSpacing(0)
main_layout.addWidget(sidebar_widget)

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

# Input area
input_widget = QWidget()
input_widget.setStyleSheet(f"background-color: {theme_manager.WINDOW_BG};")
input_layout = QVBoxLayout(input_widget)
input_layout.setContentsMargins(0, 0, 0, 0)
input_layout.setSpacing(0)

# Text box
user_input_textbox = PlaceholderTextEdit("Ask me anything")
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

    process_response(response_area_textbox, prompt, get_response_func)

send_button.clicked.connect(lambda: send_message)

# Show window and start event loop (for testing)
if __name__ == "__main__":
    window.show()
    sys.exit(app.exec_())