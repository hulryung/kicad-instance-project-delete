# this code is to delete unnecessary project in the instance block in KiCad schematic file

import os
import re
import argparse
import shutil

def remove_block(content, identifier_to_keep):
    projects = list_projects(content)
    for project in projects:
        if project != identifier_to_keep:
            content = _remove_specific_block(content, project)
    return content

def _remove_specific_block(content, identifier):
    start_string = f'(project "{identifier}"'
    
    index = 0
    while index < len(content):
        start_idx = content.find(start_string, index)
        if start_idx == -1:
            break

        end_idx = start_idx
        paren_count = 0
        while end_idx < len(content):
            if content[end_idx] == '(':
                paren_count += 1
            elif content[end_idx] == ')':
                paren_count -= 1
                if paren_count == 0:
                    break
            end_idx += 1

        content = content[:start_idx] + content[end_idx+1:]
        index = start_idx

    return content

def list_projects(content):
    pattern = r'\(project\s+"(.*?)"'
    return re.findall(pattern, content)

def main():
    parser = argparse.ArgumentParser(description="Remove project blocks from .kicad_sch files except the specified one")
    parser.add_argument('action', choices=['remove', 'list'], help='Choose "remove" to delete blocks or "list" to list projects')
    parser.add_argument('identifier', nargs='?', type=str, help='The project identifier to keep. All other project blocks will be removed.')
    args = parser.parse_args()

    if args.action == 'list':
        unique_projects = set()
        for filename in os.listdir():
            if filename.endswith('.kicad_sch'):
                with open(filename, 'r') as f:
                    content = f.read()
                unique_projects.update(list_projects(content))
        
        for project in unique_projects:
            print(project)

    if args.action == 'remove':
        for filename in os.listdir():
            if filename.endswith('.kicad_sch'):
                # Create backup
                backup_filename = filename + ".back"
                shutil.copy(filename, backup_filename)
                
                with open(filename, 'r') as f:
                    content = f.read()
                content = remove_block(content, args.identifier)
                with open(filename, 'w') as f:
                    f.write(content)

if __name__ == "__main__":
    main()

