"""
Index-Based Search Algorithm
K-mer indexing for fast pattern matching
"""

import bisect


def build_index(seq, k):
    """
    Build sorted k-mer index
    
    Args:
        seq: DNA sequence
        k: K-mer size
        
    Returns:
        Sorted list of (k-mer, position) tuples
    """
    index = []
    for i in range(len(seq) - k + 1):
        index.append((seq[i:i+k], i))
    index.sort()
    return index


def query_index(t, p, index):
    """
    Query index to find pattern
    
    Args:
        t: Original sequence
        p: Pattern to search
        index: Sorted index
        
    Returns:
        List of positions where pattern is found
    """
    if not index:
        return []
    
    keys = [r[0] for r in index]
    k_len = len(keys[0])
    
    st = bisect.bisect_left(keys, p[:k_len])
    en = bisect.bisect(keys, p[:k_len])
    hits = index[st:en]
    
    l = [h[1] for h in hits]
    offsets = []
    for i in l:
        if t[i:i+len(p)] == p:
            offsets.append(i)
    
    return offsets


def get_index_stats(index):
    """Get statistics about the index"""
    if not index:
        return {}
    
    kmer_counts = {}
    for kmer, pos in index:
        kmer_counts[kmer] = kmer_counts.get(kmer, 0) + 1
    
    return {
        'total_kmers': len(index),
        'unique_kmers': len(kmer_counts),
        'k': len(index[0][0]) if index else 0,
        'most_common': sorted(kmer_counts.items(), key=lambda x: x[1], reverse=True)[:5]
    }


def format_index_table(index, max_rows=20):
    """Format index table for display"""
    if not index:
        return "Index is empty"
    
    result = "K-mer Index (sorted):\n\n"
    result += "K-mer    Position\n"
    result += "-" * 20 + "\n"
    
    for kmer, pos in index[:min(max_rows, len(index))]:
        result += f"{kmer:8s} {pos:8d}\n"
    
    if len(index) > max_rows:
        result += f"\n... ({len(index) - max_rows} more entries)\n"
    
    result += f"\nTotal entries: {len(index)}\n"
    
    return result