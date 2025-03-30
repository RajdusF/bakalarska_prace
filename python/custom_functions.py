import random
from time import sleep


def count_to(num, display=True):
    """Counts to a given number."""
    
    print(f"Counting to {num}...")
    
    for i in range(1, num + 1):
        if display:
            print(i)

    print("Done counting!")
    
    
def find_44(l : list):
    for x in l:
        if x == 440_00000:
            print("Found 44!")
            
    print("Done searching!")
    return None

def return_list(l : list):
    sleep(random.uniform(0, 1))
    print("Returning list...")
    return l