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
        k: Minimum overlap length
    
    Returns:
        List of tuples: (index_a, index_b, overlap_length, overlap_sequence)
        Sorted by overlap length (descending)
    """
    overlaps = []

    for i, a in enumerate(reads):
        for j, b in enumerate(reads):
            if i == j:
                continue
            olen = find_overlap(a, b, k)
            if olen > 0:
                overlaps.append((i, j, olen, a[-olen:]))

    # Sort by overlap length (descending)
    overlaps.sort(key=lambda x: x[2], reverse=True)
    return overlaps


def format_overlap_table(overlaps):
    """
    Format overlap results as a table
    
    Args:
        overlaps: List of overlap tuples
    
    Returns:
        Formatted string table
    """
    if not overlaps:
        return "No overlaps found.\n"

    result = ""
    result += f"{'Seq A':10s} {'Seq B':10s} {'Overlap':10s}\n"
    result += "-" * 40 + "\n"

    for i, j, olen, _ in overlaps:
        result += f"{i:<10d} {j:<10d} {olen:<10d}\n"

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
        overlaps: List of overlap tuples
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

    overlap_lengths = [o[2] for o in overlaps]

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
    Original implementation from bioinfmatch.py
    Returns dictionary with overlap information
    
    Args:
        reads: List of sequences
        k: Minimum overlap length
    
    Returns:
        Dictionary mapping sequence pairs to overlap lengths
    """
    olap = {}
    for a, b in permutations(reads, 2):
        olen = find_overlap(a, b, k)
        if olen > 0:
            olap[(a, b)] = olen
    return olap