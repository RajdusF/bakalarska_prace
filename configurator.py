import argparse
import multiprocessing
import os
import sys
import threading
import time

from colorama import Fore, init
from prompt_toolkit import prompt
from prompt_toolkit.patch_stdout import patch_stdout

import python.email as email
import python.global_variables as global_variables
from python.decider import process_command
from python.help_func import (comments_removal, debug_write,
                              read_commands_from_file, read_json)

finished_commands_with_time = []

def send_report():
    email.report_str = f"Processed commands: \n"
    for x in finished_commands_with_time:
        email.report_str += f"\t{x}\n"
    email.report_str += f"\nTime taken: {time.time() - start_time:.2f} seconds"
    email.report_str += f"\nTime of completion: {time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())}"
    
    # print(f"Test - report_str: \n{email.report_str}")
                
    email.send_report()

def main(args):
    files = []
    added_files = []
    variables = {}  
    
    report_sent = False
    
    lock = threading.Lock()
    
    init(autoreset=True)
    
    print(Fore.YELLOW + "Type '?' for help" + Fore.RESET)
            
    readed_commands = read_commands_from_file()
    typed_commands = []
    commands_to_process = readed_commands.copy()
    current_command = ""
    finished_commands = []
    
    def status_check():
        
        global start_time
        
        while True:
            if len(commands_to_process) == 0:
                print(Fore.LIGHTBLUE_EX + f"{global_variables.path}" + Fore.GREEN + f" >> " + Fore.RESET, end="")
            else:
                # Vymazani posledniho radku
                sys.stdout.write("\033[F")
                sys.stdout.write("\033[K")


            start_pause = time.time()
            
            # print(Fore.LIGHTBLUE_EX + f"{global_variables.path}" + Fore.GREEN + f" >> " + Fore.RESET, end="")
            cmd = input()
            
            pause_duration = time.time() - start_pause
            
            
            start_time += pause_duration
            
            if cmd == "status":
                with lock:
                    print(f"Processed commands: {len(finished_commands)} / {len(readed_commands) + len(typed_commands)}", flush=True)
                    print(f"Past commands: ", flush=True)
                    for x in finished_commands:
                        print("\t" + x)
                    if current_command != "":
                        print(f"Current command: \n\t{current_command}")
                        if global_variables.status != "":
                            print(f"\tStatus: {global_variables.status}")
                    print(f"Upcoming commands: ", flush=True)
                    for x in commands_to_process:
                        print("\t" + x)
            elif cmd == "exit":
                break
            else:
                commands_to_process.append(cmd)
                typed_commands.append(cmd)
            
    threading.Thread(target=status_check, daemon=True).start()
    while True:
        if len(commands_to_process) > 0:
            command = commands_to_process.pop(0)
            with lock:
                current_command = command
            
            command = comments_removal(command)
            
            print(Fore.LIGHTBLUE_EX + f"{global_variables.path}" + Fore.GREEN + f" >> " + Fore.RESET + command)
            
            command_start_time = time.time()
            
            result = process_command(command, variables, files, added_files)
            if result == -1:
                return -1
            elif result == "report":
                send_report()
            

            debug_write(f'Command "{command}" took {time.time() - command_start_time:.4f} seconds to run')
            
            with lock:
                finished_commands.append(command)
                finished_commands_with_time.append(f"{command} - {time.time() - command_start_time:.2f} seconds")
                current_command = ""
                
            if len(commands_to_process) == 0:
                print(Fore.LIGHTBLUE_EX + f"{global_variables.path}" + Fore.GREEN + f" >> " + Fore.RESET, end="")
                
        else:
            if len(readed_commands) > 0 and report_sent == False:
                send_report()
                report_sent = True
                print(Fore.LIGHTBLUE_EX + f"{global_variables.path}" + Fore.GREEN + f" >> " + Fore.RESET, end="")
                
            time.sleep(0.2)
        

if __name__ == "__main__":
    if os.name == 'nt':
        os.system('cls')
    elif os.name == 'posix':
        os.system('clear')
        
    # print(f"sys.path: {sys.path}")
    # sys.path.append(os.path.dirname(os.path.abspath(__file__)))
    # print(f"AFTER: sys.path: {sys.path}")
    
    print(f"Cores: {multiprocessing.cpu_count()}")
    
    
    init(autoreset=True)
    multiprocessing.freeze_support()
    parser = argparse.ArgumentParser(description="Process some integers.")
    parser.add_argument('-p', type=str, default="", help='Path to the folder')
    
    if os.path.isfile("debug.txt"):
        os.remove("debug.txt")
        
    if os.path.isfile("output/output.txt"):
        os.remove("output/output.txt")
    
    args = parser.parse_args()
    
    start_time = time.time()  
    read_json("settings.json")
    
    if args.p != "":
        print(f"args.p: {args.p}")
        if os.path.exists(args.p):
            global_variables.path = args.p
        else:
            print(Fore.RED + "Path not found" + Fore.RESET)
        
        
    print(Fore.YELLOW + "Settings:" + Fore.RESET)
    print(f"Default unit: {global_variables.default_unit}")
    print(f"Search folders: {global_variables.search_folders}")
    print(f"Show duplicity: {global_variables.show_duplicity}")

    
    # cProfile.run("main(args)", sort="tottime")
    main(args)
    
    print(f"Program took {time.time() - start_time:.4f} seconds to run")
