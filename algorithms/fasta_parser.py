"""
FASTA Parser Algorithm
Parse FASTA formatted files
"""

import pandas as pd


def parse_fasta_file(filepath):
    """
    Parse FASTA file with hemolytic classification
    
    Args:
        filepath: Path to FASTA file
        
    Returns:
        DataFrame with sequences and classification
    """
    try:
        with open(filepath, 'r') as infile:
            flag = 0
            tb = []
            s = None
            
            for line in infile:
                if flag == 0:
                    s = line.split("|lcl|")
                    flag = 1
                else:
                    sequence = line[:-1]
                    if len(s) > 3:
                        if s[3] == 'non-hemolytic' or s[3] == 'non-hemolytic\n':
                            tb.append([sequence, 0])
                        else:
                            tb.append([sequence, 1])
                    flag = 0
            
            head = ['Sequence', 'Classification']
            df = pd.DataFrame(tb, columns=head)
            return df
            
    except Exception as e:
        raise Exception(f"Error parsing FASTA: {str(e)}")


def parse_simple_fasta(filepath):
    """
    Parse simple FASTA file (ID and Sequence)
    
    Args:
        filepath: Path to FASTA file
        
    Returns:
        DataFrame with ID and Sequence
    """
    try:
        with open(filepath, 'r') as infile:
            tb = []
            current_id = None
            
            for line in infile:
                line = line.strip()
                if line.startswith(">"):
                    current_id = line[1:]
                elif current_id:
                    tb.append([current_id, line])
                    current_id = None
            
            head = ['ID', 'Sequence']
            df = pd.DataFrame(tb, columns=head)
            return df
            
    except Exception as e:
        raise Exception(f"Error parsing FASTA: {str(e)}")


def get_fasta_stats(df):
    """Get statistics from parsed FASTA"""
    if df.empty:
        return {}
    
    sequences = df['Sequence'].tolist()
    lengths = [len(seq) for seq in sequences]
    
    return {
        'total_sequences': len(sequences),
        'avg_length': sum(lengths) / len(lengths) if lengths else 0,
        'min_length': min(lengths) if lengths else 0,
        'max_length': max(lengths) if lengths else 0,
        'total_bases': sum(lengths)
    }