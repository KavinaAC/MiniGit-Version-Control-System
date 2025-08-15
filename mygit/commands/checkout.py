import os
import sys

def run():
    if not os.path.exists('.mygit'):
        print("Error: No MyGit repository found. Run 'mygit init' first.")
        return

    if len(sys.argv) < 3:
        print("Usage: mygit checkout <commit_hash_or_message>")
        return

    commit_input = sys.argv[2]

    # Step 1: If input is NOT a commit hash, search commit message in log
    commit_hash = None
    log_path = '.mygit/log'
    if os.path.exists(log_path):
        with open(log_path, 'r') as log_file:
            for line in log_file:
                parts = line.strip().split(' ', 1)
                if len(parts) == 2:
                    hash_part, message_part = parts
                    if commit_input == hash_part or commit_input == message_part:
                        commit_hash = hash_part
                        break

    if not commit_hash:
        print(f"Commit '{commit_input}' not found in log.")
        return

    commit_path = f'.mygit/objects/{commit_hash}'

    if not os.path.exists(commit_path):
        print(f"Commit {commit_hash} does not exist in objects.")
        return

    # Step 2: Read commit object
    with open(commit_path, 'r') as f:
        content = f.read()

    # Step 3: Parse files section in commit content
    lines = content.splitlines()
    files_start = False
    files = []

    for line in lines:
        if files_start:
            line = line.strip()
            if line:
                parts = line.split(' ', 1)
                if len(parts) == 2:
                    files.append(parts)
        if line == "files:":
            files_start = True

    # Step 4: Restore files from objects
    for file_hash, filepath in files:
        obj_path = f'.mygit/objects/{file_hash}'
        if not os.path.exists(obj_path):
            print(f"Object {file_hash} for file {filepath} missing!")
            continue

        with open(obj_path, 'rb') as f:
            data = f.read()

        with open(filepath, 'wb') as f:
            f.write(data)
        print(f"Restored {filepath}")

    # Step 5: Update HEAD to this commit
    with open('.mygit/HEAD', 'w') as f:
        f.write(commit_hash)

    print(f"Checked out commit {commit_hash}")
