#!/bin/bash

# Get the filename from user input
echo "Enter the filename:"
read filename

# Temporary file
temp_file=$(mktemp)

while IFS= read -r line
do
  if [[ $line == Section* ]]; then
    echo "# $line" >> "$temp_file"
  else
    echo "## $line" >> "$temp_file"
  fi
done < "$filename"

# Overwrite the original file with the modified content
mv "$temp_file" "$filename"
