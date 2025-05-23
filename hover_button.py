from PyQt5.QtWidgets import QPushButton
from PyQt5.QtCore import Qt
from theme import theme_manager

# A custom QPushButton that changes its background color only when the mouse hovers over it.
class HoverButton(QPushButton):
    def __init__(self, text, *args, **kwargs):
        super().__init__(text, *args, **kwargs)
        self.hover = False
        self.setStyleSheet(f"border: none; color: {theme_manager.TEXT_COLOR};"
                           "background-color: transparent; padding: 5px 10px; text-align: left; margin: 0px 0px 10px 0px;")
        self.setCursor(Qt.PointingHandCursor)

    # Handles the mouse entering the button area, changing its style.
    def enterEvent(self, event):
        if not self.hover:
            self.setStyleSheet(
                f"QPushButton {{background-color: {theme_manager.BUTTON_BG}; color: {theme_manager.TEXT_COLOR};" 
                f"border-radius: 5px; padding: 5px 10px; text-align: left; margin: 0px 0px 10px 0px;}}"
                f"QPushButton:pressed {{background-color: {theme_manager.BUTTON_PRESSED_BG};"
                f"border-radius: 5px; padding: 5px 10px; text-align: left;}}")
            self.hover = True
        super().enterEvent(event)

    # Handles the mouse leaving the button area, reverting its style.
    def leaveEvent(self, event):
        if self.hover:
            self.setStyleSheet(f"border: none; color: {theme_manager.TEXT_COLOR};"
                               "background-color: transparent; padding: 5px 10px; text-align: left; margin: 0px 0px 10px 0px;")
            self.hover = False
        super().leaveEvent(event)