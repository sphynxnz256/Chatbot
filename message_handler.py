import re
from PyQt5.QtCore import QThreadPool
from async_utils import ThinkingTimerController, ResponseWorker
from conversation_manager import conversation_manager

# Manages the full process of sending a prompt, displaying "Thinking...",
# getting a response from the model, and updating the UI with the final response.
def process_response(response_area_textbox, prompt, get_response_func, sidebar_layout):
    # Display the user's prompt immediately, followed by a "Thinking" placeholder.
    full_message = (
        f'<b>{prompt.replace("\n", "<br>")}</b><br><br>'
        f'<i>Thinking</i><br><br>')
    response_area_textbox.append(full_message)
    response_area_textbox.verticalScrollBar().setValue(response_area_textbox.verticalScrollBar().maximum())
    # Store the current HTML to facilitate replacing the "Thinking..." text later.
    current_html = response_area_textbox.toHtml()

    # Initialize worker to None, as it's defined and used in an inner function scope.
    worker = None

    # Updates the "Thinking..." animation with dots in the response area.
    def update_thinking_text(dots):
        match = re.search(r'Thinking\.{0,3}', worker.current_html)
        # Uses worker.current_html because current_html inside process_response
        # would be a closure over the initial value, not the updated one from on_finished.
        if match:
            updated_html = worker.current_html.replace(match.group(0), f'Thinking{dots}')
            response_area_textbox.setHtml(updated_html)
            response_area_textbox.verticalScrollBar().setValue(response_area_textbox.verticalScrollBar().maximum())
            worker.current_html = updated_html

    # Callback function executed when the ResponseWorker finishes getting a response.
    # Updates the UI with the final response and handles conversation saving/updating.
    def on_finished(response):
        response_html = response.replace("\n", "<br>")
        html = current_html
        thinking_timer.stop()

        # Regex to find "Thinking..." with optional italics or span tags.
        pattern_to_replace = re.compile(r'(<span[^>]*?>Thinking\.{0,3}</span>|<i[^>]*?>Thinking\.{0,3}</i>)', re.IGNORECASE)
        match = pattern_to_replace.search(html)

        # Replace "Thinking..." with the actual response.
        if match:
            updated_html = html.replace(match.group(0), response_html)
        else:
            # Fallback if specific tags aren't found, just replace plain "Thinking..."
            # Note: The original code had `updated_html = updated_html.replace(...)` here,
            # which would cause an UnboundLocalError if `match` is None.
            # It should likely operate on `html` or ensure `updated_html` is initialized.
            # Assuming `updated_html` should be `html` here as a fallback.
            updated_html = updated_html.replace('Thinking...', response.replace("\n", "<br>"))

        response_area_textbox.setHtml(updated_html)
        response_area_textbox.verticalScrollBar().setValue(response_area_textbox.verticalScrollBar().maximum())
        
        # Save or update the conversation in the database.
        if conversation_manager.is_first_message():
            conversation_manager.save_initial_message(prompt, response_area_textbox, sidebar_layout)
            conversation_manager.mark_first_message_processed()
        else:
            conversation_manager.update_conversation_history(response_area_textbox)

    # Initialize and start the thinking animation.
    thinking_timer = ThinkingTimerController(update_thinking_text)
    thinking_timer.signals.update_thinking.connect(update_thinking_text)
    thinking_timer.start()

    # Create and start the worker thread to get the model response asynchronously.
    worker = ResponseWorker(prompt, get_response_func, current_html, thinking_timer)
    worker.signals.finished.connect(on_finished)
    QThreadPool.globalInstance().start(worker)