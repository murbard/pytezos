def get_level_by_index(cycle: int, index=0) -> int:
    return cycle * 4096 + (index % 4096) + 1
