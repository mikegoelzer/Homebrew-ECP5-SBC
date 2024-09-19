#!/usr/bin/env python3

"""
Generate a list of all E96 1% resistors pasteable into Excel
"""

def generate_e96_resistors():
    # E96 series multipliers
    e96_multipliers = [
        1.00, 1.02, 1.05, 1.07, 1.10, 1.13, 1.15, 1.18, 1.21, 1.24, 1.27, 1.30,
        1.33, 1.37, 1.40, 1.43, 1.47, 1.50, 1.54, 1.58, 1.62, 1.65, 1.69, 1.74,
        1.78, 1.82, 1.87, 1.91, 1.96, 2.00, 2.05, 2.10, 2.15, 2.21, 2.26, 2.32,
        2.37, 2.43, 2.49, 2.55, 2.61, 2.67, 2.74, 2.80, 2.87, 2.94, 3.01, 3.09,
        3.16, 3.24, 3.32, 3.40, 3.48, 3.57, 3.65, 3.74, 3.83, 3.92, 4.02, 4.12,
        4.22, 4.32, 4.42, 4.53, 4.64, 4.75, 4.87, 4.99, 5.11, 5.23, 5.36, 5.49,
        5.62, 5.76, 5.90, 6.04, 6.19, 6.34, 6.49, 6.65, 6.81, 6.98, 7.15, 7.32,
        7.50, 7.68, 7.87, 8.06, 8.25, 8.45, 8.66, 8.87, 9.09, 9.31, 9.53, 9.76
    ]

    resistors = []
    for decade in range(6):  # 10^0 to 10^5 (1 Ω to 1 MΩ)
        for multiplier in e96_multipliers:
            value = multiplier * (10 ** decade)
            resistors.append(value)

    return sorted(resistors)
def format_resistor_value(value):
    """
    Format a resistor value in ohms to its most natural representation.
    
    :param value: Resistor value in ohms (float)
    :return: Formatted string representation
    """
    if value >= 1e6:
        return f"{value/1e6:.2f} MΩ".rstrip('0').rstrip('.')
    elif value >= 1e3:
        return f"{value/1e3:.2f} kΩ".rstrip('0').rstrip('.')
    else:
        return f"{value:.2f} Ω".rstrip('0').rstrip('.')

def main():
    import argparse
    parser = argparse.ArgumentParser(description="generate a list of all E96 1% resistors (run with `| pbcopy` then paste into Excel in top left cell)")
    parser.usage = "%(prog)s | pbcopy"
    args = parser.parse_args()

    # Generate and print the resistors
    e96_resistors = generate_e96_resistors()
    row_cnt = len(e96_resistors)
    print(f"Value\tFormatted\t\tExample")
    i = 1
    for resistor in e96_resistors:
        if i == 1:
            s = "Actual Value\t10.12345"
        elif i == 2:
            s = f"E96\t=VLOOKUP(E2, A2:B{row_cnt+1}, 1, TRUE)"
        elif i == 3:
            s = f"E96 String\t=VLOOKUP(E2, A2:B{row_cnt+1}, 2, TRUE)"
        else:
            s = ""
        print(f"{resistor:.2f}\t{format_resistor_value(resistor)}\t\t{s}")
        i += 1
if __name__ == "__main__":
    import sys
    sys.exit(main())