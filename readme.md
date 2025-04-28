# Nástroj pro zpracování dat optického mapování DNA

## O čem práce je?

Tato práce se zabývá **vývojem softwarového nástroje** pro efektivní zpracování dat z optického mapování DNA (formáty BNX/CMAP/XMAP). Hlavní cíle:

-   Automatizace vyhledávání a filtrace molekulárních dat
-   Detekce duplicitních souborů
-   Optimalizace výpočetních úloh pomocí paralelního zpracování

## Technologie

-   **Programovací jazyk:** Python 3.x
-   **Klíčové knihovny:** os, re, glob, multiprocessing, json
-   **Formáty souborů:** BNX, CMAP, XMAP (Bionano Genomics)

## Jak spustit

1. Nainstalujte závislosti:
   
    pip install -r requirements.txt

    python3 configurator.py

2. Spuštění prvních příkazů:
   
    cd C:\Users\Administrator\Documents\...

    filter \*
