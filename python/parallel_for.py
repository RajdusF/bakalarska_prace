import inspect
import multiprocessing
from functools import partial
from itertools import count
from typing import Any, Callable, List, Optional

import numpy as np
from colorama import Fore

import python.global_variables as global_variables


def worker_order(args):
    func, items_chunk, index, extra_args, path = args
    try:
        if not extra_args:
            result = func(items_chunk)
        else:
            result = func(items_chunk, *extra_args)
        return index, result
    except Exception as e:
        print(Fore.RED + f"Error processing chunk: {e}")
        return index, []
        
def pfor_order(func, items, *args, path=None, num_threads=None):
    if not items:
        print("Item list is empty.")
        return []
    
    num_threads = num_threads or multiprocessing.cpu_count()
    num_threads = min(num_threads, len(items))
    
    chunk_size = (len(items) + num_threads - 1) // num_threads
    chunks = [items[i * chunk_size : (i + 1) * chunk_size] for i in range(num_threads)]
    
    task_args = [(func, chunk, i, args, path) for i, chunk in enumerate(chunks)]
    
    with multiprocessing.Pool(processes=num_threads) as pool:
        results = pool.map(worker_order, task_args)

    results.sort(key=lambda x: x[0])  
    result_data = [result for _, result in results]

    final_result = [item for sublist in result_data for item in sublist]
    
    return final_result

import multiprocessing
from functools import partial


def worker_wrapper(func, args_tuple, shared_data, chunk_with_id):
    """Wrapper that unpacks chunk and its assigned ID"""
    chunk_id, chunk = chunk_with_id
    try:
        return func(chunk, *args_tuple, shared_data=shared_data, worker_id=chunk_id)
    except Exception as e:
        print(f"Worker {chunk_id} error: {e}")
        return []

def pfor(func, items, *args, num_threads=None):
    """Parallel processing with imap_unordered and simple worker IDs"""
    if not items:
        return []
    
    items = [items] if isinstance(items, str) else list(items)
    num_threads = num_threads or multiprocessing.cpu_count()
    num_threads = min(num_threads, len(items))
    
    # Rozdělení na chunky s přiřazenými ID (0, 1, 2,...)
    chunk_size = (len(items) + num_threads - 1) // num_threads
    chunks_with_ids = [
        (i, items[i*chunk_size:(i+1)*chunk_size]) 
        for i in range(num_threads)
    ]
    
    shared_data = {
        'path': getattr(global_variables, 'path', ''),
        'variables': getattr(global_variables, 'variables', {})
    }

    with multiprocessing.Pool(num_threads) as pool:
        try:
            # Vytvoříme partial funkci s potřebnými argumenty
            worker_partial = partial(
                worker_wrapper,
                func,
                args,
                shared_data
            )
            
            # Použijeme skutečně imap_unordered
            results = []
            for result in pool.imap_unordered(worker_partial, chunks_with_ids):
                if result:
                    results.extend(result if isinstance(result, list) else [result])
            return results
            
        finally:
            pool.close()
            pool.join()
            
            
def has_argument(func, arg_name):
    signature = inspect.signature(func)
    for param in signature.parameters.values():
        if param.name == arg_name:
            return True
    return False