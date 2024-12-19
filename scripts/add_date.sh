#!/bin/bash

if [ -z "$1" ]; then
  echo "Usage: $0 <absolute_path_to_file> [creation_date]"
  exit 1
fi

FILE="$1"
CREATION_DATE="${2:-$(date +"%d-%m-%Y")}"  # Use provided date or today's date if not given

if [ ! -f "$FILE" ]; then
  echo "Error: File $FILE does not exist!"
  exit 1
fi

# Create a temporary file
TEMP_FILE=$(mktemp)

# Add the creation date at the beginning and append the original file content
{
  echo "Creation Date: $CREATION_DATE"
  cat "$FILE"
} > "$TEMP_FILE"

# Replace the original file with the updated content
mv "$TEMP_FILE" "$FILE"

echo "Done! The updated file is: $FILE"
