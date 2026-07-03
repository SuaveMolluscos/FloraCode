import sys
from PyQt5.QtWidgets import QApplication
from PyQt5.QtCore import Qt

from config.settings import settings
from gui.app import FloraMainWindow

def main():
    app = QApplication(sys.argv)
    
    app.setOrganizationName(settings.ORGANIZATION_NAME)
    app.setApplicationName(settings.APPLICATION_NAME)
    
    if settings.ENABLE_HIGH_DPI:
        app.setAttribute(Qt.AA_EnableHighDpiScaling)
        app.setAttribute(Qt.AA_UseHighDpiPixmaps)
    
    window = FloraMainWindow()
    window.show()
    
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()