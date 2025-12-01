"""
Sequence Assembly Algorithm
Find overlaps between DNA sequences
"""

from itertools import permutations


def find_overlap(a, b, min_length=3):
    """
    Find overlap between end of a and start of b
    
    Args:
        a: First sequence
        b: Second sequence
        min_length: Minimum overlap length
        
    Returns:
        Length of overlap (0 if none)
    """
    start = 0
    while True:
        start = a.find(b[:min_length], start)
        if start == -1:
            return 0
        if b.startswith(a[start:]):
            return len(a) - start
        start += 1


def find_all_overlaps(reads, k):
    """
    Find all overlaps between sequences
    
    Args:
        reads: List of DNA sequences
        k: Minimum overlap length
        
    Returns:
        Dictionary of (seq_a, seq_b) -> overlap_length
    """
    olap = {}
    for a, b in permutations(reads, 2):
        olen = find_overlap(a, b, k)
        if olen > 0:
            olap[(a, b)] = olen
    return olap


def format_overlap_table(overlaps):
    """Format overlap results as table"""
    if not overlaps:
        return "No overlaps found."
    
    result = "Sequence Overlaps:\n\n"
    result += "Sequence A          Sequence B          Overlap Length\n"
    result += "-" * 70 + "\n"
    
    for (seq_a, seq_b), overlap_len in sorted(overlaps.items(), 
                                               key=lambda x: x[1], 
                                               reverse=True):
        display_a = seq_a if len(seq_a) <= 15 else seq_a[:12] + "..."
        display_b = seq_b if len(seq_b) <= 15 else seq_b[:12] + "..."
        
        result += f"{display_a:20s} {display_b:20s} {overlap_len:14d}\n"
    
    return result


def visualize_overlap(seq_a, seq_b, overlap_len):
    """Create visual representation of overlap"""
    if overlap_len == 0:
        return "No overlap"
    
    result = "Overlap Visualization:\n\n"
    overlap_start = len(seq_a) - overlap_len
    
    result += f"Sequence A: {seq_a}\n"
    result += " " * 12 + " " * overlap_start + "↓" * overlap_len + "\n"
    result += f"Sequence B: {' ' * overlap_start}{seq_b}\n\n"
    result += f"Overlap region: {seq_a[overlap_start:]}\n"
    result += f"Overlap length: {overlap_len} bp\n"
    
    return result


def get_overlap_stats(overlaps):
    """Get statistics about overlaps"""
    if not overlaps:
        return {
            'total_pairs': 0,
            'avg_overlap': 0,
            'max_overlap': 0,
            'min_overlap': 0
        }
    
    overlap_lengths = list(overlaps.values())
    
    return {
        'total_pairs': len(overlaps),
        'avg_overlap': sum(overlap_lengths) / len(overlap_lengths),
        'max_overlap': max(overlap_lengths),
        'min_overlap': min(overlap_lengths)
    }


def greedy_assembly(reads, k):
    """Greedy sequence assembly"""
    if not reads:
        return "", []
    
    steps = []
    remaining = reads.copy()
    assembled = remaining.pop(0)
    steps.append(f"Starting with: {assembled}")
    
    while remaining:
        best_overlap = 0
        best_seq = None
        best_idx = -1
        
        for idx, seq in enumerate(remaining):
            olen = find_overlap(assembled, seq, k)
            if olen > best_overlap:
                best_overlap = olen
                best_seq = seq
                best_idx = idx
        
        if best_seq:
            assembled = assembled + best_seq[best_overlap:]
            steps.append(f"Added {best_seq} with overlap {best_overlap}")
            remaining.pop(best_idx)
        else:
            for seq in remaining:
                assembled += seq
                steps.append(f"Concatenated: {seq}")
            break
    
    return assembled, steps