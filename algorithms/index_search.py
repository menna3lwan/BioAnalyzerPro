"""
Index Search Module
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
        kmer = seq[i:i+k]
        index.append((kmer, i))
    index.sort()
    return index


def query_index(index, seq, pattern):
    """
    Query index to find pattern
    
    Args:
        index: Sorted k-mer index
        seq: Original sequence
        pattern: Pattern to search
        
    Returns:
        List of positions where pattern is found
    """
    if not index:
        return []
    
    # Get k-mer length from index
    k = len(index[0][0])
    
    # Extract all k-mers from index
    keys = [kmer for kmer, pos in index]
    
    # Find range of k-mers that match pattern prefix
    query_kmer = pattern[:k]
    st = bisect.bisect_left(keys, query_kmer)
    en = bisect.bisect_right(keys, query_kmer)
    
    # Get candidate positions
    candidates = [pos for kmer, pos in index[st:en]]
    
    # Verify full pattern match
    matches = []
    for pos in candidates:
        if seq[pos:pos+len(pattern)] == pattern:
            matches.append(pos)
    
    return sorted(matches)


def get_index_stats(index, seq, k):
    """Get statistics about the index"""
    if not index:
        return {
            'sequence_length': len(seq),
            'k': k,
            'unique_kmers': 0,
            'total_kmers': 0
        }
    
    # Count unique k-mers
    unique_kmers = len(set(kmer for kmer, pos in index))
    
    return {
        'sequence_length': len(seq),
        'k': k,
        'unique_kmers': unique_kmers,
        'total_kmers': len(index)
    }


def format_index_table(index, max_rows=20):
    """Format index table for display"""
    if not index:
        return "Index is empty\n"
    
    result = "\n"
    result += f"{'K-mer':<10s} {'Positions':<50s}\n"
    result += "-" * 60 + "\n"
    
    # Group by k-mer
    kmer_dict = {}
    for kmer, pos in index:
        if kmer not in kmer_dict:
            kmer_dict[kmer] = []
        kmer_dict[kmer].append(pos)
    
    # Display
    count = 0
    for kmer in sorted(kmer_dict.keys()):
        if count >= max_rows:
            remaining = len(kmer_dict) - count
            result += f"\n... and {remaining} more k-mers\n"
            break
        
        positions = kmer_dict[kmer]
        pos_str = str(positions) if len(positions) <= 10 else str(positions[:10]) + "..."
        result += f"{kmer:<10s} {pos_str}\n"
        count += 1
    
    return result