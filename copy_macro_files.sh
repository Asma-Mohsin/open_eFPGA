#!/bin/bash

# Define project root and target directories
GDS_DIR="openlane/user_project_wrapper/macro/gds"
LIB_DIR="openlane/user_project_wrapper/macro/lib"
LEF_DIR="openlane/user_project_wrapper/macro/lef"

# List of directories to copy from (easily extensible)
SOURCE_DIRS=(
    "S_term_single"
    "S_term_single2"
    "S_term_RAM_IO"
    "S_term_DSP"
    "N_term_single"
    "N_term_single2"
    "N_term_RAM_IO"
    "N_term_DSP"
    "DSP"
    "RAM_IO"
    "RegFile"
    "W_IO"
)


# Create target directories if they don't exist
mkdir -p "$GDS_DIR" "$LIB_DIR" "$LEF_DIR"

# Iterate through source directories and copy files
for dir in "${SOURCE_DIRS[@]}"; do
    SRC_PATH="openlane/$dir/runs/$dir/results/signoff"
    if [[ -d "$SRC_PATH" ]]; then
        echo "Processing $dir..."

        # Copy .gds files
        find "$SRC_PATH" -maxdepth 1 -type f -name "*.gds" ! -name "*.*.*" -exec cp -v {} "$GDS_DIR" \;

        # Copy .lib files
        find "$SRC_PATH" -maxdepth 1 -type f -name "*.lib" ! -name "*.*.*" -exec cp -v {} "$LIB_DIR" \;

        # Copy .lef files
        find "$SRC_PATH" -maxdepth 1 -type f -name "*.lef" ! -name "*.*.*" -exec cp -v {} "$LEF_DIR" \;
    else
        echo "Warning: Source path $SRC_PATH does not exist. Skipping..."
    fi
done

echo "File copy operation completed!"
