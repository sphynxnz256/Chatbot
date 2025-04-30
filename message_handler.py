import re
from PyQt5.QtCore import QObject, pyqtSignal, QTimer, pyqtSlot, QRunnable, QThreadPool

class ResponseSignals(QObject):
    finished = pyqtSignal(str)
    update_thinking = pyqtSignal(str)

# Worker to get a response in the background
class ResponseWorker(QRunnable):    

    def __init__(self, prompt, get_response_func, current_html, update_thinking_text_func):
        super().__init__()
        self.prompt = prompt
        self.get_response_func = get_response_func
        self.current_html = current_html
        self.update_thinking_text_func = update_thinking_text_func
        self.dot_count = 0

        self.signals = ResponseSignals()
        self.signals.update_thinking.connect(self.update_thinking_text_func)

        self.timer = QTimer()
        self.timer.setInterval(500)
        self.timer.timeout.connect(self.update_thinking)
        self.timer.moveToThread(QTimer().thread())
        self.timer.start()

    # Gets a response from the model and emits it
    def run(self):
        if self.get_response_func:
            response = self.get_response_func(self.prompt)
        else:
            response = "something went wrong."
        self.timer.stop()
        self.signals.finished.emit(response)

    # Updates the dots in the "Thinking..." text to animate
    def update_thinking(self):
        self.dot_count = (self.dot_count + 1) % 4
        dots = "."*self.dot_count
        self.signals.update_thinking.emit(dots)

# Gets the model to generate a response based on the prompt and update the response area
def process_response(response_area_textbox, prompt, get_response_func):
    # Show temporary "Thinking..." text
    full_message = (
        f'<b>{prompt.replace("\n", "<br>")}</b><br><br>'
        f'<i>Thinking</i><br><br>'
    )
    response_area_textbox.append(full_message)
    response_area_textbox.moveCursor(response_area_textbox.textCursor().End)
    #save current html so we can replace "Thinking..." later
    current_html = response_area_textbox.toHtml() 
    
    # Updates the "Thinking..." text in the response area
    @pyqtSlot(str)
    def update_thinking_text(dots):
        match = re.search(r'Thinking\.{0,3}', worker.current_html)
        if match:
            updated_html = worker.current_html.replace(match.group(0), f'Thinking{dots}')
            response_area_textbox.setHtml(updated_html)
            worker.current_html = updated_html



    # Updates the response area textbox once the worker has finished getting a response
    def on_finished(response):
        response_html = response.replace("\n", "<br>")
        html = current_html

        # Find "Thinking..." including italics tags
        pattern_to_replace = re.compile(r'(<span[^>]*?>Thinking\.{0,3}</span>|<i[^>]*?>Thinking\.{0,3}</i>)', re.IGNORECASE)
        match = pattern_to_replace.search(html)

        # Replace "Thinking..." with actual response
        if match:
            updated_html = html.replace(match.group(0), response_html)
        else:
            updated_html = updated_html.replace('Thinking...', response.replace("\n", "<br>"))

        response_area_textbox.setHtml(updated_html)

    # Create worker and thread
    worker = ResponseWorker(prompt, get_response_func, current_html, update_thinking_text)
    worker.signals.finished.connect(on_finished)
    QThreadPool.globalInstance().start(worker)