import threading


def pfor(func, items, num_threads=None):
    """
    Funkce pro paralelní zpracování položek v seznamu pomocí vláken.
    
    :param func: Funkce, která bude aplikována na každý prvek
    :param items: Seznam položek, které budou zpracovány
    :param num_threads: Počet vláken, které budou použity. Pokud není zadáno, použije se maximální počet dostupných jader.
    """
    
    # Funkce, která bude zpracovávat část seznamu
    def worker(start, end):
        for i in range(start, end):
            func(items[i])

    # Pokud není počet vláken určen, použije se počet položek
    if num_threads is None:
        num_threads = len(items)

    # Vytvoření seznamu vláken
    threads = []
    chunk_size = len(items) // num_threads  # Velikost jednoho chunku (části seznamu)

    # Vytváření a spouštění vláken
    for i in range(num_threads):
        start = i * chunk_size  # Začátek úseku
        # Pokud je poslední vlákno, vezme zbývající položky
        end = start + chunk_size if i < num_threads - 1 else len(items)
        
        # Vytvoření vlákna, které spustí worker funkci pro daný úsek
        thread = threading.Thread(target=worker, args=(start, end))
        threads.append(thread)
        thread.start()

    # Čekání na dokončení všech vláken
    for thread in threads:
        thread.join()

"""
    # Příklad funkce pro zpracování položek
    def process_item(item):
        print(f"Zpracovávám položku {item}")

    # Seznam položek
    items = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]

    # Spuštění paralelního for
    parallel_for(process_item, items, num_threads=3)
"""