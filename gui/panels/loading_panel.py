from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel, QPushButton, QFrame, QSizePolicy, QHBoxLayout, QGraphicsDropShadowEffect, QFileDialog
from PyQt5.QtSvg import QSvgRenderer
from PyQt5.QtGui import QPixmap, QPainter, QColor
from PyQt5.QtCore import Qt
from config.settings import settings

class LoadingPanel(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setAcceptDrops(True)
        layout = QVBoxLayout()
        layout.setAlignment(Qt.AlignCenter)
        self.setLayout(layout)

        #===== BLOCKS =====
        top_layout = QVBoxLayout()
        middle_layout = QVBoxLayout()
        bottom_layout = QVBoxLayout()

        #===== WINDOW FRAME =====
        frame = QFrame()
        frame.setStyleSheet(f"""
                                QFrame {{
                                    border: 2px solid {settings.PRIMARY_COLOR};
                                }}""")
        
        shadow = QGraphicsDropShadowEffect()
        shadow.setBlurRadius(20)
        shadow.setOffset(1, 1)
        shadow.setColor(QColor(settings.PRIMARY_COLOR_HP))
        frame.setGraphicsEffect(shadow)
        frame.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        layout.setContentsMargins(20, 20, 20, 20)
        frame_layout = QVBoxLayout()
        frame_layout.setAlignment(Qt.AlignCenter)
        frame.setLayout(frame_layout)
        layout.addWidget(frame)

        #===== TOP BLOCK =====
        renderer = QSvgRenderer("assets/icons/upload.svg")
        pixmap = QPixmap(120, 120)
        pixmap.fill(Qt.transparent)

        painter = QPainter(pixmap)
        renderer.render(painter)

        painter.setCompositionMode(QPainter.CompositionMode_SourceIn)
        painter.fillRect(pixmap.rect(), QColor(settings.PRIMARY_COLOR))
        painter.end()

        label = QLabel()
        label.setPixmap(pixmap)
        label.setStyleSheet("background: transparent; border: none;")
        
        instruction_label = QLabel("Drag your file here")
        instruction_label.setAlignment(Qt.AlignCenter)
        instruction_label.setStyleSheet(f"""
                                QLabel {{
                                    background: transparent;
                                    color: {settings.PRIMARY_COLOR};
                                    font-size: 18px;
                                    font-weight: bold;
                                    transparent; 
                                    border: none;
                                    margin-top: 15;
                                }}""")

        top_layout.addWidget(label, alignment=Qt.AlignCenter)
        top_layout.addWidget(instruction_label, alignment=Qt.AlignCenter)
        

        #===== MIDDLE BLOCK =====
        separator_layout = QHBoxLayout()

        line_left = QFrame()
        line_left.setFrameShape(QFrame.HLine)
        line_left.setFrameShadow(QFrame.Plain)
        line_left.setStyleSheet(f"background-color: {settings.PRIMARY_COLOR}; border: none;")
        line_left.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)

        separator_layout.addWidget(line_left)

        or_label = QLabel("OR")
        or_label.setAlignment(Qt.AlignCenter)
        or_label.setStyleSheet(f"""
                                QLabel {{
                                    background: transparent;
                                    color: {settings.PRIMARY_COLOR};
                                    font-size: 30px;
                                    font-weight: bold;
                                    border: none;
                                }}""")
        
        separator_layout.addWidget(or_label)

        line_right = QFrame()
        line_right.setFrameShape(QFrame.HLine)
        line_right.setFrameShadow(QFrame.Plain)
        line_right.setStyleSheet(f"background-color: {settings.PRIMARY_COLOR}; border: none;")
        line_right.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        separator_layout.addWidget(line_right)

        middle_layout.addLayout(separator_layout)

        #===== LOWER BLOCK =====
        button = QPushButton("select a file")
        button.setStyleSheet(f"""
                                QPushButton {{
                                    background-color: transparent;
                                    color: {settings.PRIMARY_COLOR};
                                    font-size: 18px;
                                    font-weight: bold;
                                    padding: 12px 24px;
                                    border: 2px solid {settings.PRIMARY_COLOR};
                                    outline: none;
                                }}
                                QPushButton:hover {{
                                    background-color: {settings.PRIMARY_COLOR};
                                    border: 2px solid {settings.PRIMARY_COLOR};
                                    color: {settings.TERTIARY_COLOR};
                                }}""")
        
        button.clicked.connect(self.open_file_dialog)
        bottom_layout.addWidget(button, alignment=Qt.AlignCenter)

        #===== MARGINS =====
        frame_layout.addStretch(1)          # margen superior
        frame_layout.addLayout(top_layout)  # icono + texto
        frame_layout.addStretch(1)          # espacio flexible
        frame_layout.addLayout(middle_layout) # OR
        frame_layout.addStretch(1)          # espacio flexible
        frame_layout.addLayout(bottom_layout) # botón
        frame_layout.addStretch(1)          # margen inferior

    def open_file_dialog(self):
        file_path, _ = QFileDialog.getOpenFileName(
            self,
            "Select a file",
            "",
            "Media Files (*.png *.jpg *.jpeg *.bmp *.gif *.tif *.tiff *.mp4 *.avi *.mov *.mkv)"
        )
        if file_path:
            print("Archivo seleccionado:", file_path)
    
    def dragEnterEvent(self, a0):
        super().dragEnterEvent(a0)
        if a0.mimeData().hasUrls():
            a0.acceptProposedAction()
        else:
            a0.ignore()
    
    def dropEvent(self, a0):
        if a0.mimeData().hasUrls():
            for url in a0.mimeData().urls():
                file_path = url.toLocalFile()
                if file_path.lower().endswith((".png", ".jpg", ".jpeg", ".bmp", ".gif", ".tif", ".tiff",
                                            ".mp4", ".avi", ".mov", ".mkv")):
                    print("Archivo válido arrastrado:", file_path)
                    if file_path.lower().endswith((".png", ".jpg", ".jpeg", ".bmp", ".gif", ".tif", ".tiff")):
                        print("Procesar como imagen")
                    else:
                        print("Procesar como video")
                    a0.acceptProposedAction()
                else:
                    print("Formato no soportado:", file_path)
                    a0.ignore()