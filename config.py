"""
Configuration File
Colors, Fonts, and Settings
"""

import os

class Colors:
    # Main colors
    PRIMARY = "#3d5a80"          # Dark blue header
    SECONDARY = "#3498db"        # Bright blue buttons
    ACCENT = "#2ecc71"           # Green accent
    BACKGROUND = "#f0f4f8"       # Light gray background
    WHITE = "#ffffff"
    
    # Tab colors
    TAB_BG = "#e8eef3"
    TAB_ACTIVE = "#ffffff"
    
    # Input/Output
    INPUT_BG = "#f8f9fa"
    OUTPUT_BG = "#fafbfc"
    
    # Text
    TEXT_DARK = "#2c3e50"
    TEXT_LIGHT = "#7f8c8d"
    
    # Status colors
    SUCCESS = "#27ae60"
    ERROR = "#e74c3c"
    WARNING = "#f39c12"
    INFO = "#3498db"


class Fonts:
    TITLE = ("Arial", 24, "bold")
    HEADING = ("Arial", 14, "bold")
    LABEL = ("Arial", 11)
    BUTTON = ("Arial", 10, "bold")
    TEXT = ("Consolas", 10)
    STATUS = ("Arial", 10)


class Settings:
    WINDOW_TITLE = "BioAnalyzer Pro"
    WINDOW_SIZE = "1200x800"
    MIN_SIZE = (1000, 700)
    
    # Get base path
    BASE_PATH = os.path.dirname(os.path.abspath(__file__))
    ASSETS_PATH = os.path.join(BASE_PATH, 'assets')
    
    # Icon paths
    ICON_ICO = os.path.join(ASSETS_PATH, 'icon.ico')
    ICON_PNG = os.path.join(ASSETS_PATH, 'icon_256x256.png')
    LOGO_PATH = os.path.join(ASSETS_PATH, 'logo.png')
    
    # Tab names
    TABS = {
        'fasta': '📄 FASTA Parser',
        'dna': '🧬 DNA Analysis',
        'naive': '🔍 Naive Search',
        'boyer': '⚡ Boyer-Moore',
        'index': '📇 Index Search',
        'suffix': '📊 Suffix Array',
        'assembly': '🧩 Assembly'
    }