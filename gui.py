import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QTextEdit, QPushButton, QVBoxLayout, QWidget, QHBoxLayout, QLabel, QSizePolicy
from PyQt5.QtCore import Qt
import pywinstyles

# Color scheme variables (night theme)
WINDOW_BG = "#1e1e1e"      # Dark gray for window and frames
TEXT_BG = "#2d2d2d"        # Slightly lighter gray for text areas
TEXT_FG = "#ffffff"        # White for text and cursor
BUTTON_BG = "#3c3c3c"      # Medium gray for button

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
response_area.setStyleSheet(f"background-color: {TEXT_BG}; color: {TEXT_FG}; border: none;")
main_layout.addWidget(response_area, stretch=1)

# Input area
input_widget = QWidget()
input_widget.setStyleSheet(f"background-color: {WINDOW_BG};")
input_layout = QVBoxLayout(input_widget)
input_layout.setContentsMargins(0, 0, 0, 0)
input_layout.setSpacing(0)

# Text box
user_input = QTextEdit()
user_input.setMinimumHeight(20)
user_input.setMaximumHeight(20)
user_input.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
user_input.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
user_input.document().documentLayout().documentSizeChanged.connect(
    lambda: user_input.setMaximumHeight(int(user_input.document().size().height() + 10))
)
user_input.setStyleSheet(f"background-color: {TEXT_BG}; color: {TEXT_FG}; border: none;")
input_layout.addWidget(user_input)

# Extention box
extention_box = QWidget()
extention_box.setStyleSheet(f"background-color: {TEXT_BG};")
extention_layout = QHBoxLayout(extention_box)
extention_layout.setContentsMargins(0, 0, 10, 10)
extention_layout.addStretch()
send_button = QPushButton("Send")
send_button.setFixedSize(80, 30)
send_button.setStyleSheet(f"background-color: {BUTTON_BG}; color: {TEXT_FG}; border: none;")
extention_layout.addWidget(send_button)
extention_box.setFixedHeight(40)
input_layout.addWidget(extention_box)

main_layout.addWidget(input_widget)

# Show window and start event loop
window.show()
sys.exit(app.exec_())
