"""
Pattern Matching Module
Naive and Boyer-Moore algorithms
"""


def naive_match(seq, pattern):
    """
    Naive pattern matching - find all occurrences
    
    Args:
        seq: Main sequence
        pattern: Pattern to search
        
    Returns:
        List of positions where pattern is found
    """
    positions = []
    for i in range(len(seq) - len(pattern) + 1):
        if pattern == seq[i:i+len(pattern)]:
            positions.append(i)
    return positions


def boyer_moore_match(seq, pattern):
    """
    Boyer-Moore algorithm with Bad Character table
    
    Args:
        seq: Main sequence
        pattern: Pattern to search
        
    Returns:
        Tuple of (positions, bad_char_table_dict)
    """
    # Build Bad Character table as dictionary
    bad_char = {}
    for i, char in enumerate(pattern):
        bad_char[char] = len(pattern) - 1 - i
    
    # Search using Bad Character heuristic
    positions = []
    i = 0
    
    while i <= len(seq) - len(pattern):
        j = len(pattern) - 1
        
        # Check pattern from right to left
        while j >= 0 and pattern[j] == seq[i + j]:
            j -= 1
        
        if j < 0:
            # Pattern found
            positions.append(i)
            i += 1
        else:
            # Mismatch - use bad character rule
            bad_char_shift = bad_char.get(seq[i + j], len(pattern))
            i += max(1, bad_char_shift)
    
    return positions, bad_char


def format_bad_char_table(bad_char, pattern):
    """Format Bad Character table for display"""
    result = "\nCharacter | Shift\n"
    result += "-" * 20 + "\n"
    
    # Show shifts for characters in pattern
    seen = set()
    for char in pattern:
        if char not in seen:
            shift = bad_char.get(char, len(pattern))
            result += f"{char:9s} | {shift:5d}\n"
            seen.add(char)
    
    # Show shift for characters not in pattern
    result += f"{'Other':9s} | {len(pattern):5d}\n"
    
    return result


def format_match_results(seq, pattern, positions, max_display=10):
    """Format match results with context"""
    if not positions:
        return "No matches found.\n"
    
    result = ""
    
    for i, pos in enumerate(positions[:max_display], 1):
        result += f"Match {i} at position {pos}:\n"
        
        # Show context
        context_start = max(0, pos - 10)
        context_end = min(len(seq), pos + len(pattern) + 10)
        context = seq[context_start:context_end]
        
        result += f"  {context}\n"
        
        # Show pointer
        pointer_offset = pos - context_start
        result += f"  {' ' * pointer_offset}{'^' * len(pattern)}\n\n"
    
    if len(positions) > max_display:
        result += f"... and {len(positions) - max_display} more matches\n"
    
    return result