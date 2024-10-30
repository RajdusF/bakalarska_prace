import glob
import os
import time

from colorama import Fore, init

import global_variables
from command_functions import add, output, select, settings, sort
from filter import filter
from help_func import help, read_json


def main():
    files = []
    added_files = []
    
    read_json("settings.json")
    
    if os.path.exists("output.txt"):
        os.remove("output.txt")
    
    default_unit = global_variables.default_unit
    search_folders = global_variables.search_folders
    show_duplicity = global_variables.show_duplicity
    
    print(Fore.YELLOW + "Settings:" + Fore.RESET)
    print(f"Default unit: {default_unit}")
    print(f"Search folders: {search_folders}")
    print(f"Show duplicity: {show_duplicity}")

    print(Fore.YELLOW + "Files:" + Fore.RESET)
    for file in os.listdir(global_variables.path):
        print(file)
        
    print(Fore.YELLOW + "Type '?' for help" + Fore.RESET)
    
    while True:  
        command = input(Fore.GREEN + ">> " + Fore.RESET)
        commands = command.split(" ")
        
        if command == "exit":
            break
        
        if command == "?":
            help()
            continue
        
        if "**" in command:
            print("Wrong input")
            continue
        
        if command == "*":
            for file in os.listdir(global_variables.path):
                print(file)
                
        elif command == "cd.." or command == "cd ..":
            global_variables.path = os.path.abspath(os.path.join(global_variables.path, os.pardir))
            print(Fore.GREEN + f"Current path: {global_variables.path}" + Fore.RESET)
            
        elif "cd" in command:
            path_index = commands.index("cd") + 1
            if path_index < len(commands):
                path = commands[path_index]
                if os.path.isdir(global_variables.path + "\\" + path):
                    global_variables.path = global_variables.path + "\\" + path
                    print(Fore.GREEN + f"Current path: {global_variables.path}" + Fore.RESET)
                else:
                    print("Path not found")
            else:
                print(Fore.GREEN + f"Current path: {global_variables.path}" + Fore.RESET)
                
        elif "filter" in commands:
            files = filter(commands)          
        
        elif "sort" in commands:
            files = sort(commands, files)
            
        elif "select" in commands:
            files = select(commands, files)
        
        elif "find" in commands:
            finds = []
            for file in added_files:
                finds.extend(find(commands[commands.index("find") + 1:], file))
                
            print(Fore.GREEN + f"Found {len(finds)} occurances:" + Fore.RESET)
            for find in finds:
                print(find)
        
        elif "add" in commands:
            if commands[1] == "*":
                add("*", files, added_files)
                continue
            elif len(commands) == 2:
                    name = commands[1]
                    if(add(name, files, added_files) > 0):
                        print("Added files:")
                        for x in added_files:
                            print(x)
            else:
                print("Wrong input")
                
        elif "remove" in commands:
            if commands[1] == "*":
                added_files.clear()
                print("All files removed")
                continue
            name = commands[1]
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
            elif "duplicity" in commands or "duplicate" in commands and len(commands) == 3:
                settings(2, int(commands[2]))
            elif len(commands) == 1:
                print(f"Default unit: {default_unit}")
                print(f"Search folders: {search_folders}")
                print(f"Show duplicity: {show_duplicity}")
                continue
            
            default_unit = global_variables.default_unit
            search_folders = global_variables.search_folders
            show_duplicity = global_variables.show_duplicity
            
        elif "output" in commands and len(commands) == 1:
            output(added_files)
            
        else:
            print("Wrong input")
            
if __name__ == "__main__":
    start_time = time.time()
    init()
    main()
    print(f"My program took {time.time() - start_time:.4f} seconds to run")