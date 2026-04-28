import re


def extract_zone(my_string):
    pattern = r"(?:(?<=[\[\s])|^)zone=([^\]\s]+)"
    match = re.search(pattern, my_string)
    if match:
        return match.group(1)
    return None


def extract_color(my_string):
    pattern = r"(?:(?<=[\[\s])|^)color=([^\]\s]+)"
    match = re.search(pattern, my_string)
    if match:
        if (match.group(0).split("=")[0]).strip() != "color":
            raise ValueError(f"This is not valid: {match.group(0)}")
        return match.group(1)
    return None


def extract_max_drones(my_string):
    pattern = r"(?:(?<=[\[\s])|^)max_drones=([^\]\s]+)"
    match = re.search(pattern, my_string)
    rslt = None
    if match:
        try:
            rslt = int(match.group(1))
        except ValueError:
            raise ValueError("Number of drone must be an INTEGER")
        if rslt < 0:
            raise ValueError("Number of drone must be positive")
    return rslt


def extract_max_link_capacity(my_string):
    pattern = r"(?:(?<=[\[\s])|^)max_link_capacity=([^\]\s]+)"
    match = re.search(pattern, my_string)
    rslt = None
    if match:
        try:
            rslt = int(match.group(1))
        except ValueError:
            raise ValueError("Max link capacity must be an INTEGER")
        if rslt < 0:
            raise ValueError("Max link capacity must be positive")
    return rslt


def extract_metadata(my_string):
    pattern = r"\[([^\]]+)\]"
    match = re.search(pattern, my_string)
    if match:
        return match.group(1)
    return None
