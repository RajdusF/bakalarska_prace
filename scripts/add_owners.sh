#!/bin/bash

if [ -z "$1" ]; then
  echo "Usage: $0 <absolute_path_to_file>"
  exit 1
fi

FILE="$1"

if [ ! -f "$FILE" ]; then
  echo "Error: File $FILE does not exist!"
  exit 1
fi

# Create a temporary file
TEMP_FILE=$(mktemp)

# Add text to the beginning and append the original file content
{
  echo "John Smith"
  echo "Mary Johnson"
  echo "Peter Brown"
  cat "$FILE"
} > "$TEMP_FILE"

# Move the temporary file back to the original file location
mv "$TEMP_FILE" "$FILE"

echo "Done! The updated file is: $FILE"