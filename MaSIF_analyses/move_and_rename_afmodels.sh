#!/bin/bash

if [ "$#" -ne 2 ]; then
  echo "Usage: $0 input_file output_directory"
  exit 1
fi

input_file="$1"
output_directory="$2"

if [ ! -d "$output_directory" ]; then
  mkdir -p "$output_directory"
fi

while IFS= read -r file_path; do
  if [ -f "$file_path" ]; then
    # Extract the filename without path
    file_name=$(basename "$file_path")
    
    # Remove underscores from the filename
    new_file_name="${file_name//_/-}"

    # Copy the file to the output directory with the new filename
    cp "$file_path" "$output_directory/$new_file_name"
    
    echo "Copied '$file_path' to '$output_directory/$new_file_name'"
  else
    echo "File '$file_path' not found. Skipping..."
  fi
done < "$input_file"

echo "Done."

