#!/bin/bash

# Kontrola vstupního argumentu
if [ -z "$1" ]; then
  echo "Použití: $0 <absolutní_cesta_k_souboru>"
  exit 1
fi

FILE="$1"

# Kontrola, zda soubor existuje
if [ ! -f "$FILE" ]; then
  echo "Chyba: Soubor $FILE neexistuje!"
  exit 1
fi

# Cílová složka
OUTPUT_DIR="./output"

# Vytvoření složky, pokud neexistuje
mkdir -p "$OUTPUT_DIR"

# Název výsledného souboru (stejné jméno jako původní)
OUTPUT_FILE="$OUTPUT_DIR/$(basename "$FILE")"

# Přidání nových řádků na začátek a uložení do složky output
{
  echo "Jan Novák"
  echo "Marie Svobodová"
  echo "Petr Dvořák"
  cat "$FILE"
} > "$OUTPUT_FILE"

echo "Hotovo! Upravený soubor je uložen v: $OUTPUT_FILE"