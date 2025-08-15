import os
import hashlib

def hash_file(filepath):
    if not os.path.exists(filepath):
        return None
    with open(filepath, 'rb') as f:
        content = f.read()
    return hashlib.sha1(content).hexdigest()

def run():
    if not os.path.exists('.mygit'):
        print("Error: No MyGit repository found. Run 'mygit init' first.")
        return

    index_path = '.mygit/index'
    if not os.path.exists(index_path):
        print("No files staged.")
        staged_files = []
    else:
        with open(index_path, 'r') as f:
            staged_files = f.read().splitlines()

    staged_map = {}
    for entry in staged_files:
        h, path = entry.split(' ', 1)
        staged_map[path] = h

    # Check working directory files
    all_files = [f for f in os.listdir('.') if os.path.isfile(f) and not f.startswith('.mygit')]

    modified = []
    untracked = []

    for file in all_files:
        file_hash = hash_file(file)
        if file in staged_map:
            if staged_map[file] != file_hash:
                modified.append(file)
        else:
            untracked.append(file)

    print("Changes to be committed:")
    for f in staged_map.keys():
        print(f"  {f}")

    print("\nChanges not staged for commit:")
    for f in modified:
        print(f"  {f}")

    print("\nUntracked files:")
    for f in untracked:
        print(f"  {f}")
