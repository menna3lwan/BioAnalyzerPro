"""
Edit Distance Algorithm Module (Dynamic Programming)
Calculates the minimum number of operations needed to transform one sequence into another
Operations: Insertion, Deletion, Substitution
"""


def edit_distance_DP(x, y):
    """
    Calculate edit distance between two sequences using Dynamic Programming.
    
    Args:
        x (str): First sequence
        y (str): Second sequence
    
    Returns:
        int: Minimum edit distance
    """
    # Initialize DP matrix
    D = []
    for i in range(len(x) + 1):
        D.append([0] * (len(y) + 1))
    
    # Initialize first column (deletions from x)
    for i in range(len(x) + 1):
        D[i][0] = i
    
    # Initialize first row (insertions to match y)
    for i in range(len(y) + 1):
        D[0][i] = i
    
    # Fill the DP matrix
    for i in range(1, len(x) + 1):
        for j in range(1, len(y) + 1):
            # Cost of substitution (0 if characters match, 1 if different)
            delta = 1 if x[i-1] != y[j-1] else 0
            
            # Choose minimum cost operation
            D[i][j] = min(
                D[i-1][j-1] + delta,  # Substitution (or match)
                D[i-1][j] + 1,         # Deletion
                D[i][j-1] + 1          # Insertion
            )
    
    return D[-1][-1]


def edit_distance_with_matrix(x, y):
    """
    Calculate edit distance and return both distance and DP matrix.
    
    Args:
        x (str): First sequence
        y (str): Second sequence
    
    Returns:
        tuple: (edit_distance, DP_matrix)
    """
    # Initialize DP matrix
    D = []
    for i in range(len(x) + 1):
        D.append([0] * (len(y) + 1))
    
    # Initialize first column
    for i in range(len(x) + 1):
        D[i][0] = i
    
    # Initialize first row
    for i in range(len(y) + 1):
        D[0][i] = i
    
    # Fill the DP matrix
    for i in range(1, len(x) + 1):
        for j in range(1, len(y) + 1):
            delta = 1 if x[i-1] != y[j-1] else 0
            D[i][j] = min(
                D[i-1][j-1] + delta,
                D[i-1][j] + 1,
                D[i][j-1] + 1
            )
    
    return D[-1][-1], D


def traceback_alignment(x, y, D):
    """
    Traceback through DP matrix to find optimal alignment.
    
    Args:
        x (str): First sequence
        y (str): Second sequence
        D (list): DP matrix from edit_distance_with_matrix
    
    Returns:
        tuple: (aligned_x, aligned_y, operations)
    """
    i = len(x)
    j = len(y)
    
    aligned_x = []
    aligned_y = []
    operations = []
    
    while i > 0 or j > 0:
        if i > 0 and j > 0:
            delta = 0 if x[i-1] == y[j-1] else 1
            
            # Check which operation was used
            if D[i][j] == D[i-1][j-1] + delta:
                if delta == 0:
                    operations.append('match')
                else:
                    operations.append('substitute')
                aligned_x.append(x[i-1])
                aligned_y.append(y[j-1])
                i -= 1
                j -= 1
            elif D[i][j] == D[i-1][j] + 1:
                operations.append('delete')
                aligned_x.append(x[i-1])
                aligned_y.append('-')
                i -= 1
            else:
                operations.append('insert')
                aligned_x.append('-')
                aligned_y.append(y[j-1])
                j -= 1
        elif i > 0:
            operations.append('delete')
            aligned_x.append(x[i-1])
            aligned_y.append('-')
            i -= 1
        else:
            operations.append('insert')
            aligned_x.append('-')
            aligned_y.append(y[j-1])
            j -= 1
    
    # Reverse to get correct order
    aligned_x.reverse()
    aligned_y.reverse()
    operations.reverse()
    
    return ''.join(aligned_x), ''.join(aligned_y), operations


def format_matrix(D, x, y):
    """
    Format DP matrix for display.
    
    Args:
        D (list): DP matrix
        x (str): First sequence
        y (str): Second sequence
    
    Returns:
        str: Formatted matrix string
    """
    result = []
    
    # Header row
    header = "      " + "  ".join([" "] + list(y))
    result.append(header)
    result.append("-" * len(header))
    
    # Matrix rows
    for i in range(len(x) + 1):
        if i == 0:
            row_label = " "
        else:
            row_label = x[i-1]
        
        row = f"{row_label:2} | " + "  ".join(f"{D[i][j]:2}" for j in range(len(y) + 1))
        result.append(row)
    
    return "\n".join(result)


def format_alignment(aligned_x, aligned_y, operations):
    """
    Format alignment for display.
    
    Args:
        aligned_x (str): Aligned first sequence
        aligned_y (str): Aligned second sequence
        operations (list): List of operations
    
    Returns:
        str: Formatted alignment string
    """
    result = []
    
    # Create middle line showing matches/mismatches
    middle = []
    for i in range(len(aligned_x)):
        if operations[i] == 'match':
            middle.append('|')
        elif operations[i] == 'substitute':
            middle.append('x')
        elif operations[i] == 'delete':
            middle.append('^')
        else:  # insert
            middle.append('v')
    
    result.append("Alignment:")
    result.append(f"  {aligned_x}")
    result.append(f"  {''.join(middle)}")
    result.append(f"  {aligned_y}")
    result.append("")
    result.append("Legend: | = match, x = substitution, ^ = deletion, v = insertion")
    
    # Count operations
    match_count = operations.count('match')
    sub_count = operations.count('substitute')
    del_count = operations.count('delete')
    ins_count = operations.count('insert')
    
    result.append("")
    result.append(f"Matches: {match_count}")
    result.append(f"Substitutions: {sub_count}")
    result.append(f"Deletions: {del_count}")
    result.append(f"Insertions: {ins_count}")
    
    return "\n".join(result)


if __name__ == "__main__":
    # Test the algorithm
    x = "ACGACGT"
    y = "TCGTACGT"
    
    print(f"Sequence X: {x}")
    print(f"Sequence Y: {y}")
    print()
    
    # Calculate edit distance
    distance = edit_distance_DP(x, y)
    print(f"Edit Distance: {distance}")
    print()
    
    # Get matrix
    distance, matrix = edit_distance_with_matrix(x, y)
    print("DP Matrix:")
    print(format_matrix(matrix, x, y))
    print()
    
    # Get alignment
    aligned_x, aligned_y, ops = traceback_alignment(x, y, matrix)
    print(format_alignment(aligned_x, aligned_y, ops))