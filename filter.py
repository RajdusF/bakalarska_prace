import filecmp
import glob
import os
import time

from colorama import Fore

import global_variables
from help_func import recalculate_size, search_folder, time_from_now

FILE_NAME_WIDTH = 48
SIZE_WIDTH = 18
MODIFIED_WIDTH = 16
CREATED_WIDTH = 16


def filter(commands):

    # Inicialization
    size = None
    size_operator = None
    name = None
    modified = None
    modified_operator = None
    created = None
    created_operator = None
    time_unit = None
    duplicates = []
    
    
    # Searching for name, size, modified
    if "name" in commands:
        name_index = commands.index("name") + 1
        if name_index < len(commands):
            name = commands[name_index]    
    elif commands[commands.index("filter") + 1] == "*":
        name = "*"            
                    
    if "size" in commands:
        operator_index = commands.index("size") + 1
        if operator_index < len(commands):
            size_operator = commands[operator_index]
            size_index = operator_index + 1
            if size_index < len(commands):
                size = int(commands[size_index])
                
    if "modified" in commands:
        modified_operator = commands[commands.index("modified") + 1]
        if commands.index("modified") + 1 < len(commands):
            try:
                modified = int(commands[commands.index("modified") + 2])
            except:
                print("Wrong input")
                return
            if commands.index("modified") + 2 < len(commands):
                time_unit = commands[commands.index("modified") + 3]
        if modified_operator == None or modified == None or time_unit == None:
            print("Wrong input")
            return
        
        
    if "created" in commands:
        created_operator = commands[commands.index("created") + 1]
        if commands.index("created") + 1 < len(commands):
            created = int(commands[commands.index("created") + 2])
            if commands.index("created") + 2 < len(commands):
                time_unit = commands[commands.index("created") + 3]
        if created_operator == None or created == None or time_unit == None:
            print("Wrong input")
            return
                
                
    if name == None and size == None and modified == None and created == None:
        print("Wrong input")
        return
    
    # NAME
    if name:
        if "name" in commands and commands[commands.index("name") - 1] == "not":                # NOT NAME
            all_files = glob.glob(global_variables.path + "\\*", recursive=True)
            name_files = glob.glob(global_variables.path + "\\" + name, recursive=True)
            files = [file for file in all_files if file not in name_files]
            
            only_directories = [d for d in files if os.path.isdir(d)]
        else:                                                                                   # NAME
            files = glob.glob(global_variables.path + "\\" + name, recursive=True)
            only_directories = [d for d in files if os.path.isdir(d)]
    else:                                                                                       # NO NAME                      
        files = glob.glob(global_variables.path + "\\*", recursive=True)
        only_directories = [d for d in files if os.path.isdir(d)]
        
    files_from_folders = []
    
    if global_variables.search_folders == 1:
        for folder in only_directories:
            files_from_folders.extend(search_folder(folder, commands))
    elif global_variables.search_folders == 2:
        all_files = glob.glob(global_variables.path + "\\*", recursive=True)
        all_directories = [d for d in all_files if os.path.isdir(d)]
        for folder in all_directories:
            files_from_folders.extend(search_folder(folder, commands))
            
    for x in files_from_folders:
        if os.path.isfile(x):
            files.append(x)
        
    # NOT
    if size and size_operator and commands[commands.index("size") - 1] != "not":
        if size_operator == "<":
            files = [file for file in files if os.path.getsize(file) < size]
        elif size_operator == "<=":
            files = [file for file in files if os.path.getsize(file) <= size]
        elif size_operator == ">":
            files = [file for file in files if os.path.getsize(file) > size]
        elif size_operator == ">=":
            files = [file for file in files if os.path.getsize(file) >= size]
        elif size_operator == "=":
            files = [file for file in files if os.path.getsize(file) == size]
    elif size and size_operator and commands[commands.index("size") - 1] == "not":
        if size_operator == "<":
            files = [file for file in files if os.path.getsize(file) >= size]
        elif size_operator == "<=":
            files = [file for file in files if os.path.getsize(file) > size]
        elif size_operator == ">":
            files = [file for file in files if os.path.getsize(file) <= size]
        elif size_operator == ">=":
            files = [file for file in files if os.path.getsize(file) < size]
        elif size_operator == "=":
            files = [file for file in files if os.path.getsize(file) != size]
    
    #           m_operator modified time_unit
    # filter modified < 10 days
    if modified and modified_operator and time_unit: 
        files = filter_time(files, modified_operator, modified, time_unit, "modified")
        
    if created and created_operator and time_unit: 
        files = filter_time(files, created_operator, created, time_unit, "created")

    if global_variables.show_duplicity:
        temp = files.copy()
        files.clear()
        seen_files = set()
        duplicates = []

        for x in temp:
            if x not in seen_files:
                for i in temp:
                    if i not in seen_files and x != i and filecmp.cmp(x, i, shallow=True):
                        duplicates.append(i)
                        seen_files.add(i)
                        print(f"{x.split('\\')[-1]:30} == {i.split('\\')[-1]:40} -> Removed {i.split('\\')[-1]}")
                files.append(x)
            seen_files.add(x)
            
    
    print(Fore.GREEN + f"Found {len(files)} files:" + Fore.RESET)      # Number of occurances
    if "-d" in commands:
        print(f"{"file":{FILE_NAME_WIDTH+4}} {"size":{SIZE_WIDTH}} {"modified":{MODIFIED_WIDTH}} {"created":{CREATED_WIDTH}}")
    for file in files:
        file_name = file.split("\\")[-1]
        file_size = os.path.getsize(file)
        is_folder = os.path.isdir(file)
        print(Fore.LIGHTBLUE_EX, end="") if is_folder else print(Fore.RESET, end="")
        
        if "-d" in commands and not is_folder:
            print(f"{file_name:{FILE_NAME_WIDTH}} {recalculate_size(file_size):{SIZE_WIDTH}} {time_from_now(file, 'modified'):{MODIFIED_WIDTH}} {time_from_now(file, 'created'):{CREATED_WIDTH}}")
        elif "-d" in commands and is_folder:
            print(f"{file_name:{FILE_NAME_WIDTH+SIZE_WIDTH+1}} {time_from_now(file, 'modified'):{MODIFIED_WIDTH}} {time_from_now(file, 'created'):{CREATED_WIDTH}}")
        else:
            print(f"{file_name:{FILE_NAME_WIDTH}}", end="")
            if size and size_operator and not is_folder:
                print(f"{recalculate_size(file_size):{SIZE_WIDTH}}", end="")
            else:
                print(" " * 14, end="")
            if modified and modified_operator and time_unit:
                print(f"{time_from_now(file, "modified"):{MODIFIED_WIDTH}}", end="")
            if created and created_operator and time_unit:
                print(f"{time_from_now(file, "created"):{CREATED_WIDTH}}", end="")
            print()
            
            
    if global_variables.show_duplicity == True:
        print(Fore.RED + f"Found {len(duplicates)} duplicates:" + Fore.RESET)
        for duplicate in duplicates:
            file_name = duplicate.split("\\")[-1]
            file_size = os.path.getsize(duplicate)
            print(f"{file_name:35} {recalculate_size(file_size):13}")
                
    return files


def filter_time(in_files, modified_operator, modified, time_unit, option):
    if time_unit == "s" or time_unit == "second" or time_unit == "seconds" or time_unit == "sec":
        n = 1
    elif time_unit == "m" or time_unit == "minute" or time_unit == "minutes" or time_unit == "min":
        n = 60
    elif time_unit == "h" or time_unit == "hour" or time_unit == "hours" or time_unit == "hr":
        n = 60 * 60
    elif time_unit == "d" or time_unit == "day" or time_unit == "days":
        n = 24 * 60 * 60
    elif time_unit == "w" or time_unit == "week" or time_unit == "weeks":
        n = 7 * 24 * 60 * 60
    elif time_unit == "m" or time_unit == "month" or time_unit == "months":
        n = 30 * 24 * 60 * 60
    elif time_unit == "y" or time_unit == "year" or time_unit == "years":
        n = 365 * 24 * 60 * 60
    else:
        print("Wrong time unit")
        return
    
    current_time = time.time()
    
    out_files = []
    
    for file in in_files:
        if option == "modified":
            modification_time = os.path.getmtime(os.path.join(file))
            seconds_from_now = current_time - modification_time
        elif option == "created":
            created_time = os.path.getctime(os.path.join(file))
            seconds_from_now = current_time - created_time
    
        if modified_operator == "<":
            if seconds_from_now / n < modified:
                out_files.append(file)
        elif modified_operator == "<=":
            if seconds_from_now / n <= modified:
                out_files.append(file)
        elif modified_operator == ">":
            if seconds_from_now / n > modified:
                out_files.append(file)
        elif modified_operator == ">=":
            if seconds_from_now / n >= modified:
                out_files.append(file)
        elif modified_operator == "=":
            if seconds_from_now / n == modified:
                out_files.append(file)
                
    return out_files