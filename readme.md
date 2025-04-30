# Nástroj pro zpracování dat optického mapování DNA

## O čem práce je?

Tato práce se zabývá **vývojem softwarového nástroje** pro efektivní zpracování dat z optického mapování DNA (formáty BNX/CMAP/XMAP). Hlavní cíle:

- Automatizace vyhledávání a filtrace molekulárních dat
- Detekce duplicitních souborů
- Optimalizace výpočetních úloh pomocí paralelního zpracování

## Technologie

- **Klíčové knihovny:** os, re, glob, multiprocessing, json
- **Formáty souborů:** BNX, CMAP, XMAP (Bionano Genomics)

## Požadavky

- **Python**: 3.12.3
- **pip** (správce balíčků)

## Jak spustit

1. Nainstalujte závislosti:

   `pip install -r requirements.txt`

   Pokud pip selže (například kvůli zablokovaným portům), je potřeba nainstalovat tyto knihovny:

   - colorama-0.4.6-py2.py3-none-any
   - numpy-2.2.4-cp312-cp312-manylinux_2_17_x86_64.manylinux2014_x86_64
   - path-17.1.0-py3-none-any
   - prompt_toolkit-3.0.50-py3-none-any
   - tabulate-0.9.0-py3-none-any
   - tqdm-4.67.1-py3-none-any
   - wcwidth-0.2.13-py2.py3-none-any

2. Spuštění programu:

   program lze spustit pomocí:

   `python3 configurator.py`

   - v tomto případě čte jak vstup za běhu programu, tak načítá a spouští příkazy napsané v configurator_commands.txt

   Lze dodat argument pro čtení jiných příkazů z jiného souboru, například:
   `python3 configurator.py scenarios/scenario_1`

3. Spuštění prvních příkazů:

   `cd C:\Users\Administrator\Documents\...`

   `filter \*`
