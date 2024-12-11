import os
import subprocess

from colorama import Fore
from tqdm import tqdm


def convert_to_wsl_path(windows_path):
    wsl_path = windows_path.replace("\\", "/")
    if wsl_path[1:3] == ":/":
        wsl_path = "/mnt/" + wsl_path[0].lower() + wsl_path[2:]
    return wsl_path

def read_scripts_to_run():
    readed_scripts = []
    f = open("C:\\Users\\Filip\\Documents\\bakalarska_prace\\scripts_to_run.txt", "r")
    for line in f:
        s = line.strip()
        readed_scripts.append(s)
        
    f.close()      
    
    return readed_scripts

def load_scripts_from_script_folder(readed_scripts):
    scripts = []
    script_folder = "C:\\Users\\Filip\\Documents\\bakalarska_prace\\scripts"
    
    if readed_scripts == []:
        for file in os.listdir(script_folder):
            if file.endswith(".sh"):
                scripts.append(file)
        return scripts
    else:
        for readed_script in readed_scripts:
            if not os.path.exists(script_folder + "\\" + readed_script.split(" ")[0]):
                continue
            scripts.append(readed_script)
            
    return scripts

files = []
readed_scripts = read_scripts_to_run()
scripts = load_scripts_from_script_folder(readed_scripts)

f = open("C:\\Users\\Filip\\Documents\\bakalarska_prace\\output.txt", "r")
for line in f:
    s = line.strip()
    files.append(s)
    
f.close()

print("Loaded files:")
for file in files:
    print(f"\t{file.split('\\')[-1]}")
print("Loaded scripts to run in order:")
for script in scripts:
        print(f"\t{script}")
    
print("Press any key to continue...")
input()

files = [convert_to_wsl_path(file) for file in files]

total_iterations = len(scripts) * len(files)

with tqdm(total=total_iterations, desc="Total Progress") as pbar:
    for file in files:
        for script in scripts:
            try:
                words = script.split(" ")
                command = ["bash", "./scripts/" + words[0], file]
                while len(words) > 1:
                    command.append(words.pop(1))
                result = subprocess.run(
                    command,
                    capture_output=True,
                    text=True,
                    check=True
                )
                tqdm.write(Fore.LIGHTGREEN_EX + f"Skript '{script}' úspěšně spuštěn!" + Fore.RESET)
                tqdm.write("Výstup skriptu:")
                tqdm.write(result.stdout)
            except subprocess.CalledProcessError as e:
                tqdm.write(Fore.LIGHTRED_EX + f"Chyba při spouštění skriptu '{script}':" + Fore.RESET)
                tqdm.write(e.stderr)
            finally:
                pbar.update(1)