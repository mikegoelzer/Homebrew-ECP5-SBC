#!env python3

import re
import sys

# ANSI color codes
COLOR_RED = "\033[91m"
COLOR_GREEN = "\033[92m"
COLOR_YELLOW = "\033[93m"
COLOR_BOLD = "\033[1m"
COLOR_BLUE = "\033[94m"
COLOR_RESET = "\033[0m"

class Node:
    def __init__(self, name, start, end, whitespace_prefix, whitespace_unit, attributes=None, children=None):
        self.name = name
        self.start = start
        self.end = end
        self.whitespace_prefix = whitespace_prefix
        self.whitespace_unit = whitespace_unit
        self.attributes = attributes or []
        self.children = children or []

def parse_kicad_sym(file_content):
    def parse_node(start, depth=0):
        i = start
        while i < len(file_content) and file_content[i].isspace():
            i += 1
        
        if file_content[i] != '(':
            return None, i

        node_start = i
        i += 1
        
        # Find the node name
        name_match = re.search(r'\S+', file_content[i:])
        if not name_match:
            return None, i
        name = name_match.group()
        i += name_match.end()

        attributes = []
        children = []

        while i < len(file_content):
            whitespace_prefix = ""
            while i < len(file_content) and file_content[i].isspace():
                if file_content[i] != '\n':
                    whitespace_prefix += file_content[i]
                i += 1
            
            if i >= len(file_content):
                break

            if file_content[i] == '(':
                # print(f"whitespace_prefix: '{whitespace_prefix}', depth: {depth}")
                child, i = parse_node(i, depth+1)
                if child:
                    children.append(child)
            elif file_content[i] == ')':
                if depth == 0:
                    whitespace_unit = whitespace_prefix
                else:
                    whitespace_unit_len = len(whitespace_prefix)//depth
                    whitespace_unit = whitespace_prefix[:whitespace_unit_len]
                return Node(name, node_start, i, whitespace_prefix, whitespace_unit, attributes, children), i + 1
            else:
                # Parse attribute
                attr_match = re.search(r'[^\s()]+', file_content[i:])
                if attr_match:
                    attributes.append(attr_match.group())
                    i += attr_match.end()
                else:
                    i += 1

        return None, i

    root, _ = parse_node(0)
    return root

# Example usage:
content = """
(kicad_symbol_lib
    (version 20231120)
    (generator "kicad_symbol_editor")
    (generator_version "8.0")
    (symbol "PJ-102AH"
        (property "Reference" "J"
            (at -7.6258 5.0838 0)
            (effects
                (font
                    (size 1.27 1.27)
                )
                (justify left bottom)
            )
        )
        (property "Value" "PJ-102AH"
            (at -7.6296 -5.0864 0)
            (effects
                (font
                    (size 1.27 1.27)
                )
                (justify left bottom)
            )
        )
        (symbol "PJ-102AH"
            (pin_names
                (offset 1.016)
            )
        )
    )
)
"""

# Function to print the tree structure
def print_tree(node, indent=""):
    print(f"{indent}'{node.name}' (start: {node.start}, end: {node.end}): {node.attributes}")
    for child in node.children:
        print_tree(child, indent + "  ")

def find_node_of_name(node, node_name, first_or_last="first"):
    """
    Find the first or last node of a given name in the tree.
    :param node: node to start searching from (e.g., root node)
    :param node_name: string name of the node to find
    :param first_or_last: "first" or "last"
    :return: The first or last node of the given name.
    """
    last_node_of_name = None
    for child in node.children:
        if child.name == node_name:
            last_node_of_name = child
            if first_or_last == "first":
                return child
    return last_node_of_name

def find_new_property_insertion_point(file_content):
    """
    Find the point at which we can insert new "property" blocks for the symbol
    :param file_content: string containing .kicad_sym file content as obtained from file.read()
    :return: int index of the index at which we should insert a new property block

    Example:
      ins_pt = find_new_property_insertion_point(file_content)
      updated_content = file_content[:ins_pt] + '\n' + NEW_PROPERTY_BLOCK_STRING + file_content[ins_pt:]
    """
    root = parse_kicad_sym(file_content)
    first_symbol_node = find_node_of_name(root, "symbol", "first")
    last_property = find_node_of_name(first_symbol_node, "property", "last")
    if last_property:
        # print(f"Last property: {last_property.start}-{last_property.end} with whitespace prefix: '{last_property.whitespace_prefix}'")
        return last_property.end+1, last_property.whitespace_prefix, last_property.whitespace_unit
    else:
        raise Exception("no property nodes found")

def make_property(name, value, whitespace_prefix, whitespace_unit):
    return f'''{whitespace_prefix}(property "{name}" "{value}"
{whitespace_prefix + whitespace_unit}(at 0 0 0)
{whitespace_prefix + whitespace_unit}(effects
{whitespace_prefix + whitespace_unit * 2}(font
{whitespace_prefix + whitespace_unit * 3}(size 1.27 1.27)
{whitespace_prefix + whitespace_unit * 2})
{whitespace_prefix + whitespace_unit}(hide yes)
{whitespace_prefix + whitespace_unit})
{whitespace_prefix})'''

def main():
    import os
    import argparse
    parser = argparse.ArgumentParser(description="Add a property in a .kicad_sym file", exit_on_error=False)
    parser.add_argument("FILE", help=".kicad_sym file to modify")
    parser.add_argument("-d", "--dry-run", help="just write to stdout without modifying FILE", action="store_true")
    parser.add_argument("-p", "--parse", help="print the parse tree FILE (unmodified)", action="store_true")
    try:
        args = parser.parse_args()
        if not args.FILE or not os.path.exists(args.FILE):
            print(f"{COLOR_RED}File not found: {args.FILE}{COLOR_RESET} (-h for help)")
            return 1
    except argparse.ArgumentError as e:
        return 1

    # read the file
    with open(args.FILE, 'r') as file:
        content = file.read()
    
    root = parse_kicad_sym(content)
    if args.parse:
        # print the entire file tree
        print_tree(root)
        return
    else:
        # modify the file with backup to temp file

        # check if the root node is a kicad_symbol_lib
        if not root or not root.name == "kicad_symbol_lib":
            print(f"{COLOR_RED}abort: {args.FILE} is not a valid .kicad_sym file{COLOR_RESET}")
            return 1
        
        # prompt the user for the new property name and value
        new_prop_name = input("Enter new property name  > ")
        new_prop_value = input("Enter new property value > ")

        # do the insertion of the new node NewProperty/NewValue
        ins_pt, whitespace_prefix, whitespace_unit = find_new_property_insertion_point(content)
        updated_content = content[:ins_pt] + \
            '\n' + \
            make_property(new_prop_name, new_prop_value, whitespace_prefix, whitespace_unit) + \
            content[ins_pt:]
        
        if args.dry_run:
            print(updated_content)
            print(f"\n{COLOR_BOLD}DRY RUN - FILE NOT MODIFIED{COLOR_RESET}")
        else:
            # move the old file to temp dir
            import tempfile
            with tempfile.NamedTemporaryFile(delete=False, suffix='.kicad_sym') as temp_file:
                temp_file.write(content.encode('utf-8'))
                temp_file_path = temp_file.name

            # write the updated content to the file
            with open(args.FILE, 'w') as file:
                file.write(updated_content)
            
            print(f"{COLOR_GREEN}File updated successfully{COLOR_RESET}")
            print(f"Original file saved to {COLOR_BOLD}{temp_file_path}{COLOR_RESET}")

if __name__ == "__main__":
    try:
        sys.exit(main())
    except KeyboardInterrupt: # raised by Ctrl+C
        print(f"\naborted")
        sys.exit(1)
    except EOFError: # raised by input() on Ctrl+D
        print(f"\naborted")
        sys.exit(1)