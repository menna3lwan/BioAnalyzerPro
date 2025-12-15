"""
Configuration file for BioAnalyzer Pro
"""


class Colors:
    """Color scheme"""
    PRIMARY = "#2C5F7C"
    SECONDARY = "#4A90A4"
    ACCENT = "#89B5AF"
    SUCCESS = "#52B788"
    WARNING = "#F77F00"
    ERROR = "#D62828"
    
    BACKGROUND = "#F8F9FA"
    WHITE = "#FFFFFF"
    
    TEXT_DARK = "#212529"
    TEXT_LIGHT = "#CED4DA"
    
    TAB_BG = "#E9ECEF"
    INPUT_BG = "#F8F9FA"
    OUTPUT_BG = "#F0F0F0"


class Fonts:
    """Font configurations"""
    TITLE = ("Helvetica", 24, "bold")
    HEADING = ("Helvetica", 12, "bold")
    BUTTON = ("Helvetica", 10)
    LABEL = ("Helvetica", 10)
    TEXT = ("Courier", 10)
    STATUS = ("Helvetica", 9)


class Settings:
    """Application settings"""
    WINDOW_TITLE = "🧬 BioAnalyzer Pro - Bioinformatics Tool"
    WINDOW_SIZE = "1200x800"
    MIN_SIZE = (1000, 700)
    
    TABS = {
        'fasta': '📁 FASTA Parser',
        'dna': '🧬 DNA Analysis',
        'naive': '🔍 Naive Search',
        'boyer': '⚡ Boyer-Moore',
        'index': '📇 Index Search',
        'suffix': '🔤 Suffix Array',
        'assembly': '🧩 Assembly'
    }