import os

print(f"Current working directory: {os.getcwd()}")

filename = 'output.txt'

with open(filename, 'w+') as file:
    file.write("This is an example of writing text to a file.\n")
    file.write("Python makes it easy to handle files!\n")

print(f"Text has been written to {filename}")
