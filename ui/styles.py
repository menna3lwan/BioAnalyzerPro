"""
UI Styles configuration
"""

from tkinter import ttk


def setup_styles():
    """Setup TTK styles"""
    style = ttk.Style()
    style.theme_use('clam')
    
    # Configure Notebook style
    style.configure('TNotebook', background='#F8F9FA')
    style.configure('TNotebook.Tab', padding=[20, 10], font=('Helvetica', 10))
    
    # Configure Frame style
    style.configure('TFrame', background='#FFFFFF')