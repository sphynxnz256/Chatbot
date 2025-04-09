import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QTextEdit, QPushButton, QVBoxLayout, QWidget, QHBoxLayout, QSizePolicy
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont
import pywinstyles

# Color scheme variables (night theme)
WINDOW_BG = "rgb(30, 30, 30)"           # Dark gray
TEXT_BG = "rgb(45, 45, 45)"             # Slightly lighter gray
TEXT_FG = "rgb(255, 255, 255)"          # White
BUTTON_BG = "rgb(60, 60, 60)"           # Medium gray
BUTTON_PRESSED_BG = "rgb(55, 55, 55)"   # Slightly darker gray for pressed state
PROMPT_BG = "rgb(60, 60, 60)"           # Lighter gray for prompt box


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
central_widget.setStyleSheet(f"background-color: {WINDOW_BG};")
main_layout = QVBoxLayout(central_widget)

# Response area
response_area = QTextEdit()
response_area.setReadOnly(True)
response_area.setStyleSheet(
    f"background-color: {TEXT_BG}; color: {TEXT_FG}; border: none; border-radius: 10px;"
    f"padding: 5px;"
)
response_area.setFont(QFont("Arial", 12))
main_layout.addWidget(response_area, stretch=1)

# Input area
input_widget = QWidget()
input_widget.setStyleSheet(f"background-color: {WINDOW_BG};")
input_layout = QVBoxLayout(input_widget)
input_layout.setContentsMargins(0, 0, 0, 0)
input_layout.setSpacing(0)

# Text box
user_input = QTextEdit()
user_input.setMinimumHeight(30)
user_input.setMaximumHeight(30)
user_input.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
user_input.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
user_input.document().documentLayout().documentSizeChanged.connect(
    lambda: user_input.setMaximumHeight(int(user_input.document().size().height() + 10))
)
user_input.setStyleSheet(
    f"background-color: {TEXT_BG}; color: {TEXT_FG}; border: none;"
    f"border-top-left-radius: 10px; border-top-right-radius: 10px;"
    f"padding: 5px;"
)
user_input.setFont(QFont("Arial", 12))
input_layout.addWidget(user_input)

# Extention box
extension_box = QWidget()
extension_box.setStyleSheet(
    f"background-color: {TEXT_BG};"
    f"border-bottom-left-radius: 10px; border-bottom-right-radius: 10px;"
)
extension_layout = QHBoxLayout(extension_box)
extension_layout.setContentsMargins(0, 0, 10, 10)
extension_layout.addStretch()
send_button = QPushButton("Send")
send_button.setFixedSize(80, 30)
send_button.setStyleSheet(
    f"QPushButton {{ background-color: {BUTTON_BG}; color: {TEXT_FG}; border: none; border-radius: 5px;}}"
    f"QPushButton:pressed {{ background-color: {BUTTON_PRESSED_BG}; border-radius: 5px;}}"
)
extension_layout.addWidget(send_button)
extension_box.setFixedHeight(40)
input_layout.addWidget(extension_box)

main_layout.addWidget(input_widget)

# Send button functionality
def send_message():
    # Get user input
    prompt = user_input.toPlainText().strip()
    if not prompt: # Skip if empty
        return    
    
    # Reset input box
    user_input.clear()
    user_input.setMaximumHeight(30)

    # Add prompt as a full-width box with HTML
    prompt_with_breaks = prompt.replace("\n", "<br>")
    full_message = (
        f'<b>{prompt_with_breaks}</b><br><br><br>'
        f'This is a placeholder response to:<br>{prompt_with_breaks}<br><br>'
    )
    response_area.append(full_message)


send_button.clicked.connect(send_message)

# Show window and start event loop
window.show()
sys.exit(app.exec_())
