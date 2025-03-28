import multiprocessing
from typing import Any, Callable, List, Optional

import numpy as np

import python.global_variables as global_variables


def worker(func: Callable, items: List[Any], start: int, end: int, 
           result_data: List[Any], output_files: Optional[List[str]] = None, 
           path: Optional[str] = None) -> None:
    
    for i in range(start, min(end, len(items))):
        try:
            if func.__name__ == 'load':
                result_data[i] = func(items[i], path=path)
            elif func.__name__ == 'save' and output_files is not None:
                result_data[i] = func(items[i], output_files[i])
            else:
                result_data[i] = func(items[i])
        except Exception as e:
            print(f"Error processing item {i}: {e}")
            result_data[i] = None
    print(f"Process {multiprocessing.current_process().name} completed items {start}-{end-1}")

def pfor(func: Callable, items: List[Any], path: Optional[str] = None, 
         num_threads: Optional[int] = None, 
         output_files: Optional[List[str]] = None) -> List[Any]:
    if not items:
        print("Item list is empty.")
        return []
    
    num_threads = num_threads or multiprocessing.cpu_count()
    num_threads = min(num_threads, len(items))  # Don't create more threads than items
    
    with multiprocessing.Manager() as manager:
        result_data = manager.list([None] * len(items))
        
        # Calculate chunk sizes without numpy dependency
        chunk_size = (len(items) + num_threads - 1) // num_threads
        chunks = [(i * chunk_size, (i + 1) * chunk_size) 
                 for i in range(num_threads)]
        
        processes = []
        for start, end in chunks:
            p = multiprocessing.Process(
                target=worker,
                args=(func, items, start, end, result_data, output_files, path)
            )
            processes.append(p)
            p.start()
        
        for p in processes:
            p.join()
        
        return list(result_data)