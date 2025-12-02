def build_suffix_array(text):
    if not text.endswith('$'):
        text = text + '$'
    
    text = text.upper()
    n = len(text)

    suffixes = []
    for i in range(n):
        suffixes.append((text[i:], i))

    suffixes.sort()
    
    suffix_array = [pos for suffix, pos in suffixes]
    steps = [(suffix, pos) for suffix, pos in suffixes]
    
    return suffix_array, steps


def format_suffix_array(text, suffix_array, steps):
    result = "All Suffixes (sorted lexicographically):\n\n"
    result += f"{'Index':<8s} {'Suffix':<30s}\n"
    result += "-" * 40 + "\n"
    
    for suffix, pos in steps:
        display_suffix = suffix if len(suffix) <= 25 else suffix[:25] + "..."
        result += f"{pos:<8d} {display_suffix}\n"
    
    result += "\n"
    result += f"Suffix Array: {suffix_array}\n"
    
    return result


def search_suffix_array(text, suffix_array, pattern):
    matches = []
    for pos in suffix_array:
        if text[pos:].startswith(pattern):
            matches.append(pos)
    return sorted(matches)
