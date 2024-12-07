from time import sleep

from tabulate import tabulate

data = []

f = open("C:\\Users\\Filip\\Documents\\bakalarka_out_of_github\\Bionano - Testovaci data\\Testovaci data\\all.bnx", "r")
for i, line in enumerate(f):
    if line.startswith("#0h") or not line.startswith("#"):
        s = line.split("\t")
        data.append(s)
    if i > 300:
        break
        
f.close()
print("Reading finished")

# print(data)

print(tabulate(data, headers="firstrow"))

print("Program finished")