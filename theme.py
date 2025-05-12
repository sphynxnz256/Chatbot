class ThemeManager:
    _instance = None

    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = super(ThemeManager, cls).__new__(cls, *args, **kwargs)
        return cls._instance
    
    def __init__(self):
        # This ensures __init__ runs only once for the singleton instance
        if hasattr(self, '_initialized') and self._initialized:
            return
        
        self.themes = {
            "dark": {
                "WINDOW_BG": "rgb(30, 30, 30)",               # Dark gray
                "TEXT_BG": "rgb(45, 45, 45)",                 # Slightly lighter gray
                "TEXT_COLOR": "rgb(255, 255, 255)",           # White
                "PLACEHOLDER_COLOR": "rgb(150, 150, 150)",    # Grey
                "BUTTON_BG": "rgb(60, 60, 60)",               # Medium gray
                "BUTTON_PRESSED_BG": "rgb(55, 55, 55)",       # Slightly darker gray for pressed state
                "PROMPT_BG": "rgb(60, 60, 60)",               # Lighter gray for prompt box
            }
        }
        self._active_theme_name = "dark" # Default theme
        self._active_colors = self.themes[self._active_theme_name]
        self._initialized = True

    # This allows selection of theme
    def set_theme(self, theme_name):
        if theme_name in self.themes:
            self._active_theme_name = theme_name
            self._active_colors = self.themes[theme_name]
        else:
            print(f"Warning: Theme '{theme_name}' not found. Keeping '{self._active_theme_name}' theme.")

    # This allows access to colors via variable names rather than dict lookups. ie. theme_manager.COLOR
    def __getattr__(self, name):
        if '_active_colors' in self.__dict__ and name in self._active_colors:
            return self._active_colors[name]
        if name in self.__dict__:
            return self.__dict__[name]
        
        raise AttributeError(f"'{type(self).__name__}' object has no attribute '{name}' and it's not a color key in the active theme.")
    
# Create a single, global instance of the ThemeManager for easy accesss
theme_manager = ThemeManager()