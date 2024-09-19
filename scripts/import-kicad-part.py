#!env python3

import re
import sys
import os
import argparse

# ANSI color codes
COLOR_RED = "\033[91m"
COLOR_GREEN = "\033[92m"
COLOR_YELLOW = "\033[93m"
COLOR_BOLD = "\033[1m"
COLOR_BLUE = "\033[94m"
COLOR_RESET = "\033[0m"

CWD_CONFIG_FILE_NAME = 'import-kicad-part.ini'

#
# Functions to modify files within the downloaded zip
#

def update_kicad_sym(kicad_sym_filename, part_number=None, footprint_name=None):
    """
    Modifies a <part_number>.kicad_sym file to fix the footprint property
    (e.g., "SLLB120200" -> "SLLB120200:SLLB120200")
    First part is `part_number` if non-empty, otherwise part number found in kicad_sym file is used.
    Second part is `footprint_name` if non-empty, otherwise symbol name found in kicad_sym file is used.
    """
    with open(kicad_sym_filename, 'r') as file:
        content = file.read()

    # change 'Manufacturer_Part_Number' to 'MPN'
    pattern = r'(property\s+")(Manufacturer_Part_Number)("\s+.*)'
    content, num_subs = re.subn(pattern, r'\1MPN\3', content)

    # get the symbol name (part number), e.g., 'SLLB120200'
    def get_symbol_name(content):
        symbol_match = re.search(r'\(symbol\s+"([^"]+)"', content)
        symbol_name = symbol_match.group(1) if symbol_match else None
        if symbol_name is None:
            print(f"❌ {COLOR_RED}error: symbol name not found in {COLOR_BOLD}{kicad_sym_filename}{COLOR_RESET}")
            raise Exception(f"symbol name not found in {kicad_sym_filename}")

        return symbol_name
    
    # get the right part number andfootprint name to use
    if footprint_name is None:
        footprint_name = get_symbol_name(content)
        print(f"⛔️ Warning: no footprint name provided, guessing based on symbol name: {footprint_name}")
    if part_number is None:
        part_number = get_symbol_name(content)
        print(f"⛔️ Warning: no part_number provided, guessing based on symbol name: {part_number}")

    # find the Footprint property and update its value if not already in the correct format
    pattern = r'(property "Footprint" ")([^":]+)(?::([^"]+))?(")'
    def replacement(m):
        footprint = m.group(2)
        if m.group(3) == footprint:  # already in the correct format
            return m.group(0)
        else:
            if part_number is None:
                print(f"❌ {COLOR_RED}error: part number not found in {COLOR_BOLD}{kicad_sym_filename}{COLOR_RESET}")
                raise Exception(f"part number not found in {kicad_sym_filename}")
            elif footprint_name is None:
                print(f"❌ {COLOR_RED}error: footprint name not found in {COLOR_BOLD}{kicad_sym_filename}{COLOR_RESET} by name of our strategies")
                raise Exception(f"footprint name not found in {kicad_sym_filename}")
            else:
                return f'{m.group(1)}{part_number}:{footprint_name}{m.group(4)}'
    updated_content, num_subs = re.subn(pattern, replacement, content)

    # write the updated content back to the file
    with open(kicad_sym_filename, 'w') as file:
        file.write(updated_content)

    # find the new Footprint value
    new_footprint_match = re.search(pattern, updated_content)
    new_footprint = new_footprint_match.group(2) + ':' + new_footprint_match.group(3) if new_footprint_match else "Not found"

    if num_subs > 0:
        print(f"✅ Updated footprint in {COLOR_BOLD}{kicad_sym_filename}{COLOR_RESET} to {COLOR_GREEN}{new_footprint}{COLOR_RESET}")
    else:
        print(f"🚫 No changes made to {COLOR_BOLD}{kicad_sym_filename}{COLOR_RESET} (footprint is '{new_footprint}')")


def update_3d_model_path(kicad_mod_filename, parts_dir_rel_to_project_dir, part_dir_name, step_file_sub_path):
    """
    Updates the 3D model path in a .kicad_mod file.
    
    :param file_name: Name of the .kicad_mod file to update
    :param parts_dir_rel_to_project_dir: parts dir relative to project dir (e.g., '../parts/')
    :param part_dir_name: name of the part directory (e.g., 'SLLB120200')
    :param step_file_sub_path: sub-path to step file from parts dir (e.g., 'SLLB120200/SLLB120200/3D/SLLB120200.stp')

    Example usage:
        update_3d_model_path('SLLB120200.kicad_mod', '../parts/', 'SLLB120200', 'SLLB120200/3D/SLLB120200.stp')
    """
    with open(kicad_mod_filename, 'r') as file:
        content = file.read()

    # pattern to match the 3D model filename or path
    pattern = r'(\(model\s+)("?)([^"\s]+\.(?:stp|step))("?)'
    
    # try to find the pattern in content, returning false if not found
    def has_3d_model(content):
        return re.search(pattern, content) is not None

    def replacement(m):
        model_path = m.group(3)
        if '${KIPRJMOD}' in model_path:
            return m.group(0)  # no change if ${KIPRJMOD} is already present
        new_path = f'${{KIPRJMOD}}/{parts_dir_rel_to_project_dir}/{part_dir_name}/{step_file_sub_path}'
        return f'{m.group(1)}"{new_path}"'

    def insert_new_model_block(content):
        # Create the new model block
        new_model_block = f'''{"\t"}(model "${{KIPRJMOD}}/{parts_dir_rel_to_project_dir}/{part_dir_name}/{step_file_sub_path}"
{"\t"}{"\t"}(offset (xyz 0 0 0))
{"\t"}{"\t"}(scale (xyz 1 1 1))
{"\t"}{"\t"}(rotate (xyz 0 0 0))
{"\t"})'''

        # Find the last closing parenthesis
        last_paren_index = content.rfind(')')
        if last_paren_index == -1:
            print("❌ error: failed to find closing parentheses in .kicad_mod file")
            return None  # No closing parenthesis found, return original content
        else:
            # Insert the new model block before the last closing parenthesis
            print(f"ℹ️ No preexisting model block found, so added new one to {COLOR_BOLD}{kicad_mod_filename}{COLOR_RESET}")
            return content[:last_paren_index] + new_model_block + '\n' + content[last_paren_index:]

    if not has_3d_model(content):
        # need to create a new "model" block from scratch
        updated_content = insert_new_model_block(content)

        # Write the updated content back to the file
        if updated_content is not None:
            with open(kicad_mod_filename, 'w') as file:
                file.write(updated_content)

            print(f"✅ Added 3D model block to {COLOR_BOLD}{kicad_mod_filename}{COLOR_RESET} with path '{COLOR_GREEN}${{KIPRJMOD}}/{parts_dir_rel_to_project_dir}/{part_dir_name}/{step_file_sub_path}{COLOR_RESET}'")
    else:
        # just need to fix the path
        updated_content, num_subs = re.subn(pattern, replacement, content)

        if num_subs > 0:
            with open(kicad_mod_filename, 'w') as file:
                file.write(updated_content)
            new_path_match = re.search(pattern, updated_content)
            if new_path_match:
                new_path = new_path_match.group(3)
                print(f"✅ Updated 3D model path in {COLOR_BOLD}{kicad_mod_filename}{COLOR_RESET} to '{COLOR_GREEN}{new_path}{COLOR_RESET}'")
            else:
                print(f"🚫 No changes made to {COLOR_BOLD}{kicad_mod_filename}{COLOR_RESET} (3D model path already correct)")
        else:
            print(f"❌ {COLOR_RED}error: no changes made to{COLOR_RESET} {COLOR_BOLD}{kicad_mod_filename}{COLOR_RESET} {COLOR_RED}(3D model not found){COLOR_RESET}")

#
# Functions for unzipping file or copying dir and finding the KiCad files
#
def copy_part_dir(src_dir, parts_dir, force_overwrite=False):
    import shutil

    # get the part number from the src_dir name
    part_number = get_part_number_from_zip_or_dir_name(src_dir)
    
    # Create the full path for the new directory
    dest_dir = os.path.join(parts_dir, part_number)

    # Check if the directory already exists and act accordingly
    if os.path.exists(dest_dir):
        if force_overwrite:
            print(f"🗑️ Removing existing directory: {dest_dir}")
            shutil.rmtree(dest_dir)
        else:
            print(f"🚫 {COLOR_RED}Directory already exists: {COLOR_BOLD}{dest_dir}{COLOR_RESET}\n{COLOR_RED}Use -f to overwrite{COLOR_RESET}")
            return None, None
    
    # Copy the directory
    shutil.copytree(src_dir, dest_dir)
    return dest_dir, part_number

def get_part_number_from_zip_or_dir_name(zip_or_dir_file):
    """
    Get the part number from the zip file name
    """
    # Get the name without the .zip extension (if any)
    zip_name = os.path.splitext(os.path.basename(zip_or_dir_file))[0]

    # Process the zip_name to remove 'LIB_' prefix and any download number suffix 
    # (e.g., LIB_RC1206JR_07820RL(1).zip -> RC1206JR_07820RL)
    part_number = zip_name
    if part_number.startswith('LIB_'):
        part_number = part_number[4:]
    part_number = re.sub(r'\(\d+\)$', '', part_number)
    return part_number

def unzip_part_file(zip_file, parts_dir, force_overwrite=False):
    """
    Unzips the given zip file into a directory under parts_dir.
    The new directory is named after the zip file (without the .zip extension).
    
    Example:
    If zip_file is 'LIB_SLLB120200.zip', it will be unzipped into '[parts directory]/LIB_SLLB120200'
    
    Args:
    zip_file (str): Path to the zip file
    parts_dir (str): Path to the parts directory
    
    Returns:
    str: Full path of the new directory containing the unzipped contents
    """
    import zipfile, shutil
    
    # get the part number from the zip file name
    part_number = get_part_number_from_zip_or_dir_name(zip_file)
    
    # Create the full path for the new directory
    unzip_dir = os.path.join(parts_dir, part_number)

    # Check if the directory already exists and act accordingly
    if os.path.exists(unzip_dir):
        if force_overwrite:
            print(f"🗑️ Removing existing directory: {unzip_dir}")
            shutil.rmtree(unzip_dir)
        else:
            print(f"🚫 {COLOR_RED}Directory already exists: {COLOR_BOLD}{unzip_dir}{COLOR_RESET}\n{COLOR_RED}Use -f to overwrite{COLOR_RESET}")
            return None, None
    
    # Create the directory if it doesn't exist
    os.makedirs(unzip_dir, exist_ok=True)
    
    # Unzip the file
    with zipfile.ZipFile(zip_file, 'r') as zip_ref:
        zip_ref.extractall(unzip_dir)
    
    return unzip_dir, part_number

def find_kicad_files(unzipped_dir):
    kicad_sym_files = []
    kicad_mod_files = []
    step_files = []

    for root, dirs, files in os.walk(unzipped_dir):
        for file in files:
            rel_path = os.path.relpath(os.path.join(root, file), unzipped_dir)
            if file.endswith('.kicad_sym'):
                kicad_sym_files.append(rel_path)
            elif file.endswith('.kicad_mod'):
                kicad_mod_files.append(rel_path)
            elif file.endswith('.stp') or file.endswith('.step'):
                step_files.append(rel_path)

    def prompt_user(file_list, file_type):
        print(f"\nMultiple {file_type} files found. Please choose one:")
        for i, file in enumerate(file_list, 1):
            print(f"{i}) {file}")
        while True:
            try:
                choice = int(input("Enter the number of your choice: "))
                if 1 <= choice <= len(file_list):
                    return file_list[choice - 1]
                else:
                    print("Invalid choice. Please try again.")
            except ValueError:
                print("Invalid input. Please enter a number.")

    if len(kicad_sym_files) > 1:
        kicad_sym_file = prompt_user(kicad_sym_files, "KiCad symbol")
    elif len(kicad_sym_files) == 1:
        kicad_sym_file = kicad_sym_files[0]
    else:
        kicad_sym_file = None

    if len(kicad_mod_files) > 1:
        kicad_mod_file = prompt_user(kicad_mod_files, "KiCad footprint")
    elif len(kicad_mod_files) == 1:
        kicad_mod_file = kicad_mod_files[0]
    else:
        kicad_mod_file = None

    if len(step_files) > 1:
        step_file = prompt_user(step_files, "3D model")
    elif len(step_files) == 1:
        step_file = step_files[0]
    else:
        step_file = None

    return kicad_sym_file, kicad_mod_file, step_file

#
# Functions to modifty Kicad sym-lib-table and fp-lib-table
#

def add_sym_lib_entry(proj_dir, sym_lib_table_filename, parts_dir_rel_to_proj, part_number, kicad_sym_file):
    """
    Updates the sym-lib-table file with the given part number and KiCad symbol file.

    Args:
      proj_dir (str): rel or abs path to the project directory
      sym_lib_table_filename (str): path to the sym-lib-table file
      parts_dir_rel_to_proj (str): path of the parts directory relative to the project directory
      part_number (str): part number (e.g., 'LM317')
      kicad_sym_file (str): path to the KiCad symbol file (e.g., 'LM317/KiCad/LM317.kicad_sym')

    Example usage:
      add_sym_lib_entry('path/to/proj', 'sym-lib-table', '../parts', 'LM317', 'LM317/KiCad/LM317.kicad_sym')
    """
    # Ensure proper path joining
    path = '/'.join(filter(None, [parts_dir_rel_to_proj, part_number, kicad_sym_file]))
    
    # Remove repeated slashes
    path = re.sub(r'//+', '/', path)
    
    # Generate the new line
    new_line = f'  (lib (name "{part_number}")(type "KiCad")(uri "${{KIPRJMOD}}/{path}")(options "")(descr ""))\n'
    
    # Read the current content of the file
    sym_lib_table_filename = os.path.join(proj_dir, sym_lib_table_filename)
    with open(sym_lib_table_filename, 'r') as file:
        lines = file.readlines()
    
    # Look for an existing line with the same part number
    existing_line_index = next((i for i, line in enumerate(lines) if f'(name "{part_number}")' in line), None)
    
    if existing_line_index is not None:
        # Replace the existing line
        lines[existing_line_index] = new_line
        print(f"ℹ️  Replacing entry in {COLOR_BOLD}{sym_lib_table_filename}{COLOR_RESET} for {part_number}")
    else:
        # Find the position to insert the new line (before the last parenthesis)
        insert_position = next(i for i in reversed(range(len(lines))) if ')' in lines[i])
        lines.insert(insert_position, new_line)
        print(f"✅ Adding entry to {COLOR_BOLD}{sym_lib_table_filename}{COLOR_RESET} for {part_number}")
    # Write the updated content back to the file
    with open(sym_lib_table_filename, 'w') as file:
        file.writelines(lines)

def add_fp_lib_entry(proj_dir, fp_lib_table_filename, parts_dir_rel_to_proj, part_number, kicad_footprint_dir):
    """
    Updates the fp-lib-table file with the given part number and KiCad footprint directory.

    Args:
      proj_dir (str): rel or abs path to the project directory
      fp_lib_table_filename (str): path to the fp-lib-table file
      parts_dir_rel_to_proj (str): path of the parts directory relative to the project directory
      part_number (str): part number (e.g., 'LM317')
      kicad_footprint_dir (str): path to the KiCad footprint directory (e.g., 'SLLB120200/KiCad')

    Example usage:
      add_fp_lib_entry('path/to/proj', 'fp-lib-table', '../parts', 'LM317', 'SLLB120200/KiCad')
    """
    # Ensure proper path joining
    path = '/'.join(filter(None, [parts_dir_rel_to_proj, part_number, kicad_footprint_dir]))
    
    # Remove repeated slashes
    path = re.sub(r'//+', '/', path)
    
    # Generate the new line
    new_line = f'  (lib (name "{part_number}")(type "KiCad")(uri "${{KIPRJMOD}}/{path}")(options "")(descr ""))\n'
    
    # Read the current content of the file
    fp_lib_table_filename = os.path.join(proj_dir, fp_lib_table_filename)
    with open(fp_lib_table_filename, 'r') as file:
        lines = file.readlines()
    
    # Look for an existing line with the same part number
    existing_line_index = next((i for i, line in enumerate(lines) if f'(name "{part_number}")' in line), None)
    
    if existing_line_index is not None:
        # Replace the existing line
        lines[existing_line_index] = new_line
        print(f"ℹ️  Replacing entry in {COLOR_BOLD}{fp_lib_table_filename}{COLOR_RESET} for {part_number}")
    else:
        # Find the position to insert the new line (before the last parenthesis)
        insert_position = next(i for i in reversed(range(len(lines))) if ')' in lines[i])
        lines.insert(insert_position, new_line)
        print(f"✅ Adding entry to {COLOR_BOLD}{fp_lib_table_filename}{COLOR_RESET} for {part_number}")
    # Write the updated content back to the file
    with open(fp_lib_table_filename, 'w') as file:
        file.writelines(lines)

#
# Configuration and arguments
#
def try_load_config(config_file=CWD_CONFIG_FILE_NAME):
    """
    If an 'import-kicad-parts.ini' file exists in the current directory, load it.
    Command line arguments still override values in the config file, but can be omitted
    if one is present in the current directory.
    """
    if not os.path.isfile(config_file):
        return {}
    import configparser
    config = configparser.ConfigParser()
    config.read(config_file)
    return config['PROJECT_SETTINGS'] if 'PROJECT_SETTINGS' in config else {}


#
# Main program
#
def main():
    # If the current directory is a sub-Kicad project and has a config file,
    # then there is no need to specify the project directory on the command line.
    # Also, the config file can contain a value for '-p' as well.
    # Result is that within a project directory, you can just run:
    #   import-kicad-part.py ~/Downloads/LIB_SLLB120200.zip
    config = try_load_config()
    parser = argparse.ArgumentParser(description="Fix downloaded KiCad part ZIP and import into project", exit_on_error=False)
    parser.add_argument("zip_file", help="path to the ZIP file containing the KiCad part")
    if not config:
        # second positional argument if we're not in a project directory
        parser.add_argument("proj_dir", help="path to the KiCad project directory")
    parser.add_argument("-p", "--parts_dir_rel_to_proj", default=config.get('parts_dir_rel_to_proj', 'parts'), 
                        help="path of the parts directory relative to the project directory (default: 'parts')")
    parser.add_argument('-f', '--force', action='store_true', help='force overwrite of existing part directory')
    
    try:
        args = parser.parse_args()
    except argparse.ArgumentError as e:
        print(f"❌ {COLOR_RED}error: {e}{COLOR_RESET}")
        print(f"See --help for usage")
        return 1

    zip_file = os.path.abspath(args.zip_file)
    parts_dir_rel_to_proj = args.parts_dir_rel_to_proj
    if config:
        print(f"💪 [{CWD_CONFIG_FILE_NAME}] assuming project dir:      {COLOR_BLUE}{os.path.basename(os.getcwd())}{COLOR_RESET}")
        proj_dir = os.path.abspath(os.getcwd())
    else:
        proj_dir = os.path.abspath(args.proj_dir)
    if config and config.get('parts_dir_rel_to_proj'):
        parts_dir_rel_to_proj = config.get('parts_dir_rel_to_proj')
        print(f"💪 [{CWD_CONFIG_FILE_NAME}] assuming parts directory:  {COLOR_BLUE}{parts_dir_rel_to_proj}{COLOR_RESET}")
    force_overwrite = args.force

    # check configuration and/orarguments
    if not os.path.isfile(zip_file):
        print(f"❌ {COLOR_RED}error: {zip_file} is not a valid file{COLOR_RESET}")
        print(f"See --help for usage")
        return 1
    if not os.path.isdir(proj_dir):
        print(f"❌ {COLOR_RED}error: {proj_dir} is not a valid directory{COLOR_RESET}")
        print(f"See --help for usage")
        return 1
    parts_dir_full = os.path.join(proj_dir, parts_dir_rel_to_proj)
    if not os.path.isdir(parts_dir_full):
        print(f"🚫 {COLOR_YELLOW}warning: the specified parts directory does not exist: {parts_dir_full}{COLOR_RESET}")
        user_input = input(f"{COLOR_BOLD}Do you want to create a new directory for parts at {parts_dir_full}? (y/n): {COLOR_RESET}").lower()
        if user_input == 'y':
            try:
                os.makedirs(parts_dir_full)
                print(f"✅ {COLOR_GREEN}created new parts directory: {parts_dir_full}{COLOR_RESET}")
                parts_dir_rel_to_proj = os.path.relpath(parts_dir_full, proj_dir)
            except OSError as e:
                print(f"❌ {COLOR_RED}error: failed to create parts directory: {e}{COLOR_RESET}")
                return 1
        else:
            print(f"{COLOR_RED}aborting.{COLOR_RESET}")
            return 1
    
    # Unzip the file (if necessary) and get the path to the new directory
    if not os.path.isdir(zip_file):
        unzipped_dir, part_number = unzip_part_file(zip_file, parts_dir_full, force_overwrite)
    else:
        unzipped_dir, part_number = copy_part_dir(zip_file, parts_dir_full, force_overwrite)
    if unzipped_dir is None:
        print(f"❌ error: failed to unzip {zip_file}")
        return 1
    print(f"✅ unzipped to: {COLOR_GREEN}{unzipped_dir}{COLOR_RESET}")

    # Find the KiCad files
    kicad_sym_file, kicad_mod_file, step_file = find_kicad_files(unzipped_dir)

    print(f"\nSelected files:")
    print(f"  KiCad symbol: {kicad_sym_file}")
    print(f"  KiCad footprint: {kicad_mod_file}")
    print(f"  STEP 3D model: {step_file}")
    print()

    # Update the .kicad_sym file
    kicad_sym_path = os.path.join(unzipped_dir, kicad_sym_file)
    def remove_extension(filename):
        return os.path.splitext(filename)[0]
    footprint_name = remove_extension(kicad_mod_file)
    update_kicad_sym(kicad_sym_path, part_number=part_number, footprint_name=footprint_name)

    # Update the .kicad_mod file
    kicad_mod_path = os.path.join(unzipped_dir, kicad_mod_file)
    update_3d_model_path(kicad_mod_path, parts_dir_rel_to_proj, part_number, step_file)

    # Add the part to the sym-lib-table
    add_sym_lib_entry(proj_dir, 'sym-lib-table', parts_dir_rel_to_proj, part_number, kicad_sym_file)

    # Add the part to the fp-lib-table
    kicad_mod_dir = os.path.dirname(kicad_mod_file)
    add_fp_lib_entry(proj_dir, 'fp-lib-table', parts_dir_rel_to_proj, part_number, kicad_mod_dir)

if __name__ == "__main__":
    sys.exit(main())
