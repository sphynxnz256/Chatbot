import sys
from gui import send_message, send_button, app, window
from model import generate_response

def main():
    # Connect GUI to model
    send_button.clicked.disconnect()
    send_button.clicked.connect(lambda: send_message(generate_response))
    window.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()