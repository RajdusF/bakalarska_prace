import os


def filter_by_name(file : str, find : str) -> bool:
    file = file.lower()
    find = find.lower()

    if "*" not in find and "?" not in find:
        return file == find
    elif find == "*":
        return True

    file_index, find_index, last_star_index = 0, 0, -1

    while file_index < len(file):
        if find_index < len(find) and (find[find_index] == "?" or find[find_index] == file[file_index]):
            file_index += 1
            find_index += 1
        elif find_index < len(find) and find[find_index] == "*":
            last_star_index = find_index
            find_index += 1
            last_match_index = file_index
        elif last_star_index != -1:
            find_index = last_star_index + 1
            last_match_index += 1
            file_index = last_match_index
        else:
            return False

    while find_index < len(find) and find[find_index] == "*":
        find_index += 1

    return find_index == len(find)