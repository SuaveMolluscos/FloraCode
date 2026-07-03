from PyQt5.QtWidgets import QMainWindow, QApplication, QWidget, QStackedWidget
from PyQt5.QtCore import Qt

from config.settings import settings
from gui.panels.loading_panel import LoadingPanel
from gui.panels.asciieditorpanel import AsciiEditorPanel

class FloraMainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setup_window()
        self.setup_central_widget()
        self.apply_style()
        self.setup_pages()
        
    
    def setup_window(self):
        screen = QApplication.primaryScreen().geometry()
        width = int(screen.width() * settings.WINDOW_DEFAULT_WIDTH_RATIO)
        height = int(screen.height() * settings.WINDOW_DEFAULT_HEIGHT_RATIO)
        width = max(settings.WINDOW_MIN_WIDTH, min(settings.WINDOW_MAX_WIDTH, width))
        height = max(settings.WINDOW_MIN_HEIGHT, min(settings.WINDOW_MAX_HEIGHT, height))
        x = (screen.width() - width) // 2
        y = (screen.height( ) -height) // 2
        self.setGeometry(x, y, width, height)
        self.setMinimumSize(settings.WINDOW_MIN_WIDTH, settings.WINDOW_MIN_HEIGHT)
        self.setMaximumSize(settings.WINDOW_MAX_WIDTH, settings.WINDOW_MAX_HEIGHT)
    
    def setup_central_widget(self):
        self.pages = QStackedWidget()
        self.setCentralWidget(self.pages)

    def apply_style(self):
        self.setStyleSheet(f"""QMainWindow {{background-color: {settings.COLOR_BACKGROUND};}}""")

    def setup_pages(self):
        self.ascii_editor_panel = AsciiEditorPanel()
        self.loading_panel = LoadingPanel ()
        self.pages.addWidget(self.loading_panel)
        self.pages.addWidget(self.ascii_editor_panel)
        self.pages.setCurrentWidget(self.loading_panel)