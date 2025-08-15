import sys
from mygit.commands import init, add, commit, log, status, checkout, diff, delete, prune

def main():
    if len(sys.argv) < 2:
        print("Usage: mygit <command>")
        return

    command = sys.argv[1]

    if command == 'init':
        init.run()
    elif command == 'add':
        add.run()
    elif command== 'commit':
        commit.run()
    elif command== 'log':
        log.run()
    elif command== 'status':
        status.run()
    elif command == 'checkout':
        checkout.run()
    elif command == 'diff':
        diff.run()
    elif command == 'delete':
        delete.run()
    elif command == 'prune':
        prune.run()
    else:
        print(f"Unknown command: {command}")

if __name__ == '__main__':
    main()
