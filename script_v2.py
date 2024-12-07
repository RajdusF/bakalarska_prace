import subprocess


# Funkce pro převod Windows cesty na WSL cestu
def convert_to_wsl_path(windows_path):
    # Změní zpětné lomítko na normální lomítka
    wsl_path = windows_path.replace("\\", "/")
    # Převod "C:" na "/mnt/c"
    if wsl_path[1:3] == ":/":
        wsl_path = "/mnt/" + wsl_path[0].lower() + wsl_path[2:]
    return wsl_path
    
files = []
script_path = "./add_owner.sh"

f = open("C:\\Users\\Filip\\Documents\\bakalarska_prace\\output.txt", "r")
for line in f:
    s = line.strip()
    files.append(s)
    
print(files)
f.close()

files = [convert_to_wsl_path(file) for file in files]

for file in files:
    try:
        result = subprocess.run(
            ["bash", script_path, file],
            capture_output=True,
            text=True,
            check=True
        )
        # Výstup skriptu
        print("Skript úspěšně spuštěn!")
        print("Výstup skriptu:")
        print(result.stdout)
    except subprocess.CalledProcessError as e:
        print("Chyba při spouštění skriptu:")
        print(e.stderr)
        
    