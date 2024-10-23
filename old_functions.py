def filter_by_name(file : str, find : str) -> bool:
    file = file.lower()
    find = find.lower()

    if "*" not in find and "_" not in find:
        return file == find
    elif find == "*":
        return True

    file_index, find_index, last_star_index = 0, 0, -1

    while file_index < len(file):
        if find_index < len(find) and (find[find_index] == "_" or find[find_index] == file[file_index]):
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

def filter_old(file : str, find : str = None , comparing_size = None, operator = None, my_path = None) -> bool:
    bool_name = None
    bool_size = None

    if find:
        bool_name = filter_by_name(file, find)

    if comparing_size and operator:
        if operator == "<":
            bool_size = os.path.getsize(my_path + '\\' + file) < comparing_size
        elif operator == "<=":
            bool_size = os.path.getsize(my_path + '\\' + file) <= comparing_size
        elif operator == ">":
            bool_size = os.path.getsize(my_path + '\\' + file) > comparing_size
        elif operator == ">=":
            bool_size = os.path.getsize(my_path + '\\' + file) >= comparing_size
        elif operator == "=":
            bool_size = os.path.getsize(my_path + '\\' + file) == comparing_size

    if bool_name is None and bool_size is None:
        return False
    if bool_name is None:
        return bool_size
    if bool_size is None:
        return bool_name

    return bool_name and bool_size


        # for file in os.listdir(my_path):
        #     temp_files = []
        #     is_folder = os.path.isdir(my_path + '\\' + file)
        #     if is_folder and search_folders == True:
        #         if filter(file, name, size, operator, my_path):
        #             files.append(my_path + '\\' + file)
        #         temp_files.extend(search_folder(my_path + '\\' + file))
        #         for temp in temp_files:
        #             temp_filename = temp.split("\\")[-1]
                    
        #             if filter(temp_filename, name, size, operator, temp):
        #                 files.append(temp)
        #                 print(f"Added temp file {temp}")
        #     else:
        #         if filter(file, name, size, operator, my_path):
        #             absolute_path = my_path + '\\' + file
        #             files.append(absolute_path)