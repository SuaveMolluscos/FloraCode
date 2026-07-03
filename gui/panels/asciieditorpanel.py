from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel, QPushButton, QFrame, QSizePolicy, QHBoxLayout, QGraphicsDropShadowEffect, QFileDialog, QScrollArea
from PyQt5.QtSvg import QSvgRenderer
from PyQt5.QtGui import QPixmap, QPainter, QColor
from PyQt5.QtCore import Qt
from config.settings import settings

class AsciiEditorPanel(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        main_layout = QVBoxLayout(self)

        # --- Bloque superior fijo ---
        fixed_container = QWidget()
        fixed_layout = QVBoxLayout(fixed_container)

        # Botones de vista
        buttons_frame = QFrame()
        buttons_frame.setFrameShape(QFrame.Box)
        buttons_frame.setFrameShadow(QFrame.Plain)
        buttons_frame.setStyleSheet(f"""
                                QFrame {{
                                    border: 2px solid {settings.COLOR_BACKGROUND_HP};
                                    border-radius: 4px;
                                }}""")
        view_buttons = QHBoxLayout(buttons_frame)
        view_buttons.setContentsMargins(2,2,2,2)
        view_buttons.setSpacing(1)
        preview_button = QPushButton("Preview")
        preview_button.setStyleSheet(f"""
                                QPushButton {{
                                    background-color: {settings.PRIMARY_COLOR};
                                    color: {settings.TERTIARY_COLOR};
                                    font-size: 12px;
                                    font-weight: bold;
                                    border-radius: 4px;
                                    padding: 8px 12px;
                                    border: 2px solid {settings.PRIMARY_COLOR};
                                    outline: none;
                                }}
                                QPushButton:hover {{
                                    background-color: {settings.SECUNDARY_COLOR};
                                    border: 2px solid {settings.SECUNDARY_COLOR};
                                    color: {settings.TERTIARY_COLOR};
                                }}""")
        original_button = QPushButton("Original")
        original_button.setStyleSheet(f"""
                                QPushButton {{
                                    background-color: {settings.PRIMARY_COLOR};
                                    color: {settings.TERTIARY_COLOR};
                                    font-size: 12px;
                                    font-weight: bold;
                                    border-radius: 4px;
                                    padding: 8px 12px;
                                    border: 2px solid {settings.PRIMARY_COLOR};
                                    outline: none;
                                }}
                                QPushButton:hover {{
                                    background-color: {settings.SECUNDARY_COLOR};
                                    border: 2px solid {settings.SECUNDARY_COLOR};
                                    color: {settings.TERTIARY_COLOR};
                                }}""")
        view_buttons.addWidget(preview_button)
        view_buttons.addWidget(original_button)
        fixed_layout.addWidget(buttons_frame)

        # Recuadro de contenido
        content_frame = QFrame()
        content_frame.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        fixed_layout.addWidget(content_frame)

        # Botón copiar
        copy_button = QPushButton("Copy ASCII")
        fixed_layout.addWidget(copy_button, alignment=Qt.AlignCenter)

        # Bloque opcional de video
        video_controls = QHBoxLayout()
        timeline = QLabel("Timeline")
        play_button = QPushButton("Play")
        sound_button = QPushButton("Sound")
        video_controls.addWidget(play_button)
        video_controls.addWidget(timeline)
        video_controls.addWidget(sound_button)
        fixed_layout.addLayout(video_controls)

        main_layout.addWidget(fixed_container)

        # --- Bloque inferior con scroll ---
        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)

        config_widget = QWidget()
        config_layout = QVBoxLayout(config_widget)

        # Ejemplo de configuraciones
        config_layout.addWidget(QPushButton("Saturation"))
        config_layout.addWidget(QPushButton("Black & White"))
        config_layout.addWidget(QPushButton("Negative"))

        scroll_area.setWidget(config_widget)
        main_layout.addWidget(scroll_area)
