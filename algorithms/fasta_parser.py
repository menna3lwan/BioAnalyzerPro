"""
FASTA Parser Module - Based on Original Algorithm
Uses flag-based parsing from section1.py
"""


def parse_simple_fasta(content):
    """
    Parse FASTA content using flag-based approach (like original algorithm)
    
    This mimics the original section1.py algorithm:
    - flag=0: expecting header line
    - flag=1: expecting sequence line
    
    Args:
        content: FASTA formatted text (string)
        
    Returns:
        List of (header, sequence) tuples
    """
    sequences = []
    flag = 0
    current_header = None
    
    # Split into lines - handle all newline types
    lines = content.replace('\r\n', '\n').replace('\r', '\n').split('\n')
    
    for line in lines:
        line = line.strip()
        
        # Skip empty lines
        if not line:
            continue
        
        if flag == 0:
            # Expecting header
            if line.startswith('>'):
                current_header = line[1:].strip()
                flag = 1
            else:
                # If no header found, treat as malformed - skip
                continue
                
        else:  # flag == 1
            # Expecting sequence
            # Clean the sequence - keep only ATGCN
            clean_seq = ''.join(c for c in line.upper() if c in 'ATGCN')
            
            if clean_seq and current_header is not None:
                sequences.append((current_header, clean_seq))
            
            # Reset for next sequence
            flag = 0
            current_header = None
    
    if not sequences:
        raise ValueError(
            "No valid FASTA sequences found.\n\n"
            "Required format:\n"
            ">header_name\n"
            "ATGCGATCG...\n"
            ">another_header\n"
            "GCTAGCTA...\n\n"
            "Make sure:\n"
            "- Each header starts with '>'\n"
            "- Each sequence is on the line after its header\n"
            "- Headers and sequences alternate"
        )
    
    return sequences


def parse_fasta_with_labels(content, hemolytic_keywords=None):
    """
    Parse FASTA and assign labels (like HAPPENN example)
    
    Args:
        content: FASTA formatted text
        hemolytic_keywords: List of keywords indicating hemolytic (default: ['hemolytic'])
        
    Returns:
        List of (header, sequence, label) tuples where label is 0 or 1
    """
    if hemolytic_keywords is None:
        hemolytic_keywords = ['hemolytic']
    
    sequences = parse_simple_fasta(content)
    labeled_sequences = []
    
    for header, seq in sequences:
        # Check if header contains hemolytic keywords
        is_hemolytic = any(keyword.lower() in header.lower() 
                          for keyword in hemolytic_keywords)
        
        # 1 = hemolytic, 0 = non-hemolytic
        label = 1 if is_hemolytic else 0
        labeled_sequences.append((header, seq, label))
    
    return labeled_sequences


def get_fasta_stats(sequences):
    """
    Get statistics from parsed sequences
    
    Args:
        sequences: List of (header, sequence) tuples
        
    Returns:
        Dictionary with statistics
    """
    if not sequences:
        return {
            'num_sequences': 0,
            'total_length': 0,
            'avg_length': 0,
            'min_length': 0,
            'max_length': 0
        }
    
    lengths = [len(seq) for _, seq in sequences]
    
    return {
        'num_sequences': len(sequences),
        'total_length': sum(lengths),
        'avg_length': sum(lengths) / len(lengths),
        'min_length': min(lengths),
        'max_length': max(lengths)
    }


def validate_dna_sequence(seq):
    """Check if sequence contains only valid DNA bases"""
    valid_bases = set('ATGCN')
    return all(base in valid_bases for base in seq.upper())


# Note: gc_content is already available in dna_operations.py
# Keeping this here for backward compatibility with section1.py examples
def gc_content(seq):
    """
    Calculate GC content (from example 3 in section1.py)
    
    Args:
        seq: DNA sequence string
        
    Returns:
        float: GC content as ratio (0.0 to 1.0)
    """
    l = len(seq)
    if l == 0:
        return 0.0
    
    num_G = seq.upper().count("G")
    num_C = seq.upper().count("C")
    total = num_C + num_G
    
    return total / l