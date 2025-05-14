from PyQt5.QtWidgets import QTextEdit
from theme import theme_manager

# Adds placeholder text functionality to our the user text box
class PlaceholderText(QTextEdit):
    def __init__(self, placeholder, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.placeholder = placeholder

        self._showing_placeholder = True

        self.setText(self.placeholder)
        self.setStyleSheet(
            f"background-color: {theme_manager.TEXT_BG}; color: {theme_manager.PLACEHOLDER_COLOR}; border: none;"
            f"border-top-left-radius: 10px; border-top-right-radius: 10px;"
            f"padding: 5px;")
        self.installEventFilter(self)

    def focusInEvent(self, event):
        if self._showing_placeholder:
            self.clear()
            self.setStyleSheet(
                f"background-color: {theme_manager.TEXT_BG}; color: {theme_manager.TEXT_COLOR}; border: none;"
                f"border-top-left-radius: 10px; border-top-right-radius: 10px;"
                f"padding: 5px;")
            self._showing_placeholder = False
        super().focusInEvent(event)

    def focusOutEvent(self, event):
        if not self.toPlainText().strip():
            self.setText(self.placeholder)
            self.setStyleSheet(
                f"background-color: {theme_manager.TEXT_BG}; color: {theme_manager.PLACEHOLDER_COLOR}; border: none;"
                f"border-top-left-radius: 10px; border-top-right-radius: 10px;"
                f"padding: 5px;")
            self._showing_placeholder = True
        super().focusOutEvent(event)

    def get_text(self):
        return "" if self._showing_placeholder else self.toPlainText().strip()