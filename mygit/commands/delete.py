import os
import sys

def run():
    if not os.path.exists('.mygit'):
        print("Error: No MyGit repository found. Run 'mygit init' first.")
        return

    if len(sys.argv) < 3:
        print("Usage: mygit delete <file1> [file2 ...]")
        return

    files_to_delete = sys.argv[2:]

    index_path = '.mygit/index'
    if os.path.exists(index_path):
        with open(index_path, 'r') as f:
            index = f.read().splitlines()
    else:
        index = []

    # Build a map of file -> hash for quick lookup
    file_to_hash = {}
    for entry in index:
        h, fpath = entry.split(' ', 1)
        file_to_hash[fpath] = h

    updated_index = []
    # To track object hashes that might be safe to delete
    candidate_hashes = []

    for entry in index:
        h, fpath = entry.split(' ', 1)
        if fpath in files_to_delete:
            # Delete the working file if exists
            if os.path.exists(fpath):
                os.remove(fpath)
                print(f"Deleted file: {fpath}")
            else:
                print(f"File {fpath} not found in working directory.")

            # Mark hash for possible deletion
            candidate_hashes.append(h)
            # Skip adding to updated_index to remove from staging
        else:
            updated_index.append(entry)

    # Save updated index
    with open(index_path, 'w') as f:
        f.write('\n'.join(updated_index))

    # Check if any other files still reference these object hashes
    referenced_hashes = {entry.split(' ',1)[0] for entry in updated_index}

    for h in candidate_hashes:
        if h not in referenced_hashes:
            obj_path = f'.mygit/objects/{h}'
            if os.path.exists(obj_path):
                os.remove(obj_path)
                print(f"Deleted object: {h}")
