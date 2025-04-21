import re
from PyQt5.QtCore import QObject, pyqtSignal, QThread, QTimer, Qt, QMetaObject

# Worker to get a response in the background
class ResponseWorker(QObject):
    finished = pyqtSignal(str)

    # Class constructor
    def __init__(self, prompt, get_response_func, current_html, update_thinking_func):
        super().__init__()
        self.prompt = prompt
        self.get_response_func = get_response_func
        self.current_html = current_html
        self.update_thinking_func = update_thinking_func
        self.dot_count = 0

    # Gets a response from the model and emits it
    def run(self):
        if self.get_response_func:
            response = self.get_response_func(self.prompt)
        else:
            response = "something went wrong."
        self.finished.emit(response)

    # Updates the dots in the "Thinking..." text to animate
    def update_thinking(self):
        self.dot_count = (self.dot_count + 1) % 4
        dots = "." * self.dot_count
        self.update_thinking_func(dots)

# Gets the model to generate a response based on the prompt and update the response area
def process_response(response_area_textbox, prompt, get_response_func):
    # Show temporary "Thinking..." text
    full_message = (
        f'<b>{prompt.replace("\n", "<br>")}</b><br><br>'
        f'<i>Thinking...</i><br><br>'
    )
    response_area_textbox.append(full_message)
    response_area_textbox.moveCursor(response_area_textbox.textCursor().End)
    #save current html so we can replace "Thinking..." later
    current_html = response_area_textbox.toHtml() 
    
    # Updates the "Thinking..." text in the response area
    def update_thinking_func(dots):
        def update():
            match = re.search(r'Thinking\.{0,3}', worker.current_html)
            if match:
                block_to_replace = match.group(0)
                updated_html = worker.current_html.replace(block_to_replace, f'Thinking{dots}')
                response_area_textbox.setHtml(updated_html)
        
        QMetaObject.invokeMethod(response_area_textbox, update, Qt.QueuedConnection)

    # Create worker and thread
    worker = ResponseWorker(prompt, get_response_func, current_html, update_thinking_func)
    thread = QThread()
    worker.moveToThread(thread)

    timer = QTimer()
    timer.setInterval(500)
    timer.timeout.connect(worker.update_thinking)
    timer.start()

    # Updates the response area textbox once the worker has finished getting a response
    def on_finished(response):
        response_html = response.replace("\n", "<br>")
        html = worker.current_html

        # Find "Thinking..." including italics tags
        pattern_to_replace = re.compile(r'(<span[^>]*?>Thinking\.\.\.</span>|<i[^>]*?>Thinking\.\.\.</i>)', re.IGNORECASE)
        match = pattern_to_replace.search(html)

        # Replace "Thinking..." with actual response
        if match:
            block_to_replace = match.group(0)
            updated_html = html.replace(block_to_replace, response_html)
        else:
            updated_html = updated_html.replace('Thinking...', response.replace("\n", "<br>"))

        response_area_textbox.setHtml(updated_html)
        timer.stop()
        thread.quit()
        thread.wait()
        worker.deleteLater()
        thread.deleteLater()

    worker.finished.connect(on_finished)
    thread.started.connect(worker.run)
    thread.start()