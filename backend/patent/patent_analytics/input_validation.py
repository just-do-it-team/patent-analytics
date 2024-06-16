def validate_string(s):
    parts = s.split(';')
    if len(parts[0])!=10 and len(parts[0])!=12:
        return False
    if not all(part.isdigit() for part in parts):
        return False
    return all(len(part) == 10 or 12 for part in parts)

def validate_list(s):
    return s