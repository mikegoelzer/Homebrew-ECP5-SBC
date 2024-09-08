#!env python3

import bisect, sys

# ANSI color codes
COLOR_RED = "\033[91m"
COLOR_GREEN = "\033[92m"
COLOR_YELLOW = "\033[93m"
COLOR_BOLD = "\033[1m"
COLOR_BLUE = "\033[94m"
COLOR_RESET = "\033[0m"
COLOR_GRAY = "\033[90m"

def worst_case_resistor(r, tolerance):
    """
    r in ohms
    tolerance is a percentage, e.g. 0.05 for 5%
    Returns the worst-case (lowest) resistance value
    """
    return r * (1 - tolerance)

def find_closest_greater_than_or_equal(value, series):
    index = bisect.bisect_left(series, value)
    return series[index] if index < len(series) else None

def led_current(supply_voltage, vf, r):
    return (supply_voltage - vf) / r * 1000 if r else 0

def find_lowest_safe_resistor(supply_voltage, vf, max_current, full_series, tolerance):
    """
    Find the lowest resistor in the series that will not exceed the maximum current in the worst case.
    
    :param supply_voltage: Supply voltage in volts
    :param vf: LED forward voltage in volts
    :param max_current: Maximum allowed current in amperes
    :param full_series: List of resistor values in the series (in ohms)
    :param tolerance: Tolerance as a decimal (e.g., 0.05 for 5%)
    :return: Lowest safe resistor value from the series, or None if no safe value found
    """
    min_resistance = (supply_voltage - vf) / max_current
    
    for r in sorted(full_series):
        worst_case_r = worst_case_resistor(r, tolerance)
        if worst_case_r >= min_resistance:
            return r
    
    return None  # If no resistor in the series is safe

def calculate_led_resistor(vf, max_current_ma, supply_voltage):
    # Convert max_current from mA to A
    max_current = max_current_ma / 1000
    # Calculate exact resistance
    exact_resistance = (supply_voltage - vf) / max_current

    # E6 (20%), E12 (10%), E24 (5%), and E96 (1%) series
    e6_values = [10, 15, 22, 33, 47, 68]
    e12_values = [10, 12, 15, 18, 22, 27, 33, 39, 47, 56, 68, 82]
    e24_values = [10, 11, 12, 13, 15, 16, 18, 20, 22, 24, 27, 30, 33, 36, 39, 43, 47, 51, 56, 62, 68, 75, 82, 91]
    e96_values = [100, 102, 105, 107, 110, 113, 115, 118, 121, 124, 127, 130, 133, 137, 140, 143, 147, 150, 154, 158, 162, 165, 169, 174, 178, 182, 187, 191, 196]

    # Generate full series
    full_e6 = [e * 10**n for n in range(-1, 6) for e in e6_values]
    full_e12 = [e * 10**n for n in range(-1, 6) for e in e12_values]
    full_e24 = [e * 10**n for n in range(-1, 6) for e in e24_values]
    full_e96 = [e * 10**n for n in range(-1, 6) for e in e96_values]
    
    # Find closest values that will not exceed the maximum current
    e6_value = find_closest_greater_than_or_equal(exact_resistance, full_e6)
    e12_value = find_closest_greater_than_or_equal(exact_resistance, full_e12)
    e24_value = find_closest_greater_than_or_equal(exact_resistance, full_e24)
    e96_value = find_closest_greater_than_or_equal(exact_resistance, full_e96)

    e6_safe = find_lowest_safe_resistor(supply_voltage, vf, max_current, full_e6, 0.20)
    e12_safe = find_lowest_safe_resistor(supply_voltage, vf, max_current, full_e12, 0.10)
    e24_safe = find_lowest_safe_resistor(supply_voltage, vf, max_current, full_e24, 0.05)
    e96_safe = find_lowest_safe_resistor(supply_voltage, vf, max_current, full_e96, 0.01)

    return exact_resistance, e6_value, e12_value, e24_value, e96_value, e6_safe, e12_safe, e24_safe, e96_safe

def main():
    supply_voltage = float(input("Enter supply voltage (V): "))
    vf = float(input("Enter LED forward voltage (Vf): "))
    max_current_ma = float(input("Enter desired maximum current (mA): "))

    r_exact, r_e6, r_e12, r_e24, r_e96, r_e6_safe, r_e12_safe, r_e24_safe, r_e96_safe = calculate_led_resistor(vf, max_current_ma, supply_voltage)
    r_e6_worst_case = worst_case_resistor(r_e6, 0.20)
    r_e12_worst_case = worst_case_resistor(r_e12, 0.10)
    r_e24_worst_case = worst_case_resistor(r_e24, 0.05)
    r_e96_worst_case = worst_case_resistor(r_e96, 0.01) 

    # Calculate actual currents with all resistor series
    current_e6 = led_current(supply_voltage, vf, r_e6)
    current_e12 = led_current(supply_voltage, vf, r_e12)
    current_e24 = led_current(supply_voltage, vf, r_e24)
    current_e96 = led_current(supply_voltage, vf, r_e96)
    current_e6_worst_case = led_current(supply_voltage, vf, r_e6_worst_case)
    current_e12_worst_case = led_current(supply_voltage, vf, r_e12_worst_case)
    current_e24_worst_case = led_current(supply_voltage, vf, r_e24_worst_case)
    current_e96_worst_case = led_current(supply_voltage, vf, r_e96_worst_case)
    current_e6_safe = led_current(supply_voltage, vf, r_e6_safe)
    current_e12_safe = led_current(supply_voltage, vf, r_e12_safe)
    current_e24_safe = led_current(supply_voltage, vf, r_e24_safe)
    current_e96_safe = led_current(supply_voltage, vf, r_e96_safe)

    def format_resistance(r):
        if r < 1000:
            return f"{r:>4}"
        elif r < 1000000:
            return f"{r/1000:.0f}k".rjust(4)
        else:
            return f"{r/1000000:.0f}M".rjust(4)

    print("")
    print(f"Exact resistor required: {COLOR_BOLD}{r_exact:.2f} Ω{COLOR_RESET}")
    print("")
    print("Series    | R      |  Current | Worst Case          | Safe Resistor")
    print("----------|--------|----------|---------------------|-------------------")
    print(f"E6  (20%) | {COLOR_BLUE}{format_resistance(r_e6):>4} Ω{COLOR_RESET} | {COLOR_BLUE}{current_e6:>5.1f} mA{COLOR_RESET} | {COLOR_BOLD}{r_e6_worst_case:>6.1f} Ω{COLOR_RESET} ({COLOR_GREEN if current_e6_worst_case <= max_current_ma else COLOR_RED}{current_e6_worst_case:>5.1f} mA{COLOR_RESET}) | {COLOR_BLUE}{format_resistance(r_e6_safe):>4} Ω{COLOR_RESET} ({COLOR_GREEN if current_e6_safe <= max_current_ma else COLOR_RED}{current_e6_safe:>5.1f} mA{COLOR_RESET})")
    print(f"E12 (10%) | {COLOR_BLUE}{format_resistance(r_e12):>4} Ω{COLOR_RESET} | {COLOR_BLUE}{current_e12:>5.1f} mA{COLOR_RESET} | {COLOR_BOLD}{r_e12_worst_case:>6.1f} Ω{COLOR_RESET} ({COLOR_GREEN if current_e12_worst_case <= max_current_ma else COLOR_RED}{current_e12_worst_case:>5.1f} mA{COLOR_RESET}) | {COLOR_BLUE}{format_resistance(r_e12_safe):>4} Ω{COLOR_RESET} ({COLOR_GREEN if current_e12_safe <= max_current_ma else COLOR_RED}{current_e12_safe:>5.1f} mA{COLOR_RESET})")
    print(f"E24 (5%)  | {COLOR_BLUE}{format_resistance(r_e24):>4} Ω{COLOR_RESET} | {COLOR_BLUE}{current_e24:>5.1f} mA{COLOR_RESET} | {COLOR_BOLD}{r_e24_worst_case:>6.1f} Ω{COLOR_RESET} ({COLOR_GREEN if current_e24_worst_case <= max_current_ma else COLOR_RED}{current_e24_worst_case:>5.1f} mA{COLOR_RESET}) | {COLOR_BLUE}{format_resistance(r_e24_safe):>4} Ω{COLOR_RESET} ({COLOR_GREEN if current_e24_safe <= max_current_ma else COLOR_RED}{current_e24_safe:>5.1f} mA{COLOR_RESET})")
    print(f"E96 (1%)  | {COLOR_BLUE}{format_resistance(r_e96):>4} Ω{COLOR_RESET} | {COLOR_BLUE}{current_e96:>5.1f} mA{COLOR_RESET} | {COLOR_BOLD}{r_e96_worst_case:>6.1f} Ω{COLOR_RESET} ({COLOR_GREEN if current_e96_worst_case <= max_current_ma else COLOR_RED}{current_e96_worst_case:>5.1f} mA{COLOR_RESET}) | {COLOR_BLUE}{format_resistance(r_e96_safe):>4} Ω{COLOR_RESET} ({COLOR_GREEN if current_e96_safe <= max_current_ma else COLOR_RED}{current_e96_safe:>5.1f} mA{COLOR_RESET})")
    print("")
    print(f"{COLOR_GRAY}Worst case: you get the furthest out of tolerance resistor for that series{COLOR_RESET}")
    print(f"{COLOR_GRAY}Safe: the one to pick so even worst case is under max current{COLOR_RESET}")

if __name__ == "__main__":
    sys.exit(main())