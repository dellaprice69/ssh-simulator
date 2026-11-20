# SSH PRACTICE EXAMPLES

This guide shows practical examples and exercises for learning SSH and Linux commands.

## 1. Basic Navigation (Beginner)

### Learning Objectives
- Understand file system hierarchy
- Navigate between directories
- Understand home directory

### Exercises

**Exercise 1.1: Where am I?**
```bash
$ pwd
/home/user

$ whoami
user
```

**Exercise 1.2: Go home**
```bash
$ cd ~
$ pwd
/home/user

$ cd /
$ pwd
/

$ cd ~
$ pwd
/home/user
```

**Exercise 1.3: List files**
```bash
$ ls
README.txt
notes.txt

$ ls -la
drwxr-xr-x user users 4096 Nov 18 10:00 .bashrc
-rw-r--r-- user users  120 Nov 18 10:00 README.txt
-rw-r--r-- user users   45 Nov 18 10:00 notes.txt
```

## 2. User Information (Beginner)

### Learning Objectives
- Understand user and group concepts
- Check current permissions
- Understand sudo privileges

### Exercises

**Exercise 2.1: Who are you?**
```bash
$ whoami
user
```

**Exercise 2.2: User details**
```bash
$ id
uid=1000(user) gid=1000(users) groups=1000(users)
```

**Exercise 2.3: Sudo access (should fail)**
```bash
$ sudo whoami
user is not in the sudoers file. This incident will be reported.
```

**Exercise 2.4: Login as admin and try sudo**
1. Logout from current user
2. Login with: **admin** / **admin123**
3. Run:
```bash
$ sudo whoami
root

$ id
uid=1000(admin) gid=0(root) groups=0(root)
```

## 3. File Operations (Intermediate)

### Learning Objectives
- Create and modify files
- Copy and move files
- Delete files
- Read file contents

### Exercises

**Exercise 3.1: Create a file**
```bash
$ echo "Hello SSH World" > greeting.txt
$ cat greeting.txt
Hello SSH World
```

**Exercise 3.2: Create multiple files**
```bash
$ echo "First line" > file1.txt
$ echo "Second line" > file2.txt
$ ls
greeting.txt
file1.txt
file2.txt
README.txt
notes.txt
```

**Exercise 3.3: Copy files**
```bash
$ cp greeting.txt greeting_backup.txt
$ ls
greeting.txt
greeting_backup.txt
file1.txt
file2.txt
```

**Exercise 3.4: Move/rename files**
```bash
$ mv greeting_backup.txt greeting_copy.txt
$ ls
greeting.txt
greeting_copy.txt
file1.txt
file2.txt
```

**Exercise 3.5: Delete files**
```bash
$ rm file1.txt
$ rm file2.txt
$ ls
greeting.txt
greeting_copy.txt
```

## 4. Directory Operations (Intermediate)

### Learning Objectives
- Create new directories
- Navigate complex directory structures
- Understand path types (absolute vs relative)

### Exercises

**Exercise 4.1: Create directories**
```bash
$ mkdir projects
$ mkdir documents
$ ls
greeting.txt
greeting_copy.txt
projects
documents
```

**Exercise 4.2: Navigate using paths**
```bash
$ pwd
/home/user

$ cd projects
$ pwd
/home/user/projects

$ cd /home/user
$ pwd
/home/user

$ cd /
$ pwd
/

$ cd home/user
$ pwd
/home/user
```

**Exercise 4.3: Create files in different directories**
```bash
$ cd projects
$ echo "Project 1" > project1.txt
$ cd ../documents
$ echo "Document 1" > doc1.txt
$ ls
doc1.txt

$ cd ~
$ ls
projects
documents
greeting.txt
greeting_copy.txt
```

## 5. System Information (Intermediate)

### Learning Objectives
- Check system information
- Monitor disk usage
- Understand system status

### Exercises

**Exercise 5.1: System details**
```bash
$ uname
Linux

$ uname -a
Linux ssh-simulator 5.10.0 #1 SMP x86_64 GNU/Linux
```

**Exercise 5.2: Date and time**
```bash
$ date
Fri Nov 20 12:30:45 UTC 2026
```

**Exercise 5.3: Disk usage**
```bash
$ df
Filesystem     1K-blocks Used Available Use%
/dev/sda1 102400000 51200000 51200000 50%
```

**Exercise 5.4: Directory size**
```bash
$ du /home/user
4096	/home/user

$ du projects
4096	projects
```

**Exercise 5.5: Running processes**
```bash
$ ps
PID TTY TIME CMD
  1   ?  0:00 init
 42   ?  0:01 sshd
100 pts/0 0:00 bash
150 pts/0 0:00 ps
```

## 6. Command History (Intermediate)

### Learning Objectives
- Understand command history
- Navigate history efficiently
- Repeat commands

### Exercises

**Exercise 6.1: View history**
```bash
$ pwd
/home/user

$ whoami
user

$ id
uid=1000(user) gid=1000(users) groups=1000(users)

$ history
   1 pwd
   2 whoami
   3 id
   4 history
```

**Exercise 6.2: Navigate history with arrow keys**
1. Type a command: `pwd`
2. Press Enter
3. Press ↑ (up arrow) - shows `pwd`
4. Press ↑ again - shows previous command
5. Press ↓ (down arrow) - shows next command

## 7. Sudo and Permissions (Advanced)

### Learning Objectives
- Understand sudo privileges
- Run commands with elevated privileges
- Understand permission restrictions

### Exercises

**Exercise 7.1: Sudo with admin user**

First logout and login as admin: **admin** / **admin123**

```bash
$ whoami
admin

$ sudo whoami
admin

$ sudo id
uid=0(admin) gid=0(root) groups=0(root)
```

**Exercise 7.2: Sudo failures (with regular user)**

Logout and login as: **user** / **password123**

```bash
$ whoami
user

$ sudo whoami
user is not in the sudoers file. This incident will be reported.
```

**Exercise 7.3: Check effective permissions**
```bash
$ id
uid=1000(user) gid=1000(users) groups=1000(users)

$ sudo id
user is not in the sudoers file. This incident will be reported.
```

## 8. Working with Multiple Files (Advanced)

### Learning Objectives
- Handle multiple file operations
- Organize files
- Create complex directory structures

### Exercises

**Exercise 8.1: Organize project structure**
```bash
$ mkdir -p projects/website/css
$ mkdir -p projects/website/js
$ mkdir -p projects/website/html

$ cd projects/website
$ echo "/* Styles */" > css/style.css
$ echo "// Scripts" > js/script.js
$ echo "<html>...</html>" > html/index.html

$ ls -la
html
css
js

$ ls html
index.html

$ ls css
style.css

$ ls js
script.js
```

**Exercise 8.2: Create and copy project files**
```bash
$ cd ~/projects/website
$ cp -r . ../website_backup

$ cd ~/projects
$ ls
website
website_backup
```

## 9. SSH Key Generation (Advanced)

### Learning Objectives
- Understand SSH key pairs
- Generate public/private keys
- Key management

### Exercises

**Exercise 9.1: Generate SSH keys**
```bash
$ ssh-keygen
Generated key pair for user:
Private key: ~/.ssh/id_rsa
Public key: ~/.ssh/id_rsa.pub
```

**Exercise 9.2: Try with admin**
```bash
# First logout and login as admin
$ whoami
admin

$ ssh-keygen
Generated key pair for admin:
Private key: ~/.ssh/id_rsa
Public key: ~/.ssh/id_rsa.pub
```

## 10. Real-World Scenarios (Expert)

### Scenario 1: Setting up a web project

```bash
# 1. Login and check identity
whoami                    # Verify you're the right user
pwd                       # Check you're in home directory

# 2. Create project structure
mkdir -p web_project/src
mkdir -p web_project/config
mkdir -p web_project/docs

# 3. Create project files
cd web_project
echo "# My Web Project" > README.txt
echo "Main application file" > src/app.txt
echo "Configuration settings" > config/settings.txt
echo "API Documentation" > docs/api.txt

# 4. List project
ls -la
cd src
ls -la
cd ../..

# 5. Backup project
cp -r web_project web_project_backup

# 6. Check system resources
df
du web_project
ps

# 7. View your commands
history
```

### Scenario 2: User administration (admin only)

```bash
# 1. Login as admin
whoami                    # Verify: admin

# 2. Check your privileges
id                        # Shows: uid=0 (root)
sudo whoami              # Shows: admin (or root)

# 3. Create system-level directory (simulated)
sudo mkdir -p /opt/apps
sudo touch /opt/apps/config.txt

# 4. Try as regular user (would fail in real system)
# This simulator allows it, but shows the concept

# 5. Check process info
ps                        # List running processes
```

### Scenario 3: File management workflow

```bash
# 1. Create working directory
mkdir work
cd work

# 2. Create multiple files
echo "Project notes" > notes.txt
echo "TODO list" > todo.txt
echo "Contact info" > contacts.txt

# 3. Organize into folders
mkdir archive
mkdir current

# 4. Copy current work
cp todo.txt current/todo.txt
cp notes.txt current/notes.txt

# 5. Archive old work
cp contacts.txt archive/contacts.txt

# 6. Verify organization
ls
ls current
ls archive

# 7. Cleanup
rm todo.txt
rm notes.txt
rm contacts.txt

# 8. Final check
ls
ls current
ls archive
```

## Learning Path

### Level 1: Beginner (30 minutes)
- Complete exercises 1-2
- Learn: pwd, cd, whoami, id
- Practice: Navigation and user identification

### Level 2: Intermediate (1 hour)
- Complete exercises 3-6
- Learn: File operations, directories, history
- Practice: Creating and managing files

### Level 3: Advanced (1.5 hours)
- Complete exercises 7-9
- Learn: Sudo, permissions, SSH keys
- Practice: Privilege management

### Level 4: Expert (2+ hours)
- Complete real-world scenarios
- Learn: Combining multiple commands
- Practice: Complex workflows

## Tips for Effective Learning

1. **Type commands manually** - Don't copy/paste, type each command
2. **Understand each step** - Know why you're running each command
3. **Experiment** - Try variations and see what happens
4. **Use help** - Type `help` to see all available commands
5. **Check status** - Use `pwd`, `ls`, `whoami` to verify your state
6. **Review history** - Use `history` to review what you've done
7. **Practice regularly** - Short, frequent sessions beat long, infrequent ones
8. **Challenge yourself** - Create scenarios and solve them

## Common Mistakes to Avoid

❌ **Mistake**: Forgetting where you are
✓ **Solution**: Use `pwd` frequently to check location

❌ **Mistake**: Incorrect directory paths
✓ **Solution**: Use `cd ~` to go home, then navigate carefully

❌ **Mistake**: Trying sudo with regular user
✓ **Solution**: Use admin user (admin/admin123) for sudo commands

❌ **Mistake**: Not understanding file locations
✓ **Solution**: Learn about absolute (/) vs relative paths

❌ **Mistake**: Trying unsupported commands
✓ **Solution**: Check `help` for available commands

## Keyboard Shortcuts

| Shortcut | Action |
|----------|--------|
| ↑ | Previous command in history |
| ↓ | Next command in history |
| Tab | Auto-complete (future feature) |
| Ctrl+C | Cancel current command |
| Ctrl+L | Clear screen |
| Enter | Execute command |

## Quick Reference

```bash
pwd              # Where am I?
whoami           # Who am I?
id               # What groups am I in?
ls               # What's here?
cd               # Where to go?
mkdir            # Create directory
touch            # Create file
cat              # Read file
echo             # Print text
cp               # Copy
mv               # Move/rename
rm               # Delete
cd ~             # Go home
cd /             # Go to root
cd ..            # Go up one level
history          # See past commands
help             # Get help
sudo             # Run as admin
uname            # System info
date             # Current time
df               # Disk usage
ps               # Process list
```

---

**Keep practicing and you'll master Linux commands! 🎓**
