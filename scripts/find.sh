#!/bin/bash

if [ -z "$1" ] || [ -z "$2" ]; then
  echo "Použití: $0 <cesta_k_souboru> <hledané_slovo>"
  exit 1
fi

FILE="$1"
WORD="$2"

if [ ! -f "$FILE" ]; then
  echo "Chyba: Soubor $FILE neexistuje!"
  exit 1
fi

echo "Hledám '$WORD' v souboru $FILE..."
grep -in "$WORD" "$FILE"

if [ $? -eq 0 ]; then
  echo "Slovo '$WORD' bylo nalezeno v souboru $FILE."
else
  echo "Slovo '$WORD' nebylo v souboru $FILE nalezeno."
fi
