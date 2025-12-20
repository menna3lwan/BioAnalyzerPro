"""
Sequence Assembly Module
Contains functions for finding overlaps and assembling sequences
"""

from itertools import permutations


def find_overlap(a, b, min_length=3):
    """
    Find overlap between end of sequence a and start of sequence b
    
    Args:
        a: First sequence (string)
        b: Second sequence (string)
        min_length: Minimum overlap length to consider
    
    Returns:
        Length of overlap (0 if no overlap found)
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
        reads: List of sequences (strings)
        k: Minimum overlap length (minlength)
    
    Returns:
        Dictionary mapping sequence pairs (a, b) to overlap lengths
    """
    overlaps = {}
    for a, b in permutations(reads, 2):
        overlap_length = find_overlap(a, b, k)
        if overlap_length > 0:
            overlaps[(a, b)] = overlap_length
    return overlaps


def format_overlap_table(overlaps, reads=None):
    """
    Format overlap results as a table
    
    Args:
        overlaps: Dictionary of overlap pairs to lengths
        reads: Optional list of original sequences for index lookup
    
    Returns:
        Formatted string table
    """
    if not overlaps:
        return "No overlaps found.\n"

    result = ""
    result += f"{'Seq A':30s} {'Seq B':30s} {'Overlap':10s}\n"
    result += "-" * 80 + "\n"

    # Sort by overlap length (descending)
    sorted_overlaps = sorted(overlaps.items(), key=lambda x: x[1], reverse=True)

    for (seq_a, seq_b), olen in sorted_overlaps:
        # Truncate sequences if too long
        a_display = seq_a if len(seq_a) <= 25 else seq_a[:22] + "..."
        b_display = seq_b if len(seq_b) <= 25 else seq_b[:22] + "..."
        result += f"{a_display:30s} {b_display:30s} {olen:<10d}\n"

    return result


def visualize_overlap(seq_a, seq_b, overlap_len):
    """
    Create visual representation of overlap between two sequences
    
    Args:
        seq_a: First sequence
        seq_b: Second sequence
        overlap_len: Length of overlap
    
    Returns:
        String visualization
    """
    if overlap_len == 0:
        return "No overlap\n"

    start = len(seq_a) - overlap_len

    out = ""
    out += f"Sequence A: {seq_a}\n"
    out += " " * 12 + " " * start + "↓" * overlap_len + "\n"
    out += f"Sequence B: {' ' * start}{seq_b}\n"
    out += f"\nOverlap Region: {seq_a[start:]}\n"
    return out


def get_overlap_stats(overlaps, sequences):
    """
    Calculate statistics about overlaps
    
    Args:
        overlaps: Dictionary of overlap pairs to lengths
        sequences: List of original sequences
    
    Returns:
        Dictionary with statistics
    """
    if not overlaps:
        return {
            "num_sequences": len(sequences),
            "num_overlaps": 0,
            "max_overlap_length": 0,
            "avg_overlap_length": 0
        }

    overlap_lengths = list(overlaps.values())

    return {
        "num_sequences": len(sequences),
        "num_overlaps": len(overlaps),
        "max_overlap_length": max(overlap_lengths),
        "avg_overlap_length": sum(overlap_lengths) / len(overlap_lengths)
    }


def greedy_assembly(reads, k):
    """
    Perform greedy sequence assembly
    
    Args:
        reads: List of sequences to assemble
        k: Minimum overlap length
    
    Returns:
        Tuple of (final_contig, assembly_steps)
    """
    if not reads:
        return "", []

    sequences = reads.copy()
    contig = sequences.pop(0)
    steps = []

    while sequences:
        best_olen = 0
        best_index = None
        best_seq = None

        # Find best overlap
        for idx, seq in enumerate(sequences):
            olen = find_overlap(contig, seq, k)
            if olen > best_olen:
                best_olen = olen
                best_index = idx
                best_seq = seq

        if best_seq is None:
            # No overlap found → append remaining sequences
            for seq in sequences:
                contig += seq
            break

        # Merge sequences
        new_contig = contig + best_seq[best_olen:]

        # Record step
        steps.append({
            "seq1_idx": -1,
            "seq2_idx": best_index,
            "overlap": best_olen,
            "result": new_contig
        })

        contig = new_contig
        sequences.pop(best_index)

    return contig, steps


def native_overlap(reads, k):
    """
    Original implementation - wrapper for find_all_overlaps
    Returns dictionary with overlap information
    
    Args:
        reads: List of sequences
        k: Minimum overlap length
    
    Returns:
        Dictionary mapping sequence pairs to overlap lengths
    """
    return find_all_overlaps(reads, k)