from database import save_conversation

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

    def is_first_message(self):
        return  self._is_first_message
    
    def mark_first_message_processed(self):
        self._is_first_message = False

    def reset_conversation_state(self):
        self._is_first_message = True

    def save_initial_message(self, prompt, response):
        title = prompt[:20] + "..." if len(prompt) > 20 else prompt
        conversation_content = f"User: {prompt}\nAssistant: {response}"
        save_conversation(title, conversation_content)

# Create a single instance of the ConversationManager
conversation_manager = ConversationManager()