from database import save_conversation, update_conversation

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

    # Gets is first message status
    def is_first_message(self):
        return  self._is_first_message
    
    # Sets is first message to false (once conversation is added to db)
    def mark_first_message_processed(self):
        self._is_first_message = False

    # Sets is first message to true (when we start a new conversation)
    def reset_conversation_state(self):
        self._is_first_message = True

    # Creates a new conversation entry in the db
    def save_initial_message(self, prompt, response):
        title = prompt[:20] + "..." if len(prompt) > 20 else prompt
        conversation_content = f"User: {prompt}\nAssistant: {response}"
        conversation_id = save_conversation(title, conversation_content)
        self._current_conversation_id = conversation_id
        return conversation_id
    
    # Updates the current conversation in the db
    def update_conversation_history(self, prompt, response):
        if self._current_conversation_id is not None:
            conversation_content = f"User: {prompt}\nAssistant: {response}"
            update_conversation(self._current_conversation_id, conversation_content)
        

# Create a single instance of the ConversationManager
conversation_manager = ConversationManager()