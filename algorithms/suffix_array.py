"""
Suffix Array Algorithm
Build suffix array using iterative doubling
"""


def build_suffix_array(T):
    """
    Build suffix array
    
    Args:
        T: Input text
        
    Returns:
        Table of ranks at each iteration
    """
    if not T.endswith('$'):
        T = T + '$'
    
    T = T.upper()
    
    dec = {'$': 0, 'A': 1, 'C': 2, 'G': 3, 'T': 4}
    table = []
    i = 2**0
    n = 0
    
    while True:
        l = []
        dec2 = {}
        
        if i > 1:
            for j in range(len(T)):
                if not (table[n-1][j:j+i] in l):
                    l.append(table[n-1][j:j+i])
            l.sort()
            for j in range(len(l)):
                dec2[tuple(l[j])] = j
        
        row = []
        for j in range(len(T)):
            if i == 1:
                row.append(dec[T[j]])
            else:
                row.append(dec2[tuple(table[n-1][j:j+i])])
        
        table.append(row)
        
        flag = 0
        for j in range(len(row)):
            c = row.count(j)
            if c > 1:
                flag = 1
                break
        
        if flag == 0:
            break
        
        n += 1
        i = 2**n
    
    return table, T


def format_suffix_array(table, text):
    """Format suffix array for display"""
    result = "Suffix Array Construction:\n\n"
    result += f"Text: {text}\n"
    result += f"Length: {len(text)}\n\n"
    
    result += "Pos | Suffix        | "
    for i in range(len(table)):
        result += f"2^{i} "
    result += "\n"
    result += "-" * (25 + len(table) * 4) + "\n"
    
    for j in range(len(text)):
        suffix = text[j:min(j+10, len(text))]
        if len(text[j:]) > 10:
            suffix += "..."
        result += f"{j:3d} | {suffix:13s} | "
        for i in range(len(table)):
            result += f"{table[i][j]:3d} "
        result += "\n"
    
    result += "\n"
    
    # Show final order
    final_ranks = table[-1]
    sorted_indices = sorted(range(len(final_ranks)), key=lambda k: final_ranks[k])
    
    result += "Final Suffix Array Order:\n"
    result += "Rank | Position | Suffix\n"
    result += "-" * 40 + "\n"
    
    for rank, idx in enumerate(sorted_indices):
        suffix = text[idx:min(idx+15, len(text))]
        if len(text[idx:]) > 15:
            suffix += "..."
        result += f"{rank:4d} | {idx:8d} | {suffix}\n"
    
    return result