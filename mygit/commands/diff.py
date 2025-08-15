import os

def run():
    import sys

    if not os.path.exists('.mygit'):
        print("Error: No MyGit repository found. Run 'mygit init' first.")
        return

    if len(sys.argv) < 4:
        print("Usage: mygit diff <commit-id-1> <commit-id-2>")
        return

    commit1 = sys.argv[2]
    commit2 = sys.argv[3]

    commit_path1 = f'.mygit/objects/{commit1}'
    commit_path2 = f'.mygit/objects/{commit2}'

    if not os.path.exists(commit_path1):
        print(f"Commit {commit1} does not exist.")
        return
    if not os.path.exists(commit_path2):
        print(f"Commit {commit2} does not exist.")
        return

    def parse_commit(commit_path):
        with open(commit_path, 'r') as f:
            lines = f.read().splitlines()
        files_section = False
        files = {}
        for line in lines:
            if files_section:
                line = line.strip()
                if line:
                    h, path = line.split(' ', 1)
                    files[path] = h
            if line == 'files:':
                files_section = True
        return files

    files1 = parse_commit(commit_path1)
    files2 = parse_commit(commit_path2)

    all_files = set(files1.keys()) | set(files2.keys())

    added = [f for f in all_files if f not in files1]
    removed = [f for f in all_files if f not in files2]
    modified = [f for f in all_files if f in files1 and f in files2 and files1[f] != files2[f]]

    if not (added or removed or modified):
        print("No differences found between the commits.")
        return

    if added:
        print("Added files:")
        for f in added:
            print(f"  {f}")

    if removed:
        print("Removed files:")
        for f in removed:
            print(f"  {f}")

    if modified:
        print("Modified files:")
        for f in modified:
            print(f"  {f}")
