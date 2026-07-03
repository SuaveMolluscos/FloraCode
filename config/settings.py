from dataclasses import dataclass
from PyQt5.QtCore import QSize

@dataclass
class AppSettings:

    #--- Tamaños de ventana ---
    WINDOW_MIN_WIDTH: int = 500
    WINDOW_MIN_HEIGHT: int = 650
    WINDOW_MAX_WIDTH: int = 600
    WINDOW_MAX_HEIGHT: int = 900
    WINDOW_DEFAULT_WIDTH_RATIO: float = 0.3
    WINDOW_DEFAULT_HEIGHT_RATIO: float = 0.8

    # --- DPI / Escalado ---
    ENABLE_HIGH_DPI: bool = True

    #--- Configuracion de paneles ---
    ORGANIZATION_NAME = "FloraCode"
    APPLICATION_NAME = "FloraASCII"

    #--- Configuracion de fuentes ---

    #--- Configuracion ASCII ---

    #--- Charsets predefinidos ---

    #--- Configuracion de exportacion ---

    #--- Paleta de colores ---
    COLOR_BACKGROUND: str = "#0A0A0A"
    COLOR_BACKGROUND_HP: str = "#A1A1A1"
    PRIMARY_COLOR: str = "#A7CF00"
    PRIMARY_COLOR_HP: str = "#85A300"
    SECUNDARY_COLOR: str = "#8116E0"
    TERTIARY_COLOR: str = "#FEFFFC"


settings = AppSettings()