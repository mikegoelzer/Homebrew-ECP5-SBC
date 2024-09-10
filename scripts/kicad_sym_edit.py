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

class ExcelPasteValues:
    def __init__(self):
        self.mpn = ""
        self.digikey = ""
    def __str__(self):
        return f"{self.mpn}\t❌\t{self.digikey}"
    def __setitem__(self, key, value):
        if key.lower() == "mpn":
            setattr(self, "mpn", value)
        elif key.lower() == "digikey":
            setattr(self, "digikey", value)
        else:
            # silently ignore properties we don't care about for Excel
            pass
    def __getitem__(self, key):
        return getattr(self, key) if key in ["mpn", "digikey"] else None
    def set_macos_pboard(self):
        # Fill macOS pasteboard with tab-separated values for easy pasting into Excel
        try:
            import subprocess
            pboard_content = f"{self}"
            subprocess.run(['pbcopy'], input=pboard_content.encode('utf-8'), check=True)
            return True
        except OSError as e:
            # silently ignore as this is probably not macOS
            pass
        except Exception as e:
            print(f"😰 {COLOR_YELLOW}warning: failed to copy Excel values to clipboard:{COLOR_RESET} {COLOR_RED}{str(e)}{COLOR_RESET}")
        return False

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
                if file_content[i] == '"':
                    # Quoted attribute value
                    attr_match = re.search(r'"([^"\\]*(?:\\.[^"\\]*)*)"', file_content[i:])
                    if attr_match:
                        attributes.append('"' + attr_match.group(1) + '"')
                        i += attr_match.end()
                    else:
                        # Unclosed quote, treat as plain text
                        attr_match = re.search(r'[^\s()]+', file_content[i:])
                        if attr_match:
                            attributes.append(attr_match.group())
                            i += attr_match.end()
                        else:
                            i += 1
                else:
                    # Unquoted attribute value
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
kontent = """
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

def find_nodes_of_name(node, node_name, first_last_or_all="first"):
    """
    Find the first node, or last node, or all nodes of a given name in the tree.
    :param node: node to start searching from (e.g., root node)
    :param node_name: string name of the node to find
    :param first_last_or_all: "first", "last", or "all"
    :return: An array containing either (1) only the first node, (2) only the last node, or (3) 
    all the nodes of the given name.
    """
    all_nodes_of_name = []
    last_node_of_name = None
    for child in node.children:
        if child.name == node_name:
            last_node_of_name = child
            if first_last_or_all == "first":
                return [child]
            elif first_last_or_all == "all":
                all_nodes_of_name.append(child)
    if first_last_or_all == "last":
        return [last_node_of_name]
    elif first_last_or_all == "all":
        return all_nodes_of_name
    else:
        raise Exception(f"invalid value for first_last_or_all: '{first_last_or_all}'")

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
    first_symbol_node = (find_nodes_of_name(root, "symbol", "first"))[0]
    last_property = (find_nodes_of_name(first_symbol_node, "property", "last"))[0]
    if last_property:
        # print(f"Last property: {last_property.start}-{last_property.end} with whitespace prefix: '{last_property.whitespace_prefix}'")
        return last_property.end+1, last_property.whitespace_prefix, last_property.whitespace_unit
    else:
        raise Exception("no property nodes found")
    
def get_all_property_names(file_content):
    """
    Get all property names from the file content
    :param file_content: string containing .kicad_sym file content as obtained from file.read()
    :return: list of property names
    """
    root = parse_kicad_sym(file_content)
    first_symbol_node = find_nodes_of_name(root, "symbol", "first")[0]
    all_property_nodes = find_nodes_of_name(first_symbol_node, "property", "all")
    return [node.attributes[0] for node in all_property_nodes]

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

def update_file(file_path, updated_content, dry_run=False, make_backup=True):
    if dry_run:
        print(updated_content)
        print(f"\n{COLOR_BOLD}DRY RUN - FILE NOT MODIFIED{COLOR_RESET}")
    else:
        if make_backup:
            # move the old file to temp dir
            import tempfile
            with tempfile.NamedTemporaryFile(delete=False, suffix='.kicad_sym') as temp_file:
                temp_file.write(updated_content.encode('utf-8'))
                temp_file_path = temp_file.name

        # write the updated content to the file
        with open(file_path, 'w') as file:
            file.write(updated_content)
        
        if make_backup:
            print(f"💾 Original file saved to {COLOR_BOLD}{temp_file_path}{COLOR_RESET}")

def fixup_digikey_url(s):
    if not s.startswith(("http://", "https://")):
        return s, False
    else:
        # Strip out any "?s=..." part at the end of the URL
        valid_digikey_url = s.split('?')[0]
        return valid_digikey_url, True

def main():
    import os
    import argparse
    parser = argparse.ArgumentParser(description="Add standard (or optionally custom) property/ies to a .kicad_sym file", exit_on_error=False)
    parser.add_argument("FILE", help=".kicad_sym file to modify")
    parser.add_argument("-d", "--dry-run", help="just write to stdout without modifying FILE", action="store_true")
    parser.add_argument("-p", "--show-parse", help="print the parse tree FILE (unmodified)", action="store_true")
    parser.add_argument("-c", "--custom-names", help="prompt for custom property names instead of assuming standard properites: Datasheet, Digikey, Mfgr and MPN", action="store_true", default=False)
    try:
        args = parser.parse_args()
        if not args.FILE or not os.path.exists(args.FILE):
            print(f"{COLOR_RED}File not found: {args.FILE}{COLOR_RESET} (-h for help)")
            return 1
    except argparse.ArgumentError:
        return 1

    # read the file
    with open(args.FILE, 'r') as file:
        content = file.read()
    
    # parse the file and verify that it is a valid kicad_symbol_lib
    root = parse_kicad_sym(content)
    if not root or not root.name == "kicad_symbol_lib":
        print(f"{COLOR_RED}abort: {args.FILE} is not a valid .kicad_sym file{COLOR_RESET}")
        return 1

    if args.show_parse:
        # print the entire file tree
        print_tree(root)
        print()
    else:
        # modify the file with backup to temp file
        if not args.custom_names:
            property_names = ["Datasheet", "Digikey", "Mfgr", "MPN"]
            excel_pboard = ExcelPasteValues()
        else:
            property_names = [ input("Enter a new property name > ") ]

        # find the insertion point for the new property block(s)
        ins_pt, whitespace_prefix, whitespace_unit = find_new_property_insertion_point(content)

        # prompt the user for the new property values
        new_prop_blocks_string = ""
        for new_prop_name in property_names:
            if new_prop_name in [prop.strip('"') for prop in get_all_property_names(content)]:
                print(f"✋ {COLOR_YELLOW}warning: property '{new_prop_name}' already exists{COLOR_RESET}: skipping")
                continue
            new_prop_value = input(f"Enter value for {COLOR_BOLD}{new_prop_name}{COLOR_RESET} (leave blank to skip) > ")
            if new_prop_value:
                # special handling for vendor URLs
                if new_prop_name == "Digikey":
                    new_prop_value, url_valid = fixup_digikey_url(new_prop_value)
                    if not url_valid:
                        print(f"⚠️ {COLOR_YELLOW}warning: skipping invalid url '{new_prop_value}'{COLOR_RESET}")
                        continue
                
                new_prop_blocks_string += '\n' + make_property(new_prop_name, new_prop_value, whitespace_prefix, whitespace_unit)
                
                # saving of values for Excel pboard at end
                excel_pboard[new_prop_name] = new_prop_value

        # do the insertion of the new node(s) and update the file
        if new_prop_blocks_string:
            updated_content = content[:ins_pt] + new_prop_blocks_string + content[ins_pt:]
            update_file(args.FILE, updated_content, args.dry_run)
            print(f"✅ {COLOR_GREEN}File updated successfully{COLOR_RESET}")
            
            # Fill macOS pasteboard with tab-separated values for easy pasting into Excel
            if excel_pboard.set_macos_pboard():
                print(f"✅ {COLOR_GREEN}Copied pasteable Excel values:{COLOR_RESET} '{excel_pboard}'")
        else:
            print(f"🚫 aborting: no new properties to add")
            return 1

if __name__ == "__main__":
    try:
        sys.exit(main())
    except KeyboardInterrupt: # raised by Ctrl+C
        print(f"\naborted")
        sys.exit(1)
    except EOFError: # raised by input() on Ctrl+D
        print(f"\naborted")
        sys.exit(1)