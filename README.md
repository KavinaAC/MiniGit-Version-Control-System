MiniGit – Simple Version Control System in Python

MiniGit is a lightweight, educational version control system written entirely in Python.  
It mimics basic Git commands (`init`, `add`,`status`,`delete`,`prune`,`log`,`diff`,`commit`, `checkout`) 
to help beginners understand how version control works internally.

🚀 Features
- **Initialize a repository** – Create a `.mygit` folder to track file changes.  
- **Stage files** – Add files to the staging area before committing.  
- **Commit changes** – Save file snapshots with commit messages.  
- **Checkout** – Restore files from a specific commit.  

📦 Installation

1. Clone the repository
git clone https://github.com/<KavinaAC>/MiniGit.git
cd MiniGit

🛠 Usage
Run all commands from inside your MiniGit project folder.

1️⃣ Initialize a repository

python main.py init
Creates a .mygit folder in your project directory.

2️⃣ Add files to the staging area

python main.py add <filename>

3️⃣ Commit changes
python main.py commit "Your commit message"

4️⃣ View commit log
python main.py log

5️⃣ Checkout a commit
python main.py checkout <commit_hash>

📄 License
This project is licensed under the MIT License – you can use, modify, and distribute it fr

Installation

git clone https://github.com/KavinaAC/MiniGit-Version-Control-System.git
cd MiniGit-Version-Control-System
