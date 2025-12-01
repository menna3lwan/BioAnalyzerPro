"""
UI Styles and Theme
"""

from tkinter import ttk
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from config import Colors


def setup_styles():
    """Configure ttk styles"""
    style = ttk.Style()
    
    # Use clam theme as base
    style.theme_use('clam')
    
    # Configure Notebook (tabs)
    style.configure('TNotebook', background=Colors.TAB_BG, borderwidth=0)
    style.configure('TNotebook.Tab',
                    background=Colors.TAB_BG,
                    foreground=Colors.TEXT_DARK,
                    padding=[15, 8],
                    font=('Arial', 10))
    style.map('TNotebook.Tab',
              background=[('selected', Colors.TAB_ACTIVE)],
              foreground=[('selected', Colors.PRIMARY)])
    
    # Configure Frame
    style.configure('TFrame', background=Colors.WHITE)
    
    # Configure Label
    style.configure('TLabel',
                    background=Colors.WHITE,
                    foreground=Colors.TEXT_DARK)
    
    # Configure Entry
    style.configure('TEntry',
                    fieldbackground=Colors.INPUT_BG,
                    borderwidth=1)
    
    # Configure Checkbutton
    style.configure('TCheckbutton',
                    background=Colors.WHITE,
                    foreground=Colors.TEXT_DARK)
    
    return style