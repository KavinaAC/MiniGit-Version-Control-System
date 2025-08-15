import os
import sys
import hashlib

def hash_file_contents(contents):
    return hashlib.sha1(contents).hexdigest()

def run():
    if len(sys.argv) < 3:
        print("Usage: mygit add <file1> [file2 ...]")
        return

    if not os.path.exists('.mygit'):
        print("Error: No MyGit repository found. Run 'mygit init' first.")
        return

    files = sys.argv[2:]

    index_path = '.mygit/index'
    # Load existing index if exists
    if os.path.exists(index_path):
        with open(index_path, 'r') as f:
            index = f.read().splitlines()
    else:
        index = []

    for filepath in files:
        if not os.path.exists(filepath):
            print(f"File not found: {filepath}")
            continue

        with open(filepath, 'rb') as f:
            content = f.read()

        file_hash = hash_file_contents(content)
        object_path = f'.mygit/objects/{file_hash}'

        # Save the object if it doesn't exist yet
        if not os.path.exists(object_path):
            with open(object_path, 'wb') as obj_file:
                obj_file.write(content)

        print(f"Added file: {filepath} with hash {file_hash}")

        # Add to index if not already there
        entry = f"{file_hash} {filepath}"
        if entry not in index:
            index.append(entry)

    # Save updated index
    with open(index_path, 'w') as f:
        f.write('\n'.join(index))
