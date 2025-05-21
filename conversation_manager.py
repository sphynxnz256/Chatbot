import json
from database import save_conversation, update_conversation, fetch_all_conversation_titles, fetch_single_conversation, delete_conversation
from hover_button import HoverButton
from PyQt5.QtGui import QFont
from PyQt5.QtCore import pyqtSignal, QObject
from PyQt5.QtWidgets import QWidget, QHBoxLayout
from model import model_manager


class ConversationManagerSignals(QObject):
    button_created = pyqtSignal(object)

class ConversationManager:
    _instance = None

    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = super(ConversationManager, cls).__new__(cls, *args, **kwargs)
            return cls._instance

    def __init__(self):
        if hasattr(self, '_initialized') and self._initialized:
            return
        self._initialized = True

        self._is_first_message = True
        self._current_conversation_id = None
        self.buttons = []
        self.signals = ConversationManagerSignals()

    # Gets is first message status
    def is_first_message(self):
        return  self._is_first_message
    
    # Sets is first message to false (once conversation is added to db)
    def mark_first_message_processed(self):
        self._is_first_message = False

    # Sets is first message to true (when we start a new conversation)
    def reset_conversation_state(self):
        self._is_first_message = True
        model_manager.clear_history()

    # Create a button for a conversation
    def create_conversation_buttons(self, conversation_id, title, response_area_textbox, parent_layout):
        buttons_widget = QWidget()
        buttons_layout = QHBoxLayout()
        buttons_layout.setSpacing(0)
        buttons_layout.setContentsMargins(0, 0, 0, 0)

        load_button = HoverButton(title)
        load_button.setFont(QFont("Arial", 12))
        load_button.setToolTip("<font color='#999999'>Load</font>")
        load_button.clicked.connect(lambda: self.load_conversation(conversation_id, response_area_textbox))
        buttons_layout.addWidget(load_button, 1)

        delete_button = HoverButton("-")
        delete_button.setFont(QFont("Arial", 12))
        delete_button.setToolTip("<font color='#999999'>Delete<font>")
        delete_button.clicked.connect(lambda: self.remove_conversation(conversation_id, parent_layout, response_area_textbox))
        buttons_layout.addWidget(delete_button, 0)

        buttons_widget.setLayout(buttons_layout)
        buttons_widget.conversation_id = conversation_id
        self.buttons.append(buttons_widget)        
        return buttons_widget

    # Creates a new conversation entry in the db
    def save_initial_message(self, prompt, response_area_textbox, parent_layout):
        title = prompt[:15] + "..." if len(prompt) > 15 else prompt
        conversation_content = response_area_textbox.toHtml()
        model_history = json.dumps(model_manager.get_history())
        conversation_id = save_conversation(title, conversation_content, model_history)
        self._current_conversation_id = conversation_id
        button = self.create_conversation_buttons(conversation_id, title, response_area_textbox, parent_layout)
        self.signals.button_created.emit(button)
        return conversation_id

    # Updates the current conversation in the db
    def update_conversation_history(self, response_area_textbox):
        if self._current_conversation_id is not None:
            conversation_content = response_area_textbox.toHtml()
            model_history = json.dumps(model_manager.get_history())
            update_conversation(self._current_conversation_id, conversation_content, model_history)

    # Creates buttons for each conversation.
    def get_conversation_buttons(self, response_area_textbox, parent_layout):
        if not self.buttons:
            conversations = fetch_all_conversation_titles()
            if not conversations:
                return self.buttons
            for conv_id, title in conversations:
                self.create_conversation_buttons(conv_id, title, response_area_textbox, parent_layout)
        return self.buttons

    # Loads a conversation from the database
    def load_conversation(self, conversation_id, response_area_textbox):
        current_content, model_history_json = fetch_single_conversation(conversation_id)
        response_area_textbox.clear()
        response_area_textbox.setHtml(current_content)
        self._current_conversation_id = conversation_id
        model_manager.set_history(json.loads(model_history_json))
        self._is_first_message = False

    # Removes a conversation from the database and its associated buttons
    def remove_conversation(self, conversation_id, parent_layout, response_area_textbox):
        delete_conversation(conversation_id)

        # Find the buttons_widget to delete
        buttons_to_remove = None
        for buttons_widget in self.buttons:
            if hasattr(buttons_widget, 'conversation_id') and buttons_widget.conversation_id == conversation_id:
                buttons_to_remove = buttons_widget
                break

        # Remove the buttons
        if buttons_to_remove:
            self.buttons.remove(buttons_to_remove)
            parent_layout.removeWidget(buttons_to_remove)
            buttons_to_remove.deleteLater()

        if self._current_conversation_id == conversation_id:
            response_area_textbox.clear()
            self.reset_conversation_state()
            self._current_conversation_id = None
# Create a single instance of the ConversationManager
conversation_manager = ConversationManager()

