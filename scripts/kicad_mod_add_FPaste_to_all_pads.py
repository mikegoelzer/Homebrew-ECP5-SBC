#
# This script goes through each pad in a .kicad_mod footprint and 
# adds an "F.Paste" layer to each pad.
#
import re

def add_paste_layer(filename):
    # Read the file
    with open(filename, 'r') as file:
        content = file.read()

    # Regular expression to find pad definitions and their layer lists
    pattern = r'\(layers "F\.Cu" "F\.Mask"\)'
    
    # Count original occurrences
    count = len(re.findall(pattern, content))
    
    # Replace each occurrence, adding F.Paste to the layers list
    modified_content = re.sub(
        pattern,
        r'(layers "F.Cu" "F.Paste" "F.Mask")',
        content
    )

    # Write the modified content back to the file
    with open(filename, 'w') as file:
        file.write(modified_content)
    
    # Print the number of modifications
    print(f"Modified {count} layer definitions")
    if count != 100:
        print("Warning: Expected 100 modifications for 100 pads!")

# Use the script
filename = "../hardware/parts/DF40C_100DS_0_4V_51_/HIROSE_DF40C-100DS-0.4V_51_.kicad_mod"
add_paste_layer(filename)
