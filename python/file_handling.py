import csv
import json
import os
import re

from colorama import Fore

import python.global_variables as g
from python.MyFile import XData


def load(name_input, shared_data=None, worker_id=None):
    if isinstance(name_input, str):
        name_input = [name_input]
        
    files = []
    
    for name in name_input:
        name = os.path.normpath(name)

        if not os.path.isabs(name):
            print(f"Warning: {name} is not an absolute path")
            return None

        files.append(name)
        
    if not files:
        print("Error: No valid files found")
        return None

    if len(files) > 1:
        return [load(file, shared_data, worker_id) for file in files]

    name = files[0]
    if name.endswith(".json"):
        with open(name, "r") as file:
            return json.load(file)

    return load_json(name)
        
    
        
    # for name in name_input:
    #     if path is None:
    #         print(Fore.RED + "Path is not set" + Fore.RESET)
    #         return None
        
    #     # Úprava escape characterů pro Windows
    #     name = name.replace("\\", "\\\\")
    #     escaped_path = re.escape(path)
    #     name = re.sub(
    #         r'\bpath\b(?=(?:[^"]*"[^"]*")*[^"]*$)',
    #         f'"{escaped_path}"',
    #         name
    #     )
        
    #     if "+" in name and all(part.strip(' "\'') for part in name.split("+")):
    #         parts = [part.strip(' "\'') for part in name.split("+")]
    #         name = os.path.join(parts[0], parts[1].lstrip("\\"))
            
    #     files.append(name)

        
        
def load_json(name):
    data = []
    comments = []
    headers = {}
    data_types = {}
    warning_count = 0

    if not os.path.isfile(name):
        print(Fore.RED + "File not found")
        return -1

    try:
        with open(name, 'r') as f:
            fields = None

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

    except Exception as e:
        print(Fore.RED + f"An error occurred in load_json(): {e}")
        return None

    output_data = {
        "comments": comments,
        "headers": headers,
        "data_types": data_types,
        "data": data
    }
    
    if warning_count > 0:
        print(Fore.YELLOW + f"Warning: {warning_count} rows were not processed correctly")

    x = XData(output_data)
    x.name = os.path.basename(name)
    print(f"name saved: {x.name}")
        
    g.status = ""
    
    return x