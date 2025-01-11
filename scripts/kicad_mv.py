#!/usr/bin/env python3

"""
`kicad_mv.py OLD_NAME NEW_NAME` is run in a kicad project directory to rename the project from 
OLD_NAME to NEW_NAME.

This script will update the contents of all .kicad_* files and rename the files themselves.
"""


import sys
import argparse
from pathlib import Path

def replace_in_file(filepath, old_name, new_name):
    """Replace all occurrences of old_name with new_name in the file."""
    try:
        with open(filepath, 'r', encoding='utf-8') as file:
            content = file.read()
        
        # Only write if there are actually changes to make
        if old_name in content:
            new_content = content.replace(old_name, new_name)
            with open(filepath, 'w', encoding='utf-8') as file:
                file.write(new_content)
            print(f"Updated contents in {filepath}")
    except Exception as e:
        print(f"Error processing {filepath}: {e}")

def rename_kicad_project(old_name, new_name):
    """Rename a KiCad project from old_name to new_name."""
    # Get current directory
    current_dir = Path('.')
    
    # First, replace text inside all .kicad_* files
    kicad_files = list(current_dir.glob("*.kicad_*"))
    
    print("\nUpdating file contents...")
    for filepath in kicad_files:
        replace_in_file(filepath, old_name, new_name)
    
    print("\nRenaming files...")
    # Then rename the files
    for filepath in kicad_files:
        if old_name in filepath.name:
            new_filepath = filepath.parent / filepath.name.replace(old_name, new_name)
            try:
                filepath.rename(new_filepath)
                print(f"Renamed {filepath} to {new_filepath}")
            except Exception as e:
                print(f"Error renaming {filepath}: {e}")

def remove_backup_dir(old_name):
    """Remove the KiCad backup directory if it exists."""
    backup_dir = Path(f"{old_name}-backups")
    if backup_dir.exists():
        try:
            import shutil
            shutil.rmtree(backup_dir)
            print(f"Removed backup directory: {backup_dir}")
        except Exception as e:
            print(f"Error removing backup directory {backup_dir}: {e}")

def main():
    parser = argparse.ArgumentParser(description="Rename a KiCad project from OLD_NAME to NEW_NAME",
                                     epilog="Example: kicad_mv.py pd-booster pd-booster-null")
    parser.add_argument('OLD_NAME', help='Current name of the KiCad project')
    parser.add_argument('NEW_NAME', help='New name for the KiCad project')
    args = parser.parse_args()
    
    old_name = args.OLD_NAME
    new_name = args.NEW_NAME

    # make sure files exist with old_name in the current directory
    current_dir = Path('.')
    matching_files = list(current_dir.glob(f"{old_name}.*"))
    if not matching_files:
        print(f"Error: No files found matching '{old_name}.*' in current directory")
        sys.exit(1)
    
    # remove backup directory
    remove_backup_dir(old_name)
    
    print(f"Renaming KiCad project from '{old_name}' to '{new_name}'")
    rename_kicad_project(old_name, new_name)
    print("\nDone!")

if __name__ == "__main__":
    main()