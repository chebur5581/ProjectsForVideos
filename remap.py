def remap(value, old_min, old_max, new_min, new_max):
    newValue = (((value - old_min) * (new_max - new_min)) / (old_max - old_min)) + new_min
    return newValue