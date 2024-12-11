#!/bin/bash

if [ -z "$1" ] || [ -z "$2" ]; then
  echo "Použití: $0 <absolutní_cesta_k_souboru> <datum_vytvoření>"
  exit 1
fi

FILE="$1"
CREATION_DATE="$2"

if [ ! -f "$FILE" ]; then
  echo "Chyba: Soubor $FILE neexistuje!"
  exit 1
fi

OUTPUT_DIR="./output"

mkdir -p "$OUTPUT_DIR"

OUTPUT_FILE="$OUTPUT_DIR/$(basename "$FILE")"

{
  echo "Datum vytvoření: $CREATION_DATE"
  cat "$FILE"
} > "$OUTPUT_FILE"

echo "Hotovo! Upravený soubor je uložen v: $OUTPUT_FILE"