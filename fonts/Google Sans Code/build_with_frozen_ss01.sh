#!/usr/bin/env bash

# This script freezes ss01 in Google Sans Code, THEN adds ligatures

SRC=$(realpath "$(dirname "${BASH_SOURCE[0]}")")
LIGA_DIR=$SRC/../..

# Activate virtual environment if it exists
if [ -f "$LIGA_DIR/.venv/bin/activate" ]; then
    source "$LIGA_DIR/.venv/bin/activate"
    echo "Activated Python virtual environment"
fi

SCRIPTS_DIR=$LIGA_DIR/scripts
source "$SCRIPTS_DIR"/build_family.sh
declare -A FONT_WEIGHT

INPUT_DIR="$LIGA_DIR/input/Google Sans Code"
FROZEN_INPUT_DIR="$LIGA_DIR/input/Google Sans Code Frozen SS01"
OUTPUT_NAME="Google Sans Code"
OUTPUT_DIR="$LIGA_DIR/output/$OUTPUT_NAME"
CONFIG="$SRC/config.py"

echo "Step 1: Freezing ss01 in original fonts..."

# Create frozen input directory
rm -rf "$FROZEN_INPUT_DIR"
mkdir -p "$FROZEN_INPUT_DIR"

# Freeze ss01 in each input font
for font_file in "$INPUT_DIR"/*.ttf; do
    if [ -f "$font_file" ]; then
        filename=$(basename "$font_file")
        echo "  Freezing ss01 in $filename..."
        python3 "$LIGA_DIR/freeze_ss01.py" "$font_file" "$FROZEN_INPUT_DIR/$filename" ss01
    fi
done

echo ""
echo "Step 2: Building ligated fonts from frozen versions..."

# Configuration from build.sh
FONT_WEIGHT=()
FILTER_BY_FONT_WEIGHT=false
COPY_GLYPHS=true
REMOVE_ORIGINAL_LIGATURES=true

# Use frozen input directory
INPUT_DIR="$FROZEN_INPUT_DIR"

# Build fonts using the frozen inputs
pushd "$LIGA_DIR" || exit
    build_family
popd || exit

# Copy license
cp "$LIGA_DIR/input/Google Sans Code/OFL.txt" "$OUTPUT_DIR" 2>/dev/null || true

echo ""
echo "✨ All done! Fonts with frozen ss01 + ligatures are in: $OUTPUT_DIR"
echo "   Frozen input fonts (without ligatures) are in: $FROZEN_INPUT_DIR"
