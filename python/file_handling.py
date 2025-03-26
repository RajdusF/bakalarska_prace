import csv
import json
import os
import re

from colorama import Fore

import python.global_variables as g
from python.MyFile import Molecule, MyFile, XData


def load(name, path=None):
    if path is not None:
        g.path = path
    # print(f"g.path: {g.path}")
    name = name.replace("\\", "\\\\")  # Escape backslashes
    escaped_path = re.escape(g.path)  # Escape regex special chars in the path
    name = re.sub(
        r'\bpath\b(?=(?:[^"]*"[^"]*")*[^"]*$)',
        f'"{escaped_path}"',
        name
    )
    
    if "+" in name and all(part.strip(' "\'') for part in name.split("+")):
        parts = [part.strip(' "\'') for part in name.split("+")]
        name = os.path.join(parts[0], parts[1].lstrip("\\"))

    if isinstance(name, list):
        files = []
        for file in name:
            files.append(load(file))
                
        return files
    
    
    return load_json(name)

    if name.endswith(".bnx"):
        return load_bnx(name)
    elif name.endswith(".cmap"):
        return load_cmap(name)
    elif name.endswith(".xmap"):
        return load_xmap(name)
        
        
def load_json(name):
    data = []
    comments = []
    headers = {}
    data_types = {}
    warning_count = 0

    if not os.path.isfile(name):
        print(Fore.RED + "File not found")
        return -1

    # try:
    with open(name, 'r') as f:
        fields = None  # Proměnná pro uchování hlaviček

        for i, line in enumerate(f):
            line = line.strip()
            
            g.status = f"load: Currently processing line: {i}"

            # Zpracování hlaviček
            if line.startswith('#h'):
                headers["h"] = [column.strip() for column in line[2:].split("\t")]
            elif line.startswith('#f'):
                data_types["f"] = [dtype.strip() for dtype in line[2:].split("\t")]
            elif line[0] == "#" and line[1].isdigit() and line[2] == "h":
                headers[line[1] + "h"] = [column.strip() for column in line[3:].split("\t")]
            elif line[0] == "#" and line[1].isdigit() and line[2] == "f":
                data_types[line[1] + "f"] = [dtype.strip() for dtype in line[3:].split("\t")]
            elif line.startswith('#Qh'):
                headers["Qh"] = [column.strip() for column in line[3:].split("\t")]
            elif line.startswith('#Qf'):
                data_types["Qf"] = [dtype.strip() for dtype in line[3:].split("\t")]
            elif line.startswith('#'):  # Komentáře
                comments.append(line)
            else:
                # Zpracování datových řádků podle toho, zda začínají '0' nebo '1'
                if line[0].isdigit():
                    try:
                        label_channel = line[0]
                        fields = headers.get(label_channel + "h")
                        fields_data_types = data_types.get(label_channel + "f")
                        if fields is None:
                            fields = headers.get("h")
                            fields_data_types = data_types.get("f")
                    except:
                        print(Fore.RED + f"Warning: No headers found for row: {line}")
                        continue

                # Pokud máme hlavičky, čteme data
                if fields:
                    values = line.split("\t")

                    data_row = {}
                    for i in range(len(fields)):
                        field_name = fields[i]
                        value = values[i]
                        try:
                            if fields_data_types[i] == "float" or fields_data_types[i] == "float[N]":
                                value = float(value)
                            elif fields_data_types[i] == "int" or fields_data_types[i] == "int[N]":
                                value = int(value)
                            elif fields_data_types[i] == "bool" or fields_data_types[i] == "bool[N]":
                                value = bool(value)
                            elif fields_data_types[i] == "string" or fields_data_types[i] == "string[N]":
                                value = str(value)
                        except:
                            if not value.startswith("QX"):
                                print(Fore.YELLOW + f"Warning: Could not convert value '{value}' to type '{fields_data_types[i]}'")

                        # Pokud má pole '[N]' v názvu, rozdělíme hodnotu
                        if '[' in field_name and ']' in field_name:
                            try:
                                if fields_data_types[i] == "float" or fields_data_types[i] == "float[N]":
                                    data_row[field_name] = [float(v) for v in values[i:]]
                                elif fields_data_types[i] == "int" or fields_data_types[i] == "int[N]":
                                    data_row[field_name] = [int(v) for v in values[i:]]
                                elif fields_data_types[i] == "bool" or fields_data_types[i] == "bool[N]":
                                    data_row[field_name] = [bool(v) for v in values[i:]]
                                elif fields_data_types[i] == "string" or fields_data_types[i] == "string[N]":
                                    data_row[field_name] = [str(v) for v in values[i:]]
                            except:
                                print(Fore.YELLOW + f"Warning: Could not convert values '{values[i:]}' to type '{fields_data_types[i]}'")
                        else:
                            data_row[field_name] = value
                    data.append(data_row)
                else:
                    print(Fore.RED + f"Warning: No headers found for row: {line}")
                    warning_count += 1
                    continue

    # except Exception as e:
    #     print(Fore.RED + f"An error occurred in load_json(): {e}")
    #     return -1

    output_data = {
        "comments": comments,
        "headers": headers,
        "data_types": data_types,
        "data": data
    }
    
    if warning_count > 0:
        print(Fore.YELLOW + f"Warning: {warning_count} rows were not processed correctly")

    x = XData(output_data)
        
    g.status = ""
    
    return x


def load_bnx(name):
    if os.path.isfile(name):
        with open(name, 'r') as f:
            my_f = MyFile()
            
            my_f.name = name
            my_f.size = os.path.getsize(name)
            my_f.content = f.read()
            lines = my_f.content.split("\n")
            
            for line in lines:
                if line == "":
                    continue
                
                if line[0] == "#" and "h" in line:
                    first_word = line.split()[0]
                    header_id = first_word[1:first_word.find("h")]
                    
                    if header_id.isdecimal() or header_id == "Q":                        
                        header = line.split()[1:]
                        header.insert(0, header_id)
                        
                        my_f.header.append(header)
                    
                if not line.startswith("#"):
                    molecule = Molecule()
                    
                    data = line.strip().split("\t")
                        
                    headers = my_f.header  
                    for i, header in enumerate(headers):
                        if isinstance(header, list) and len(header) - 1 == len(data) and data[0] == header[0]:
                            for h, d in zip(header[1:], data):
                                setattr(molecule, h, d)
                            break
                        elif data[0] == header[0]:
                            for i, h in enumerate(header[1:]):
                                if "[N]" in h:
                                    molecule.__setattr__(h, data[i:])
                                else:
                                    molecule.__setattr__(h, data[i])
                            break
                        elif data[0][0] == header[0]:
                            for i, h in enumerate(header[1:]):
                                if "[N]" in h:
                                    molecule.__setattr__(h, data[i:])
                                else:
                                    molecule.__setattr__(h, data[i])

                    
                    if molecule._specs:
                        my_f.add_molecule(molecule)
            
            
            return my_f
    else:
        print(Fore.RED + "load error")
        
def load_cmap(name):
    if os.path.isfile(name):
        with open(name, 'r') as f:
            my_f = MyFile()
            
            my_f.name = name
            my_f.size = os.path.getsize(name)
            my_f.content = f.read()
            lines = my_f.content.split("\n")
            
            for line in lines:
                if line == "":
                    continue
                if line.startswith("#h"):
                    my_f.header = line.removeprefix("#h").strip().split("\t")
                    
                if not line.startswith("#"):
                    molecule = Molecule()
                    
                    data = line.strip().split("\t")
                        
                    headers = my_f.header  
                    for i, header in enumerate(headers):
                        if isinstance(header, list):
                            if len(header) == len(data):
                                for j, h in enumerate(header):
                                    molecule.__setattr__(h, data[j])
                        else:
                            molecule.__setattr__(header, data[i])
                    
                    my_f.molecules.append(molecule)
            
            
            return my_f
    else:
        print(Fore.RED + "load error")
        
def load_xmap(name):
    if os.path.isfile(name):
        with open(name, 'r') as f:
            my_f = MyFile()
            
            my_f.name = name
            my_f.size = os.path.getsize(name)
            my_f.content = f.read()
            lines = my_f.content.split("\n")
            
            for line in lines:
                if line == "":
                    continue
                if line.startswith("#h"):
                    my_f.header = line.removeprefix("#h").strip().split("\t")
                    
                if not line.startswith("#"):
                    molecule = Molecule()
                    
                    data = line.strip().split("\t")
                        
                    headers = my_f.header  
                    for i, header in enumerate(headers):
                        if isinstance(header, list):
                            if len(header) == len(data):
                                for j, h in enumerate(header):
                                    molecule.__setattr__(h, data[j])
                        else:
                            molecule.__setattr__(header, data[i])
                    
                    my_f.molecules.append(molecule)
            
            
            return my_f
    else:
        print(Fore.RED + "load error")