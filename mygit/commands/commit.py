import os
import sys
import hashlib
import time
import datetime

def hash_content(content):
    return hashlib.sha1(content.encode()).hexdigest()

def run():
    if not os.path.exists('.mygit'):
        print("Error: No MyGit repository found. Run 'mygit init' first.")
        return

    index_path = '.mygit/index'
    if not os.path.exists(index_path):
        print("Nothing to commit, index is empty.")
        return

    # Read staged files from index
    with open(index_path, 'r') as f:
        staged_files = f.read().splitlines()

    if len(sys.argv) < 3:
        print("Usage: mygit commit <message>")
        return

    message = ' '.join(sys.argv[2:])

    # Human-readable timestamp
    readable_time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')

    # Build commit content
    commit_content = f"commit message: {message}\n"
    commit_content += f"timestamp: {readable_time}\n"
    commit_content += "files:\n"
    for line in staged_files:
        commit_content += f"  {line}\n"

    commit_hash = hash_content(commit_content)
    commit_path = f'.mygit/objects/{commit_hash}'

    with open(commit_path, 'w') as f:
        f.write(commit_content)

    # Save commit in log for easy lookup
    with open('.mygit/log', 'a') as log_file:
        log_file.write(f"{commit_hash} | {readable_time} | {message}\n")

    # Update HEAD
    head_path = '.mygit/HEAD'
    with open(head_path, 'w') as f:
        f.write(commit_hash)

    print(f"[{commit_hash}] {message} at {readable_time}")
    print(f"Committed {len(staged_files)} files.")
