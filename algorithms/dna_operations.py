"""
DNA Operations Module
GC Content, Complement, Reverse, Translation
"""


def gc_content(seq):
    """Calculate GC content percentage"""
    seq = seq.upper()
    if len(seq) == 0:
        return 0
    num_G = seq.count("G")
    num_C = seq.count("C")
    total = num_C + num_G
    return (total / len(seq)) * 100


def at_content(seq):
    """Calculate AT content percentage"""
    return 100 - gc_content(seq)


def complement(seq):
    """Get DNA complement"""
    dic = {"G": "C", "C": "G", "A": "T", "T": "A"}
    s = list(seq.upper())
    for i in range(len(s)):
        s[i] = dic.get(s[i], s[i])
    return "".join(s)


def reverse(seq):
    """Reverse DNA sequence"""
    return seq[::-1]


def reverse_complement(seq):
    """Get reverse complement"""
    return complement(reverse(seq))


def translate(seq):
    """Translate DNA to protein"""
    codon_table = {
        "TTT": "F", "CTT": "L", "ATT": "I", "GTT": "V",
        "TTC": "F", "CTC": "L", "ATC": "I", "GTC": "V",
        "TTA": "L", "CTA": "L", "ATA": "I", "GTA": "V",
        "TTG": "L", "CTG": "L", "ATG": "M", "GTG": "V",
        "TCT": "S", "CCT": "P", "ACT": "T", "GCT": "A",
        "TCC": "S", "CCC": "P", "ACC": "T", "GCC": "A",
        "TCA": "S", "CCA": "P", "ACA": "T", "GCA": "A",
        "TCG": "S", "CCG": "P", "ACG": "T", "GCG": "A",
        "TAT": "Y", "CAT": "H", "AAT": "N", "GAT": "D",
        "TAC": "Y", "CAC": "H", "AAC": "N", "GAC": "D",
        "TAA": "*", "CAA": "Q", "AAA": "K", "GAA": "E",
        "TAG": "*", "CAG": "Q", "AAG": "K", "GAG": "E",
        "TGT": "C", "CGT": "R", "AGT": "S", "GGT": "G",
        "TGC": "C", "CGC": "R", "AGC": "S", "GGC": "G",
        "TGA": "*", "CGA": "R", "AGA": "R", "GGA": "G",
        "TGG": "W", "CGG": "R", "AGG": "R", "GGG": "G"
    }
    
    seq = seq.upper()
    protein = ""
    for i in range(0, len(seq) - 2, 3):
        codon = seq[i:i+3]
        protein += codon_table.get(codon, "X")
    return protein