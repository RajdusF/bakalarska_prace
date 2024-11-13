import argparse
import cProfile
import os
import time

from colorama import Fore, init

import global_variables
from command_functions import (add, add_folder, output, remove, save, select,
                               set_operations, settings, sort)
from filter import filter
from help_func import (add_history, help, load_history, print_history,
                       read_added_folders, read_json, show_added_files,
                       show_files)


def main(args):
    print(f"args.p: {args.p}")
    files = []
    added_files = []
    added_folders = []
    dict = {}
    
    read_json("settings.json")
    added_folders.extend(read_added_folders())
    
    if args.p != "":
        if os.path.exists(args.p):
            global_variables.path = args.p
        else:
            print("Path not found")
            return
        
    
    if os.path.exists("output.txt"):
        os.remove("output.txt")
    
    
    print(Fore.YELLOW + "Settings:" + Fore.RESET)
    print(f"Default unit: {global_variables.default_unit}")
    print(f"Search folders: {global_variables.search_folders}")
    print(f"Show duplicity: {global_variables.show_duplicity}")

    print(Fore.YELLOW + "Files:" + Fore.RESET)
    for file in os.listdir(global_variables.path):
        print(file)
        
    print(Fore.YELLOW + "Type '?' for help" + Fore.RESET)
    
    if added_folders != []:
        for x in added_folders:
            files.extend(add_folder(x))
        print("Added folders:")
        for folder in added_folders:
            print(folder)
        print("Files from folders:")
        for x in files:
            print(x)
    
    while True:  
        if args.c != "":
            command = args.c
            args.c = ""
        else:
            command = input(Fore.GREEN + f"{global_variables.path} >> " + Fore.RESET)
        command_start_time = time.time()
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
            add_history(command, files)
        
        elif "sort" in commands:
            files = sort(commands, files)
            add_history(command, files)
            
        elif "select" in commands:
            files = select(commands, files)
            add_history(command, files)
        
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
                # continue
            elif "\\" in command and len(commands) == 2:
                files.extend(add_folder(commands[1]))
                show_files(files)
            elif len(commands) == 2:
                    name = commands[1]
                    if(add(name, files, added_files) > 0):
                        print("Added files:")
                        for x in added_files:
                            print(x)
            else:
                print("Wrong input")
                
        elif "remove" in commands:
            r = remove(commands, added_files)
            print(f"Removed {r} files")
                
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
                print(f"Default unit: {global_variables.default_unit}")
                print(f"Search folders: {global_variables.search_folders}")
                print(f"Show duplicity: {global_variables.show_duplicity}")
                continue

            
        elif commands[0] == "save" and commands[1] == "to" and len(commands) == 3:
            save(added_files, commands[2])
            
        elif commands[0] == "load" and commands[1] == "from" and len(commands) == 3:
            if commands[2] in dict:
                added_files = dict[commands[2]].copy()
                print("Files loaded")
            else:
                print("File not found")
                    
        
        elif "output" in commands and len(commands) == 1:
            output(added_files)
            
        elif "history" in commands and len(commands) == 1:
            print_history()
            
        elif "history" in commands and len(commands) == 2:
            try:
                files = load_history(int(commands[1]))
                show_files(files)
            except:
                print("Wrong input")
            
        # Sjednocení, průnik, rozdíl
        elif "A" in commands or "U" in commands or "-" in commands:
            dict["a"] = [1]
            dict["b"] = [2]
            dict["c"] = [3]
            files = set_operations(command, dict)
            
            
        elif command == "":
            continue
        
        else:
            print("Wrong input")
            
        print(f"Command took {time.time() - command_start_time:.4f} seconds to run")
        if args.c != "":
            break
                     
def scenario_1():
    global_variables.path = "C:\\Users\\Filip\\Documents\\bakalarska_prace\\files"
    
    files = []
    added_files = []
    dict = {}
    
    read_json("settings.json")
    
    print(Fore.YELLOW + "Settings:" + Fore.RESET)
    print(f"Default unit: {global_variables.default_unit}")
    print(f"Search folders: {global_variables.search_folders}")
    print(f"Show duplicity: {global_variables.show_duplicity}")

    print(Fore.YELLOW + "Files:" + Fore.RESET)
    for file in os.listdir(global_variables.path):
        print(file)
        
    print(Fore.GREEN + ">> filter name *.txt" + Fore.RESET, end="")
    input()
    files = filter("filter name *.txt".split(" "))
    
    print(Fore.GREEN + ">> add *" + Fore.RESET, end="")
    input()
    add("*", files, added_files)
    
    print(Fore.GREEN + ">> save to a" + Fore.RESET, end="")
    input()
    save("a", added_files, dict)
    
    print(Fore.GREEN + ">> filter name *.py" + Fore.RESET, end="")
    input()
    files = filter("filter name *.py".split(" "))
    
    print(Fore.GREEN + ">> add *" + Fore.RESET, end="")
    input()
    add("*", files, added_files)
    
    print(Fore.GREEN + ">> show" + Fore.RESET, end="")
    input()
    show_added_files(added_files)
    
    print(Fore.GREEN + ">> save to b" + Fore.RESET, end="")
    input()
    save("b", added_files, dict)
    
    print(Fore.GREEN + ">> remove *" + Fore.RESET, end="")
    input()
    r = remove(["remove", "*"], added_files)
    print(f"Removed {r} files")
    
    print(Fore.GREEN + ">> a U b" + Fore.RESET, end="")
    input()
    files = set_operations("a U b", dict)
    
    print(Fore.GREEN + ">> add *" + Fore.RESET, end="")
    input()
    add("*", files, added_files)
    
    print(Fore.GREEN + ">> output" + Fore.RESET, end="")
    input()
    output(added_files)
    
def scenario_2():
    global_variables.path = "C:\\Users\\Filip\\Documents\\bakalarska_prace\\files"
    
    files = []
    added_files = []
    added_folders = []
    dict = {}
    
    read_json("settings.json")
    added_folders.extend(read_added_folders())
    
    print(Fore.YELLOW + "Settings:" + Fore.RESET)
    print(f"Default unit: {global_variables.default_unit}")
    print(f"Search folders: {global_variables.search_folders}")
    print(f"Show duplicity: {global_variables.show_duplicity}")

    print(Fore.YELLOW + "Files:" + Fore.RESET)
    for file in os.listdir(global_variables.path):
        print(file)
        
    if added_folders != []:
        for x in added_folders:
            files.extend(add_folder(x))
        print("Added folders:")
        for folder in added_folders:
            print(folder)
        print("Files from folders:")
        for x in files:
            print(x)
            
    print(Fore.GREEN + ">> filter modified < 10 w" + Fore.RESET, end="")
    input()
    files = filter(str("filter modified < 10 w").split(" "))
    add_history("filter modified < 10 w", files)
    
    print(Fore.GREEN + ">> sort by modified" + Fore.RESET, end="")
    input()
    files = sort(str("sort by modified").split(" "), files)
    add_history("sort by size", files)
    
    print(Fore.GREEN + ">> history" + Fore.RESET, end="")
    input()
    print_history()
    
    print(Fore.GREEN + ">> filter *" + Fore.RESET, end="")
    input()
    files = filter(str("filter *").split(" "))
    add_history("filter *", files)
    
    print(Fore.GREEN + ">> filter name *.py" + Fore.RESET, end="")
    input()
    files = filter(str("filter name *.py").split(" "))
    add_history("filter name *.py", files)
    
    print(Fore.GREEN + ">> history" + Fore.RESET, end="")
    input()
    print_history()
    
    print(Fore.GREEN + ">> history 1" + Fore.RESET, end="")
    input()
    try:
        files = load_history(1)
        show_files(files)
    except:
        print("Wrong input")
        
    print(Fore.GREEN + ">> select top 5" + Fore.RESET, end="")
    input()
    files = select(str("select top 5").split(" "), files)
    add_history("select top 5", files)
    
    print(Fore.GREEN + ">> add *" + Fore.RESET, end="")
    input()
    add("*", files, added_files)
    
    print(Fore.GREEN + ">> output" + Fore.RESET, end="")
    input()
    output(added_files)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Process some integers.")
    parser.add_argument('-p', type=str, default="", help='Path to the folder')
    parser.add_argument('-c', type=str, default="", help='Command to run')
    
    args = parser.parse_args()
    
    start_time = time.time()
    init()
    # cProfile.run("main(args)", sort="tottime")
    # scenario_1()
    scenario_2()
    print(f"Program took {time.time() - start_time:.4f} seconds to run")
    
    # main()