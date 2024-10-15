import os
import time

from colorama import Fore, init

import global_variables
from command_functions import add, filter, find, settings
from help_func import (help, process_command, read_json, recalculate_size,
                       search_folder)

# path="C:\\Users\\Filip\\Downloads"
my_path="C:\\Users\\Filip\\Documents\\bakalarska_prace\\files"

def main():
    files = []
    added_files = []
    
    read_json("settings.json")
    
    default_unit = global_variables.default_unit
    search_folders = global_variables.search_folders
    
    
    print(f"Default unit: {default_unit}")
    print(f"Search folders: {search_folders}")

    for file in os.listdir(my_path):
        print(file)
        
    print(Fore.YELLOW + "Type '?' for help" + Fore.RESET)
    
    # find(["SiteID", "<", "5"], "C:\\Users\\Filip\\Documents\\bakalarska_prace\\files\\exp_refineFinal1_r_cropped.cmap")
    # print(find(["SiteID", ">", "650"], "C:\\Users\\Filip\\Documents\\bakalarska_prace\\files\\exp_refineFinal1_r_cropped.cmap"))
    # print(find([""], "C:\\Users\\Filip\\Documents\\bakalarska_prace\\files\\exp_refineFinal1_r_cropped.cmap"))
    
    # file = "C:\\Users\\Filip\\Documents\\bakalarska_prace\\files\\exp_refineFinal1_r_cropped.cmap"
    
    # command = input(Fore.GREEN + "> " + Fore.RESET)
    # command = "find all \"Number of Testing\""
    # parts = process_command(command)
    
    # print(find(parts[parts.index("find") + 1:], file))
    
    # return
    
    while True:  
        command = input(Fore.GREEN + "> " + Fore.RESET)
        commands = command.split(" ")
        
        # name = commands[0]
        # files.clear()
        # for file in os.listdir(path):
        #     if filter(file, name):
        #         files.append(file)
                
        # print(Fore.GREEN + f"Founded {len(files)} files" + Fore.RESET)      # Number of occurances
        # for x in files:
        #     print(x)
                
        # print("Files: ", files)
                
        # continue
        
        if command == "exit":
            break
        
        if command == "?":
            help()
            continue
        
        if "**" in command:
            print("Wrong input")
            continue
        
        if command == "*":
            for file in os.listdir(my_path):
                print(file)
                
        elif "filter" in commands:
            size = None
            operator = None
            name = None
            
            if "name" in commands:
                name_index = commands.index("name") + 1
                if name_index < len(commands):
                    name = commands[name_index]    
            elif commands[commands.index("filter") + 1] == "*":
                name = "*"            
                            
            if "size" in commands:
                operator_index = commands.index("size") + 1
                if operator_index < len(commands):
                    operator = commands[operator_index]
                    size_index = operator_index + 1
                    if size_index < len(commands):
                        size = int(commands[size_index])
                        
            if name or size:
                files.clear()
                for file in os.listdir(my_path):
                    temp_files = []
                    is_folder = os.path.isdir(my_path + '\\' + file)
                    if is_folder and search_folders == True:
                        if filter(file, name, size, operator, my_path):
                            files.append(my_path + '\\' + file)
                        temp_files.extend(search_folder(my_path + '\\' + file))
                        for temp in temp_files:
                            temp_filename = temp.split("\\")[-1]
                            
                            if filter(temp_filename, name, size, operator, temp):
                                files.append(temp)
                                print(f"Added temp file {temp}")
                    else:
                        if filter(file, name, size, operator, my_path):
                            absolute_path = my_path + '\\' + file
                            files.append(absolute_path)
                    
                        
                print(Fore.GREEN + f"Found {len(files)} files" + Fore.RESET)      # Number of occurances
                for file in files:
                    file_name = file.split("\\")[-1]
                    file_size = os.path.getsize(file)
                    is_folder = os.path.isdir(file)
                    if is_folder:
                        print(f"{file_name:25}")
                    else:
                        print(f"{file_name:25} {str(recalculate_size(file_size, default_unit))} {default_unit}")
            else:
                print("Wrong input")
                
        
        elif "find" in commands:
            finds = []
            for file in added_files:
                finds.extend(find(commands[commands.index("find") + 1:], file))
                
            print(Fore.GREEN + f"Found {len(finds)} occurances" + Fore.RESET)
            for find in finds:
                print(find)
        
        elif "add" in commands:
            if commands[1] == "*":
                add("*", files, added_files)
                continue
            elif "name" in commands:
                name_index = commands.index("name") + 1
                if name_index < len(commands):
                    name = commands[name_index]
                    add(name, files, added_files)
            
            print("Files added")
                
        elif "remove" in commands and "name" in commands:
            name_index = commands.index("name") + 1
            if name_index < len(commands):
                name = commands[name_index]
                if name in added_files:
                    added_files.remove(name)
                    print("File removed")
                else:
                    print("File not found")
                
        elif "show" in commands:
            print("Added files:")
            for x in added_files:
                print(x)
            
        elif "set" in commands:
            if "unit" in commands and len(commands) == 3:
                settings(0, commands[2])
                
            elif "search" in commands and len(commands) == 3:
                settings(1, int(commands[2]))
                
            else:
                print("Wrong input")
                continue
            
            default_unit = global_variables.default_unit
            search_folders = global_variables.search_folders
            
        else:
            print("Wrong input")
            
if __name__ == "__main__":
    start_time = time.time()
    init()
    main()
    print(f"My program took {time.time() - start_time:.4f} seconds to run")