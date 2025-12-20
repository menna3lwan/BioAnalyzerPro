"""
BioAnalyzer Pro - Main Application
Complete Bioinformatics Desktop Tool
All 8 Tabs - WITH EDIT DISTANCE (EMBEDDED)
"""

import tkinter as tk
from tkinter import ttk, scrolledtext, filedialog, messagebox
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from config import Colors, Fonts, Settings
from ui.styles import setup_styles

import algorithms.fasta_parser as fasta
import algorithms.dna_operations as dna
import algorithms.pattern_matching as pattern
import algorithms.index_search as index
import algorithms.suffix_array as suffix
import algorithms.assembly as assembly


# ============================================================================
# EDIT DISTANCE FUNCTIONS (EMBEDDED) - NO SEPARATE FILE NEEDED
# ============================================================================

def edit_distance_DP(x, y):
    """Calculate edit distance using Dynamic Programming"""
    D = []
    for i in range(len(x) + 1):
        D.append([0] * (len(y) + 1))
    
    for i in range(len(x) + 1):
        D[i][0] = i
    
    for i in range(len(y) + 1):
        D[0][i] = i
    
    for i in range(1, len(x) + 1):
        for j in range(1, len(y) + 1):
            delta = 1 if x[i-1] != y[j-1] else 0
            D[i][j] = min(
                D[i-1][j-1] + delta,
                D[i-1][j] + 1,
                D[i][j-1] + 1
            )
    
    return D[-1][-1]


def edit_distance_with_matrix(x, y):
    """Calculate edit distance and return matrix"""
    D = []
    for i in range(len(x) + 1):
        D.append([0] * (len(y) + 1))
    
    for i in range(len(x) + 1):
        D[i][0] = i
    
    for i in range(len(y) + 1):
        D[0][i] = i
    
    for i in range(1, len(x) + 1):
        for j in range(1, len(y) + 1):
            delta = 1 if x[i-1] != y[j-1] else 0
            D[i][j] = min(
                D[i-1][j-1] + delta,
                D[i-1][j] + 1,
                D[i][j-1] + 1
            )
    
    return D[-1][-1], D


def format_edit_distance_matrix(D, x, y):
    """Format DP matrix for display"""
    result = []
    header = "      " + "  ".join([" "] + list(y))
    result.append(header)
    result.append("-" * len(header))
    
    for i in range(len(x) + 1):
        row_label = " " if i == 0 else x[i-1]
        row = f"{row_label:2} | " + "  ".join(f"{D[i][j]:2}" for j in range(len(y) + 1))
        result.append(row)
    
    return "\n".join(result)


def traceback_alignment(x, y, D):
    """Traceback to find alignment"""
    i, j = len(x), len(y)
    aligned_x, aligned_y, operations = [], [], []
    
    while i > 0 or j > 0:
        if i > 0 and j > 0:
            delta = 0 if x[i-1] == y[j-1] else 1
            if D[i][j] == D[i-1][j-1] + delta:
                operations.append('match' if delta == 0 else 'substitute')
                aligned_x.append(x[i-1])
                aligned_y.append(y[j-1])
                i -= 1
                j -= 1
            elif D[i][j] == D[i-1][j] + 1:
                operations.append('delete')
                aligned_x.append(x[i-1])
                aligned_y.append('-')
                i -= 1
            else:
                operations.append('insert')
                aligned_x.append('-')
                aligned_y.append(y[j-1])
                j -= 1
        elif i > 0:
            operations.append('delete')
            aligned_x.append(x[i-1])
            aligned_y.append('-')
            i -= 1
        else:
            operations.append('insert')
            aligned_x.append('-')
            aligned_y.append(y[j-1])
            j -= 1
    
    aligned_x.reverse()
    aligned_y.reverse()
    operations.reverse()
    
    return ''.join(aligned_x), ''.join(aligned_y), operations


def format_alignment(aligned_x, aligned_y, operations):
    """Format alignment for display"""
    result = []
    middle = []
    for i in range(len(aligned_x)):
        if operations[i] == 'match':
            middle.append('|')
        elif operations[i] == 'substitute':
            middle.append('x')
        elif operations[i] == 'delete':
            middle.append('^')
        else:
            middle.append('v')
    
    result.append("Alignment:")
    result.append(f"  {aligned_x}")
    result.append(f"  {''.join(middle)}")
    result.append(f"  {aligned_y}")
    result.append("")
    result.append("Legend: | = match, x = substitution, ^ = deletion, v = insertion")
    
    match_count = operations.count('match')
    sub_count = operations.count('substitute')
    del_count = operations.count('delete')
    ins_count = operations.count('insert')
    
    result.append("")
    result.append(f"Matches: {match_count}")
    result.append(f"Substitutions: {sub_count}")
    result.append(f"Deletions: {del_count}")
    result.append(f"Insertions: {ins_count}")
    
    return "\n".join(result)

# ============================================================================
# END OF EDIT DISTANCE FUNCTIONS
# ============================================================================


class BioAnalyzerApp:
    def __init__(self, root):
        self.root = root
        self.setup_window()
        setup_styles()
        self.create_ui()
        self.current_index = None
        self.current_seq = None
    
    def setup_window(self):
        self.root.title(Settings.WINDOW_TITLE)
        self.root.geometry(Settings.WINDOW_SIZE)
        self.root.minsize(*Settings.MIN_SIZE)
        self.root.configure(bg=Colors.BACKGROUND)
    
    def create_ui(self):
        self.create_header()
        self.notebook = ttk.Notebook(self.root)
        self.notebook.pack(fill='both', expand=True, padx=10, pady=10)
        self.create_all_tabs()
        self.status_var = tk.StringVar(value="Ready")
        status_bar = tk.Label(self.root, textvariable=self.status_var,
                             bd=1, relief='sunken', anchor='w',
                             bg=Colors.TAB_BG, font=Fonts.STATUS)
        status_bar.pack(side='bottom', fill='x')
    
    def create_header(self):
        header = tk.Frame(self.root, bg=Colors.PRIMARY, height=80)
        header.pack(fill='x')
        header.pack_propagate(False)
        tk.Label(header, text="🧬 BioAnalyzer Pro",
                 font=Fonts.TITLE, bg=Colors.PRIMARY, fg="white").pack(side='left', padx=20)
        tk.Label(header, text="v1.0",
                 font=Fonts.STATUS, bg=Colors.PRIMARY, fg=Colors.TEXT_LIGHT).pack(side='left')
    
    def create_all_tabs(self):
        self.create_fasta_tab()
        self.create_dna_tab()
        self.create_naive_tab()
        self.create_boyer_tab()
        self.create_index_tab()
        self.create_suffix_tab()
        self.create_assembly_tab()
        self.create_edit_distance_tab()  # NEW TAB
    
    def update_status(self, message):
        self.status_var.set(message)
        self.root.update_idletasks()
    
    # TAB 1: FASTA
    def create_fasta_tab(self):
        tab = ttk.Frame(self.notebook)
        self.notebook.add(tab, text=Settings.TABS['fasta'])
        
        tk.Label(tab, text="📁 Input", font=Fonts.HEADING,
                 bg=Colors.WHITE, fg=Colors.PRIMARY).pack(anchor='w', padx=20, pady=(20, 5))
        
        btn_frame = tk.Frame(tab, bg=Colors.WHITE)
        btn_frame.pack(anchor='w', padx=20, pady=5)
        
        tk.Button(btn_frame, text="⬆ Upload FASTA File", command=self.upload_fasta,
                  bg=Colors.SECONDARY, fg='white', font=Fonts.BUTTON,
                  relief='flat', padx=15, pady=8, cursor='hand2').pack(side='left', padx=(0, 10))
        
        tk.Button(btn_frame, text="📝 Load Example", command=self.load_fasta_example,
                  bg=Colors.WHITE, fg=Colors.SECONDARY, font=Fonts.BUTTON,
                  relief='solid', bd=1, padx=15, pady=8, cursor='hand2').pack(side='left')
        
        self.fasta_input = scrolledtext.ScrolledText(tab, height=6, font=Fonts.TEXT,
                                                      bg=Colors.INPUT_BG, wrap='word')
        self.fasta_input.pack(fill='x', padx=20, pady=(5, 10))
        self.fasta_input.insert('1.0', "Paste FASTA formatted sequence here or upload file...")
        
        action_frame = tk.Frame(tab, bg=Colors.WHITE)
        action_frame.pack(anchor='w', padx=20, pady=10)
        
        tk.Button(action_frame, text="▶ Parse FASTA", command=self.parse_fasta,
                  bg=Colors.SECONDARY, fg='white', font=Fonts.BUTTON,
                  relief='flat', padx=20, pady=10, cursor='hand2').pack(side='left', padx=(0, 10))
        
        tk.Button(action_frame, text="🗑️ Clear",
                  command=lambda: self.clear_tab(self.fasta_input, self.fasta_results),
                  bg=Colors.WHITE, fg=Colors.TEXT_DARK, font=Fonts.BUTTON,
                  relief='solid', bd=1, padx=20, pady=10, cursor='hand2').pack(side='left')
        
        tk.Label(tab, text="📊 Results", font=Fonts.HEADING,
                 bg=Colors.WHITE, fg=Colors.PRIMARY).pack(anchor='w', padx=20, pady=(10, 5))
        
        self.fasta_results = scrolledtext.ScrolledText(tab, height=12, font=Fonts.TEXT,
                                                        bg=Colors.OUTPUT_BG, wrap='none', state='disabled')
        self.fasta_results.pack(fill='both', expand=True, padx=20, pady=(5, 20))
    
    def upload_fasta(self):
        filepath = filedialog.askopenfilename(
            title="Select FASTA File",
            filetypes=[("FASTA files", "*.fasta *.fa *.fna"), ("All files", "*.*")])
        if filepath:
            try:
                with open(filepath, 'r') as f:
                    content = f.read()
                self.fasta_input.delete('1.0', 'end')
                self.fasta_input.insert('1.0', content)
                self.update_status("File loaded successfully")
            except Exception as e:
                messagebox.showerror("Error", f"Failed to load file:\n{str(e)}")
    
    def load_fasta_example(self):
        example = """>sequence_1_hemolytic
ATGCGATCGATCGATCGCGATCGATCGATCGATC
>sequence_2_non_hemolytic
GCTAGCTAGCTAGCTAG"""
        self.fasta_input.delete('1.0', 'end')
        self.fasta_input.insert('1.0', example)
        self.update_status("Example loaded")
    
    def parse_fasta(self):
        content = self.fasta_input.get('1.0', 'end-1c')
        
        if not content or "Paste FASTA" in content:
            messagebox.showwarning("Warning", "Please provide FASTA content")
            return
        
        try:
            self.update_status("Parsing FASTA...")
            
            sequences = fasta.parse_simple_fasta(content)
            stats = fasta.get_fasta_stats(sequences)
            
            result = "=" * 60 + "\nFASTA PARSING RESULTS\n" + "=" * 60 + "\n\n"
            result += f"Total Sequences: {stats['num_sequences']}\n"
            result += f"Total Length: {stats['total_length']} bp\n"
            result += f"Average Length: {stats['avg_length']:.1f} bp\n"
            result += f"Min Length: {stats['min_length']} bp\n"
            result += f"Max Length: {stats['max_length']} bp\n\n"
            
            for i, (header, seq) in enumerate(sequences, 1):
                result += f"Sequence {i}:\nHeader: {header}\nLength: {len(seq)} bp\n"
                result += f"Sequence: {seq[:60]}{'...' if len(seq) > 60 else ''}\n\n"
            
            self.fasta_results.config(state='normal')
            self.fasta_results.delete('1.0', 'end')
            self.fasta_results.insert('1.0', result)
            self.fasta_results.config(state='disabled')
            
            self.update_status(f"✓ Parsed {len(sequences)} sequences")
        except Exception as e:
            messagebox.showerror("Error", f"Parsing failed:\n{str(e)}")
            self.update_status("✗ Parsing failed")
    
    # TAB 2: DNA
    def create_dna_tab(self):
        tab = ttk.Frame(self.notebook)
        self.notebook.add(tab, text=Settings.TABS['dna'])
        
        tk.Label(tab, text="📁 DNA Sequence", font=Fonts.HEADING,
                 bg=Colors.WHITE, fg=Colors.PRIMARY).pack(anchor='w', padx=20, pady=(20, 5))
        
        btn_frame = tk.Frame(tab, bg=Colors.WHITE)
        btn_frame.pack(anchor='w', padx=20, pady=5)
        
        tk.Button(btn_frame, text="📝 Load Example", command=self.load_dna_example,
                  bg=Colors.SECONDARY, fg='white', font=Fonts.BUTTON,
                  relief='flat', padx=15, pady=8, cursor='hand2').pack(side='left')
        
        self.dna_input = scrolledtext.ScrolledText(tab, height=5, font=Fonts.TEXT,
                                                    bg=Colors.INPUT_BG, wrap='char')
        self.dna_input.pack(fill='x', padx=20, pady=(5, 10))
        self.dna_input.insert('1.0', "Paste DNA sequence here...")
        
        action_frame = tk.Frame(tab, bg=Colors.WHITE)
        action_frame.pack(anchor='w', padx=20, pady=10)
        
        tk.Button(action_frame, text="▶ Run Analysis", command=self.analyze_dna,
                  bg=Colors.SECONDARY, fg='white', font=Fonts.BUTTON,
                  relief='flat', padx=20, pady=10, cursor='hand2').pack(side='left', padx=(0, 10))
        
        tk.Button(action_frame, text="🗑️ Clear",
                  command=lambda: self.clear_tab(self.dna_input, self.dna_results),
                  bg=Colors.WHITE, fg=Colors.TEXT_DARK, font=Fonts.BUTTON,
                  relief='solid', bd=1, padx=20, pady=10, cursor='hand2').pack(side='left')
        
        tk.Label(tab, text="📊 Results", font=Fonts.HEADING,
                 bg=Colors.WHITE, fg=Colors.PRIMARY).pack(anchor='w', padx=20, pady=(10, 5))
        
        self.dna_results = scrolledtext.ScrolledText(tab, height=12, font=Fonts.TEXT,
                                                      bg=Colors.OUTPUT_BG, wrap='none', state='disabled')
        self.dna_results.pack(fill='both', expand=True, padx=20, pady=(5, 20))
    
    def load_dna_example(self):
        self.dna_input.delete('1.0', 'end')
        self.dna_input.insert('1.0', "ATGGCGTCGCTGTGGAGGCGATCGATCG")
        self.update_status("Example loaded")
    
    def analyze_dna(self):
        seq = self.dna_input.get('1.0', 'end-1c').strip().upper()
        if not seq or "Paste DNA" in seq:
            messagebox.showwarning("Warning", "Please provide a DNA sequence")
            return
        
        try:
            self.update_status("Analyzing...")
            result = "=" * 60 + "\nDNA SEQUENCE ANALYSIS\n" + "=" * 60 + "\n\n"
            result += f"Input Sequence: {seq[:60]}{'...' if len(seq) > 60 else ''}\n"
            result += f"Length: {len(seq)} bp\n\n"
            result += f"GC Content: {dna.gc_content(seq):.2f}%\n"
            result += f"AT Content: {dna.at_content(seq):.2f}%\n"
            
            comp = dna.complement(seq)
            result += f"\nComplement: {comp[:60]}{'...' if len(comp) > 60 else ''}\n"
            
            rev_comp = dna.reverse_complement(seq)
            result += f"Reverse Complement: {rev_comp[:60]}{'...' if len(rev_comp) > 60 else ''}\n"
            
            protein = dna.translate(seq)
            result += f"\nTranslation: {protein[:60]}{'...' if len(protein) > 60 else ''}\n"
            
            self.dna_results.config(state='normal')
            self.dna_results.delete('1.0', 'end')
            self.dna_results.insert('1.0', result)
            self.dna_results.config(state='disabled')
            
            self.update_status("✓ Analysis complete")
        except Exception as e:
            messagebox.showerror("Error", f"Analysis failed:\n{str(e)}")
            self.update_status("✗ Analysis failed")
    
    # TAB 3: NAIVE
    def create_naive_tab(self):
        tab = ttk.Frame(self.notebook)
        self.notebook.add(tab, text=Settings.TABS['naive'])
        
        tk.Label(tab, text="📁 Input Sequence", font=Fonts.HEADING,
                 bg=Colors.WHITE, fg=Colors.PRIMARY).pack(anchor='w', padx=20, pady=(20, 5))
        
        tk.Button(tab, text="📝 Load Example", command=self.load_naive_example,
                  bg=Colors.SECONDARY, fg='white', font=Fonts.BUTTON,
                  relief='flat', padx=15, pady=8, cursor='hand2').pack(anchor='w', padx=20, pady=5)
        
        self.naive_seq = scrolledtext.ScrolledText(tab, height=4, font=Fonts.TEXT,
                                                    bg=Colors.INPUT_BG, wrap='char')
        self.naive_seq.pack(fill='x', padx=20, pady=(5, 10))
        self.naive_seq.insert('1.0', "Paste sequence here...")
        
        tk.Label(tab, text="🔍 Pattern to Search", font=Fonts.HEADING,
                 bg=Colors.WHITE, fg=Colors.PRIMARY).pack(anchor='w', padx=20, pady=(10, 5))
        
        self.naive_pattern = tk.Entry(tab, font=Fonts.TEXT, bg=Colors.INPUT_BG)
        self.naive_pattern.pack(fill='x', padx=20, pady=(5, 10))
        
        action_frame = tk.Frame(tab, bg=Colors.WHITE)
        action_frame.pack(anchor='w', padx=20, pady=10)
        
        tk.Button(action_frame, text="🔍 Run Naive Search", command=self.run_naive_search,
                  bg=Colors.SECONDARY, fg='white', font=Fonts.BUTTON,
                  relief='flat', padx=20, pady=10, cursor='hand2').pack(side='left', padx=(0, 10))
        
        tk.Button(action_frame, text="🗑️ Clear",
                  command=lambda: self.clear_tab(self.naive_seq, self.naive_results),
                  bg=Colors.WHITE, fg=Colors.TEXT_DARK, font=Fonts.BUTTON,
                  relief='solid', bd=1, padx=20, pady=10, cursor='hand2').pack(side='left')
        
        tk.Label(tab, text="📊 Results", font=Fonts.HEADING,
                 bg=Colors.WHITE, fg=Colors.PRIMARY).pack(anchor='w', padx=20, pady=(10, 5))
        
        self.naive_results = scrolledtext.ScrolledText(tab, height=12, font=Fonts.TEXT,
                                                        bg=Colors.OUTPUT_BG, wrap='none', state='disabled')
        self.naive_results.pack(fill='both', expand=True, padx=20, pady=(5, 20))
    
    def load_naive_example(self):
        self.naive_seq.delete('1.0', 'end')
        self.naive_seq.insert('1.0', "ATGCGATCGATCGATCGATCGATCGATCG")
        self.naive_pattern.delete(0, 'end')
        self.naive_pattern.insert(0, "GATC")
        self.update_status("Example loaded")
    
    def run_naive_search(self):
        seq = self.naive_seq.get('1.0', 'end-1c').strip().upper()
        pat = self.naive_pattern.get().strip().upper()
        
        if not seq or not pat or "Paste sequence" in seq:
            messagebox.showwarning("Warning", "Please provide both sequence and pattern")
            return
        
        try:
            self.update_status("Searching...")
            positions = pattern.naive_match(seq, pat)
            
            result = "=" * 60 + "\nNAIVE PATTERN SEARCH\n" + "=" * 60 + "\n\n"
            result += f"Sequence Length: {len(seq)} bp\n"
            result += f"Pattern: {pat}\nPattern Length: {len(pat)} bp\n\n"
            
            if positions:
                result += f"✓ Found {len(positions)} match(es):\n\n"
                result += pattern.format_match_results(seq, pat, positions)
            else:
                result += "✗ Pattern not found\n"
            
            self.naive_results.config(state='normal')
            self.naive_results.delete('1.0', 'end')
            self.naive_results.insert('1.0', result)
            self.naive_results.config(state='disabled')
            
            self.update_status(f"✓ Found {len(positions)} matches" if positions else "✗ No matches")
        except Exception as e:
            messagebox.showerror("Error", str(e))
            self.update_status("✗ Search failed")
    
    # TAB 4: BOYER-MOORE
    def create_boyer_tab(self):
        tab = ttk.Frame(self.notebook)
        self.notebook.add(tab, text=Settings.TABS['boyer'])
        
        tk.Label(tab, text="📁 Input Sequence", font=Fonts.HEADING,
                 bg=Colors.WHITE, fg=Colors.PRIMARY).pack(anchor='w', padx=20, pady=(20, 5))
        
        tk.Button(tab, text="📝 Load Example", command=self.load_boyer_example,
                  bg=Colors.SECONDARY, fg='white', font=Fonts.BUTTON,
                  relief='flat', padx=15, pady=8, cursor='hand2').pack(anchor='w', padx=20, pady=5)
        
        self.boyer_seq = scrolledtext.ScrolledText(tab, height=4, font=Fonts.TEXT,
                                                    bg=Colors.INPUT_BG, wrap='char')
        self.boyer_seq.pack(fill='x', padx=20, pady=(5, 10))
        self.boyer_seq.insert('1.0', "Paste sequence here...")
        
        tk.Label(tab, text="🔍 Pattern to Search", font=Fonts.HEADING,
                 bg=Colors.WHITE, fg=Colors.PRIMARY).pack(anchor='w', padx=20, pady=(10, 5))
        
        self.boyer_pattern = tk.Entry(tab, font=Fonts.TEXT, bg=Colors.INPUT_BG)
        self.boyer_pattern.pack(fill='x', padx=20, pady=(5, 10))
        
        action_frame = tk.Frame(tab, bg=Colors.WHITE)
        action_frame.pack(anchor='w', padx=20, pady=10)
        
        tk.Button(action_frame, text="⚡ Run Boyer-Moore", command=self.run_boyer_search,
                  bg=Colors.SECONDARY, fg='white', font=Fonts.BUTTON,
                  relief='flat', padx=20, pady=10, cursor='hand2').pack(side='left', padx=(0, 10))
        
        tk.Button(action_frame, text="🗑️ Clear",
                  command=lambda: self.clear_tab(self.boyer_seq, self.boyer_results),
                  bg=Colors.WHITE, fg=Colors.TEXT_DARK, font=Fonts.BUTTON,
                  relief='solid', bd=1, padx=20, pady=10, cursor='hand2').pack(side='left')
        
        tk.Label(tab, text="📊 Results", font=Fonts.HEADING,
                 bg=Colors.WHITE, fg=Colors.PRIMARY).pack(anchor='w', padx=20, pady=(10, 5))
        
        self.boyer_results = scrolledtext.ScrolledText(tab, height=15, font=Fonts.TEXT,
                                                        bg=Colors.OUTPUT_BG, wrap='none', state='disabled')
        self.boyer_results.pack(fill='both', expand=True, padx=20, pady=(5, 20))
    
    def load_boyer_example(self):
        self.boyer_seq.delete('1.0', 'end')
        self.boyer_seq.insert('1.0', "ATGCGATCGATCGATCGATCGATCGATCG")
        self.boyer_pattern.delete(0, 'end')
        self.boyer_pattern.insert(0, "GATC")
        self.update_status("Example loaded")
    
    def run_boyer_search(self):
        seq = self.boyer_seq.get('1.0', 'end-1c').strip().upper()
        pat = self.boyer_pattern.get().strip().upper()
        
        if not seq or not pat or "Paste sequence" in seq:
            messagebox.showwarning("Warning", "Please provide both sequence and pattern")
            return
        
        try:
            self.update_status("Running Boyer-Moore...")
            positions, bc_table = pattern.boyer_moore_match(seq, pat)
            
            result = "=" * 60 + "\nBOYER-MOORE PATTERN SEARCH\n" + "=" * 60 + "\n\n"
            result += f"Sequence Length: {len(seq)} bp\n"
            result += f"Pattern: {pat}\nPattern Length: {len(pat)} bp\n\n"
            result += "Bad Character Table:\n"
            result += pattern.format_bad_char_table(bc_table, pat)
            result += "\n"
            
            if positions:
                result += f"✓ Found {len(positions)} match(es):\n\n"
                result += pattern.format_match_results(seq, pat, positions)
            else:
                result += "✗ Pattern not found\n"
            
            self.boyer_results.config(state='normal')
            self.boyer_results.delete('1.0', 'end')
            self.boyer_results.insert('1.0', result)
            self.boyer_results.config(state='disabled')
            
            self.update_status(f"✓ Found {len(positions)} matches" if positions else "✗ No matches")
        except Exception as e:
            messagebox.showerror("Error", str(e))
            self.update_status("✗ Search failed")
    
    # TAB 5: INDEX
    def create_index_tab(self):
        tab = ttk.Frame(self.notebook)
        self.notebook.add(tab, text=Settings.TABS['index'])
        
        tk.Label(tab, text="📁 Input Sequence", font=Fonts.HEADING,
                 bg=Colors.WHITE, fg=Colors.PRIMARY).pack(anchor='w', padx=20, pady=(20, 5))
        
        tk.Button(tab, text="📝 Load Example", command=self.load_index_example,
                  bg=Colors.SECONDARY, fg='white', font=Fonts.BUTTON,
                  relief='flat', padx=15, pady=8, cursor='hand2').pack(anchor='w', padx=20, pady=5)
        
        self.index_seq = scrolledtext.ScrolledText(tab, height=4, font=Fonts.TEXT,
                                                    bg=Colors.INPUT_BG, wrap='char')
        self.index_seq.pack(fill='x', padx=20, pady=(5, 10))
        self.index_seq.insert('1.0', "Paste sequence here...")
        
        tk.Label(tab, text="⚙️ K-mer Size", font=Fonts.HEADING,
                 bg=Colors.WHITE, fg=Colors.PRIMARY).pack(anchor='w', padx=20, pady=(10, 5))
        
        params_frame = tk.Frame(tab, bg=Colors.WHITE)
        params_frame.pack(anchor='w', padx=20, pady=5)
        
        tk.Label(params_frame, text="K-mer length:", font=Fonts.LABEL,
                 bg=Colors.WHITE).pack(side='left', padx=(0, 10))
        
        self.kmer_size = tk.Spinbox(params_frame, from_=2, to=10, width=10, font=Fonts.LABEL)
        self.kmer_size.delete(0, 'end')
        self.kmer_size.insert(0, '3')
        self.kmer_size.pack(side='left')
        
        action_frame1 = tk.Frame(tab, bg=Colors.WHITE)
        action_frame1.pack(anchor='w', padx=20, pady=10)
        
        tk.Button(action_frame1, text="🔨 Build Index", command=self.build_sequence_index,
                  bg=Colors.ACCENT, fg='white', font=Fonts.BUTTON,
                  relief='flat', padx=20, pady=10, cursor='hand2').pack(side='left', padx=(0, 10))
        
        tk.Button(action_frame1, text="🗑️ Clear", command=self.clear_index_tab,
                  bg=Colors.WHITE, fg=Colors.TEXT_DARK, font=Fonts.BUTTON,
                  relief='solid', bd=1, padx=20, pady=10, cursor='hand2').pack(side='left')
        
        tk.Label(tab, text="🔍 Search Pattern", font=Fonts.HEADING,
                 bg=Colors.WHITE, fg=Colors.PRIMARY).pack(anchor='w', padx=20, pady=(10, 5))
        
        self.index_pattern = tk.Entry(tab, font=Fonts.TEXT, bg=Colors.INPUT_BG)
        self.index_pattern.pack(fill='x', padx=20, pady=(5, 10))
        
        tk.Button(tab, text="🔍 Search in Index", command=self.search_in_index,
                  bg=Colors.SECONDARY, fg='white', font=Fonts.BUTTON,
                  relief='flat', padx=20, pady=10, cursor='hand2').pack(anchor='w', padx=20, pady=10)
        
        tk.Label(tab, text="📊 Results", font=Fonts.HEADING,
                 bg=Colors.WHITE, fg=Colors.PRIMARY).pack(anchor='w', padx=20, pady=(10, 5))
        
        self.index_results = scrolledtext.ScrolledText(tab, height=12, font=Fonts.TEXT,
                                                        bg=Colors.OUTPUT_BG, wrap='none', state='disabled')
        self.index_results.pack(fill='both', expand=True, padx=20, pady=(5, 20))
    
    def load_index_example(self):
        self.index_seq.delete('1.0', 'end')
        self.index_seq.insert('1.0', "ATGCGATCGATCGATCGATCGATCGATCG")
        self.index_pattern.delete(0, 'end')
        self.index_pattern.insert(0, "GAT")
        self.update_status("Example loaded")
    
    def build_sequence_index(self):
        seq = self.index_seq.get('1.0', 'end-1c').strip().upper()
        if not seq or "Paste sequence" in seq:
            messagebox.showwarning("Warning", "Please provide a sequence")
            return
        
        try:
            k = int(self.kmer_size.get())
            self.update_status(f"Building {k}-mer index...")
            
            self.current_index = index.build_index(seq, k)
            self.current_seq = seq
            
            stats = index.get_index_stats(self.current_index, seq, k)
            
            result = "=" * 60 + "\nINDEX BUILT SUCCESSFULLY\n" + "=" * 60 + "\n\n"
            result += f"Sequence Length: {stats['sequence_length']} bp\n"
            result += f"K-mer Size: {stats['k']}\n"
            result += f"Unique K-mers: {stats['unique_kmers']}\n"
            result += f"Total K-mers: {stats['total_kmers']}\n\n"
            result += "K-mer Index Table:\n"
            result += index.format_index_table(self.current_index)
            
            self.index_results.config(state='normal')
            self.index_results.delete('1.0', 'end')
            self.index_results.insert('1.0', result)
            self.index_results.config(state='disabled')
            
            self.update_status("✓ Index built successfully")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to build index:\n{str(e)}")
            self.update_status("✗ Index build failed")
    
    def search_in_index(self):
        if self.current_index is None:
            messagebox.showwarning("Warning", "Please build the index first")
            return
        
        pat = self.index_pattern.get().strip().upper()
        if not pat:
            messagebox.showwarning("Warning", "Please provide a search pattern")
            return
        
        try:
            self.update_status("Searching in index...")
            positions = index.query_index(self.current_index, self.current_seq, pat)
            
            result = "=" * 60 + "\nINDEX SEARCH RESULTS\n" + "=" * 60 + "\n\n"
            result += f"Pattern: {pat}\nPattern Length: {len(pat)} bp\n\n"
            
            if positions:
                result += f"✓ Found {len(positions)} match(es):\n\n"
                for i, pos in enumerate(positions[:10], 1):
                    context_start = max(0, pos - 10)
                    context_end = min(len(self.current_seq), pos + len(pat) + 10)
                    context = self.current_seq[context_start:context_end]
                    result += f"Match {i} at position {pos}:\n  {context}\n"
                    result += f"  {' ' * (pos - context_start)}{'^' * len(pat)}\n\n"
                
                if len(positions) > 10:
                    result += f"... and {len(positions) - 10} more matches\n"
            else:
                result += "✗ Pattern not found in index\n"
            
            self.index_results.config(state='normal')
            self.index_results.delete('1.0', 'end')
            self.index_results.insert('1.0', result)
            self.index_results.config(state='disabled')
            
            self.update_status(f"✓ Found {len(positions)} matches" if positions else "✗ No matches")
        except Exception as e:
            messagebox.showerror("Error", str(e))
            self.update_status("✗ Search failed")
    
    def clear_index_tab(self):
        self.index_seq.delete('1.0', 'end')
        self.index_pattern.delete(0, 'end')
        self.index_results.config(state='normal')
        self.index_results.delete('1.0', 'end')
        self.index_results.config(state='disabled')
        self.current_index = None
        self.current_seq = None
        self.update_status("Cleared")
    
    # TAB 6: SUFFIX
    def create_suffix_tab(self):
        tab = ttk.Frame(self.notebook)
        self.notebook.add(tab, text=Settings.TABS['suffix'])
        
        tk.Label(tab, text="📁 Input Sequence (max 20 chars)", 
                 font=Fonts.HEADING, bg=Colors.WHITE, fg=Colors.PRIMARY).pack(anchor='w', padx=20, pady=(20, 5))
        
        tk.Button(tab, text="📝 Load Example", command=self.load_suffix_example,
                  bg=Colors.SECONDARY, fg='white', font=Fonts.BUTTON,
                  relief='flat', padx=15, pady=8, cursor='hand2').pack(anchor='w', padx=20, pady=5)
        
        self.suffix_seq = tk.Entry(tab, font=Fonts.TEXT, bg=Colors.INPUT_BG)
        self.suffix_seq.pack(fill='x', padx=20, pady=(5, 10))
        self.suffix_seq.insert(0, "Enter short sequence (e.g., BANANA)...")
        
        action_frame = tk.Frame(tab, bg=Colors.WHITE)
        action_frame.pack(anchor='w', padx=20, pady=10)
        
        tk.Button(action_frame, text="🔨 Build Suffix Array", command=self.build_suffix_array_viz,
                  bg=Colors.SECONDARY, fg='white', font=Fonts.BUTTON,
                  relief='flat', padx=20, pady=10, cursor='hand2').pack(side='left', padx=(0, 10))
        
        tk.Button(action_frame, text="🗑️ Clear", command=self.clear_suffix_tab,
                  bg=Colors.WHITE, fg=Colors.TEXT_DARK, font=Fonts.BUTTON,
                  relief='solid', bd=1, padx=20, pady=10, cursor='hand2').pack(side='left')
        
        tk.Label(tab, text="📊 Suffix Array Construction", font=Fonts.HEADING,
                 bg=Colors.WHITE, fg=Colors.PRIMARY).pack(anchor='w', padx=20, pady=(10, 5))
        
        self.suffix_results = scrolledtext.ScrolledText(tab, height=15, font=Fonts.TEXT,
                                                         bg=Colors.OUTPUT_BG, wrap='none', state='disabled')
        self.suffix_results.pack(fill='both', expand=True, padx=20, pady=(5, 20))
    
    def load_suffix_example(self):
        self.suffix_seq.delete(0, 'end')
        self.suffix_seq.insert(0, "BANANA")
        self.update_status("Example loaded")
    
    def build_suffix_array_viz(self):
        seq = self.suffix_seq.get().strip().upper()
        if not seq or "Enter short" in seq:
            messagebox.showwarning("Warning", "Please provide a sequence")
            return
        
        if len(seq) > 20:
            messagebox.showwarning("Warning", "For visualization, please use sequences ≤ 20 characters")
            return
        
        try:
            self.update_status("Building suffix array...")
            sa, steps = suffix.build_suffix_array(seq)
            
            result = "=" * 60 + "\nSUFFIX ARRAY CONSTRUCTION\n" + "=" * 60 + "\n\n"
            result += f"Input Sequence: {seq}\nLength: {len(seq)}\n\n"
            result += suffix.format_suffix_array(seq, sa, steps)
            
            self.suffix_results.config(state='normal')
            self.suffix_results.delete('1.0', 'end')
            self.suffix_results.insert('1.0', result)
            self.suffix_results.config(state='disabled')
            
            self.update_status("✓ Suffix array built")
        except Exception as e:
            messagebox.showerror("Error", f"Build failed:\n{str(e)}")
            self.update_status("✗ Build failed")
    
    def clear_suffix_tab(self):
        self.suffix_seq.delete(0, 'end')
        self.suffix_results.config(state='normal')
        self.suffix_results.delete('1.0', 'end')
        self.suffix_results.config(state='disabled')
        self.update_status("Cleared")
    
    # TAB 7: ASSEMBLY (UPDATED FOR NEW DICTIONARY-BASED OVERLAPS)
    def create_assembly_tab(self):
        tab = ttk.Frame(self.notebook)
        self.notebook.add(tab, text=Settings.TABS['assembly'])
        
        tk.Label(tab, text="📁 Input Sequences (one per line)", font=Fonts.HEADING,
                 bg=Colors.WHITE, fg=Colors.PRIMARY).pack(anchor='w', padx=20, pady=(20, 5))
        
        tk.Button(tab, text="📝 Load Example", command=self.load_assembly_example,
                  bg=Colors.SECONDARY, fg='white', font=Fonts.BUTTON,
                  relief='flat', padx=15, pady=8, cursor='hand2').pack(anchor='w', padx=20, pady=5)
        
        self.assembly_seqs = scrolledtext.ScrolledText(tab, height=6, font=Fonts.TEXT,
                                                        bg=Colors.INPUT_BG, wrap='word')
        self.assembly_seqs.pack(fill='x', padx=20, pady=(5, 10))
        self.assembly_seqs.insert('1.0', "Paste sequences here (one per line)...")
        
        tk.Label(tab, text="⚙️ Parameters", font=Fonts.HEADING,
                 bg=Colors.WHITE, fg=Colors.PRIMARY).pack(anchor='w', padx=20, pady=(10, 5))
        
        params_frame = tk.Frame(tab, bg=Colors.WHITE)
        params_frame.pack(anchor='w', padx=20, pady=5)
        
        tk.Label(params_frame, text="Minimum Overlap:", font=Fonts.LABEL,
                 bg=Colors.WHITE).pack(side='left', padx=(0, 10))
        
        self.min_overlap = tk.Spinbox(params_frame, from_=2, to=20, width=10, font=Fonts.LABEL)
        self.min_overlap.delete(0, 'end')
        self.min_overlap.insert(0, '3')
        self.min_overlap.pack(side='left')
        
        action_frame = tk.Frame(tab, bg=Colors.WHITE)
        action_frame.pack(anchor='w', padx=20, pady=10)
        
        tk.Button(action_frame, text="🔍 Find Overlaps", command=self.find_overlaps,
                  bg=Colors.ACCENT, fg='white', font=Fonts.BUTTON,
                  relief='flat', padx=15, pady=10, cursor='hand2').pack(side='left', padx=(0, 10))
        
        tk.Button(action_frame, text="🧩 Greedy Assembly", command=self.run_greedy_assembly,
                  bg=Colors.SECONDARY, fg='white', font=Fonts.BUTTON,
                  relief='flat', padx=15, pady=10, cursor='hand2').pack(side='left', padx=(0, 10))
        
        tk.Button(action_frame, text="🗑️ Clear",
                  command=lambda: self.clear_tab(self.assembly_seqs, self.assembly_results),
                  bg=Colors.WHITE, fg=Colors.TEXT_DARK, font=Fonts.BUTTON,
                  relief='solid', bd=1, padx=15, pady=10, cursor='hand2').pack(side='left')
        
        tk.Label(tab, text="📊 Results", font=Fonts.HEADING,
                 bg=Colors.WHITE, fg=Colors.PRIMARY).pack(anchor='w', padx=20, pady=(10, 5))
        
        self.assembly_results = scrolledtext.ScrolledText(tab, height=12, font=Fonts.TEXT,
                                                           bg=Colors.OUTPUT_BG, wrap='none', state='disabled')
        self.assembly_results.pack(fill='both', expand=True, padx=20, pady=(5, 20))
    
    def load_assembly_example(self):
        example = "ATGCGATCG\nTCGATCGAT\nATCGATCGC\nCGCTAGCTA"
        self.assembly_seqs.delete('1.0', 'end')
        self.assembly_seqs.insert('1.0', example)
        self.update_status("Example loaded")
    
    def find_overlaps(self):
        """UPDATED: Handle dictionary-based overlaps from new assembly.py"""
        content = self.assembly_seqs.get('1.0', 'end-1c').strip()
        if not content or "Paste sequences" in content:
            messagebox.showwarning("Warning", "Please provide sequences")
            return
        
        try:
            sequences = [s.strip().upper() for s in content.split('\n') if s.strip()]
            if len(sequences) < 2:
                messagebox.showwarning("Warning", "Please provide at least 2 sequences")
                return
            
            min_ov = int(self.min_overlap.get())
            self.update_status("Finding overlaps...")
            
            # ✅ NEW: overlaps is now a dictionary {(seq_a, seq_b): overlap_length}
            overlaps = assembly.find_all_overlaps(sequences, min_ov)
            stats = assembly.get_overlap_stats(overlaps, sequences)
            
            result = "=" * 60 + "\nOVERLAP ANALYSIS\n" + "=" * 60 + "\n\n"
            result += f"Number of Sequences: {stats['num_sequences']}\n"
            result += f"Minimum Overlap: {min_ov} bp\n"
            result += f"Overlaps Found: {stats['num_overlaps']}\n"
            result += f"Max Overlap Length: {stats['max_overlap_length']} bp\n"
            result += f"Avg Overlap Length: {stats['avg_overlap_length']:.1f} bp\n\n"
            
            if overlaps:
                result += "Overlap Table:\n"
                result += assembly.format_overlap_table(overlaps)
                result += "\n\nOverlap Visualization (top 5):\n"
                
                # ✅ NEW: Iterate over dictionary items, sorted by overlap length
                count = 0
                for (seq_a, seq_b), length in sorted(overlaps.items(), 
                                                       key=lambda x: x[1], 
                                                       reverse=True):
                    if count >= 5:
                        break
                    result += assembly.visualize_overlap(seq_a, seq_b, length)
                    result += "\n"
                    count += 1
                
                if len(overlaps) > 5:
                    result += f"... and {len(overlaps) - 5} more overlaps\n"
            else:
                result += "No overlaps found with minimum length requirement\n"
            
            self.assembly_results.config(state='normal')
            self.assembly_results.delete('1.0', 'end')
            self.assembly_results.insert('1.0', result)
            self.assembly_results.config(state='disabled')
            
            self.update_status(f"✓ Found {len(overlaps)} overlaps")
        except Exception as e:
            messagebox.showerror("Error", str(e))
            self.update_status("✗ Overlap analysis failed")
    
    def run_greedy_assembly(self):
        content = self.assembly_seqs.get('1.0', 'end-1c').strip()
        if not content or "Paste sequences" in content:
            messagebox.showwarning("Warning", "Please provide sequences")
            return
        
        try:
            sequences = [s.strip().upper() for s in content.split('\n') if s.strip()]
            if len(sequences) < 2:
                messagebox.showwarning("Warning", "Please provide at least 2 sequences")
                return
            
            min_ov = int(self.min_overlap.get())
            self.update_status("Running greedy assembly...")
            
            contig, steps = assembly.greedy_assembly(sequences, min_ov)
            
            result = "=" * 60 + "\nGREEDY ASSEMBLY RESULTS\n" + "=" * 60 + "\n\n"
            result += f"Input Sequences: {len(sequences)}\n"
            result += f"Minimum Overlap: {min_ov} bp\n\n"
            result += f"Final Contig:\nLength: {len(contig)} bp\nSequence: {contig}\n\n"
            
            total_input = sum(len(s) for s in sequences)
            compression = ((total_input - len(contig)) / total_input * 100) if total_input > 0 else 0
            result += f"Compression: {compression:.1f}%\n"
            result += f"  (Input: {total_input} bp → Output: {len(contig)} bp)\n"
            
            self.assembly_results.config(state='normal')
            self.assembly_results.delete('1.0', 'end')
            self.assembly_results.insert('1.0', result)
            self.assembly_results.config(state='disabled')
            
            self.update_status("✓ Assembly complete")
        except Exception as e:
            messagebox.showerror("Error", str(e))
            self.update_status("✗ Assembly failed")
    
    # TAB 8: EDIT DISTANCE - NEW TAB (EMBEDDED FUNCTIONS)
    def create_edit_distance_tab(self):
        tab = ttk.Frame(self.notebook)
        self.notebook.add(tab, text="🧬 Edit Distance")
        
        tk.Label(tab, text="📁 Sequence X", font=Fonts.HEADING,
                 bg=Colors.WHITE, fg=Colors.PRIMARY).pack(anchor='w', padx=20, pady=(20, 5))
        
        tk.Button(tab, text="📝 Load Example", command=self.load_edit_distance_example,
                  bg=Colors.SECONDARY, fg='white', font=Fonts.BUTTON,
                  relief='flat', padx=15, pady=8, cursor='hand2').pack(anchor='w', padx=20, pady=5)
        
        self.edit_seq_x = tk.Entry(tab, font=Fonts.TEXT, bg=Colors.INPUT_BG)
        self.edit_seq_x.pack(fill='x', padx=20, pady=(5, 10))
        self.edit_seq_x.insert(0, "ACGACGT")
        
        tk.Label(tab, text="📁 Sequence Y", font=Fonts.HEADING,
                 bg=Colors.WHITE, fg=Colors.PRIMARY).pack(anchor='w', padx=20, pady=(10, 5))
        
        self.edit_seq_y = tk.Entry(tab, font=Fonts.TEXT, bg=Colors.INPUT_BG)
        self.edit_seq_y.pack(fill='x', padx=20, pady=(5, 10))
        self.edit_seq_y.insert(0, "TCGTACGT")
        
        tk.Label(tab, text="⚙️ Options", font=Fonts.HEADING,
                 bg=Colors.WHITE, fg=Colors.PRIMARY).pack(anchor='w', padx=20, pady=(10, 5))
        
        options_frame = tk.Frame(tab, bg=Colors.WHITE)
        options_frame.pack(anchor='w', padx=20, pady=5)
        
        self.show_matrix = tk.BooleanVar(value=True)
        tk.Checkbutton(options_frame, text="Show DP Matrix", variable=self.show_matrix,
                      bg=Colors.WHITE, font=Fonts.LABEL).pack(side='left', padx=(0, 15))
        
        self.show_alignment = tk.BooleanVar(value=True)
        tk.Checkbutton(options_frame, text="Show Alignment", variable=self.show_alignment,
                      bg=Colors.WHITE, font=Fonts.LABEL).pack(side='left')
        
        action_frame = tk.Frame(tab, bg=Colors.WHITE)
        action_frame.pack(anchor='w', padx=20, pady=10)
        
        tk.Button(action_frame, text="⚡ Calculate Distance", command=self.calculate_edit_distance,
                  bg=Colors.SECONDARY, fg='white', font=Fonts.BUTTON,
                  relief='flat', padx=20, pady=10, cursor='hand2').pack(side='left', padx=(0, 10))
        
        tk.Button(action_frame, text="🗑️ Clear", command=self.clear_edit_distance_tab,
                  bg=Colors.WHITE, fg=Colors.TEXT_DARK, font=Fonts.BUTTON,
                  relief='solid', bd=1, padx=20, pady=10, cursor='hand2').pack(side='left')
        
        tk.Label(tab, text="📊 Results", font=Fonts.HEADING,
                 bg=Colors.WHITE, fg=Colors.PRIMARY).pack(anchor='w', padx=20, pady=(10, 5))
        
        self.edit_results = scrolledtext.ScrolledText(tab, height=15, font=('Courier', 9),
                                                       bg=Colors.OUTPUT_BG, wrap='none', state='disabled')
        self.edit_results.pack(fill='both', expand=True, padx=20, pady=(5, 20))
    
    def load_edit_distance_example(self):
        self.edit_seq_x.delete(0, 'end')
        self.edit_seq_x.insert(0, "ACGACGT")
        self.edit_seq_y.delete(0, 'end')
        self.edit_seq_y.insert(0, "TCGTACGT")
        self.update_status("Example loaded")
    
    def calculate_edit_distance(self):
        x = self.edit_seq_x.get().strip().upper()
        y = self.edit_seq_y.get().strip().upper()
        
        if not x or not y:
            messagebox.showwarning("Warning", "Please provide both sequences")
            return
        
        # Validate DNA sequences
        valid_chars = set('ACGT')
        if not all(c in valid_chars for c in x):
            messagebox.showwarning("Input Error", "Sequence X contains invalid characters. Use only A, C, G, T.")
            return
        
        if not all(c in valid_chars for c in y):
            messagebox.showwarning("Input Error", "Sequence Y contains invalid characters. Use only A, C, G, T.")
            return
        
        try:
            self.update_status("Calculating edit distance...")
            
            # Calculate edit distance and get matrix - USING EMBEDDED FUNCTIONS
            distance, matrix = edit_distance_with_matrix(x, y)
            
            # Build result
            result = "=" * 60 + "\nEDIT DISTANCE ANALYSIS\n" + "=" * 60 + "\n\n"
            result += f"Sequence X: {x} (length: {len(x)})\n"
            result += f"Sequence Y: {y} (length: {len(y)})\n\n"
            result += "=" * 60 + "\n"
            result += f"EDIT DISTANCE: {int(distance)}\n"
            result += "=" * 60 + "\n\n"
            
            # Show DP matrix if requested
            if self.show_matrix.get():
                result += "DYNAMIC PROGRAMMING MATRIX:\n"
                result += "-" * 60 + "\n"
                result += format_edit_distance_matrix(matrix, x, y)
                result += "\n\n"
            
            # Show alignment if requested
            if self.show_alignment.get():
                aligned_x, aligned_y, operations = traceback_alignment(x, y, matrix)
                result += "=" * 60 + "\n"
                result += format_alignment(aligned_x, aligned_y, operations)
                result += "\n" + "=" * 60 + "\n"
            
            self.edit_results.config(state='normal')
            self.edit_results.delete('1.0', 'end')
            self.edit_results.insert('1.0', result)
            self.edit_results.config(state='disabled')
            
            self.update_status(f"✓ Edit distance: {int(distance)}")
            messagebox.showinfo("Success", f"Edit distance calculated: {int(distance)}")
        
        except Exception as e:
            messagebox.showerror("Error", f"Calculation failed:\n{str(e)}")
            self.update_status("✗ Calculation failed")
    
    def clear_edit_distance_tab(self):
        self.edit_seq_x.delete(0, 'end')
        self.edit_seq_y.delete(0, 'end')
        self.edit_results.config(state='normal')
        self.edit_results.delete('1.0', 'end')
        self.edit_results.config(state='disabled')
        self.update_status("Cleared")
    
    # UTILITY
    def clear_tab(self, input_widget, output_widget):
        input_widget.delete('1.0', 'end')
        output_widget.config(state='normal')
        output_widget.delete('1.0', 'end')
        output_widget.config(state='disabled')
        self.update_status("Cleared")


def main():
    root = tk.Tk()
    app = BioAnalyzerApp(root)
    root.mainloop()


if __name__ == "__main__":
    main()