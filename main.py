import sys
from gui import app, window

# Main entry point for the application.
# Connects the GUI's send button to the model's response generation and shows the main window.
def main():
    window.show() 
    sys.exit(app.exec_()) # Start the PyQt event loop.

if __name__ == "__main__":
    main()