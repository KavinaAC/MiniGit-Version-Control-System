import os

def run():
    if not os.path.exists('.mygit'):
        print("Error: No MyGit repository found. Run 'mygit init' first.")
        return

    head_path = '.mygit/HEAD'
    if not os.path.exists(head_path):
        print("No commits yet.")
        return

    with open(head_path, 'r') as f:
        commit_hash = f.read().strip()

    commit_path = f'.mygit/objects/{commit_hash}'
    if not os.path.exists(commit_path):
        print("Commit object missing.")
        return

    with open(commit_path, 'r') as f:
        commit_content = f.read()

    print(f"Commit {commit_hash}:\n{commit_content}")
