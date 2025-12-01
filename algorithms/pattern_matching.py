"""
Pattern Matching Algorithms
Naive Search and Boyer-Moore
"""

import numpy as np


def naive_match(seq, sub_seq):
    """
    Naive pattern matching - finds all occurrences
    
    Args:
        seq: Main sequence
        sub_seq: Pattern to search
        
    Returns:
        List of positions where pattern is found
    """
    positions = []
    for i in range(len(seq)):
        if sub_seq == seq[i:i+len(sub_seq)]:
            positions.append(i)
    return positions


def boyer_moore_match(seq, sub_seq):
    """
    Boyer-Moore algorithm with Bad Character table
    
    Args:
        seq: Main sequence
        sub_seq: Pattern to search
        
    Returns:
        Tuple of (positions, bad_char_table)
    """
    # Build Bad Character table
    table = np.zeros([4, len(sub_seq)])
    row = ["A", "C", "G", "T"]
    
    for i in range(4):
        num = -1
        for j in range(len(sub_seq)):
            if row[i] == sub_seq[j]:
                table[i, j] = -1
                num = -1
            else:
                num += 1
                table[i, j] = num
    
    # Search using Bad Character table
    positions = []
    i = 0
    while i < len(seq) - len(sub_seq) + 1:
        if sub_seq == seq[i:i+len(sub_seq)]:
            positions.append(i)
        else:
            for j in range(len(sub_seq) - 1, -1, -1):
                if seq[i+j] != sub_seq[j]:
                    if seq[i+j] in row:
                        k = row.index(seq[i+j])
                        i += int(table[k, j])
                    break
        i = int(i + 1)
    
    return positions, table


def format_bad_char_table(table, pattern):
    """Format Bad Character table for display"""
    result = "Bad Character Table:\n\n"
    result += "     " + "  ".join(list(pattern)) + "\n"
    result += "   " + "-" * (len(pattern) * 3 + 2) + "\n"
    
    bases = ["A", "C", "G", "T"]
    for i, base in enumerate(bases):
        result += f"{base} | "
        for j in range(len(pattern)):
            val = int(table[i, j])
            result += f"{val:2d} "
        result += "\n"
    
    return result


def format_match_results(seq, pattern, positions):
    """Format match results with context"""
    if not positions:
        return "No matches found."
    
    result = f"Found {len(positions)} match(es):\n\n"
    
    for i, pos in enumerate(positions[:10], 1):  # Show first 10
        result += f"Match {i} at position {pos}:\n"
        start = max(0, pos - 20)
        end = min(len(seq), pos + len(pattern) + 20)
        context = seq[start:pos] + f"[{seq[pos:pos+len(pattern)]}]" + seq[pos+len(pattern):end]
        result += f"  ...{context}...\n\n"
    
    if len(positions) > 10:
        result += f"... and {len(positions) - 10} more matches\n"
    
    return result