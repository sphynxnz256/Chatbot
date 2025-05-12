from PyQt5.QtCore import pyqtSignal, QTimer, QRunnable, QObject

class ResponseSignals(QObject):
    finished = pyqtSignal(str)
    update_thinking = pyqtSignal(str)

# Handles the timer for updating the Thinking... text
class ThinkingTimerController:
    def __init__(self, update_thinking_text_func):
        self.timer = QTimer()
        self.timer.setInterval(500)
        self.update_thinking_text_func = update_thinking_text_func
        self.timer.timeout.connect(self.update_thinking)
        self.dot_count = 0
        self.signals = ResponseSignals()

    def start(self):
        self.timer.start()
    
    def stop(self):
        self.timer.stop()

    # Updates the dots in the "Thinking..." text to animate
    def update_thinking(self):
        self.dot_count = (self.dot_count + 1) % 4
        dots = "."*self.dot_count
        self.signals.update_thinking.emit(dots)

# Worker to get a response in the background
class ResponseWorker(QRunnable):    

    def __init__(self, prompt, get_response_func, current_html, thinking_timer):
        super().__init__()
        self.prompt = prompt
        self.get_response_func = get_response_func
        self.current_html = current_html
        self.thinking_timer = thinking_timer
        self.signals = ResponseSignals()        

    # Gets a response from the model and emits it
    def run(self):
        if self.get_response_func:
            response = self.get_response_func(self.prompt)
        else:
            response = "something went wrong."
  
        self.signals.finished.emit(response)