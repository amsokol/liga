#!/usr/bin/env python3
"""
Freeze ss01 feature in a font file - makes the ss01 substitution permanent.
Usage: python3 freeze_ss01.py input_font.ttf output_font.ttf
"""

import fontforge
import sys

def freeze_feature(font_path, output_path, feature_name="ss01"):
    """Freeze a stylistic set feature by making its substitutions permanent."""
    print(f"Opening font: {font_path}")
    font = fontforge.open(font_path)
    
    print(f"Freezing feature '{feature_name}'...")
    frozen_count = 0
    
    # Find all lookups associated with the feature
    for lookup_name in font.gsub_lookups:
        lookup_info = font.getLookupInfo(lookup_name)
        if lookup_info and len(lookup_info) > 2 and lookup_info[2]:
            # lookup_info[2] contains list of (feature, script, lang) tuples
            feature_tags = [f[0] for f in lookup_info[2]]
            
            if feature_name in feature_tags:
                print(f"  Found lookup '{lookup_name}' for feature '{feature_name}'")
                
                # Get all subtables for this lookup
                for subtable_name in font.getLookupSubtables(lookup_name):
                    # Collect all substitutions to apply
                    substitutions = []
                    for glyph in font.glyphs():
                        try:
                            pos_sub = glyph.getPosSub(subtable_name)
                            if pos_sub:
                                for item in pos_sub:
                                    # item is tuple: (subtable_name, pos_type, variant)
                                    if item[1] == 'Substitution':
                                        target = item[2]
                                        if target in font:
                                            substitutions.append((glyph.glyphname, target))
                        except:
                            pass
                    
                    # Apply the substitutions by copying alternate glyph over base
                    for base_glyph_name, alt_glyph_name in substitutions:
                        if base_glyph_name in font and alt_glyph_name in font:
                            print(f"    Permanently replacing '{base_glyph_name}' with '{alt_glyph_name}'")
                            # Clear the base glyph and copy the alternate glyph
                            font.selection.none()
                            font.selection.select(alt_glyph_name)
                            font.copy()
                            font.selection.none()
                            font.selection.select(base_glyph_name)
                            # Clear the glyph first, then paste
                            font[base_glyph_name].clear()
                            font.paste()
                            # Preserve the width
                            font[base_glyph_name].width = font[alt_glyph_name].width
                            frozen_count += 1
    
    if frozen_count == 0:
        print(f"Warning: No substitutions found for feature '{feature_name}'")
    else:
        print(f"Successfully froze {frozen_count} substitution(s)")
    
    print(f"Saving font to: {output_path}")
    font.generate(output_path)
    font.close()
    print("Done!")

if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("Usage: python3 freeze_ss01.py input_font.ttf output_font.ttf [feature]")
        print("Example: python3 freeze_ss01.py input.ttf output.ttf ss01")
        sys.exit(1)
    
    input_font = sys.argv[1]
    output_font = sys.argv[2]
    feature = sys.argv[3] if len(sys.argv) > 3 else "ss01"
    
    freeze_feature(input_font, output_font, feature)
