import argparse
import cProfile
import os
import time

from colorama import Fore, init

import global_variables
from help_func import (process_command, read_commands_from_file, read_json, show_current_folder)


def main(args):
    files = []
    added_files = []
    dict = {}    
        
    print(Fore.YELLOW + "Type '?' for help" + Fore.RESET)
            
    commands = read_commands_from_file()
    
    while len(commands) > 0:
        command = commands.pop(0)
        print(Fore.GREEN + f"{global_variables.path} >> {command}" + Fore.RESET)
        command_start_time = time.time()
        process_command(command, dict, files, added_files)
        print(f"Command took {time.time() - command_start_time:.4f} seconds to run")
    
    while True:  
        command = input(Fore.GREEN + f"{global_variables.path} >> " + Fore.RESET)
            
        command_start_time = time.time()
        
        result = process_command(command, dict, files, added_files)
        
        print(f"Command took {time.time() - command_start_time:.4f} seconds to run")
        if result == -1:
            break


# SCENARIOS         
{                     
# def scenario_1():
#     global_variables.path = "C:\\Users\\Administrator\\Documents\\bakalarska_prace\\files"
    
#     files = []
#     added_files = []
#     dict = {}
    
#     read_json("settings.json")
    
#     print(Fore.YELLOW + "Settings:" + Fore.RESET)
#     print(f"Default unit: {global_variables.default_unit}")
#     print(f"Search folders: {global_variables.search_folders}")
#     print(f"Show duplicity: {global_variables.show_duplicity}")

#     print(Fore.YELLOW + "Files:" + Fore.RESET)
#     for file in os.listdir(global_variables.path):
#         print(file)
        
#     print(Fore.GREEN + ">> filter name *.txt" + Fore.RESET, end="")
#     input()
#     files = filter("filter name *.txt".split(" "))
    
#     print(Fore.GREEN + ">> add *" + Fore.RESET, end="")
#     input()
#     add("*", files, added_files)
    
#     print(Fore.GREEN + ">> save to a" + Fore.RESET, end="")
#     input()
#     save("a", added_files, dict)
    
#     print(Fore.GREEN + ">> filter name *.py" + Fore.RESET, end="")
#     input()
#     files = filter("filter name *.py".split(" "))
    
#     print(Fore.GREEN + ">> add *" + Fore.RESET, end="")
#     input()
#     add("*", files, added_files)
    
#     print(Fore.GREEN + ">> show" + Fore.RESET, end="")
#     input()
#     show_added_files(added_files)
    
#     print(Fore.GREEN + ">> save to b" + Fore.RESET, end="")
#     input()
#     save("b", added_files, dict)
    
#     print(Fore.GREEN + ">> remove *" + Fore.RESET, end="")
#     input()
#     r = remove(["remove", "*"], added_files)
#     print(f"Removed {r} files")
    
#     print(Fore.GREEN + ">> a U b" + Fore.RESET, end="")
#     input()
#     files = set_operations("a U b", dict)
    
#     print(Fore.GREEN + ">> add *" + Fore.RESET, end="")
#     input()
#     add("*", files, added_files)
    
#     print(Fore.GREEN + ">> output" + Fore.RESET, end="")
#     input()
#     output(added_files)
    
# def scenario_2():
#     global_variables.path = "C:\\Users\\Administrator\\Documents\\bakalarska_prace\\files"
    
#     files = []
#     added_files = []
#     added_folders = []
#     dict = {}
    
#     read_json("settings.json")
#     added_folders.extend(read_added_folders())
    
#     print(Fore.YELLOW + "Settings:" + Fore.RESET)
#     print(f"Default unit: {global_variables.default_unit}")
#     print(f"Search folders: {global_variables.search_folders}")
#     print(f"Show duplicity: {global_variables.show_duplicity}")

#     print(Fore.YELLOW + "Files:" + Fore.RESET)
#     for file in os.listdir(global_variables.path):
#         print(file)
        
#     if added_folders != []:
#         for x in added_folders:
#             files.extend(add_folder(x))
#         print("Added folders:")
#         for folder in added_folders:
#             print(folder)
#         print("Files from folders:")
#         for x in files:
#             print(x)
            
#     print(Fore.GREEN + ">> filter modified < 10 w" + Fore.RESET, end="")
#     input()
#     files = filter(str("filter modified < 10 w").split(" "))
#     add_history("filter modified < 10 w", files)
    
#     print(Fore.GREEN + ">> sort by modified" + Fore.RESET, end="")
#     input()
#     files = sort(str("sort by modified").split(" "), files)
#     add_history("sort by size", files)
    
#     print(Fore.GREEN + ">> history" + Fore.RESET, end="")
#     input()
#     print_history()
    
#     print(Fore.GREEN + ">> filter *" + Fore.RESET, end="")
#     input()
#     files = filter(str("filter *").split(" "))
#     add_history("filter *", files)
    
#     print(Fore.GREEN + ">> filter name *.py" + Fore.RESET, end="")
#     input()
#     files = filter(str("filter name *.py").split(" "))
#     add_history("filter name *.py", files)
    
#     print(Fore.GREEN + ">> history" + Fore.RESET, end="")
#     input()
#     print_history()
    
#     print(Fore.GREEN + ">> history 1" + Fore.RESET, end="")
#     input()
#     try:
#         files = load_history(1)
#         show_files(files)
#     except:
#         print("Wrong input")
        
#     print(Fore.GREEN + ">> select top 5" + Fore.RESET, end="")
#     input()
#     files = select(str("select top 5").split(" "), files)
#     add_history("select top 5", files)
    
#     print(Fore.GREEN + ">> add *" + Fore.RESET, end="")
#     input()
#     add("*", files, added_files)
    
#     print(Fore.GREEN + ">> output" + Fore.RESET, end="")
#     input()
#     output(added_files)
}

if __name__ == "__main__":
    init()
    parser = argparse.ArgumentParser(description="Process some integers.")
    parser.add_argument('-p', type=str, default="", help='Path to the folder')
    
    args = parser.parse_args()
    
    start_time = time.time()
    
    
    read_json("settings.json")
    
    if args.p != "":
        print(f"args.p: {args.p}")
        if os.path.exists(args.p):
            global_variables.path = args.p
        else:
            print("Path not found")
        
        
    print(Fore.YELLOW + "Settings:" + Fore.RESET)
    print(f"Default unit: {global_variables.default_unit}")
    print(f"Search folders: {global_variables.search_folders}")
    print(f"Show duplicity: {global_variables.show_duplicity}")

    
    # cProfile.run("main(args)", sort="tottime")
    main(args)
    # scenario_1()
    # scenario_2()
    print(f"Program took {time.time() - start_time:.4f} seconds to run")
    
    # main()