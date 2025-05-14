import re
from PyQt5.QtCore import QThreadPool
from async_utils import ThinkingTimerController, ResponseWorker
from conversation_manager import conversation_manager

# Gets the model to generate a response based on the prompt and update the response area
def process_response(response_area_textbox, prompt, get_response_func):
    # Show temporary "Thinking..." text
    full_message = (
        f'<b>{prompt.replace("\n", "<br>")}</b><br><br>'
        f'<i>Thinking</i><br><br>')
    response_area_textbox.append(full_message)
    response_area_textbox.verticalScrollBar().setValue(response_area_textbox.verticalScrollBar().maximum())
    #save current html so we can replace "Thinking..." later
    current_html = response_area_textbox.toHtml()

    # Temporary worker container (so we can use it inside inner functions)
    worker = None

        # Updates the "Thinking..." text in the response area
    def update_thinking_text(dots):
        match = re.search(r'Thinking\.{0,3}', worker.current_html)
        if match:
            updated_html = worker.current_html.replace(match.group(0), f'Thinking{dots}')
            response_area_textbox.setHtml(updated_html)
            response_area_textbox.verticalScrollBar().setValue(response_area_textbox.verticalScrollBar().maximum())
            worker.current_html = updated_html

    # Updates the response area textbox once the worker has finished getting a response
    def on_finished(response):
        response_html = response.replace("\n", "<br>")
        html = current_html
        thinking_timer.stop()

        # Find "Thinking..." including italics tags
        pattern_to_replace = re.compile(r'(<span[^>]*?>Thinking\.{0,3}</span>|<i[^>]*?>Thinking\.{0,3}</i>)', re.IGNORECASE)
        match = pattern_to_replace.search(html)

        # Replace "Thinking..." with actual response
        if match:
            updated_html = html.replace(match.group(0), response_html)
        else:
            updated_html = updated_html.replace('Thinking...', response.replace("\n", "<br>"))

        response_area_textbox.setHtml(updated_html)
        response_area_textbox.verticalScrollBar().setValue(response_area_textbox.verticalScrollBar().maximum())
        
        # If first prompt/response, create a new conversation in database
        if conversation_manager.is_first_message():
            conversation_manager.save_initial_message(prompt, response)
            conversation_manager.mark_first_message_processed()

    # Create thinking timer instance for thinking animation
    thinking_timer = ThinkingTimerController(update_thinking_text)
    thinking_timer.signals.update_thinking.connect(update_thinking_text)
    thinking_timer.start()

    # Create the response worker and connect the finished signal
    worker = ResponseWorker(prompt, get_response_func, current_html, thinking_timer)
    worker.signals.finished.connect(on_finished)
    QThreadPool.globalInstance().start(worker)