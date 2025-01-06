#!/usr/bin/env python3

# Pin name mappings (from the image)
# Unit A pins (1-100)
UNIT_A_PINS = {
    1: "JTAG_TDO",
    2: "JTAG_TMS",
    3: "JTAG_TCK",
    4: "JTAG_TDI",
    5: "GND",
    6: "ECP5_INITN",
    7: "ECP5_PRGMN_BTN",
    8: "ECP5_DONE",
    9: "IO_C12",
    10: "IO_P2",
    11: "IO_C13",
    12: "IO_P4",
    13: "IO_C14",
    14: "IO_N4",
    15: "IO_C15",
    16: "NC",
    17: "IO_C16",
    18: "IO_F19",
    19: "IO_C17",
    20: "IO_F17",
    21: "IO_B18",
    22: "IO_E19",
    23: "IO_B17",
    24: "IO_E18",
    25: "IO_B16",
    26: "IO_D19",
    27: "IO_B15",
    28: "IO_D18",
    29: "IO_B13",
    30: "IO_E17",
    31: "IO_B12",
    32: "IO_A18",
    33: "IO_B11",
    34: "IO_A17",
    35: "IO_B10",
    36: "IO_A16",
    37: "IO_B9",
    38: "IO_A15",
    39: "IO_B8",
    40: "IO_A14",
    41: "IO_B6",
    42: "IO_A13",
    43: "IO_U19",
    44: "IO_A12",
    45: "IO_T19",
    46: "IO_A11",
    47: "IO_P19",
    48: "IO_A10",
    49: "IO_N19",
    50: "IO_A9",
    51: "IO_P5",
    52: "IO_A8",
    53: "IO_M19",
    54: "IO_A7",
    55: "IO_N5",
    56: "IO_A6",
    57: "IO_L19",
    58: "IO_U20",
    59: "IO_E7",
    60: "IO_T20",
    61: "IO_K19",
    62: "IO_R20",
    63: "IO_J19",
    64: "IO_P20",
    65: "GND",
    66: "IO_N20",
    67: "GND",
    68: "IO_M20",
    69: "GND",
    70: "IO_L20",
    71: "GND",
    72: "IO_K20",
    73: "GND",
    74: "IO_J20",
    75: "GND",
    76: "IO_H20",
    77: "3V3_OUT",
    78: "IO_G20",
    79: "3V3_OUT",
    80: "IO_F20",
    81: "3V3_OUT",
    82: "IO_E20",
    83: "3V3_OUT",
    84: "IO_D20",
    85: "3V3_OUT",
    86: "IO_C20",
    87: "3V3_OUT",
    88: "IO_B20",
    89: "5V_IN",
    90: "IO_D14",
    91: "5V_IN",
    92: "IO_D15",
    93: "5V_IN",
    94: "IO_D13",
    95: "5V_IN",
    96: "IO_D12",
    97: "5V_IN",
    98: "IO_B19",
    99: "5V_IN",
    100: "IO_A19"
}

# Unit B pins (101-200)
UNIT_B_PINS = {
    101: "IO_V1",
    102: "IO_C10",
    103: "NC",
    104: "IO_P3",
    105: "IO_U1",
    106: "IO_D11",
    107: "NC",
    108: "IO_N2",
    109: "IO_T1",
    110: "IO_C9",
    111: "NC",
    112: "IO_N3",
    113: "IO_R1",
    114: "IO_C8",
    115: "NC",
    116: "IO_M3",
    117: "IO_P1",
    118: "IO_C7",
    119: "NC",
    120: "IO_L3",
    121: "IO_N1",
    122: "IO_C6",
    123: "NC",
    124: "IO_L2",
    125: "IO_M1",
    126: "IO_C11",
    127: "NC",
    128: "IO_F3",
    129: "IO_L1",
    130: "IO_K2",
    131: "NC",
    132: "IO_K3",
    133: "IO_K1",
    134: "IO_J3",
    135: "IO_J1",
    136: "IO_H2",
    137: "NC",
    138: "IO_E3",
    139: "IO_H1",
    140: "IO_D3",
    141: "NC",
    142: "IO_C2",
    143: "IO_G1",
    144: "NC",
    145: "NC",
    146: "NC",
    147: "IO_F1",
    148: "IO_C3",
    149: "IO_F2",
    150: "NC",
    151: "IO_E1",
    152: "IO_B3",
    153: "IO_E2",
    154: "IO_H3",
    155: "IO_D1",
    156: "IO_F4",
    157: "IO_D2",
    158: "IO_G3",
    159: "IO_C1",
    160: "IO_G5",
    161: "NC",
    162: "NC",
    163: "IO_B1",
    164: "IO_B5",
    165: "NC",
    166: "NC",
    167: "IO_B2",
    168: "IO_D5",
    169: "NC",
    170: "NC",
    171: "IO_A2",
    172: "IO_D6",
    173: "NC",
    174: "NC",
    175: "IO_A3",
    176: "IO_E6",
    177: "NC",
    178: "NC",
    179: "IO_A4",
    180: "IO_E5",
    181: "NC",
    182: "IO_F4",
    183: "IO_A5",
    184: "NC",
    185: "IO_E9",
    186: "IO_E4",
    187: "IO_E14",
    188: "IO_C4",
    189: "IO_E13",
    190: "IO_B4",
    191: "IO_E15",
    192: "IO_F5",
    193: "IO_E10",
    194: "IO_C5",
    195: "IO_D9",
    196: "IO_D7",
    197: "IO_E11",
    198: "IO_E8",
    199: "IO_D10",
    200: "IO_D8"
}

# Update the output paths
OUTPUT_FILE_A = "../hardware/parts/compute-module/TEMP_GCM_PASTEABLE-UNIT-A.kicad_sym"
OUTPUT_FILE_B = "../hardware/parts/compute-module/TEMP_GCM_PASTEABLE-UNIT-B.kicad_sym"

def generate_unit(unit_name, start_pin, pin_map):
    unit = f'''    (symbol "{unit_name}"
        (pin_names
            (offset 1.016)
        )
        (in_bom yes)
        (on_board yes)
        (property "Reference" "J" (at 0 66.04 0)
            (effects (font (size 1.27 1.27)))
        )
        (property "Value" "{unit_name}" (at 0 -68.58 0)
            (effects (font (size 1.27 1.27)))
        )
        (property "Footprint" "" (at 0 0 0)
            (effects (font (size 1.27 1.27)) hide)
        )
        (property "Datasheet" "" (at 0 0 0)
            (effects (font (size 1.27 1.27)) hide)
        )
        (rectangle (start -15.24 63.5) (end 15.24 -66.04)
            (stroke (width 0.254) (type default))
            (fill (type background))
        )'''
        
    # Adjust pin positions to align with rectangle edges
    # Increase pin length from 5.08 to 7.62 (20 mil to 30 mil)
    y_pos = 60.96  # Start slightly lower from the top
    for pin_num in range(start_pin + 98, start_pin - 1, -2):  # Start at 99, go down to 1
        pin_name = pin_map.get(pin_num, f"Pin_{pin_num}")
        unit += f'''
    (pin passive line (at 22.86 {y_pos:.2f} 180) (length 7.62)
        (name "{pin_name}" (effects (font (size 1.27 1.27))))
        (number "{pin_num}" (effects (font (size 1.27 1.27))))
    )'''
        y_pos -= 2.54
    
    y_pos = 60.96  # Reset for left side
    for pin_num in range(start_pin + 99, start_pin, -2):  # Start at 100, go down to 2
        pin_name = pin_map.get(pin_num, f"Pin_{pin_num}")
        unit += f'''
    (pin passive line (at -22.86 {y_pos:.2f} 0) (length 7.62)
        (name "{pin_name}" (effects (font (size 1.27 1.27))))
        (number "{pin_num}" (effects (font (size 1.27 1.27))))
    )'''
        y_pos -= 2.54
        
    unit += "\n    )"
    return unit

def generate_kicad_symbol_file(unit_name, start_pin, pin_map, output_path):
    # Move header inside this function since we need it for each file
    header = '''(kicad_symbol_lib
    (version 20231120)
    (generator "kicad_symbol_editor")
    (generator_version "8.0")'''
    
    content = header + "\n"
    content += generate_unit(unit_name, start_pin, pin_map) + "\n"
    content += ")"
    
    # Write to file
    with open(output_path, "w") as f:
        f.write(content)

def generate_kicad_symbol():
    # Generate Unit A file
    generate_kicad_symbol_file("Unit_A", 1, UNIT_A_PINS, OUTPUT_FILE_A)
    
    # Generate Unit B file
    generate_kicad_symbol_file("Unit_B", 101, UNIT_B_PINS, OUTPUT_FILE_B)

if __name__ == "__main__":
    generate_kicad_symbol()