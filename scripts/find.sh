#!/bin/bash

if [ -z "$1" ] || [ -z "$2" ]; then
  echo "Usage: $0 <file_path> <search_word>"
  exit 1
fi

FILE="$1"
WORD="$2"

if [ ! -f "$FILE" ]; then
  echo "Error: File $FILE does not exist!"
  exit 1
fi

echo "Searching for '$WORD' in file $FILE..."
grep -in "$WORD" "$FILE"

if [ $? -eq 0 ]; then
  echo "Word '$WORD' was found in file $FILE."
else
  echo "Word '$WORD' was not found in file $FILE."
fi