import os

def run():
    if os.path.exists('.mygit'):
        print("Repository already initialized.")
        return
    os.makedirs('.mygit/objects')
    os.makedirs('.mygit/refs')
    with open('.mygit/HEAD', 'w') as f:
        f.write('ref: refs/heads/master\n')
    print("Initialized empty MyGit repository in .mygit/")
