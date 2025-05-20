from PyQt5.QtWidgets import QPushButton
from PyQt5.QtCore import Qt
from theme import theme_manager

# Creates a button that only shows the button background when mouse hovers over it
class HoverButton(QPushButton):
    def __init__(self, text, *args, **kwargs):
        super().__init__(text, *args, **kwargs)
        self.hover = False
        self.setStyleSheet(f"border: none; color: {theme_manager.TEXT_COLOR};"
                           "background-color: transparent; padding: 5px 10px; text-align: left; margin: 0px 0px 10px 0px;")
        self.setCursor(Qt.PointingHandCursor)

    # Handles event where mouse starts hovering over button
    def enterEvent(self, event):
        if not self.hover:
            self.setStyleSheet(
                f"QPushButton {{background-color: {theme_manager.BUTTON_BG}; color: {theme_manager.TEXT_COLOR};" 
                f"border-radius: 5px; padding: 5px 10px; text-align: left; margin: 0px 0px 10px 0px;}}"
                f"QPushButton:pressed {{background-color: {theme_manager.BUTTON_PRESSED_BG};"
                f"border-radius: 5px; padding: 5px 10px; text-align: left;}}")
            self.hover = True
        super().enterEvent(event)

    # Handles event where mouse stops hovering over button
    def leaveEvent(self, event):
        if self.hover:
            self.setStyleSheet(f"border: none; color: {theme_manager.TEXT_COLOR};"
                               "background-color: transparent; padding: 5px 10px; text-align: left; margin: 0px 0px 10px 0px;")
            self.hover = False
        super().leaveEvent(event)